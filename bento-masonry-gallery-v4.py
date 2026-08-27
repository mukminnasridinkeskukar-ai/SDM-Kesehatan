#!/usr/bin/env python3
"""
===========================================
MODERN BENTO + MASONRY HYBRID GALLERY v4.0
===========================================

Clean, Modern, Photography-Focused Photo Gallery
- Bento Grid with 3+ layout variations (A, B, C)
- Masonry-style photo grid
- Featured Event section with special Bento layout
- Premium Fullscreen Lightbox:
  * Zoom: mouse wheel / pinch / double-click / +/- buttons
  * Drag when zoomed
  * Thumbnail strip at bottom
  * Keyboard navigation (ESC/←/→)
  * Swipe support (mobile)
  * Click outside to close
- Category Filters (Pelatihan, Sosialisasi, Bimtek, Rapat, Kunjungan, Lainnya)
- Load More functionality
- Dark Mode with localStorage persistence
- Scroll animations (Intersection Observer)
- Mobile-perfect responsive design
- Photo protection (right-click disabled)

Author: Auto-generated for Dinas Kesehatan Kab. Kutai Kartanegara
"""

import cloudinary
from cloudinary.api import resources
import json
import re
from datetime import datetime
from collections import defaultdict

# ============================================
# KONFIGURASI CLOUDINARY
# ============================================
CLOUD_CONFIG = {
    "cloud_name": "cla7jrww",
    "api_key": "488796372967593",
    "api_secret": "MvIaCN2zMacCWhJ2f2gJnFev0xw"
}

