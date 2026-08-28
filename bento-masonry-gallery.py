#!/usr/bin/env python3
"""
===========================================
MODERN BENTO + MASONRY HYBRID GALLERY v5.0
===========================================

UPDATE v5.0:
✅ Support folder structure: SDM KESEHATAN/Subfolder/Foto
✅ Auto-detect activities from FOLDER NAMES
✅ Support multiple subfolders
✅ Better Cloudinary API integration

Clean, Modern, Photography-Focused Photo Gallery
- Bento Grid with 3+ layout variations (A, B, C)
- Masonry-style photo grid
- Featured Event section with special Bento layout
- Premium Fullscreen Lightbox with zoom/swipe/thumbnails
- Category Filters (Pelatihan, Sosialisasi, Bimtek, Rapat, Kunjungan, Lainnya)
- Load More functionality
- Dark Mode with localStorage persistence
- Scroll animations (Intersection Observer)
- Mobile-perfect responsive design

Author: Auto-generated for Dinas Kesehatan Kab. Kutai Kartanegara
"""

import cloudinary
from cloudinary.api import resources as api_resources, subfolders as api_subfolders
import json
import re
from datetime import datetime
from collections import defaultdict
import urllib.request

# ============================================
# KONFIGURASI CLOUDINARY
# ============================================
CLOUD_CONFIG = {
    "cloud_name": "cla7jrww",
    "api_key": "488796372967593",
    "api_secret": "MvIaCN2zMacCWhJ2f2gJnFev0xw"
}