# ============================================
# BENTO + MASONRY HTML TEMPLATE
# ============================================
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="id" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <meta name="description" content="Galeri Foto Kegiatan Dinas Kesehatan Kabupaten Kutai Kartanegara - Modern Bento + Masonry Gallery">
    <title>Galeri Foto — Dinas Kesehatan Kabupaten Kutai Kartanegara</title>
    
    <!-- Preconnect -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <!-- Fonts: Inter (Modern Clean) -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        /* ============================================
           CSS CUSTOM PROPERTIES (THEME)
        ============================================ */
        :root {
            /* Light Theme */
            --bg-primary: #FFFFFF;
            --bg-secondary: #F8F9FA;
            --bg-tertiary: #F1F3F5;
            --bg-card: #FFFFFF;
            --bg-header: rgba(255, 255, 255, 0.95);
            
            --text-primary: #212529;
            --text-secondary: #495057;
            --text-muted: #868E96;
            --text-inverse: #FFFFFF;
            
            --accent-color: #2563EB;
            --accent-hover: #1D4ED8;
            --accent-light: #DBEAFE;
            
            --border-color: #DEE2E6;
            --border-light: #E9ECEF;
            
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 40px rgba(0,0,0,0.15);
            --shadow-xl: 0 20px 60px rgba(0,0,0,0.2);
            
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 24px;
            
            --transition-fast: 0.15s ease;
            --transition-normal: 0.25s ease;
            --transition-slow: 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            
            --header-height: 72px;
            --max-width: 1400px;
        }
        
        [data-theme="dark"] {
            --bg-primary: #0F1117;
            --bg-secondary: #16181D;
            --bg-tertiary: #1C1F26;
            --bg-card: #1C1F26;
            --bg-header: rgba(15, 17, 23, 0.95);
            
            --text-primary: #F1F3F5;
            --text-secondary: #CED4DA;
            --text-muted: #868E96;
            --text-inverse: #0F1117;
            
            --accent-color: #3B82F6;
            --accent-hover: #60A5FA;
            --accent-light: #1E293B;
            
            --border-color: #2D3748;
            --border-light: #1E293B;
            
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
            --shadow-lg: 0 10px 40px rgba(0,0,0,0.5);
            --shadow-xl: 0 20px 60px rgba(0,0,0,0.6);
        }
        
        /* ============================================
           RESET & BASE
        ============================================ */
        *, *::before, *::after {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html {
            scroll-behavior: smooth;
            -webkit-text-size-adjust: 100%;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
            transition: background var(--transition-normal), color var(--transition-normal);
        }
        
        img {
            max-width: 100%;
            height: auto;
            display: block;
        }
        
        a {
            text-decoration: none;
            color: inherit;
        }
        
        button {
            font-family: inherit;
            cursor: pointer;
            border: none;
            background: none;
        }
        
        /* ============================================
           HEADER / HERO SECTION
        ============================================ */
        .gallery-header {
            position: sticky;
            top: 0;
            z-index: 1000;
            background: var(--bg-header);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border-light);
            transition: all var(--transition-normal);
        }
        
        .header-scrolled {
            box-shadow: var(--shadow-md);
        }
        
        .header-inner {
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 0 24px;
            height: var(--header-height);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
        }
        
        .header-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-shrink: 0;
        }
        
        .brand-icon {
            width: 42px;
            height: 42px;
            background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 18px;
        }
        
        .brand-text h1 {
            font-size: 16px;
            font-weight: 700;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }
        
        .brand-text span {
            font-size: 11px;
            color: var(--text-muted);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Header Controls */
        .header-controls {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }
        
        .search-wrapper {
            position: relative;
        }
        
        .search-input {
            width: 220px;
            padding: 10px 16px 10px 42px;
            border: 1px solid var(--border-color);
            border-radius: 50px;
            background: var(--bg-secondary);
            color: var(--text-primary);
            font-size: 14px;
            transition: all var(--transition-fast);
            outline: none;
        }
        
        .search-input:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 0 3px var(--accent-light);
            width: 280px;
        }
        
        .search-input::placeholder {
            color: var(--text-muted);
        }
        
        .search-icon {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }
        
        .filter-select {
            padding: 10px 36px 10px 16px;
            border: 1px solid var(--border-color);
            border-radius: 50px;
            background: var(--bg-secondary);
            color: var(--text-primary);
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23868e96' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 14px center;
            transition: all var(--transition-fast);
            outline: none;
        }
        
        .filter-select:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 0 3px var(--accent-light);
        }
        
        .theme-toggle {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            background: var(--bg-tertiary);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all var(--transition-fast);
            color: var(--text-secondary);
        }
        
        .theme-toggle:hover {
            background: var(--accent-light);
            color: var(--accent-color);
            transform: rotate(15deg);
        }
        
        .mobile-menu-btn {
            display: none;
            width: 42px;
            height: 42px;
            border-radius: 50%;
            background: var(--bg-tertiary);
            align-items: center;
            justify-content: center;
            color: var(--text-secondary);
        }
        
        /* Stats Bar */
        .stats-bar {
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-light);
            padding: 16px 0;
        }
        
        .stats-inner {
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 0 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 32px;
            flex-wrap: wrap;
        }
        
        .stat-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .stat-number {
            font-size: 24px;
            font-weight: 800;
            color: var(--accent-color);
            letter-spacing: -0.02em;
        }
        
        .stat-label {
            font-size: 13px;
            color: var(--text-muted);
            font-weight: 500;
        }
        
        /* Category Filter Pills */
        .category-filters {
            background: var(--bg-primary);
            border-bottom: 1px solid var(--border-light);
            padding: 12px 0;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }
        
        .category-filters::-webkit-scrollbar {
            display: none;
        }
        
        .filters-inner {
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 0 24px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .filter-pill {
            padding: 8px 18px;
            border-radius: 50px;
            font-size: 13px;
            font-weight: 600;
            white-space: nowrap;
            transition: all var(--transition-fast);
            background: var(--bg-secondary);
            color: var(--text-secondary);
            border: 1px solid transparent;
        }
        
        .filter-pill:hover {
            background: var(--accent-light);
            color: var(--accent-color);
        }
        
        .filter-pill.active {
            background: var(--accent-color);
            color: white;
            border-color: var(--accent-color);
        }
        
        /* ============================================
           MAIN CONTENT AREA
        ============================================ */
        .main-content {
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 40px 24px 80px;
        }
        
        /* ============================================
           FEATURED EVENT SECTION (BENTO LAYOUT)
        ============================================ */
        .featured-section {
            margin-bottom: 64px;
        }
        
        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
        }
        
        .section-title-group {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .section-badge {
            padding: 6px 14px;
            background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
            color: white;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            border-radius: 50px;
        }
        
        .section-title {
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: var(--text-primary);
        }
        
        /* Featured Bento Grid */
        .featured-bento {
            display: grid;
            grid-template-columns: 1.6fr 1fr;
            grid-template-rows: repeat(2, 240px);
            gap: 16px;
        }
        
        .featured-main {
            grid-row: 1 / -1;
            position: relative;
            border-radius: var(--radius-lg);
            overflow: hidden;
            cursor: pointer;
            background: var(--bg-tertiary);
        }
        
        .featured-main img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform var(--transition-slow);
        }
        
        .featured-main:hover img {
            transform: scale(1.04);
        }
        
        .featured-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.2) 50%, transparent 100%);
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            padding: 28px;
            opacity: 0;
            transition: opacity var(--transition-normal);
        }
        
        .featured-main:hover .featured-overlay,
        .featured-sub:hover .featured-overlay {
            opacity: 1;
        }
        
        .featured-label {
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--accent-color);
            margin-bottom: 8px;
        }
        
        .featured-event-title {
            font-size: 22px;
            font-weight: 700;
            color: white;
            line-height: 1.3;
            margin-bottom: 8px;
        }
        
        .featured-meta {
            display: flex;
            align-items: center;
            gap: 16px;
            font-size: 13px;
            color: rgba(255,255,255,0.8);
        }
        
        .featured-meta svg {
            width: 14px;
            height: 14px;
            margin-right: 4px;
        }
        
        .featured-sub {
            position: relative;
            border-radius: var(--radius-lg);
            overflow: hidden;
            cursor: pointer;
            background: var(--bg-tertiary);
        }
        
        .featured-sub img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform var(--transition-slow);
        }
        
        .featured-sub:hover img {
            transform: scale(1.06);
        }
        
        .featured-sub .featured-overlay {
            padding: 20px;
        }
        
        .featured-sub .featured-event-title {
            font-size: 16px;
        }
        
        .photo-count-badge {
            position: absolute;
            top: 14px;
            right: 14px;
            padding: 6px 12px;
            background: rgba(0,0,0,0.65);
            backdrop-filter: blur(10px);
            color: white;
            font-size: 12px;
            font-weight: 600;
            border-radius: 50px;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        /* ============================================
           EVENT SECTIONS (MASONRY BENTO)
        ============================================ */
        .event-section {
            margin-bottom: 64px;
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .event-section.visible {
            opacity: 1;
            transform: translateY(0);
        }
        
        .event-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-light);
        }
        
        .event-info h2 {
            font-size: 20px;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 6px;
            color: var(--text-primary);
        }
        
        .event-meta {
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
            font-size: 13px;
            color: var(--text-muted);
        }
        
        .event-meta-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .event-meta-item svg {
            width: 14px;
            height: 14px;
            opacity: 0.7;
        }
        
        .event-category-tag {
            padding: 5px 12px;
            background: var(--accent-light);
            color: var(--accent-color);
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-radius: 50px;
        }
        
        /* BENTO LAYOUT VARIATIONS */
        
        /* Layout A: Large left + 2x2 grid right */
        .bento-layout-a {
            display: grid;
            grid-template-columns: 1.4fr 1fr;
            grid-template-rows: repeat(2, 200px);
            gap: 14px;
        }
        
        .bento-layout-a .bento-large {
            grid-row: 1 / -1;
        }
        
        /* Layout B: Top banner + 3 columns below */
        .bento-layout-b {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            grid-template-rows: 180px 180px;
            gap: 14px;
        }
        
        .bento-layout-b .bento-wide {
            grid-column: 1 / -1;
            grid-row: 1;
        }
        
        /* Layout C: Asymmetric masonry-like */
        .bento-layout-c {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-template-rows: repeat(2, 190px);
            gap: 14px;
        }
        
        .bento-layout-c .bento-tall {
            grid-row: 1 / -1;
        }
        
        .bento-layout-c .bento-wide-2 {
            grid-column: span 2;
        }
        
        /* Bento Card Base */
        .bento-card {
            position: relative;
            border-radius: var(--radius-md);
            overflow: hidden;
            cursor: pointer;
            background: var(--bg-tertiary);
            aspect-ratio: auto;
        }
        
        .bento-card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform var(--transition-slow);
        }
        
        .bento-card:hover img {
            transform: scale(1.05);
        }
        
        .bento-card-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 60%);
            opacity: 0;
            transition: opacity var(--transition-normal);
            display: flex;
            align-items: flex-end;
            padding: 16px;
        }
        
        .bento-card:hover .bento-card-overlay {
            opacity: 1;
        }
        
        .bento-card-info {
            color: white;
        }
        
        .bento-card-info span {
            font-size: 12px;
            opacity: 0.9;
        }
        
        /* Shimmer Loading Effect */
        .shimmer {
            position: relative;
            overflow: hidden;
            background: var(--bg-tertiary);
        }
        
        .shimmer::after {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(
                90deg,
                transparent 0%,
                rgba(255,255,255,0.08) 50%,
                transparent 100%
            );
            animation: shimmer 1.5s infinite;
        }
        
        [data-theme="dark"] .shimmer::after {
            background: linear-gradient(
                90deg,
                transparent 0%,
                rgba(255,255,255,0.04) 50%,
                transparent 100%
            );
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        /* ============================================
           LOAD MORE SECTION
        ============================================ */
        .load-more-container {
            text-align: center;
            margin-top: 48px;
            padding-top: 32px;
            border-top: 1px solid var(--border-light);
        }
        
        .load-more-stats {
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: 16px;
        }
        
        .load-more-stats strong {
            color: var(--accent-color);
            font-weight: 700;
        }
        
        .load-more-btn {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 16px 36px;
            background: var(--accent-color);
            color: white;
            font-size: 15px;
            font-weight: 600;
            border-radius: 50px;
            transition: all var(--transition-normal);
            box-shadow: 0 4px 20px rgba(37, 99, 235, 0.35);
        }
        
        .load-more-btn:hover {
            background: var(--accent-hover);
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(37, 99, 235, 0.45);
        }
        
        .load-more-btn:active {
            transform: translateY(0);
        }
        
        .load-more-btn svg {
            transition: transform var(--transition-fast);
        }
        
        .load-more-btn:hover svg {
            transform: translateY(3px);
        }
        
        .all-loaded .load-more-btn {
            background: var(--bg-tertiary);
            color: var(--text-muted);
            box-shadow: none;
            cursor: default;
            pointer-events: none;
        }
        
        /* ============================================
           PREMIUM LIGHTBOX
        ============================================ */
        .lightbox-overlay {
            position: fixed;
            inset: 0;
            z-index: 9999;
            background: rgba(0, 0, 0, 0.97);
            display: flex;
            flex-direction: column;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s ease, visibility 0.3s ease;
        }
        
        .lightbox-active {
            opacity: 1;
            visibility: visible;
        }
        
        /* Lightbox Header */
        .lightbox-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 24px;
            background: rgba(0,0,0,0.5);
            backdrop-filter: blur(10px);
            flex-shrink: 0;
        }
        
        .lightbox-info {
            color: white;
        }
        
        .lightbox-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 2px;
        }
        
        .lightbox-counter {
            font-size: 13px;
            color: rgba(255,255,255,0.6);
        }
        
        .lightbox-actions {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .lightbox-btn {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: rgba(255,255,255,0.1);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all var(--transition-fast);
        }
        
        .lightbox-btn:hover {
            background: rgba(255,255,255,0.2);
            transform: scale(1.08);
        }
        
        .lightbox-close {
            background: rgba(255,255,255,0.15);
        }
        
        .lightbox-close:hover {
            background: #EF4444;
        }
        
        /* Lightbox Main Area */
        .lightbox-main {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
            touch-action: pinch-zoom;
        }
        
        .lightbox-image-container {
            position: relative;
            max-width: 90vw;
            max-height: calc(100vh - 200px);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .lightbox-image {
            max-width: 100%;
            max-height: calc(100vh - 200px);
            object-fit: contain;
            border-radius: var(--radius-md);
            transition: transform 0.2s ease;
            user-select: none;
            -webkit-user-drag: none;
            will-change: transform;
        }
        
        .lightbox-image.dragging {
            transition: none;
        }
        
        /* Navigation Arrows */
        .lightbox-nav {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: rgba(255,255,255,0.12);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all var(--transition-fast);
            z-index: 10;
        }
        
        .lightbox-nav:hover {
            background: rgba(255,255,255,0.25);
            transform: translateY(-50%) scale(1.1);
        }
        
        .lightbox-prev { left: 20px; }
        .lightbox-next { right: 20px; }
        
        /* Zoom Controls */
        .zoom-controls {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(10px);
            border-radius: 50px;
        }
        
        .zoom-btn {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: rgba(255,255,255,0.15);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: 600;
            transition: all var(--transition-fast);
        }
        
        .zoom-btn:hover {
            background: rgba(255,255,255,0.25);
        }
        
        .zoom-level {
            color: white;
            font-size: 13px;
            font-weight: 500;
            min-width: 50px;
            text-align: center;
        }
        
        /* Thumbnail Strip */
        .lightbox-thumbnails {
            padding: 16px 24px;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(10px);
            flex-shrink: 0;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }
        
        .lightbox-thumbnails::-webkit-scrollbar {
            height: 6px;
        }
        
        .lightbox-thumbnails::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.1);
            border-radius: 3px;
        }
        
        .lightbox-thumbnails::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.3);
            border-radius: 3px;
        }
        
        .thumbnail-list {
            display: flex;
            gap: 10px;
            justify-content: center;
        }
        
        .thumbnail-item {
            width: 72px;
            height: 52px;
            border-radius: var(--radius-sm);
            overflow: hidden;
            cursor: pointer;
            opacity: 0.5;
            transition: all var(--transition-fast);
            border: 2px solid transparent;
            flex-shrink: 0;
        }
        
        .thumbnail-item:hover {
            opacity: 0.75;
        }
        
        .thumbnail-item.active {
            opacity: 1;
            border-color: var(--accent-color);
        }
        
        .thumbnail-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        /* ============================================
           EMPTY STATE
        ============================================ */
        .empty-state {
            text-align: center;
            padding: 80px 24px;
            color: var(--text-muted);
        }
        
        .empty-state svg {
            width: 80px;
            height: 80px;
            margin-bottom: 20px;
            opacity: 0.4;
        }
        
        .empty-state h3 {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--text-secondary);
        }
        
        /* ============================================
           FOOTER
        ============================================ */
        .gallery-footer {
            background: var(--bg-secondary);
            border-top: 1px solid var(--border-light);
            padding: 32px 24px;
            text-align: center;
        }
        
        .footer-text {
            font-size: 13px;
            color: var(--text-muted);
        }
        
        .footer-text strong {
            color: var(--text-secondary);
        }
        
        /* ============================================
           RESPONSIVE DESIGN
        ============================================ */
        @media (max-width: 1024px) {
            .featured-bento {
                grid-template-columns: 1fr;
                grid-template-rows: 300px 200px 200px;
            }
            
            .featured-main {
                grid-row: 1;
            }
            
            .bento-layout-a,
            .bento-layout-b,
            .bento-layout-c {
                grid-template-columns: repeat(2, 1fr);
                grid-template-rows: auto;
            }
            
            .bento-layout-a .bento-large {
                grid-row: auto;
            }
            
            .bento-layout-b .bento-wide {
                grid-column: auto;
                grid-row: auto;
            }
            
            .bento-layout-c .bento-tall {
                grid-row: auto;
            }
            
            .bento-layout-c .bento-wide-2 {
                grid-column: span 1;
            }
        }
        
        @media (max-width: 768px) {
            :root {
                --header-height: auto;
            }
            
            .header-inner {
                flex-wrap: wrap;
                padding: 12px 16px;
                height: auto;
                gap: 12px;
            }
            
            .header-brand {
                flex: 1;
            }
            
            .header-controls {
                order: 3;
                width: 100%;
                justify-content: space-between;
            }
            
            .search-input {
                width: 100%;
                max-width: 200px;
            }
            
            .search-input:focus {
                width: 100%;
                max-width: 100%;
            }
            
            .filter-select {
                flex: 1;
                min-width: 120px;
            }
            
            .stats-inner {
                gap: 20px;
            }
            
            .stat-number {
                font-size: 20px;
            }
            
            .section-title {
                font-size: 22px;
            }
            
            .featured-bento {
                grid-template-rows: 250px 160px 160px;
                gap: 12px;
            }
            
            .bento-layout-a,
            .bento-layout-b,
            .bento-layout-c {
                grid-template-columns: 1fr;
                gap: 12px;
            }
            
            .bento-card {
                aspect-ratio: 16/10;
            }
            
            .event-header {
                flex-direction: column;
                gap: 12px;
            }
            
            .lightbox-nav {
                width: 44px;
                height: 44px;
            }
            
            .lightbox-prev { left: 10px; }
            .lightbox-next { right: 10px; }
            
            .thumbnail-item {
                width: 56px;
                height: 42px;
            }
            
            .main-content {
                padding: 24px 16px 60px;
            }
        }
        
        @media (max-width: 480px) {
            .brand-text h1 {
                font-size: 14px;
            }
            
            .brand-text span {
                font-size: 10px;
            }
            
            .section-title {
                font-size: 19px;
            }
            
            .featured-event-title {
                font-size: 17px;
            }
            
            .featured-overlay {
                padding: 18px;
            }
            
            .filters-inner {
                padding: 0 16px;
            }
            
            .filter-pill {
                padding: 7px 14px;
                font-size: 12px;
            }
            
            .lightbox-title {
                font-size: 14px;
            }
            
            .zoom-controls {
                bottom: 10px;
            }
        }
        
        /* ============================================
           ANIMATIONS
        ============================================ */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(24px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animate-in {
            animation: fadeInUp 0.5s ease forwards;
        }
        
        /* Hide sections when filtering */
        .event-section.hidden {
            display: none;
        }
        
        /* Photo protection (subtle) */
        .photo-protected {
            -webkit-touch-callout: none;
            user-select: none;
        }
    </style>
</head>
<body class="photo-protected">
    
    <!-- ============================================
         HEADER / NAVIGATION
    ============================================ -->
    <header class="gallery-header" id="galleryHeader">
        <div class="header-inner">
            <div class="header-brand">
                <div class="brand-icon">DK</div>
                <div class="brand-text">
                    <h1>Galeri Foto Kegiatan</h1>
                    <span>Dinkes Kutai Kartanegara</span>
                </div>
            </div>
            
            <div class="header-controls">
                <div class="search-wrapper">
                    <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                    <input type="text" class="search-input" id="searchInput" placeholder="Cari kegiatan...">
                </div>
                
                <select class="filter-select" id="yearFilter">
                    <option value="all">Semua Tahun</option>
                </select>
                
                <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="sun-icon"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="moon-icon" style="display:none"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
                </button>
                
                <button class="mobile-menu-btn" aria-label="Menu">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
                </button>
            </div>
        </div>
    </header>
    
    <!-- STATS BAR -->
    <div class="stats-bar">
        <div class="stats-inner">
            <div class="stat-item">
                <span class="stat-number" id="totalActivities">{{total_activities}}</span>
                <span class="stat-label">Kegiatan</span>
            </div>
            <div class="stat-item">
                <span class="stat-number" id="totalPhotos">{{total_photos}}</span>
                <span class="stat-label">Foto</span>
            </div>
            <div class="stat-item">
                <span class="stat-number" id="totalCategories">{{total_categories}}</span>
                <span class="stat-label">Kategori</span>
            </div>
        </div>
    </div>
    
    <!-- CATEGORY FILTERS -->
    <div class="category-filters">
        <div class="filters-inner" id="categoryFilters">
            <button class="filter-pill active" data-category="all">Semua Kegiatan</button>
            <button class="filter-pill" data-category="Pelatihan">Pelatihan</button>
            <button class="filter-pill" data-category="Sosialisasi">Sosialisasi</button>
            <button class="filter-pill" data-category="Bimtek">Bimtek</button>
            <button class="filter-pill" data-category="Rapat">Rapat</button>
            <button class="filter-pill" data-category="Kunjungan">Kunjungan</button>
            <button class="filter-pill" data-category="Lainnya">Lainnya</button>
        </div>
    </div>
    
    <!-- ============================================
         MAIN CONTENT
    ============================================ -->
    <main class="main-content" id="mainContent">
        
        {{featured_section}}
        
        {{event_sections}}
        
        <!-- LOAD MORE -->
        <div class="load-more-container" id="loadMoreContainer">
            <p class="load-more-stats">
                Menampilkan <strong id="shownCount">0</strong> dari <strong id="totalCount">0</strong> kegiatan
            </p>
            <button class="load-more-btn" id="loadMoreBtn">
                Muat Lebih Banyak
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>
            </button>
        </div>
        
        <!-- EMPTY STATE (hidden by default) -->
        <div class="empty-state" id="emptyState" style="display: none;">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>
            <h3>Tidak Ada Kegiatan Ditemukan</h3>
            <p>Coba ubah filter atau kata kunci pencarian</p>
        </div>
        
    </main>
    
    <!-- FOOTER -->
    <footer class="gallery-footer">
        <p class="footer-text">
            <strong>&copy; 2026 Dinas Kesehatan Kabupaten Kutai Kartanegara</strong><br>
            Galeri Foto Dokumentasi Kegiatan SDMK
        </p>
    </footer>
    
    <!-- ============================================
         PREMIUM LIGHTBOX
    ============================================ -->
    <div class="lightbox-overlay" id="lightbox">
        <div class="lightbox-header">
            <div class="lightbox-info">
                <h3 class="lightbox-title" id="lightboxTitle">Foto Kegiatan</h3>
                <span class="lightbox-counter" id="lightboxCounter">1 / 10</span>
            </div>
            <div class="lightbox-actions">
                <button class="lightbox-btn" id="zoomOutBtn" title="Perkecil (−)">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3M8 11h6"/></svg>
                </button>
                <button class="lightbox-btn" id="zoomInBtn" title="Perbesar (+)">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3M11 8v6M8 11h6"/></svg>
                </button>
                <button class="lightbox-btn" id="resetZoomBtn" title="Reset Zoom">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
                </button>
                <button class="lightbox-btn lightbox-close" id="lightboxClose" title="Tutup (ESC)">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg>
                </button>
            </div>
        </div>
        
        <div class="lightbox-main" id="lightboxMain">
            <button class="lightbox-nav lightbox-prev" id="lightboxPrev" title="Sebelumnya (←)">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m15 18-6-6 6-6"/></svg>
            </button>
            
            <div class="lightbox-image-container" id="imageContainer">
                <img src="" alt="" class="lightbox-image" id="lightboxImage" draggable="false">
            </div>
            
            <button class="lightbox-nav lightbox-next" id="lightboxNext" title="Selanjutnya (→)">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m9 18 6-6-6-6"/></svg>
            </button>
            
            <div class="zoom-controls">
                <button class="zoom-btn" id="zoomMinus">−</button>
                <span class="zoom-level" id="zoomLevel">100%</span>
                <button class="zoom-btn" id="zoomPlus">+</button>
            </div>
        </div>
        
        <div class="lightbox-thumbnails" id="lightboxThumbnails">
            <div class="thumbnail-list" id="thumbnailList"></div>
        </div>
    </div>

    <script>
        // ============================================
        // GALLERY DATA
        // ============================================
        const GALLERY_DATA = {{{gallery_data}}};
        
        // State
        let currentCategory = 'all';
        let currentSearch = '';
        let currentYear = 'all';
        let visibleCount = 6; // Initial visible events
        let filteredEvents = [];
        
        // Lightbox state
        let lightboxOpen = false;
        let currentLightboxIndex = 0;
        let currentLightboxPhotos = [];
        let zoomLevel = 1;
        let panX = 0;
        let panY = 0;
        let isDragging = false;
        let dragStartX = 0;
        let dragStartY = 0;
        let lastPanX = 0;
        let lastPanY = 0;
        
        // DOM Elements
        const header = document.getElementById('galleryHeader');
        const searchInput = document.getElementById('searchInput');
        const yearFilter = document.getElementById('yearFilter');
        const themeToggle = document.getElementById('themeToggle');
        const categoryFilters = document.getElementById('categoryFilters');
        const mainContent = document.getElementById('mainContent');
        const loadMoreBtn = document.getElementById('loadMoreBtn');
        const loadMoreContainer = document.getElementById('loadMoreContainer');
        const shownCountEl = document.getElementById('shownCount');
        const totalCountEl = document.getElementById('totalCount');
        
        // Lightbox elements
        const lightbox = document.getElementById('lightbox');
        const lightboxImage = document.getElementById('lightboxImage');
        const lightboxTitle = document.getElementById('lightboxTitle');
        const lightboxCounter = document.getElementById('lightboxCounter');
        const lightboxClose = document.getElementById('lightboxClose');
        const lightboxPrev = document.getElementById('lightboxPrev');
        const lightboxNext = document.getElementById('lightboxNext');
        const thumbnailList = document.getElementById('thumbnailList');
        const imageContainer = document.getElementById('imageContainer');
        const zoomLevelEl = document.getElementById('zoomLevel');
        
        // ============================================
        // INITIALIZATION
        // ============================================
        function init() {
            populateYearFilter();
            applySavedTheme();
            setupEventListeners();
            filterAndRenderEvents();
            setupScrollAnimations();
            updateStats();
        }
        
        function populateYearFilter() {
            const years = [...new Set(GALLERY_DATA.map(e => e.tahun))].sort((a,b) => b-a);
            years.forEach(year => {
                const option = document.createElement('option');
                option.value = year;
                option.textContent = year;
                yearFilter.appendChild(option);
            });
        }
        
        function updateStats() {
            const categories = new Set(GALLERY_DATA.map(e => e.kategori || 'Lainnya'));
            document.getElementById('totalActivities').textContent = GALLERY_DATA.length;
            document.getElementById('totalPhotos').textContent = GALLERY_DATA.reduce((sum, e) => sum + e.photos.length, 0);
            document.getElementById('totalCategories').textContent = categories.size;
        }
        
        // ============================================
        // THEME (DARK MODE)
        // ============================================
        function applySavedTheme() {
            const savedTheme = localStorage.getItem('gallery-theme') || 'light';
            document.documentElement.setAttribute('data-theme', savedTheme);
            updateThemeIcon(savedTheme);
        }
        
        function toggleTheme() {
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('gallery-theme', next);
            updateThemeIcon(next);
        }
        
        function updateThemeIcon(theme) {
            const sunIcon = themeToggle.querySelector('.sun-icon');
            const moonIcon = themeToggle.querySelector('.moon-icon');
            if (theme === 'dark') {
                sunIcon.style.display = 'none';
                moonIcon.style.display = 'block';
            } else {
                sunIcon.style.display = 'block';
                moonIcon.style.display = 'none';
            }
        }
        
        // ============================================
        // HEADER SCROLL EFFECT
        // ============================================
        function handleScroll() {
            if (window.scrollY > 20) {
                header.classList.add('header-scrolled');
            } else {
                header.classList.remove('header-scrolled');
            }
        }
        
        // ============================================
        // FILTERING & RENDERING
        // ============================================
        function filterAndRenderEvents() {
            // Filter events
            filteredEvents = GALLERY_DATA.filter(event => {
                const matchCategory = currentCategory === 'all' || (event.kategori || 'Lainnya') === currentCategory;
                const matchYear = currentYear === 'all' || event.tahun === currentYear;
                const matchSearch = currentSearch === '' || 
                    event.judul.toLowerCase().includes(currentSearch.toLowerCase()) ||
                    (event.tempat || '').toLowerCase().includes(currentSearch.toLowerCase());
                return matchCategory && matchYear && matchSearch;
            });
            
            // Update counts
            totalCountEl.textContent = filteredEvents.length;
            
            // Get DOM elements
            const emptyState = document.getElementById('emptyState');
            const eventSections = document.querySelectorAll('.event-section');
            
            // Show/hide empty state
            if (filteredEvents.length === 0) {
                emptyState.style.display = 'block';
                loadMoreContainer.style.display = 'none';
                eventSections.forEach(section => section.classList.add('hidden'));
            } else {
                emptyState.style.display = 'none';
                loadMoreContainer.style.display = 'block';
                
                // Show/hide events based on visible count
                eventSections.forEach((section) => {
                    const eventId = section.dataset.eventId;
                    const eventIndex = filteredEvents.findIndex(e => e.id === eventId);
                    
                    if (eventIndex === -1) {
                        section.classList.add('hidden');
                    } else if (eventIndex < visibleCount) {
                        section.classList.remove('hidden');
                    } else {
                        section.classList.add('hidden');
                    }
                });
                
                // Update shown count
                const visibleSections = document.querySelectorAll('.event-section:not(.hidden)');
                shownCountEl.textContent = Math.min(visibleSections.length, filteredEvents.length);
                
                // Update load more button state
                if (visibleCount >= filteredEvents.length) {
                    loadMoreContainer.classList.add('all-loaded');
                } else {
                    loadMoreContainer.classList.remove('all-loaded');
                }
            }
        }
        
        function loadMore() {
            visibleCount += 3;
            filterAndRenderEvents();
        }
        
        // ============================================
        // SCROLL ANIMATIONS (Intersection Observer)
        // ============================================
        function setupScrollAnimations() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            }, {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            });
            
            document.querySelectorAll('.event-section').forEach(section => {
                observer.observe(section);
            });
        }
        
        // ============================================
        // EVENT LISTENERS
        // ============================================
        function setupEventListeners() {
            // Scroll
            window.addEventListener('scroll', handleScroll, { passive: true });
            
            // Search
            searchInput.addEventListener('debounce', () => {
                currentSearch = searchInput.value;
                visibleCount = 6;
                filterAndRenderEvents();
            });
            
            let searchTimeout;
            searchInput.addEventListener('input', () => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    currentSearch = searchInput.value;
                    visibleCount = 6;
                    filterAndRenderEvents();
                }, 300);
            });
            
            // Year filter
            yearFilter.addEventListener('change', () => {
                currentYear = yearFilter.value;
                visibleCount = 6;
                filterAndRenderEvents();
            });
            
            // Theme toggle
            themeToggle.addEventListener('click', toggleTheme);
            
            // Category filters
            categoryFilters.addEventListener('click', (e) => {
                if (e.target.classList.contains('filter-pill')) {
                    categoryFilters.querySelectorAll('.filter-pill').forEach(pill => pill.classList.remove('active'));
                    e.target.classList.add('active');
                    currentCategory = e.target.dataset.category;
                    visibleCount = 6;
                    filterAndRenderEvents();
                }
            });
            
            // Load more
            loadMoreBtn.addEventListener('click', loadMore);
            
            // Lightbox controls
            lightboxClose.addEventListener('click', closeLightbox);
            lightboxPrev.addEventListener('click', () => navigateLightbox(-1));
            lightboxNext.addEventListener('click', () => navigateLightbox(1));
            
            document.getElementById('zoomInBtn').addEventListener('click', () => adjustZoom(0.25));
            document.getElementById('zoomOutBtn').addEventListener('click', () => adjustZoom(-0.25));
            document.getElementById('resetZoomBtn').addEventListener('click', resetZoom);
            document.getElementById('zoomPlus').addEventListener('click', () => adjustZoom(0.25));
            document.getElementById('zoomMinus').addEventListener('click', () => adjustZoom(-0.25));
            
            // Click outside image to close
            lightbox.addEventListener('click', (e) => {
                if (e.target === lightbox || e.target.closest('.lightbox-main') && !e.target.closest('.lightbox-image-container')) {
                    closeLightbox();
                }
            });
            
            // Keyboard navigation
            document.addEventListener('keydown', handleKeyboard);
            
            // Mouse wheel zoom
            lightbox.addEventListener('wheel', handleWheel, { passive: false });
            
            // Touch/drag for zoomed image
            lightboxImage.addEventListener('mousedown', startDrag);
            document.addEventListener('mousemove', drag);
            document.addEventListener('mouseup', endDrag);
            
            // Touch events for mobile
            lightboxImage.addEventListener('touchstart', startTouchDrag, { passive: false });
            document.addEventListener('touchmove', touchDrag, { passive: false });
            document.addEventListener('touchend', endDrag);
            
            // Double click to zoom
            lightboxImage.addEventListener('dblclick', handleDoubleClick);
            
            // Prevent context menu on images
            lightboxImage.addEventListener('contextmenu', (e) => e.preventDefault());
        }
        
        // ============================================
        // LIGHTBOX FUNCTIONS
        // ============================================
        function openLightbox(photoUrl, photos, index, eventTitle) {
            currentLightboxPhotos = photos;
            currentLightboxIndex = index;
            lightboxOpen = true;
            
            lightbox.classList.add('lightbox-active');
            document.body.style.overflow = 'hidden';
            
            showLightboxPhoto(eventTitle);
            renderThumbnails();
        }
        
        function closeLightbox() {
            lightboxOpen = false;
            lightbox.classList.remove('lightbox-active');
            document.body.style.overflow = '';
            resetZoom();
        }
        
        function showLightboxPhoto(eventTitle) {
            const photo = currentLightboxPhotos[currentLightboxIndex];
            if (!photo) return;
            
            // Use high quality version for lightbox
            const highResUrl = photo.highResUrl || photo.originalUrl || photo.url;
            
            lightboxImage.src = highResUrl;
            lightboxImage.alt = photo.filename || 'Foto kegiatan';
            lightboxTitle.textContent = eventTitle || 'Foto Kegiatan';
            lightboxCounter.textContent = `${currentLightboxIndex + 1} / ${currentLightboxPhotos.length}`;
            
            resetZoom();
            updateThumbnailActive();
        }
        
        function navigateLightbox(direction) {
            currentLightboxIndex += direction;
            if (currentLightboxIndex < 0) currentLightboxIndex = currentLightboxPhotos.length - 1;
            if (currentLightboxIndex >= currentLightboxPhotos.length) currentLightboxIndex = 0;
            showLightboxPhoto(lightboxTitle.textContent);
        }
        
        function goToPhoto(index) {
            currentLightboxIndex = index;
            showLightboxPhoto(lightboxTitle.textContent);
        }
        
        // ============================================
        // THUMBNAILS
        // ============================================
        function renderThumbnails() {
            thumbnailList.innerHTML = '';
            currentLightboxPhotos.forEach((photo, index) => {
                const thumb = document.createElement('div');
                thumb.className = `thumbnail-item${index === currentLightboxIndex ? ' active' : ''}`;
                thumb.innerHTML = `<img src="${photo.thumbUrl}" alt="Thumbnail ${index + 1}" loading="lazy">`;
                thumb.addEventListener('click', () => goToPhoto(index));
                thumbnailList.appendChild(thumb);
            });
            
            // Scroll active thumbnail into view
            setTimeout(() => {
                const activeThumb = thumbnailList.querySelector('.active');
                if (activeThumb) {
                    activeThumb.scrollIntoView({ behavior: 'smooth', inline: 'center' });
                }
            }, 100);
        }
        
        function updateThumbnailActive() {
            thumbnailList.querySelectorAll('.thumbnail-item').forEach((thumb, index) => {
                thumb.classList.toggle('active', index === currentLightboxIndex);
            });
            
            const activeThumb = thumbnailList.querySelector('.active');
            if (activeThumb) {
                activeThumb.scrollIntoView({ behavior: 'smooth', inline: 'center' });
            }
        }
        
        // ============================================
        // ZOOM FUNCTIONS
        // ============================================
        function adjustZoom(delta) {
            zoomLevel = Math.max(0.5, Math.min(5, zoomLevel + delta));
            applyZoom();
        }
        
        function setZoom(level) {
            zoomLevel = Math.max(0.5, Math.min(5, level));
            applyZoom();
        }
        
        function resetZoom() {
            zoomLevel = 1;
            panX = 0;
            panY = 0;
            applyZoom();
        }
        
        function applyZoom() {
            lightboxImage.style.transform = `translate(${panX}px, ${panY}px) scale(${zoomLevel})`;
            zoomLevelEl.textContent = `${Math.round(zoomLevel * 100)}%`;
            
            // Show/hide reset button
            document.getElementById('resetZoomBtn').style.opacity = zoomLevel !== 1 ? '1' : '0.5';
        }
        
        function handleWheel(e) {
            e.preventDefault();
            const delta = e.deltaY > 0 ? -0.15 : 0.15;
            adjustZoom(delta);
        }
        
        function handleDoubleClick(e) {
            if (zoomLevel === 1) {
                // Zoom to click position
                const rect = lightboxImage.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width;
                const y = (e.clientY - rect.top) / rect.height;
                
                zoomLevel = 2.5;
                panX = -(x - 0.5) * rect.width * 1.5;
                panY = -(y - 0.5) * rect.height * 1.5;
                applyZoom();
            } else {
                resetZoom();
            }
        }
        
        // Drag functions (for panning when zoomed)
        function startDrag(e) {
            if (zoomLevel <= 1) return;
            isDragging = true;
            dragStartX = e.clientX;
            dragStartY = e.clientY;
            lastPanX = panX;
            lastPanY = panY;
            lightboxImage.classList.add('dragging');
        }
        
        function drag(e) {
            if (!isDragging) return;
            e.preventDefault();
            panX = lastPanX + (e.clientX - dragStartX);
            panY = lastPanY + (e.clientY - dragStartY);
            applyZoom();
        }
        
        function endDrag() {
            isDragging = false;
            lightboxImage.classList.remove('dragging');
        }
        
        // Touch drag
        let touchStartDist = 0;
        let touchStartZoom = 1;
        
        function startTouchDrag(e) {
            if (e.touches.length === 1 && zoomLevel > 1) {
                // Single touch - pan
                const touch = e.touches[0];
                isDragging = true;
                dragStartX = touch.clientX;
                dragStartY = touch.clientY;
                lastPanX = panX;
                lastPanY = panY;
                lightboxImage.classList.add('dragging');
            } else if (e.touches.length === 2) {
                // Pinch zoom
                e.preventDefault();
                const dx = e.touches[0].clientX - e.touches[1].clientX;
                const dy = e.touches[0].clientY - e.touches[1].clientY;
                touchStartDist = Math.sqrt(dx * dx + dy * dy);
                touchStartZoom = zoomLevel;
            }
        }
        
        function touchDrag(e) {
            if (!isDragging && e.touches.length !== 2) return;
            
            if (e.touches.length === 1 && isDragging) {
                // Pan
                const touch = e.touches[0];
                panX = lastPanX + (touch.clientX - dragStartX);
                panY = lastPanY + (touch.clientY - dragStartY);
                applyZoom();
            } else if (e.touches.length === 2) {
                // Pinch zoom
                e.preventDefault();
                const dx = e.touches[0].clientX - e.touches[1].clientX;
                const dy = e.touches[0].clientY - e.touches[1].clientY;
                const dist = Math.sqrt(dx * dx + dy * dy);
                const scale = dist / touchStartDist;
                zoomLevel = Math.max(0.5, Math.min(5, touchStartZoom * scale));
                applyZoom();
            }
        }
        
        // Swipe navigation
        let touchStartX = 0;
        let touchEndX = 0;
        
        lightboxImage.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        
        lightboxImage.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, { passive: true });
        
        function handleSwipe() {
            const diff = touchStartX - touchEndX;
            const threshold = 80;
            
            if (Math.abs(diff) > threshold && zoomLevel <= 1.2) {
                if (diff > 0) {
                    navigateLightbox(1); // Swipe left = next
                } else {
                    navigateLightbox(-1); // Swipe right = prev
                }
            }
        }
        
        // Keyboard navigation
        function handleKeyboard(e) {
            if (!lightboxOpen) return;
            
            switch(e.key) {
                case 'Escape':
                    closeLightbox();
                    break;
                case 'ArrowLeft':
                    navigateLightbox(-1);
                    break;
                case 'ArrowRight':
                    navigateLightbox(1);
                    break;
                case '+':
                case '=':
                    adjustZoom(0.25);
                    break;
                case '-':
                    adjustZoom(-0.25);
                    break;
                case '0':
                    resetZoom();
                    break;
            }
        }
        
        // ============================================
        // PHOTO CLICK HANDLERS (attached to cards)
        // ============================================
        function attachPhotoHandlers() {
            document.querySelectorAll('[data-photos]').forEach(card => {
                card.addEventListener('click', (e) => {
                    e.preventDefault();
                    const photosJson = card.dataset.photos;
                    const eventTitle = card.dataset.eventTitle || 'Foto Kegiatan';
                    const photoIndex = parseInt(card.dataset.photoIndex) || 0;
                    
                    try {
                        const photos = JSON.parse(photosJson);
                        openLightbox(photos[photoIndex]?.url, photos, photoIndex, eventTitle);
                    } catch(err) {
                        console.error('Error parsing photos:', err);
                    }
                });
            });
        }
        
        // Initialize handlers after DOM ready
        document.addEventListener('DOMContentLoaded', () => {
            init();
            attachPhotoHandlers();
        });
        
        // Also run immediately in case DOM already loaded
        if (document.readyState !== 'loading') {
            init();
            attachPhotoHandlers();
        }
    </script>
</body>
</html>'''


def fetch_cloudinary_photos():
    """Fetch all photos from Cloudinary (all resources)"""
    cloudinary.config(
        cloud_name=CLOUD_CONFIG["cloud_name"],
        api_key=CLOUD_CONFIG["api_key"],
        api_secret=CLOUD_CONFIG["api_secret"]
    )
    
    print("📡 Mengambil data dari Cloudinary...")
    
    all_resources = []
    next_cursor = None
    
    while True:
        try:
            params = {
                "type": "upload",
                "max_results": 500,
                "resource_type": "image"
            }
            if next_cursor:
                params["next_cursor"] = next_cursor
            
            result = resources(**params)
            
            all_resources.extend(result.get('resources', []))
            next_cursor = result.get('next_cursor')
            
            if not next_cursor:
                break
                
            print(f"   ↳ Terambil {len(all_resources)} resource...")
            
        except Exception as e:
            print(f"❌ Error fetching from Cloudinary: {e}")
            break
    
    # Return all image resources (filtering will happen in process_activities)
    print(f"✅ Total resource ditemukan: {len(all_resources)}")
    return all_resources


def categorize_activity(judul):
    """Auto-categorize activity based on title keywords"""
    judul_lower = judul.lower()
    
    if any(word in judul_lower for word in ['pelatihan', 'workshop', 'training']):
        return 'Pelatihan'
    elif any(word in judul_lower for word in ['sosialisasi', 'edukasi', 'penyuluhan']):
        return 'Sosialisasi'
    elif any(word in judul_lower for word in ['bimtek', 'bimbingan teknis']):
        return 'Bimtek'
    elif any(word in judul_lower for word in ['rapat', 'koordinasi', 'musyawarah']):
        return 'Rapat'
    elif any(word in judul_lower for word in ['kunjungan', 'monitoring', 'evaluasi', 'supervisi']):
        return 'Kunjungan'
    else:
        return 'Lainnya'


def extract_date_from_public_id(public_id):
    """Extract date from various filename patterns"""
    patterns = [
        (r'(20\d{2})[-_](\d{2})[-_](\d{2})', lambda m: f"{m.group(1)}-{m.group(2)}-{m.group(3)}"),
        (r'(\d{4})(\d{2})(\d{2})', lambda m: f"{m.group(1)}-{m.group(2)}-{m.group(3)}"),
    ]
    
    for pattern, formatter in patterns:
        match = re.search(pattern, public_id)
        if match:
            year, month, day = match.groups()
            if 2020 <= int(year) <= 2030 and 1 <= int(month) <= 12 and 1 <= int(day) <= 31:
                return formatter(match)
    return None


import urllib.request

def validate_cloudinary_url(url):
    """Validate that a Cloudinary URL returns 200 OK"""
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        response = urllib.request.urlopen(req, timeout=5)
        return response.status == 200
    except:
        return False


def process_activities(resources, config_data):
    """Process raw resources into organized activities by date - ONLY VALID URLs"""
    activities_config = config_data.get("activities_config", {})
    photos_by_date = defaultdict(list)
    
    print(f"📅 Processing {len(resources)} resources...")
    
    valid_count = 0
    invalid_count = 0
    
    for resource in resources:
        public_id = resource.get("public_id", "")
        format = resource.get("format", "jpg")
        
        # Skip sample images
        if public_id.startswith('samples/') or 'sample' in public_id.lower():
            continue
        
        # Extract date from filename
        date_str = extract_date_from_public_id(public_id)
        
        if not date_str:
            # Try to find matching activity by checking config IDs in public_id
            for cfg_date, cfg_info in activities_config.items():
                cfg_id = cfg_info.get("id", "")
                if cfg_id and cfg_id.lower() in public_id.lower():
                    date_str = cfg_date
                    break
        
        if not date_str:
            continue
        
        # Create photo URL (use simpler format for better compatibility)
        photo_url = f"https://res.cloudinary.com/{CLOUD_CONFIG['cloud_name']}/image/upload/w_800,q_auto/{public_id}.jpg"
        thumb_url = f"https://res.cloudinary.com/{CLOUD_CONFIG['cloud_name']}/image/upload/w_150,q_auto/{public_id}.jpg"
        original_url = f"https://res.cloudinary.com/{CLOUD_CONFIG['cloud_name']}/image/upload/q_auto:eco/{public_id}.jpg"
        high_res_url = f"https://res.cloudinary.com/{CLOUD_CONFIG['cloud_name']}/image/upload/w_1920,q_auto/{public_id}.jpg"
        
        # VALIDATE URL before adding
        if validate_cloudinary_url(photo_url):
            photos_by_date[date_str].append({
                "public_id": public_id,
                "filename": public_id.split("/")[-1] if '/' in public_id else public_id,
                "format": "jpg",
                "url": photo_url,
                "thumbUrl": thumb_url,
                "originalUrl": original_url,
                "highResUrl": high_res_url,
                "created_at": resource.get("created_at", "")
            })
            valid_count += 1
            print(f"  ✅ Valid: {public_id[:40]}...")
        else:
            invalid_count += 1
            print(f"  ❌ Invalid: {public_id[:40]}...")
    
    print(f"\n📊 Validation Results: {valid_count} valid, {invalid_count} invalid")
    
    # Convert to activities list with config metadata
    activities = []
    
    for date_str in sorted(photos_by_date.keys(), reverse=True):
        photos = photos_by_date[date_str]
        
        # Get config for this date if exists
        activity_info = activities_config.get(date_str, {})
        
        if activity_info:
            activity = {
                "id": activity_info.get("id", f"kegiatan-{date_str}"),
                "judul": activity_info.get("judul", f"Kegiatan {date_str}"),
                "tanggal": activity_info.get("tanggal", date_str),
                "tempat": activity_info.get("tempat", "Dokumentasi Kegiatan"),
                "tahun": activity_info.get("tahun", date_str[:4]),
                "deskripsi": activity_info.get("deskripsi", ""),
                "kategori": categorize_activity(activity_info.get("judul", "")),
                "folder": activity_info.get("id", ""),
                "photos": sorted(photos, key=lambda x: x["filename"])
            }
        else:
            activity = {
                "id": f"kegiatan-{date_str}",
                "judul": f"Kegiatan {date_str}",
                "tanggal": date_str,
                "tempat": "Dokumentasi Kegiatan",
                "tahun": date_str[:4],
                "deskripsi": "",
                "kategori": "Lainnya",
                "folder": "",
                "photos": sorted(photos, key=lambda x: x["filename"])
            }
        
        activities.append(activity)
    
    return activities


def generate_featured_section(activities_list):
    """Generate featured event section HTML"""
    if not activities_list:
        return "<!-- No featured events -->"
    
    # Get first/most recent activity as featured
    featured = activities_list[0]
    photos = featured.get("photos", [])
    
    if not photos:
        return "<!-- No photos for featured -->"
    
    main_photo = photos[0]
    secondary_photos = photos[1:3] if len(photos) > 1 else [photos[0]]
    
    # Pre-compute JSON for data attributes
    photos_json = json.dumps(photos)
    
    html = f'''
    <!-- FEATURED EVENT SECTION -->
    <section class="featured-section event-section animate-in" data-event-id="{featured['id']}" data-category="{featured.get('kategori', 'Lainnya')}">
        <div class="section-header">
            <div class="section-title-group">
                <span class="section-badge">⭐ Unggulan</span>
                <h2 class="section-title">Kegiatan Terbaru</h2>
            </div>
            <span class="event-category-tag">{featured.get('kategori', 'Lainnya')}</span>
        </div>
        
        <div class="featured-bento">
            <!-- Main Featured Photo -->
            <div class="featured-main shimmer photo-protected" 
                 data-photos='{photos_json}' 
                 data-event-title="{featured['judul']}"
                 data-photo-index="0">
                <img src="{main_photo['url']}" 
                     alt="{featured['judul']}" 
                     loading="eager"
                     onerror="this.style.background='#f1f3f5'">
                <div class="featured-overlay">
                    <span class="featured-label">Kegiatan Terbaru</span>
                    <h3 class="featured-event-title">{featured['judul']}</h3>
                    <div class="featured-meta">
                        <span>📅 {featured['tanggal']}</span>
                        <span>📍 {featured.get('tempat', 'Dokumentasi')}</span>
                    </div>
                </div>
                <span class="photo-count-badge">
                    📷 {len(photos)} foto
                </span>
            </div>