# Root folder name in Cloudinary
ROOT_FOLDER = "SDM KESEHATAN"

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
            border-radius: var(--radius-md);
            background: var(--bg-secondary);
            color: var(--text-primary);
            font-size: 14px;
            transition: all var(--transition-fast);
        }
        
        .search-input:focus {
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 0 3px var(--accent-light);
            width: 280px;
        }
        
        .search-icon {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }

        /* Dark Mode Toggle */
        .theme-toggle {
            width: 44px;
            height: 44px;
            border-radius: var(--radius-md);
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all var(--transition-fast);
            color: var(--text-secondary);
        }
        
        .theme-toggle:hover {
            background: var(--accent-light);
            color: var(--accent-color);
            border-color: var(--accent-color);
        }

        .theme-toggle .icon-sun { display: none; }
        .theme-toggle .icon-moon { display: block; }
        [data-theme="dark"] .theme-toggle .icon-sun { display: block; }
        [data-theme="dark"] .theme-toggle .icon-moon { display: none; }

        /* ============================================
           HERO SECTION
        ============================================ */
        .hero-section {
            padding: 80px 24px 60px;
            text-align: center;
            background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
        }
        
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: var(--accent-light);
            color: var(--accent-color);
            border-radius: 50px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 24px;
        }
        
        .hero-title {
            font-size: clamp(32px, 5vw, 56px);
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.1;
            margin-bottom: 16px;
            background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .hero-subtitle {
            font-size: clamp(16px, 2vw, 20px);
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto 32px;
            line-height: 1.6;
        }

        .hero-stats {
            display: flex;
            justify-content: center;
            gap: 48px;
            flex-wrap: wrap;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 36px;
            font-weight: 800;
            color: var(--accent-color);
            line-height: 1;
            margin-bottom: 4px;
        }
        
        .stat-label {
            font-size: 13px;
            color: var(--text-muted);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* ============================================
           CATEGORY FILTERS
        ============================================ */
        .filters-section {
            padding: 0 24px 32px;
            max-width: var(--max-width);
            margin: 0 auto;
        }
        
        .filters-container {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .filter-btn {
            padding: 10px 20px;
            border-radius: 50px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all var(--transition-fast);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .filter-btn:hover {
            border-color: var(--accent-color);
            color: var(--accent-color);
            transform: translateY(-2px);
        }
        
        .filter-btn.active {
            background: var(--accent-color);
            border-color: var(--accent-color);
            color: white;
        }

        .filter-count {
            background: rgba(255,255,255,0.2);
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .filter-btn:not(.active) .filter-count {
            background: var(--bg-tertiary);
        }

        /* ============================================
           FEATURED EVENT SECTION
        ============================================ */
        .featured-section {
            padding: 0 24px 60px;
            max-width: var(--max-width);
            margin: 0 auto;
        }
        
        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 32px;
        }
        
        .section-title {
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -0.02em;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .section-title-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 18px;
        }

        /* Featured Bento Grid */
        .featured-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            grid-template-rows: 400px 200px;
            gap: 16px;
            border-radius: var(--radius-xl);
            overflow: hidden;
        }
        
        @media (max-width: 768px) {
            .featured-grid {
                grid-template-columns: 1fr;
                grid-template-rows: 300px 200px 150px 150px;
            }
        }
        
        .featured-main {
            grid-row: 1 / 3;
            position: relative;
            border-radius: var(--radius-lg);
            overflow: hidden;
            cursor: pointer;
        }
        
        .featured-secondary {
            position: relative;
            border-radius: var(--radius-lg);
            overflow: hidden;
            cursor: pointer;
        }
        
        .featured-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform var(--transition-slow);
        }
        
        .featured-card:hover .featured-img {
            transform: scale(1.05);
        }
        
        .featured-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, transparent 30%, rgba(0,0,0,0.8) 100%);
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            opacity: 0;
            transition: opacity var(--transition-normal);
        }
        
        .featured-card:hover .featured-overlay {
            opacity: 1;
        }
        
        .featured-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            background: var(--accent-color);
            color: white;
            border-radius: 50px;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 12px;
            width: fit-content;
        }
        
        .featured-title {
            font-size: 22px;
            font-weight: 700;
            color: white;
            margin-bottom: 8px;
        }
        
        .featured-meta {
            font-size: 14px;
            color: rgba(255,255,255,0.8);
            display: flex;
            align-items: center;
            gap: 16px;
        }
        
        .featured-photo-count {
            position: absolute;
            top: 16px;
            right: 16px;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(10px);
            color: white;
            padding: 8px 14px;
            border-radius: 50px;
            font-size: 13px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* ============================================
           GALLERY GRID SECTION
        ============================================ */
        .gallery-section {
            padding: 0 24px 80px;
            max-width: var(--max-width);
            margin: 0 auto;
        }
        
        .activity-group {
            margin-bottom: 64px;
        }
        
        .activity-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-light);
        }
        
        .activity-info h2 {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 8px;
            letter-spacing: -0.01em;
        }
        
        .activity-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            font-size: 14px;
            color: var(--text-muted);
        }
        
        .activity-meta-item {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .activity-category-badge {
            display: inline-flex;
            padding: 6px 14px;
            background: var(--accent-light);
            color: var(--accent-color);
            border-radius: 50px;
            font-size: 12px;
            font-weight: 600;
        }

        /* Bento Layout Variations */
        .gallery-grid {
            display: grid;
            gap: 16px;
        }
        
        /* Layout A: Mixed sizes */
        .layout-a {
            grid-template-columns: repeat(4, 1fr);
            grid-auto-rows: 200px;
        }
        
        .layout-a .photo-card:nth-child(1) {
            grid-column: span 2;
            grid-row: span 2;
        }
        
        .layout-a .photo-card:nth-child(4) {
            grid-column: span 2;
        }
        
        @media (max-width: 1024px) {
            .layout-a {
                grid-template-columns: repeat(2, 1fr);
            }
            .layout-a .photo-card:nth-child(1) {
                grid-column: span 2;
                grid-row: span 2;
            }
            .layout-a .photo-card:nth-child(4) {
                grid-column: span 1;
            }
        }
        
        @media (max-width: 640px) {
            .layout-a {
                grid-template-columns: 1fr;
            }
            .layout-a .photo-card:nth-child(1),
            .layout-a .photo-card:nth-child(4) {
                grid-column: span 1;
                grid-row: span 1;
            }
        }

        /* Layout B: Masonry-like */
        .layout-b {
            grid-template-columns: repeat(3, 1fr);
            grid-auto-rows: 240px;
        }
        
        .layout-b .photo-card:nth-child(3n+1) {
            grid-row: span 2;
        }
        
        @media (max-width: 1024px) {
            .layout-b {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (max-width: 640px) {
            .layout-b {
                grid-template-columns: 1fr;
                grid-auto-rows: 240px;
            }
            .layout-b .photo-card:nth-child(3n+1) {
                grid-row: span 1;
            }
        }

        /* Layout C: Grid with featured */
        .layout-c {
            grid-template-columns: repeat(3, 1fr);
            grid-auto-rows: 220px;
        }
        
        .layout-c .photo-card:first-child {
            grid-column: span 2;
            grid-row: span 2;
        }
        
        @media (max-width: 1024px) {
            .layout-c {
                grid-template-columns: repeat(2, 1fr);
            }
            .layout-c .photo-card:first-child {
                grid-column: span 2;
            }
        }
        
        @media (max-width: 640px) {
            .layout-c {
                grid-template-columns: 1fr;
            }
            .layout-c .photo-card:first-child {
                grid-column: span 1;
                grid-row: span 1;
            }
        }

        /* Photo Card */
        .photo-card {
            position: relative;
            border-radius: var(--radius-lg);
            overflow: hidden;
            cursor: pointer;
            background: var(--bg-secondary);
        }
        
        .photo-card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform var(--transition-slow);
        }
        
        .photo-card:hover img {
            transform: scale(1.08);
        }
        
        .photo-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, transparent 50%, rgba(0,0,0,0.7) 100%);
            opacity: 0;
            transition: opacity var(--transition-normal);
            display: flex;
            align-items: flex-end;
            padding: 16px;
        }
        
        .photo-card:hover .photo-overlay {
            opacity: 1;
        }
        
        .photo-info {
            color: white;
        }
        
        .photo-info-title {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 4px;
        }
        
        .photo-info-meta {
            font-size: 12px;
            opacity: 0.8;
        }

        /* Load More Button */
        .load-more-container {
            text-align: center;
            margin-top: 48px;
        }
        
        .load-more-btn {
            padding: 16px 40px;
            background: var(--accent-color);
            color: white;
            border-radius: 50px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all var(--transition-fast);
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: none;
        }
        
        .load-more-btn:hover {
            background: var(--accent-hover);
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 80px 24px;
            color: var(--text-muted);
        }
        
        .empty-state-icon {
            font-size: 64px;
            margin-bottom: 24px;
            opacity: 0.5;
        }
        
        .empty-state-title {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 12px;
            color: var(--text-secondary);
        }
        
        .empty-state-text {
            font-size: 16px;
            max-width: 400px;
            margin: 0 auto;
        }

        /* ============================================
           LIGHTBOX
        ============================================ */
        .lightbox {
            position: fixed;
            inset: 0;
            z-index: 9999;
            background: rgba(0, 0, 0, 0.95);
            display: none;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity var(--transition-normal);
        }
        
        .lightbox.active {
            display: flex;
            opacity: 1;
        }
        
        .lightbox-close {
            position: absolute;
            top: 24px;
            right: 24px;
            width: 48px;
            height: 48px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            cursor: pointer;
            transition: all var(--transition-fast);
            z-index: 10;
            border: none;
            font-size: 24px;
        }
        
        .lightbox-close:hover {
            background: rgba(255,255,255,0.2);
            transform: rotate(90deg);
        }
        
        .lightbox-nav {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 56px;
            height: 56px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            cursor: pointer;
            transition: all var(--transition-fast);
            z-index: 10;
            border: none;
            font-size: 24px;
        }
        
        .lightbox-nav:hover {
            background: rgba(255,255,255,0.2);
        }
        
        .lightbox-prev { left: 24px; }
        .lightbox-next { right: 24px; }
        
        .lightbox-content {
            position: relative;
            max-width: 90vw;
            max-height: 85vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .lightbox-image {
            max-width: 100%;
            max-height: 85vh;
            object-fit: contain;
            border-radius: var(--radius-md);
            transition: transform var(--transition-fast);
            cursor: grab;
        }
        
        .lightbox-image.zoomed {
            cursor: grabbing;
            transform: scale(var(--zoom-level, 1));
        }
        
        .lightbox-info {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 24px;
            background: linear-gradient(transparent, rgba(0,0,0,0.8));
            color: white;
            text-align: center;
        }
        
        .lightbox-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .lightbox-counter {
            font-size: 14px;
            opacity: 0.8;
        }

        /* Zoom Controls */
        .zoom-controls {
            position: absolute;
            bottom: 100px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 12px;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(10px);
            padding: 8px 16px;
            border-radius: 50px;
            z-index: 10;
        }
        
        .zoom-btn {
            width: 36px;
            height: 36px;
            background: rgba(255,255,255,0.1);
            border: none;
            border-radius: 50%;
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            transition: all var(--transition-fast);
        }
        
        .zoom-btn:hover {
            background: rgba(255,255,255,0.2);
        }

        /* Thumbnail Strip */
        .thumbnail-strip {
            position: absolute;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 8px;
            max-width: 80vw;
            overflow-x: auto;
            padding: 8px;
            background: rgba(0,0,0,0.4);
            backdrop-filter: blur(10px);
            border-radius: var(--radius-md);
            z-index: 10;
        }
        
        .thumbnail-strip::-webkit-scrollbar {
            height: 4px;
        }
        
        .thumbnail-strip::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.3);
            border-radius: 2px;
        }
        
        .thumb {
            width: 60px;
            height: 60px;
            border-radius: var(--radius-sm);
            overflow: hidden;
            cursor: pointer;
            opacity: 0.5;
            transition: all var(--transition-fast);
            flex-shrink: 0;
            border: 2px solid transparent;
        }
        
        .thumb:hover,
        .thumb.active {
            opacity: 1;
            border-color: var(--accent-color);
        }
        
        .thumb img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        /* ============================================
           FOOTER
        ============================================ */
        .gallery-footer {
            background: var(--bg-secondary);
            border-top: 1px solid var(--border-light);
            padding: 40px 24px;
            text-align: center;
        }
        
        .footer-brand {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 16px;
        }
        
        .footer-text {
            font-size: 14px;
            color: var(--text-muted);
        }
        
        .footer-link {
            color: var(--accent-color);
            font-weight: 500;
        }

        /* ============================================
           ANIMATIONS
        ============================================ */
        .fade-in {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .fade-in.visible {
            opacity: 1;
            transform: translateY(0);
        }
        
        /* Photo protection */
        .photo-card img,
        .featured-img,
        .lightbox-image {
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            pointer-events: none;
        }
        
        .photo-card,
        .featured-card {
            pointer-events: auto;
        }

        /* Loading skeleton */
        .skeleton {
            background: linear-gradient(90deg, var(--bg-secondary) 25%, var(--bg-tertiary) 50%, var(--bg-secondary) 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
        }
        
        @keyframes shimmer {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
    </style>
</head>
<body>

<!-- ============================================
     HEADER
=========================================== -->
<header class="gallery-header" id="header">
    <div class="header-inner">
        <div class="header-brand">
            <div class="brand-icon">📸</div>
            <div class="brand-text">
                <h1>Galeri Foto SDMK</h1>
                <span>Dinas Kesehatan Kab. Kutai Kartanegara</span>
            </div>
        </div>
        
        <div class="header-controls">
            <div class="search-wrapper">
                <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.35-4.35"></path>
                </svg>
                <input type="text" class="search-input" placeholder="Cari kegiatan atau foto..." id="searchInput">
            </div>
            
            <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode">
                <span class="icon-moon">🌙</span>
                <span class="icon-sun">☀️</span>
            </button>
        </div>
    </div>
</header>

<!-- ============================================
     HERO SECTION
=========================================== -->
<section class="hero-section">
    <div class="hero-badge">
        <span>📷</span>
        <span>Dokumentasi Kegiatan</span>
    </div>
    <h2 class="hero-title">Galeri Foto Kegiatan SDMK</h2>
    <p class="hero-subtitle">Dokumentasi lengkap kegiatan Sumber Daya Manusia Kesehatan Dinas Kesehatan Kabupaten Kutai Kartanegara</p>
    
    <div class="hero-stats">
        <div class="stat-item">
            <div class="stat-number" id="totalPhotos">0</div>
            <div class="stat-label">Foto</div>
        </div>
        <div class="stat-item">
            <div class="stat-number" id="totalActivities">0</div>
            <div class="stat-label">Kegiatan</div>
        </div>
        <div class="stat-item">
            <div class="stat-number" id="totalCategories">0</div>
            <div class="stat-label">Kategori</div>
        </div>
    </div>
</section>

<!-- ============================================
     CATEGORY FILTERS
=========================================== -->
<section class="filters-section">
    <div class="filters-container" id="filtersContainer">
        <!-- Filters will be generated by JS -->
    </div>
</section>

<!-- ============================================
     FEATURED EVENT SECTION
=========================================== -->
<section class="featured-section" id="featuredSection">
    <div class="section-header">
        <h2 class="section-title">
            <span class="section-title-icon">⭐</span>
            Kegiatan Terbaru
        </h2>
    </div>
    <div id="featuredContent">
        <!-- Featured content will be generated by JS -->
    </div>
</section>

<!-- ============================================
     GALLERY GRID
=========================================== -->
<section class="gallery-section" id="gallerySection">
    <div id="galleryContent">
        <!-- Gallery content will be generated by JS -->
    </div>
    
    <div class="load-more-container" id="loadMoreContainer" style="display: none;">
        <button class="load-more-btn" id="loadMoreBtn">
            <span>Muat Lebih Banyak</span>
            <span>↓</span>
        </button>
    </div>
</section>

<!-- ============================================
     EMPTY STATE
=========================================== -->
<div class="empty-state" id="emptyState" style="display: none;">
    <div class="empty-state-icon">📭</div>
    <h3 class="empty-state-title">Tidak Ada Foto Ditemukan</h3>
    <p class="empty-state-text">Tidak ada foto yang cocok dengan filter yang dipilih. Coba ganti kategori atau kata kunci pencarian.</p>
</div>

<!-- ============================================
     LIGHTBOX
=========================================== -->
<div class="lightbox" id="lightbox">
    <button class="lightbox-close" id="lightboxClose">✕</button>
    <button class="lightbox-nav lightbox-prev" id="lightboxPrev">‹</button>
    <button class="lightbox-nav lightbox-next" id="lightboxNext">›</button>
    
    <div class="lightbox-content">
        <img src="" alt="" class="lightbox-image" id="lightboxImage">
        
        <div class="thumbnail-strip" id="thumbnailStrip"></div>
        
        <div class="zoom-controls">
            <button class="zoom-btn" id="zoomOut" title="Zoom out">−</button>
            <button class="zoom-btn" id="zoomIn" title="Zoom in">+</button>
            <button class="zoom-btn" id="zoomReset" title="Reset zoom">↺</button>
        </div>
        
        <div class="lightbox-info">
            <div class="lightbox-title" id="lightboxTitle"></div>
            <div class="lightbox-counter" id="lightboxCounter"></div>
        </div>
    </div>
</div>

<!-- ============================================
     FOOTER
=========================================== -->
<footer class="gallery-footer">
    <div class="footer-brand">
        <div class="brand-icon" style="width: 36px; height: 36px; font-size: 14px;">🏥</div>
    </div>
    <p class="footer-text">
        © 2026 <strong>Dinas Kesehatan Kabupaten Kutai Kartanegara</strong><br>
        <span style="font-size: 12px;">Galeri Foto otomatis di-update dari Cloudinary</span>
    </p>
</footer>

<!-- ============================================
     JAVASCRIPT
=========================================== -->
<script>
// Gallery Data (auto-generated)
const GALLERY_DATA = __GALLERY_DATA__;

// State
let currentFilter = 'all';
let displayedActivities = 0;
const ACTIVITIES_PER_PAGE = 3;
let currentLightboxIndex = 0;
let currentZoomLevel = 1;
let isDragging = false;
let dragStart = { x: 0, y: 0 };
let imageTranslate = { x: 0, y: 0 };

// DOM Elements
const header = document.getElementById('header');
const themeToggle = document.getElementById('themeToggle');
const searchInput = document.getElementById('searchInput');
const filtersContainer = document.getElementById('filtersContainer');
const featuredContent = document.getElementById('featuredContent');
const galleryContent = document.getElementById('galleryContent');
const loadMoreContainer = document.getElementById('loadMoreContainer');
const loadMoreBtn = document.getElementById('loadMoreBtn');
const emptyState = document.getElementById('emptyState');
const lightbox = document.getElementById('lightbox');
const lightboxImage = document.getElementById('lightboxImage');
const lightboxTitle = document.getElementById('lightboxTitle');
const lightboxCounter = document.getElementById('lightboxCounter');
const lightboxClose = document.getElementById('lightboxClose');
const lightboxPrev = document.getElementById('lightboxPrev');
const lightboxNext = document.getElementById('lightboxNext');
const thumbnailStrip = document.getElementById('thumbnailStrip');
const zoomIn = document.getElementById('zoomIn');
const zoomOut = document.getElementById('zoomOut');
const zoomReset = document.getElementById('zoomReset');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    updateStats();
    renderFilters();
    renderFeatured();
    renderGallery();
    initScrollEffects();
    initKeyboardNav();
    initTouchGestures();
});

// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('gallery-theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

themeToggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('gallery-theme', next);
});

// Update Statistics
function updateStats() {
    let totalPhotos = 0;
    const categories = new Set();
    
    GALLERY_DATA.forEach(activity => {
        totalPhotos += activity.photos.length;
        categories.add(activity.kategori);
    });
    
    animateNumber('totalPhotos', totalPhotos);
    animateNumber('totalActivities', GALLERY_DATA.length);
    animateNumber('totalCategories', categories.size);
}

function animateNumber(elementId, target) {
    const el = document.getElementById(elementId);
    let current = 0;
    const increment = target / 30;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            el.textContent = target;
            clearInterval(timer);
        } else {
            el.textContent = Math.floor(current);
        }
    }, 30);
}

// Render Category Filters
function renderFilters() {
    const categoryCount = {};
    GALLERY_DATA.forEach(activity => {
        const cat = activity.kategori;
        categoryCount[cat] = (categoryCount[cat] || 0) + 1;
    });
    
    let html = `<button class="filter-btn active" data-category="all">
        <span>Semua</span>
        <span class="filter-count">${GALLERY_DATA.length}</span>
    </button>`;
    
    Object.keys(categoryCount).sort().forEach(cat => {
        html += `<button class="filter-btn" data-category="${cat}">
            <span>${cat}</span>
            <span class="filter-count">${categoryCount[cat]}</span>
        </button>`;
    });
    
    filtersContainer.innerHTML = html;
    
    // Add click handlers
    filtersContainer.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            filtersContainer.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.category;
            displayedActivities = 0;
            renderGallery();
        });
    });
}