'''
    
    # Add secondary photos
    for i, photo in enumerate(secondary_photos[:2]):
        idx = i + 1
        html += f'''
            <!-- Secondary Photo {i+1} -->
            <div class="featured-sub shimmer photo-protected"
                 data-photos='{photos_json}'
                 data-event-title="{featured['judul']}"
                 data-photo-index="{idx}">
                <img src="{photo['url']}"
                     alt="{featured['judul']} - Foto {idx+1}"
                     loading="lazy"
                     onerror="this.style.background='#f1f3f5'">
                <div class="featured-overlay">
                    <span class="featured-label">{featured['kategori']}</span>
                    <h4 class="featured-event-title">{featured['judul']}</h4>
                </div>
            </div>
'''
    
    html += "</div></section>"
    return html


def get_bento_layout_class(index, photo_count):
    """Get bento layout class based on index (alternating patterns)"""
    layouts = ['bento-layout-a', 'bento-layout-b', 'bento-layout-c']
    return layouts[index % 3]


def generate_event_sections(activities_list):
    """Generate all event sections with alternating bento layouts"""
    sections_html = ""
    
    for i, activity in enumerate(activities_list):
        photos = activity.get("photos", [])
        if not photos:
            continue
            
        layout_class = get_bento_layout_class(i, len(photos))
        kategori = activity.get("kategori", "Lainnya")
        
        section_html = f'''
    <!-- Event Section: {activity['judul']} -->
    <section class="event-section" data-event-id="{activity['id']}" data-category="{kategori}">
        <div class="event-header">
            <div class="event-info">
                <h2>{activity['judul']}</h2>
                <div class="event-meta">
                    <span class="event-meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
                        {activity['tanggal']}
                    </span>
                    <span class="event-meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                        {activity.get('tempat', 'Dokumentasi')}
                    </span>
                    <span class="event-meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>
                        {len(photos)} foto
                    </span>
                </div>
            </div>
            <span class="event-category-tag">{kategori}</span>
        </div>
        
        <div class="{layout_class}">
'''
        
        # Generate bento cards based on layout
        if layout_class == 'bento-layout-a':
            # Layout A: Large left + 2x2 grid right
            section_html += generate_layout_a_cards(activity, photos)
        elif layout_class == 'bento-layout-b':
            # Layout B: Top wide + 3 below
            section_html += generate_layout_b_cards(activity, photos)
        else:
            # Layout C: Asymmetric masonry
            section_html += generate_layout_c_cards(activity, photos)
        
        section_html += """
        </div>
    </section>
"""
        sections_html += section_html
    
    return sections_html


def generate_layout_a_cards(activity, photos):
    """Layout A: Large left card + smaller right cards"""
    html = ""
    
    # Pre-compute JSON for data attributes
    photos_json = json.dumps(photos)
    
    # Main large card (first photo)
    main_photo = photos[0]
    html += f'''<div class="bento-card bento-large shimmer photo-protected"
                 data-photos='{photos_json}'
                 data-event-title="{activity['judul']}"
                 data-photo-index="0">
                <img src="{main_photo['url']}"
                     alt="{activity['judul']}"
                     loading="lazy"
                     onerror="this.style.background='#f1f3f5'">
                <div class="bento-card-overlay">
                    <div class="bento-card-info">
                        <span>{len(photos)} foto tersedia</span>
                    </div>
                </div>
            </div>