// Render Featured Section
function renderFeatured() {
    if (!GALLERY_DATA.length) return;
    
    const featured = GALLERY_DATA[0];
    const photos = featured.photos.slice(0, 4);
    
    if (!photos.length) return;
    
    let html = `
    <div class="featured-grid" data-event-id="${featured.id}" data-category="${featured.kategori}">
        <div class="featured-main featured-card" onclick='openLightbox("${featured.id}", 0)'>
            <img src="${photos[0].highResUrl || photos[0].url}" 
                 alt="${featured.judul}" 
                 class="featured-img"
                 loading="lazy">
            <div class="featured-photo-count">
                <span>📷</span>
                <span>${featured.photos.length} foto</span>
            </div>
            <div class="featured-overlay">
                <span class="featured-badge">${featured.kategori}</span>
                <h3 class="featured-title">${featured.judul}</h3>
                <div class="featured-meta">
                    <span>📅 ${featured.tanggal}</span>
                    <span>📍 ${featured.tempat}</span>
                </div>
            </div>
        </div>
    `;
    
    if (photos[1]) {
        html += `
        <div class="featured-secondary featured-card" onclick='openLightbox("${featured.id}", 1)'>
            <img src="${photos[1].highResUrl || photos[1].url}" 
                 alt="${featured.judul}" 
                 class="featured-img"
                 loading="lazy">
        </div>`;
    }
    
    if (photos[2]) {
        html += `
        <div class="featured-secondary featured-card" onclick='openLightbox("${featured.id}", 2)'>
            <img src="${photos[2].highResUrl || photos[2].url}" 
                 alt="${featured.judul}" 
                 class="featured-img"
                 loading="lazy">
        </div>`;
    }
    
    html += '</div>';
    featuredContent.innerHTML = html;
}