'''
    
    # Remaining photos in grid
    remaining = photos[1:5]  # Up to 4 more
    for i, photo in enumerate(remaining):
        idx = i + 1
        html += f'''<div class="bento-card shimmer photo-protected"
                 data-photos='{photos_json}'
                 data-event-title="{activity['judul']}"
                 data-photo-index="{idx}">
                <img src="{photo['url']}"
                     alt="{activity['judul']} - {idx+1}"
                     loading="lazy"
                     onerror="this.style.background='#f1f3f5'">
                <div class="bento-card-overlay">
                    <div class="bento-card-info">
                        <span>Foto {idx+1}</span>
                    </div>
                </div>
            </div>
'''
    
    return html


def generate_layout_b_cards(activity, photos):
    """Layout B: Wide top + 3 column below"""
    html = ""
    
    # Pre-compute JSON for data attributes
    photos_json = json.dumps(photos)
    
    # Wide top card
    top_photo = photos[0] if len(photos) > 0 else None
    if top_photo:
        html += f'''<div class="bento-card bento-wide shimmer photo-protected"
                 data-photos='{photos_json}'
                 data-event-title="{activity['judul']}"
                 data-photo-index="0">
                <img src="{top_photo['url']}"
                     alt="{activity['judul']}"
                     loading="lazy"
                     onerror="this.style.background='#f1f3f5'">
                <div class="bento-card-overlay">
                    <div class="bento-card-info">
                        <span>{activity['judul']}</span>
                    </div>
                </div>
            </div>