// Render Gallery Grid
function renderGallery() {
    const filtered = currentFilter === 'all' 
        ? GALLERY_DATA 
        : GALLERY_DATA.filter(a => a.kategori === currentFilter);
    
    // Search filter
    const searchTerm = searchInput.value.toLowerCase();
    const searched = searchTerm 
        ? filtered.filter(a => 
            a.judul.toLowerCase().includes(searchTerm) ||
            a.deskripsi.toLowerCase().includes(searchTerm) ||
            a.tanggal.toLowerCase().includes(searchTerm)
          )
        : filtered;
    
    if (!searched.length) {
        galleryContent.innerHTML = '';
        emptyState.style.display = 'block';
        loadMoreContainer.style.display = 'none';
        return;
    }
    
    emptyState.style.display = 'none';
    
    const toShow = searched.slice(0, displayedActivities + ACTIVITIES_PER_PAGE);
    
    let html = '';
    const layouts = ['layout-a', 'layout-b', 'layout-c'];
    
    toShow.forEach((activity, idx) => {
        const layout = layouts[idx % 3];
        html += generateActivityHTML(activity, layout);
    });
    
    galleryContent.innerHTML = html;
    displayedActivities = toShow.length;
    
    // Show/hide load more
    if (displayedActivities < searched.length) {
        loadMoreContainer.style.display = 'block';
    } else {
        loadMoreContainer.style.display = 'none';
    }
    
    // Re-init scroll animations for new elements
    initScrollAnimations();
}

function generateActivityHTML(activity, layoutClass) {
    const photos = activity.photos;
    
    let photosHTML = photos.map((photo, idx) => `
        <div class="photo-card fade-in" onclick='openLightbox("${activity.id}", ${idx})' data-public-id="${photo.public_id}">
            <img src="${photo.url}" alt="${photo.filename}" loading="lazy">
            <div class="photo-overlay">
                <div class="photo-info">
                    <div class="photo-info-title">${activity.judul}</div>
                    <div class="photo-info-meta">${photo.format.toUpperCase()} • ${getFileSize(photo.url)}</div>
                </div>
            </div>
        </div>
    `).join('');
    
    return `
    <div class="activity-group fade-in" data-event-id="${activity.id}" data-category="${activity.kategori}">
        <div class="activity-header">
            <div class="activity-info">
                <h2>${activity.judul}</h2>
                <div class="activity-meta">
                    <span class="activity-meta-item">📅 ${activity.tanggal}</span>
                    <span class="activity-meta-item">📍 ${activity.tempat}</span>
                    <span class="activity-meta-item">📷 ${photos.length} foto</span>
                </div>
            </div>
            <span class="activity-category-badge">${activity.kategori}</span>
        </div>
        <div class="gallery-grid ${layoutClass}">
            ${photosHTML}
        </div>
    </div>
    `;
}

// Lightbox Functions
function openLightbox(activityId, photoIndex) {
    const activity = GALLERY_DATA.find(a => a.id === activityId);
    if (!activity || !activity.photos.length) return;
    
    currentLightboxIndex = photoIndex;
    currentZoomLevel = 1;
    imageTranslate = { x: 0, y: 0 };
    
    updateLightboxContent(activity);
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    renderThumbnails(activity.photos);
}

function closeLightbox() {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
    resetZoom();
}

function updateLightboxContent(activity) {
    const photo = activity.photos[currentLightboxIndex];
    lightboxImage.src = photo.highResUrl || photo.originalUrl || photo.url;
    lightboxImage.alt = photo.filename;
    lightboxTitle.textContent = activity.judul;
    lightboxCounter.textContent = `${currentLightboxIndex + 1} / ${activity.photos.length}`;
    
    updateThumbnailActive();
}

function navigateLightbox(direction) {
    const activity = getCurrentActivity();
    if (!activity) return;
    
    currentLightboxIndex += direction;
    
    if (currentLightboxIndex < 0) currentLightboxIndex = activity.photos.length - 1;
    if (currentLightboxIndex >= activity.photos.length) currentLightboxIndex = 0;
    
    resetZoom();
    updateLightboxContent(activity);
}

function getCurrentActivity() {
    // Find activity from current context (simplified)
    for (const activity of GALLERY_DATA) {
        if (currentLightboxIndex < activity.photos.length) {
            return activity;
        }
    }
    return GALLERY_DATA[0];
}