'''
    
    # 3 cards below
    below_photos = photos[1:4]
    for i, photo in enumerate(below_photos):
        idx = i + 1
        html += f'''<div class="bento-card shimmer photo-protected"
                 data-photos='{photos_json}'
                 data-event-title="{activity['judul']}"
                 data-photo-index="{idx}">
                <img src="{photo['url']}"
                     alt="{activity['judul']} - {idx+1}"
                     loading="lazy"
                     onerror="this.style.background='#f1f3f5'">
            </div>
'''
    
    return html


def generate_layout_c_cards(activity, photos):
    """Layout C: Asymmetric masonry-style"""
    html = ""
    
    # Pre-compute JSON for data attributes
    photos_json = json.dumps(photos)
    
    # First tall card
    if len(photos) > 0:
        html += f'''<div class="bento-card bento-tall shimmer photo-protected"
                 data-photos='{photos_json}'
                 data-event-title="{activity['judul']}"
                 data-photo-index="0">
                <img src="{photos[0]['url']}"
                     alt="{activity['judul']}"
                     loading="lazy"
                     onerror="this.style.background='#f1f3f5'">
            </div>
'''
    
    # Wide card (spans 2 cols)
    if len(photos) > 1:
        html += f'''<div class="bento-card bento-wide-2 shimmer photo-protected"
                 data-photos='{photos_json}'
                 data-event-title="{activity['judul']}"
                 data-photo-index="1">
                <img src="{photos[1]['url']}"
                     alt="{activity['judul']} - 2"
                     loading="lazy"
                     onerror="this.style.background='#f1f3f5'">
            </div>