// Zoom Functions
function setZoom(level) {
    currentZoomLevel = Math.max(1, Math.min(5, level));
    lightboxImage.style.transform = `translate(${imageTranslate.x}px, ${imageTranslate.y}px) scale(${currentZoomLevel})`;
    lightboxImage.classList.toggle('zoomed', currentZoomLevel > 1);
}

function resetZoom() {
    currentZoomLevel = 1;
    imageTranslate = { x: 0, y: 0 };
    lightboxImage.style.transform = '';
    lightboxImage.classList.remove('zoomed');
}

zoomIn.addEventListener('click', () => setZoom(currentZoomLevel + 0.5));
zoomOut.addEventListener('click', () => setZoom(currentZoomLevel - 0.5));
zoomReset.addEventListener('click', resetZoom);

// Mouse wheel zoom
lightbox.addEventListener('wheel', (e) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? -0.5 : 0.5;
    setZoom(currentZoomLevel + delta);
}, { passive: false });

// Double-click zoom
lightboxImage.addEventListener('dblclick', (e) => {
    e.preventDefault();
    if (currentZoomLevel === 1) {
        setZoom(2.5);
    } else {
        resetZoom();
    }
});

// Drag when zoomed
lightboxImage.addEventListener('mousedown', (e) => {
    if (currentZoomLevel > 1) {
        isDragging = true;
        dragStart = { x: e.clientX - imageTranslate.x, y: e.clientY - imageTranslate.y };
        lightboxImage.style.cursor = 'grabbing';
    }
});

document.addEventListener('mousemove', (e) => {
    if (isDragging && currentZoomLevel > 1) {
        imageTranslate.x = e.clientX - dragStart.x;
        imageTranslate.y = e.clientY - dragStart.y;
        lightboxImage.style.transform = `translate(${imageTranslate.x}px, ${imageTranslate.y}px) scale(${currentZoomLevel})`;
    }
});

document.addEventListener('mouseup', () => {
    isDragging = false;
    if (lightboxImage) lightboxImage.style.cursor = 'grab';
});

// Thumbnail Strip
function renderThumbnails(photos) {
    thumbnailStrip.innerHTML = photos.map((photo, idx) => `
        <div class="thumb ${idx === currentLightboxIndex ? 'active' : ''}" onclick="goToThumbnail(${idx})">
            <img src="${photo.thumbUrl}" alt="" loading="lazy">
        </div>
    `).join('');
}

function goToThumbnail(index) {
    currentLightboxIndex = index;
    resetZoom();
    updateLightboxContent(getCurrentActivity());
}

function updateThumbnailActive() {
    const thumbs = thumbnailStrip.querySelectorAll('.thumb');
    thumbs.forEach((t, i) => t.classList.toggle('active', i === currentLightboxIndex));
    
    // Scroll active thumb into view
    const activeThumb = thumbnailStrip.querySelector('.thumb.active');
    if (activeThumb) {
        activeThumb.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
}

// Event Listeners
lightboxClose.addEventListener('click', closeLightbox);
lightboxPrev.addEventListener('click', () => navigateLightbox(-1));
lightboxNext.addEventListener('click', () => navigateLightbox(1));

lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLightbox();
});

loadMoreBtn.addEventListener('click', () => {
    renderGallery();
});

searchInput.addEventListener('input', () => {
    displayedActivities = 0;
    renderGallery();
});

// Keyboard Navigation
function initKeyboardNav() {
    document.addEventListener('keydown', (e) => {
        if (!lightbox.classList.contains('active')) return;
        
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
                setZoom(currentZoomLevel + 0.5);
                break;
            case '-':
                setZoom(currentZoomLevel - 0.5);
                break;
            case '0':
                resetZoom();
                break;
        }
    });
}

// Touch Gestures
function initTouchGestures() {
    let touchStartX = 0;
    let touchStartY = 0;
    
    lightbox.addEventListener('touchstart', (e) => {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    }, { passive: true });
    
    lightbox.addEventListener('touchend', (e) => {
        const touchEndX = e.changedTouches[0].clientX;
        const touchEndY = e.changedTouches[0].clientY;
        const diffX = touchEndX - touchStartX;
        const diffY = touchEndY - touchStartY;
        
        // Swipe detection
        if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
            if (diffX > 0) navigateLightbox(-1);
            else navigateLightbox(1);
        }
        
        // Pinch zoom (basic)
        if (e.touches.length < 2 && Math.abs(diffY) < 10 && Math.abs(diffX) < 10) {
            if (currentZoomLevel === 1) setZoom(2);
            else resetZoom();
        }
    }, { passive: true });
}

// Scroll Effects
function initScrollEffects() {
    window.addEventListener('scroll', () => {
        header.classList.toggle('window.scrollY > 50', 'header-scrolled');
    });
}

function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
}

// Utility Functions
function getFileSize(url) {
    // Estimate file size from URL parameters (simplified)
    if (url.includes('w_1920')) return '~500 KB';
    if (url.includes('w_800')) return '~200 KB';
    if (url.includes('w_150')) return '~30 KB';
    return '~100 KB';
}
</script>