'''
    
    # Regular cards
    for i, photo in enumerate(photos[2:6]):
        idx = i + 2
        html += f'''<div class="bento-card shimmer photo-protected"
                 data-photos='{photos_json}'
                 data-event-title="{activity['judul']}"
                 data-photo-index="{idx}">
                <img src="{photo['url']}"
                     alt="{activity['judul']} - {idx+1}"
                     loading="lazy"
                     onerror="this.style.background='#f1f3f5'">
            </div>
'''
    
    return html


def main():
    """Main function to generate gallery HTML"""
    print("=" * 60)
    print("🖼️  BENTO + MASONRY HYBRID GALLERY v4.0 GENERATOR")
    print("=" * 60)
    
    # Step 1: Fetch from Cloudinary
    resources = fetch_cloudinary_photos()
    
    if not resources:
        print("❌ Tidak ada foto ditemukan di Cloudinary!")
        return
    
    # Step 2: Load config
    try:
        with open("/home/z/my-project/scripts/gallery-config.json", "r") as f:
            config_data = json.load(f)
        print("✅ Config loaded successfully")
    except Exception as e:
        print(f"⚠️ Config load error: {e}")
        config_data = {}
    
    # Step 3: Process into activities (already sorted by date, newest first)
    activities_list = process_activities(resources, config_data)
    
    total_photos = sum(len(a["photos"]) for a in activities_list)
    
    print(f"\n📊 STATISTIK:")
    print(f"   • Total Kegiatan: {len(activities_list)}")
    print(f"   • Total Foto: {total_photos}")
    
    for act in activities_list:
        print(f"      - {act['judul'][:50]}... ({len(act['photos'])} foto)")
    
    # Step 4: Generate HTML sections
    print(f"\n🎨 Generating Bento + Masonry layout...")
    
    featured_html = generate_featured_section(activities_list)
    events_html = generate_event_sections(activities_list)
    
    # Step 5: Build final HTML
    gallery_json = json.dumps(activities_list, ensure_ascii=False)
    
    final_html = HTML_TEMPLATE.replace("{{total_activities}}", str(len(activities_list)))
    final_html = final_html.replace("{{total_photos}}", str(total_photos))
    final_html = final_html.replace("{{total_categories}}", str(len(set(a.get("kategori", "Lainnya") for a in activities_list))))
    final_html = final_html.replace("{{featured_section}}", featured_html)
    final_html = final_html.replace("{{event_sections}}", events_html)
    final_html = final_html.replace("{{{gallery_data}}}", gallery_json)
    
    # Step 6: Write output file
    output_path = "/home/z/my-project/download/galeri-foto-standalone.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)
    
    print(f"\n✅ SUCCESS! Gallery generated:")
    print(f"   📁 Output: {output_path}")
    print(f"   📦 Size: {len(final_html):,} bytes")
    print(f"   🖼️  Ready to deploy!")
    
    return output_path


if __name__ == "__main__":
    main()