</body>
</html>'''


def setup_cloudinary():
    """Initialize Cloudinary configuration"""
    cloudinary.config(
        cloud_name=CLOUD_CONFIG["cloud_name"],
        api_key=CLOUD_CONFIG["api_key"],
        api_secret=CLOUD_CONFIG["api_secret"]
    )


def get_subfolders(folder_path):
    """Get list of subfolders from Cloudinary"""
    try:
        result = api_subfolders(folder_path, max_results=50)
        return result.get('folders', [])
    except Exception as e:
        print(f"   ⚠️ Error getting subfolders of {folder_path}: {e}")
        return []


def fetch_resources_from_folder(folder_prefix):
    """Fetch all image resources from a specific folder"""
    resources_list = []
    next_cursor = None
    
    while True:
        try:
            params = {
                "type": "upload",
                "prefix": folder_prefix,
                "resource_type": "image",
                "max_results": 100
            }
            if next_cursor:
                params["next_cursor"] = next_cursor
            
            result = api_resources(**params)
            
            if 'resources' in result:
                resources_list.extend(result['resources'])
            
            next_cursor = result.get('next_cursor')
            if not next_cursor:
                break
                
        except Exception as e:
            print(f"   ❌ Error fetching from {folder_prefix}: {e}")
            break
    
    return resources_list


def validate_url(url):
    """Validate that a URL returns 200 OK"""
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        response = urllib.request.urlopen(req, timeout=5)
        return response.status == 200
    except:
        return False


def parse_folder_name_to_activity(folder_name):
    """
    Parse folder name like:
    "13 s.d 14 Agustus 2026 | Pelatihan Peningkatan Kemahiran Berbahasa Indonesia pada Pelayanan Publik dan Media Sosial | RSUD AM Parikesit"
    
    Returns: dict with activity info
    """
    parts = folder_name.split('|')
    
    date_part = parts[0].strip() if len(parts) > 0 else ""
    title_part = parts[1].strip() if len(parts) > 1 else ""
    location_part = parts[2].strip() if len(parts) > 2 else ""
    
    # Generate ID from folder name
    safe_id = folder_name[:50].lower().replace(' ', '-').replace('|', '-').replace('.', '-')
    safe_id = ''.join(c for c in safe_id if c.isalnum() or c in '-')
    
    # Try to extract date
    date_match = re.search(r'(\d{1,2})\s*s\.?d\.?\s*(\d{1,2})\s*(\w+)\s*(\d{4})', date_part, re.IGNORECASE)
    tanggal_formatted = date_part
    
    if date_match:
        day_start, day_end, month_name, year = date_match.groups()
        month_map = {
            'januari': '01', 'februari': '02', 'maret': '03', 'april': '04',
            'mei': '05', 'juni': '06', 'juli': '07', 'agustus': '08',
            'september': '09', 'oktober': '10', 'november': '11', 'desember': '12'
        }
        month_num = month_map.get(month_name.lower(), '08')
        tanggal_formatted = f"{day_start}-{day_end} {month_map.get(month_name.lower(), month_name)} {year}"
    
    return {
        "id": safe_id,
        "judul": title_part or folder_name,
        "tanggal": tanggal_formatted,
        "tempat": location_part or "Dokumentasi Kegiatan",
        "tahun": year if 'year' in dir() else date_part[-4:] if len(date_part) >= 4 else "2026",
        "deskripsi": f"{title_part} - {date_part}",
        "folder_original": folder_name
    }


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


def main():
    print("=" * 70)
    print("🖼️  BENTO + MASONRY HYBRID GALLERY v5.0 GENERATOR")
    print("=" * 70)
    print("\n📁 SUPPORT: Folder Structure (SDM KESEHATAN/Subfolder/Foto)")
    print("✅ Auto-detect activities from folder names")
    print("✅ Fallback: Root-level photos support")
    print("")
    
    # Setup Cloudinary
    setup_cloudinary()
    print("📡 Mengambil data dari Cloudinary...")
    
    activities = []
    
    # Step 1: Try to get from FOLDER STRUCTURE first
    print(f"\n🔍 Mencari subfolder di '{ROOT_FOLDER}'...")
    subfolders = get_subfolders(ROOT_FOLDER)
    
    folder_activities_found = False
    
    if subfolders:
        print(f"   ✅ Ditemukan {len(subfolders)} subfolder:")
        for sf in subfolders:
            print(f"      📂 {sf['path']}")
        
        # Try to fetch photos from each subfolder
        for subfolder in sorted(subfolders, key=lambda x: x.get('name', ''), reverse=True):
            folder_path = subfolder['path']
            folder_name = subfolder['name']
            
            print(f"\n📦 Memproses folder: {folder_name[:60]}...")
            
            # Parse folder name to get activity info
            activity_info = parse_folder_name_to_activity(folder_name)
            
            # Fetch resources from this subfolder
            resources_list = fetch_resources_from_folder(folder_path)
            
            if not resources_list:
                print(f"   ⚠️ Kosong - tidak ada foto di folder")
                continue
            
            print(f"   📷 Ditemukan {len(resources_list)} resource di folder")
            
            # Process each resource into photo objects
            photos = process_resources_to_photos(resources_list)
            
            if photos:
                activity_info["kategori"] = categorize_activity(activity_info["judul"])
                activity_info["photos"] = photos
                activities.append(activity_info)
                folder_activities_found = True
                print(f"   ✅ Activity siap: {len(photos)} foto valid")
    else:
        print(f"   ℹ️ Tidak ada subfolder ditemukan")
    
    # Step 2: FALLBACK - Check ROOT level if no folder photos found
    if not folder_activities_found:
        print(f"\n🔄 FALLBACK: Mencari foto di root level...")
        
        # Fetch ALL resources
        all_resources = fetch_resources_from_folder("")  # Empty prefix = all
        
        # Filter out samples and non-photos
        real_photos = [r for r in all_resources if not (
            r.get('public_id', '').startswith('samples/') or 
            'sample' in r.get('public_id', '').lower()
        )]
        
        if real_photos:
            print(f"   ✅ Ditemukan {len(real_photos)} foto di root level")
            activities = create_activities_from_root_photos(real_photos)
        else:
            print(f"   ❌ Tidak ada foto ditemukan sama sekali")
    
    if not activities:
        print("\n⚠️ Tidak ada aktivitas dengan foto valid!")
        return
    
    # Step 3: Generate HTML
    print(f"\n{'='*70}")
    print(f"📊 STATISTIK:")
    print(f"   • Total Kegiatan: {len(activities)}")
    
    total_photos = sum(len(a['photos']) for a in activities)
    print(f"   • Total Foto: {total_photos}")
    
    for act in activities:
        print(f"      - {act['judul'][:50]}... ({len(act['photos'])} foto)")
    
    print(f"\n🎨 Generating Bento + Masonry layout...")
    
    # Convert activities to JSON for template
    gallery_json = json.dumps(activities, ensure_ascii=False, indent=2)
    
    # Replace placeholder in template
    html_output = HTML_TEMPLATE.replace('__GALLERY_DATA__', gallery_json)
    
    # Write output file
    output_path = '/home/z/my-project/download/galeri-foto-standalone.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    output_size = len(html_output.encode('utf-8'))
    
    print(f"\n{'='*70}")
    print(f"✅ SUCCESS! Gallery generated:")
    print(f"   📁 Output: {output_path}")
    print(f"   📦 Size: {output_size:,} bytes ({output_size/1024:.1f} KB)")
    print(f"   🖼️  Ready to deploy!")


def process_resources_to_photos(resources_list):
    """Convert Cloudinary resources to photo objects with validation"""
    photos = []
    
    for res in resources_list:
        public_id = res.get('public_id', '')
        fmt = res.get('format', 'jpg')
        
        # Create URLs
        base_url = f"https://res.cloudinary.com/{CLOUD_CONFIG['cloud_name']}/image/upload"
        photo_url = f"{base_url}/w_800,q_auto/{public_id}.{fmt}"
        thumb_url = f"{base_url}/w_150,q_auto/{public_id}.{fmt}"
        original_url = f"{base_url}/q_auto:eco/{public_id}.{fmt}"
        high_res_url = f"{base_url}/w_1920,q_auto/{public_id}.{fmt}"
        
        # Validate URL
        if validate_url(photo_url):
            photos.append({
                "public_id": public_id,
                "filename": public_id.split('/')[-1],
                "format": fmt,
                "url": photo_url,
                "thumbUrl": thumb_url,
                "originalUrl": original_url,
                "highResUrl": high_res_url,
                "created_at": res.get('created_at', '')
            })
            print(f"      ✅ Valid: {public_id.split('/')[-1][:40]}")
        else:
            print(f"      ❌ Invalid: {public_id.split('/')[-1][:40]}")
    
    return sorted(photos, key=lambda x: x["filename"])


def create_activities_from_root_photos(resources_list):
    """Create activities from root-level photos (fallback method)"""
    from collections import defaultdict
    
    photos_by_date = defaultdict(list)
    
    for res in resources_list:
        public_id = res.get('public_id', '')
        
        # Skip samples (already filtered, but double-check)
        if 'sample' in public_id.lower():
            continue
        
        # Try to extract date from filename (IMG_YYYYMMDD_HHMMSS format)
        date_match = re.search(r'(\d{4})(\d{2})(\d{2})', public_id)
        if date_match:
            year, month, day = date_match.groups()
            if 2020 <= int(year) <= 2030:
                formatted_date = f"{year}-{month}-{day}"
            else:
                formatted_date = "2026-08-28"
        else:
            formatted_date = "2026-08-28"  # Default
        
        fmt = res.get('format', 'jpg')
        base_url = f"https://res.cloudinary.com/{CLOUD_CONFIG['cloud_name']}/image/upload"
        
        photo_url = f"{base_url}/w_800,q_auto/{public_id}.{fmt}"
        
        # Validate URL before adding
        if validate_url(photo_url):
            photo_obj = {
                "public_id": public_id,
                "filename": public_id,
                "format": fmt,
                "url": photo_url,
                "thumbUrl": f"{base_url}/w_150,q_auto/{public_id}.{fmt}",
                "originalUrl": f"{base_url}/q_auto:eco/{public_id}.{fmt}",
                "highResUrl": f"{base_url}/w_1920,q_auto/{public_id}.{fmt}",
                "created_at": res.get('created_at', '')
            }
            photos_by_date[formatted_date].append(photo_obj)
    
    # Create activities with smart grouping
    activities = []
    
    # Load config if exists for better titles
    try:
        with open('/home/z/my-project/scripts/gallery-config.json', 'r') as f:
            config_data = json.load(f)
            activities_config = config_data.get('activities_config', {})
    except:
        activities_config = {}
    
    for date_str in sorted(photos_by_date.keys(), reverse=True):
        photos = photos_by_date[date_str]
        
        # Check if we have config for this date
        if date_str in activities_config:
            cfg = activities_config[date_str]
            activity = {
                "id": cfg.get("id", f"kegiatan-{date_str}"),
                "judul": cfg.get("judul", f"Kegiatan {date_str}"),
                "tanggal": cfg.get("tanggal", date_str),
                "tempat": cfg.get("tempat", "Dokumentasi Kegiatan"),
                "tahun": cfg.get("tahun", date_str[:4]),
                "deskripsi": cfg.get("deskripsi", ""),
                "kategori": categorize_activity(cfg.get("judul", "")),
                "folder_original": "Root Level (Auto-detected)",
                "photos": photos
            }
        else:
            # Generate title based on date range or generic
            if len(photos) >= 5:
                judul = f"Dokumentasi Kegiatan SDMK - {date_str}"
            else:
                judul = f"Foto Dokumentasi ({date_str})"
            
            activity = {
                "id": f"kegiatan-{date_str}",
                "judul": judul,
                "tanggal": date_str,
                "tempat": "Dokumentasi Kegiatan",
                "tahun": date_str[:4],
                "deskripsi": f"Kumpulan foto dokumentasi tanggal {date_str}",
                "kategori": "Pelatihan",  # Default assumption
                "folder_original": "Root Level (Auto-detected)",
                "photos": photos
            }
        
        activities.append(activity)
    
    return activities


if __name__ == "__main__":
    main()
