/* =====================================================================
 * MUSIC PLAYER MODULE — Vanilla JS, no dependencies
 * ---------------------------------------------------------------------
 * Self-contained module. Tidak mengubah / mengganggu script website lain.
 *
 * Inisialisasi otomatis: panggil window.MusicPlayer.init()
 * Anti-double instance: semua state & audio element hidup di satu
 * singleton (window.MusicPlayer). Jika module dipanggil dua kali (misal
 * script dimuat ulang), instance lama di-destroy otomatis.
 *
 * Lokasi: /assets/js/music-player.js
 * CSS   : /assets/css/music-player.css
 * ===================================================================== */
(function () {
  'use strict';

  /* ============================================================
   * 1. KONFIGURASI PLAYLIST  (ubah / tambah lagu di sini saja)
   * ------------------------------------------------------------
   * `src` boleh relative atau absolute. Player akan menggunakan
   * URL relatif terhadap posisi dokumen saat ini, jadi otomatis
   * menyesuaikan struktur folder website apapun.
   * ============================================================ */
  var DEFAULT_PLAYLIST = [
    { title: 'Lagu 01', src: 'assets/audio/lagu-01.mp3' },
    { title: 'Lagu 02',        src: 'assets/audio/lagu-02.mp3' },
    { title: 'Lagu 03',        src: 'assets/audio/lagu-03.mp3' },
    { title: 'Lagu 04',        src: 'assets/audio/lagu-04.mp3' },
    { title: 'Lagu 05',        src: 'assets/audio/lagu-05.mp3' }
    { title: 'Lagu 06', src: 'assets/audio/lagu-06.mp3' },
    { title: 'Lagu 07',        src: 'assets/audio/lagu-07.mp3' },
    { title: 'Lagu 08',        src: 'assets/audio/lagu-08.mp3' },
    { title: 'Lagu 09',        src: 'assets/audio/lagu-09.mp3' },
    { title: 'Lagu 10',        src: 'assets/audio/lagu-10.mp3' }
  ];

  /* ============================================================
   * 2. SINGLETON — mencegah double audio / double init
   * ============================================================ */
  var instance = null;

  function MusicPlayer() {
    if (instance) {
      instance.destroy();
    }
    instance = this;
    this._init();
  }

  MusicPlayer.prototype._init = function () {
    var self = this;

    /* state */
    this.playlist           = DEFAULT_PLAYLIST.slice();
    this.currentIndex        = DEFAULT_TRACK_INDEX;
    this.playMode            = DEFAULT_PLAY_MODE;
    this.volume              = DEFAULT_VOLUME;
    this.muted               = DEFAULT_MUTED;
    this.lastVolumeBeforeMute = DEFAULT_VOLUME;
    this.isReady             = false;
    this.isPlaying           = false;
    this.isSeeking           = false;
    this.isAutoplayBlocked   = false;
    this.isPlaylistOpen      = false;
    this.isCollapsed         = false;
    this.trackErrors         = {}; // { src: true } daftar lagu yang gagal load
    { title: 'Lagu 04',        src: 'assets/audio/lagu-04.mp3' },
    { title: 'Lagu 05',        src: 'assets/audio/lagu-05.mp3' }
  ];

  /* Default track index (Step From Hell = index 0) */
  var DEFAULT_TRACK_INDEX = 0;

  /* Default preferences */
  var DEFAULT_VOLUME      = 0.3;     // 30%
  var DEFAULT_MUTED       = false;
  var DEFAULT_PLAY_MODE   = 'sequential'; // sequential | repeat_one | repeat_all | shuffle

  /* localStorage keys (scoped, tidak bentrok dengan key website lain) */
  var LS = {
    volume:       'music_volume',
    muted:        'music_muted',
    currentTrack: 'music_current_track',
    playMode:     'music_play_mode',
    playlistOpen: 'music_playlist_open',
    position:     'music_last_position',
    collapsed:    'music_collapsed'
  };

  /* Mode konstan */
  var MODE = {
    SEQUENTIAL:  'sequential',   // urut, berhenti di lagu terakhir
    REPEAT_ONE:  'repeat_one',   // ulang lagu yang sama
    REPEAT_ALL:  'repeat_all',   // ulang seluruh playlist
    SHUFFLE:     'shuffle'       // acak tanpa pengulangan langsung
  };

  var MODE_LABELS = {
    sequential: 'Berurutan',
    repeat_one: 'Ulangi Lagu',
    repeat_all: 'Ulangi Playlist',
    shuffle:    'Acak'
  };

  /* ============================================================
   * 2. SINGLETON — mencegah double audio / double init
   * ============================================================ */
  var instance = null;

  function MusicPlayer() {
    if (instance) {
      instance.destroy();
    }
    instance = this;
    this._init();
  }

  MusicPlayer.prototype._init = function () {
    var self = this;

    /* state */
    this.playlist           = DEFAULT_PLAYLIST.slice();
    this.currentIndex        = DEFAULT_TRACK_INDEX;
    this.playMode            = DEFAULT_PLAY_MODE;
    this.volume              = DEFAULT_VOLUME;
    this.muted               = DEFAULT_MUTED;
    this.lastVolumeBeforeMute = DEFAULT_VOLUME;
    this.isReady             = false;
    this.isPlaying           = false;
    this.isSeeking           = false;
    this.isAutoplayBlocked   = false;
    this.isPlaylistOpen      = false;
    this.isCollapsed         = false;
    this.trackErrors         = {}; // { src: true } daftar lagu yang gagal load
    this.firstInteractionHandled = false;
    this.positionSaveTimer   = null;

    /* The single audio instance for the whole module */
    this.audio = new Audio();
    this.audio.preload = 'metadata';
    this.audio.volume  = this.volume;

    /* restore preferences */
    this._restorePreferences();

    /* build UI */
    this._buildUI();
    this._applyModeUI();
    this._applyVolumeUI();
    this._applyPlaylistUI();
    this._updateTrackDisplay();

    /* attach audio events */
    this._bindAudioEvents();

    /* attach UI events */
    this._bindUIEvents();

    /* load initial track */
    this._loadTrack(this.currentIndex, { autoplay: false });

    /* try autoplay (will likely be blocked by browser policy) */
    this._tryAutoplay();

    /* attempt resume after first user interaction (anywhere) */
    this._attachFirstInteractionHandler();

    /* save position periodically for resume across page navigation */
    this._startPositionSaver();

    this.isReady = true;
  };

  /* ============================================================
   * 3. UI BUILD
   * ============================================================ */
  MusicPlayer.prototype._buildUI = function () {
    var existing = document.getElementById('music-player-root');
    if (existing) { existing.remove(); }

    var root = document.createElement('div');
    root.id = 'music-player-root';
    root.className = 'music-player is-paused';
    root.setAttribute('role', 'region');
    root.setAttribute('aria-label', 'Music Player');

    root.innerHTML =
      '<div class="music-player__fab" title="Buka music player" aria-hidden="true">'
      + '<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
      + '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>'
      + '</svg></div>'

      + '<div class="music-player__header">'
      +   '<div class="music-player__brand">'
      +     '<span class="music-player__brand-icon" aria-hidden="true">'
      +       '<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">'
      +         '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>'
      +       '</svg>'
      +     '</span>'
      +     '<span>Music Player</span>'
      +   '</div>'
      +   '<div class="music-player__header-actions">'
      +     '<button type="button" class="music-player__icon-btn mp-js-collapse" title="Minimalkan" aria-label="Minimalkan">'
      +       '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="19" x2="19" y2="5"/></svg>'
      +     '</button>'
      +   '</div>'
      + '</div>'

      + '<div class="music-player__body">'
      +   '<div class="music-player__autoplay-prompt mp-js-autoplay-prompt" role="button" tabindex="0">'
      +     '<span class="music-player__autoplay-prompt-icon" aria-hidden="true">'
      +       '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>'
      +     '</span>'
      +     '<span>Klik untuk memutar musik</span>'
      +   '</div>'

      +   '<div class="music-player__track">'
      +     '<span class="music-player__eq" aria-hidden="true">'
      +       '<span class="music-player__eq-bar"></span>'
      +       '<span class="music-player__eq-bar"></span>'
      +       '<span class="music-player__eq-bar"></span>'
      +       '<span class="music-player__eq-bar"></span>'
      +     '</span>'
      +     '<span class="music-player__track-title mp-js-title">—</span>'
      +     '<span class="music-player__track-status mp-js-status"></span>'
      +   '</div>'

      +   '<div class="music-player__progress mp-js-progress" role="slider" tabindex="0" aria-label="Posisi lagu" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">'
      +     '<div class="music-player__progress-buffer mp-js-buffer"></div>'
      +     '<div class="music-player__progress-fill mp-js-fill"></div>'
      +     '<div class="music-player__progress-thumb"></div>'
      +   '</div>'

      +   '<div class="music-player__time">'
      +     '<span class="mp-js-current">00:00</span>'
      +     '<span class="mp-js-duration">00:00</span>'
      +   '</div>'

      +   '<div class="music-player__controls">'
      +     '<button type="button" class="music-player__btn mp-js-prev" title="Previous" aria-label="Previous">'
      +       '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="19 20 9 12 19 4 19 20"/><line x1="5" y1="19" x2="5" y2="5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
      +     '</button>'
      +     '<button type="button" class="music-player__btn music-player__btn--play mp-js-play" title="Play / Pause" aria-label="Play / Pause">'
      +       '<svg class="mp-js-play-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 4 20 12 6 20 6 4"/></svg>'
      +       '<svg class="mp-js-pause-icon" style="display:none" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>'
      +     '</button>'
      +     '<button type="button" class="music-player__btn mp-js-next" title="Next" aria-label="Next">'
      +       '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 4 15 12 5 20 5 4"/><line x1="19" y1="5" x2="19" y2="19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
      +     '</button>'
      +     '<span class="music-player__spacer"></span>'
      +     '<button type="button" class="music-player__btn mp-js-mode" title="Mode putar" aria-label="Mode putar">'
      +       '<span class="mp-js-mode-icon"></span>'
      +     '</button>'
      +     '<button type="button" class="music-player__btn mp-js-playlist-toggle" title="Playlist" aria-label="Playlist">'
      +       '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>'
      +     '</button>'
      +   '</div>'

      +   '<div class="music-player__volume">'
      +     '<button type="button" class="music-player__volume-icon mp-js-mute" title="Mute / Unmute" aria-label="Mute / Unmute">'
      +       '<span class="mp-js-mute-icon"></span>'
      +     '</button>'
      +     '<input type="range" min="0" max="100" step="1" value="30" class="music-player__volume-slider mp-js-volume" aria-label="Volume" />'
      +     '<span class="music-player__volume-value mp-js-volume-value">30%</span>'
      +   '</div>'

      +   '<div class="music-player__mode">'
      +     '<span>Mode:</span>'
      +     '<span class="music-player__mode-badge mp-js-mode-label">Berurutan</span>'
      +   '</div>'
      + '</div>'

      + '<div class="music-player__playlist" role="list" aria-label="Playlist">'
      +   '<div class="music-player__playlist-header">'
      +     '<span class="music-player__playlist-title">Playlist</span>'
      +     '<button type="button" class="music-player__icon-btn mp-js-playlist-close" title="Tutup" aria-label="Tutup playlist">'
      +       '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="19" x2="19" y2="5"/></svg>'
      +     '</button>'
      +   '</div>'
      +   '<ul class="music-player__playlist-list mp-js-playlist-list"></ul>'
      + '</div>';

    document.body.appendChild(root);
    this.root = root;

    /* cache elements */
    this.el = {
      fab:              root.querySelector('.mp-js-collapse'),
      autoplayPrompt:  root.querySelector('.mp-js-autoplay-prompt'),
      title:            root.querySelector('.mp-js-title'),
      status:           root.querySelector('.mp-js-status'),
      progress:         root.querySelector('.mp-js-progress'),
      buffer:           root.querySelector('.mp-js-buffer'),
      fill:             root.querySelector('.mp-js-fill'),
      current:          root.querySelector('.mp-js-current'),
      duration:         root.querySelector('.mp-js-duration'),
      playBtn:          root.querySelector('.mp-js-play'),
      playIcon:         root.querySelector('.mp-js-play-icon'),
      pauseIcon:        root.querySelector('.mp-js-pause-icon'),
      prevBtn:          root.querySelector('.mp-js-prev'),
      nextBtn:          root.querySelector('.mp-js-next'),
      modeBtn:          root.querySelector('.mp-js-mode'),
      modeIcon:         root.querySelector('.mp-js-mode-icon'),
      modeLabel:        root.querySelector('.mp-js-mode-label'),
      playlistToggle:   root.querySelector('.mp-js-playlist-toggle'),
      playlistClose:    root.querySelector('.mp-js-playlist-close'),
      playlistList:     root.querySelector('.mp-js-playlist-list'),
      muteBtn:          root.querySelector('.mp-js-mute'),
      muteIcon:         root.querySelector('.mp-js-mute-icon'),
      volumeSlider:     root.querySelector('.mp-js-volume'),
      volumeValue:      root.querySelector('.mp-js-volume-value')
    };
  };

  /* ============================================================
   * 4. AUDIO EVENTS
   * ============================================================ */
  MusicPlayer.prototype._bindAudioEvents = function () {
    var self = this, a = this.audio;

    a.addEventListener('loadedmetadata', function () {
      self.el.duration.textContent = self._formatTime(a.duration);
    });

    a.addEventListener('timeupdate', function () {
      if (!self.isSeeking) {
        self.el.current.textContent = self._formatTime(a.currentTime);
        var dur = a.duration;
        if (isFinite(dur) && dur > 0) {
          var pct = (a.currentTime / dur) * 100;
          self.el.fill.style.width = pct + '%';
          self.el.progress.setAttribute('aria-valuenow', String(Math.round(pct)));
        }
      }
    });

    a.addEventListener('progress', function () {
      try {
        if (a.buffered && a.buffered.length > 0 && isFinite(a.duration)) {
          var end = a.buffered.end(a.buffered.length - 1);
          var pct = (end / a.duration) * 100;
          self.el.buffer.style.width = pct + '%';
        }
      } catch (e) { /* ignore */ }
    });

    a.addEventListener('play', function () {
      self.isPlaying = true;
      self.root.classList.remove('is-paused');
      self.root.classList.add('is-playing');
      self.el.playIcon.style.display  = 'none';
      self.el.pauseIcon.style.display = 'inline-block';
      self._hideAutoplayPrompt();
    });

    a.addEventListener('pause', function () {
      self.isPlaying = false;
      self.root.classList.add('is-paused');
      self.root.classList.remove('is-playing');
      self.el.playIcon.style.display  = 'inline-block';
      self.el.pauseIcon.style.display = 'none';
    });

    a.addEventListener('ended', function () {
      self._onTrackEnded();
    });

    a.addEventListener('error', function () {
      var src = a.currentSrc || (self.playlist[self.currentIndex] && self.playlist[self.currentIndex].src);
      self.trackErrors[src] = true;
      self._setStatus('File audio tidak tersedia', 'is-error');
      self._applyPlaylistUI();
      self._updateTrackDisplay();
      // stop trying to play this track; advance to next after a short delay
      window.setTimeout(function () {
        if (self.playMode === MODE.REPEAT_ONE) return; // do not auto-advance in repeat_one
        self._next({ auto: true });
      }, 800);
    }, true);

    a.addEventListener('stalled waiting', function () {
      self._setStatus('Memuat…', 'is-loading');
    });

    a.addEventListener('canplay playing', function () {
      self._setStatus('');
    });
  };

  /* ============================================================
   * 5. UI EVENTS
   * ============================================================ */
  MusicPlayer.prototype._bindUIEvents = function () {
    var self = this;

    /* Play / Pause */
    this.el.playBtn.addEventListener('click', function (e) {
      e.preventDefault();
      self.togglePlay();
    });

    /* Previous */
    this.el.prevBtn.addEventListener('click', function (e) {
      e.preventDefault();
      self.prev();
    });

    /* Next */
    this.el.nextBtn.addEventListener('click', function (e) {
      e.preventDefault();
      self.next();
    });

    /* Mode toggle */
    this.el.modeBtn.addEventListener('click', function (e) {
      e.preventDefault();
      self.cycleMode();
    });

    /* Playlist open/close */
    this.el.playlistToggle.addEventListener('click', function (e) {
      e.preventDefault();
      self.togglePlaylist();
    });
    this.el.playlistClose.addEventListener('click', function (e) {
      e.preventDefault();
      self.closePlaylist();
    });

    /* Mute */
    this.el.muteBtn.addEventListener('click', function (e) {
      e.preventDefault();
      self.toggleMute();
    });

    /* Volume slider */
    this.el.volumeSlider.addEventListener('input', function (e) {
      var v = parseInt(e.target.value, 10) / 100;
      self.setVolume(v);
    });

    /* Progress bar — click & drag to seek */
    var onSeekStart = function (clientX) {
      self.isSeeking = true;
      self.root.classList.add('is-seeking');
      self._seekToClientX(clientX);
    };
    var onSeekMove = function (clientX) {
      if (!self.isSeeking) return;
      self._seekToClientX(clientX);
    };
    var onSeekEnd = function () {
      if (!self.isSeeking) return;
      self.isSeeking = false;
      self.root.classList.remove('is-seeking');
    };

    /* mouse */
    this.el.progress.addEventListener('mousedown', function (e) {
      e.preventDefault();
      onSeekStart(e.clientX);
      var move = function (ev) { onSeekMove(ev.clientX); };
      var up   = function () {
        onSeekEnd();
        document.removeEventListener('mousemove', move);
        document.removeEventListener('mouseup',   up);
      };
      document.addEventListener('mousemove', move);
      document.addEventListener('mouseup',   up);
    });

    /* touch */
    this.el.progress.addEventListener('touchstart', function (e) {
      if (e.touches.length === 0) return;
      onSeekStart(e.touches[0].clientX);
    }, { passive: true });
    this.el.progress.addEventListener('touchmove', function (e) {
      if (e.touches.length === 0) return;
      onSeekMove(e.touches[0].clientX);
    }, { passive: true });
    this.el.progress.addEventListener('touchend',   onSeekEnd);
    this.el.progress.addEventListener('touchcancel', onSeekEnd);

    /* keyboard on progress */
    this.el.progress.addEventListener('keydown', function (e) {
      var dur = self.audio.duration;
      if (!isFinite(dur) || dur <= 0) return;
      if (e.key === 'ArrowLeft') {
        e.preventDefault();
        self.audio.currentTime = Math.max(0, self.audio.currentTime - 5);
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        self.audio.currentTime = Math.min(dur, self.audio.currentTime + 5);
      }
    });

    /* Autoplay prompt click */
    this.el.autoplayPrompt.addEventListener('click', function (e) {
      e.preventDefault();
      self.play();
    });
    this.el.autoplayPrompt.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        self.play();
      }
    });

    /* Collapse button */
    this.el.fab.addEventListener('click', function (e) {
      e.preventDefault();
      self._setCollapsed(false);
    });

    /* Click outside playlist to close (optional nicety) */
    document.addEventListener('click', function (e) {
      if (!self.isPlaylistOpen) return;
      if (!self.root.contains(e.target)) {
        self.closePlaylist();
      }
    });
  };

  /* ============================================================
   * 6. CORE PLAYBACK
   * ============================================================ */
  MusicPlayer.prototype._loadTrack = function (index, opts) {
    opts = opts || {};
    if (index < 0 || index >= this.playlist.length) return;

    var track = this.playlist[index];
    if (!track) return;

    this.currentIndex = index;

    /* If the same src is already loaded, don't reload (avoid double audio / replay bug) */
    var fullSrc = this._resolveUrl(track.src);
    if (this.audio.currentSrc !== fullSrc && this.audio.src !== fullSrc) {
      try {
        this.audio.src = fullSrc;
        this.audio.load();
      } catch (e) { /* ignore */ }
    }

    this.trackErrors[track.src] = !!this.trackErrors[track.src]; // keep flag if any
    this._updateTrackDisplay();
    this._applyPlaylistUI();

    if (opts.autoplay) {
      this.play();
    }

    this._savePreferences();
  };

  MusicPlayer.prototype.play = function () {
    var self = this;
    var track = this.playlist[this.currentIndex];
    if (!track) return;
    if (this.trackErrors[track.src]) {
      this._setStatus('File audio tidak tersedia', 'is-error');
      return;
    }
    var p = this.audio.play();
    if (p && typeof p.then === 'function') {
      p.then(function () {
        self.isAutoplayBlocked = false;
        self._hideAutoplayPrompt();
      }).catch(function (err) {
        // Not allowed to play — likely autoplay policy
        self.isAutoplayBlocked = true;
        self._showAutoplayPrompt();
        // do NOT log err to console repeatedly
      });
    }
  };

  MusicPlayer.prototype.pause = function () {
    try { this.audio.pause(); } catch (e) {}
  };

  MusicPlayer.prototype.togglePlay = function () {
    if (this.audio.paused) {
      this.play();
    } else {
      this.pause();
    }
  };

  MusicPlayer.prototype.prev = function () {
    if (this.playMode === MODE.SHUFFLE) {
      this._shuffleTo(this.currentIndex, -1);
      return;
    }
    var idx = this.currentIndex - 1;
    if (idx < 0) idx = this.playlist.length - 1;
    this._loadTrack(idx, { autoplay: true });
  };

  MusicPlayer.prototype.next = function () {
    this._next({ auto: false });
  };

  MusicPlayer.prototype._next = function (opts) {
    opts = opts || {};
    var idx;
    if (this.playMode === MODE.SHUFFLE) {
      this._shuffleTo(this.currentIndex, 1);
      return;
    }
    if (this.playMode === MODE.REPEAT_ONE) {
      idx = this.currentIndex;
    } else {
      idx = this.currentIndex + 1;
      if (idx >= this.playlist.length) {
        if (this.playMode === MODE.REPEAT_ALL || opts.auto) {
          idx = 0; // wrap
        } else {
          // SEQUENTIAL + end: stop at end
          this.pause();
          return;
        }
      }
    }
    this._loadTrack(idx, { autoplay: opts.auto || this.isPlaying });
  };

  MusicPlayer.prototype._onTrackEnded = function () {
    if (this.playMode === MODE.REPEAT_ONE) {
      this.audio.currentTime = 0;
      this.play();
      return;
    }
    this._next({ auto: true });
  };

  /* ============================================================
   * 7. MODE
   * ============================================================ */
  MusicPlayer.prototype.cycleMode = function () {
    var order = [MODE.SEQUENTIAL, MODE.REPEAT_ALL, MODE.REPEAT_ONE, MODE.SHUFFLE];
    var i = order.indexOf(this.playMode);
    i = (i + 1) % order.length;
    this.playMode = order[i];
    this._applyModeUI();
    this._savePreferences();
  };

  MusicPlayer.prototype._applyModeUI = function () {
    var icon;
    switch (this.playMode) {
      case MODE.REPEAT_ONE:
        icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/><text x="12" y="15" text-anchor="middle" font-size="7" font-weight="700" fill="currentColor" stroke="none">1</text></svg>';
        break;
      case MODE.REPEAT_ALL:
        icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>';
        break;
      case MODE.SHUFFLE:
        icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/><line x1="4" y1="4" x2="9" y2="9"/></svg>';
        break;
      case MODE.SEQUENTIAL:
      default:
        icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="14" y2="12"/><line x1="3" y1="18" x2="11" y2="18"/></svg>';
        break;
    }
    this.el.modeIcon.innerHTML = icon;
    this.el.modeLabel.textContent = MODE_LABELS[this.playMode] || 'Berurutan';

    if (this.playMode !== MODE.SEQUENTIAL) {
      this.el.modeBtn.classList.add('is-active');
    } else {
      this.el.modeBtn.classList.remove('is-active');
    }
  };

  /* ============================================================
   * 8. VOLUME & MUTE
   * ============================================================ */
  MusicPlayer.prototype.setVolume = function (v) {
    v = Math.max(0, Math.min(1, v));
    this.volume = v;
    this.audio.volume = v;
    if (v > 0 && this.muted) {
      this.muted = false;
    } else if (v === 0 && !this.muted) {
      // user dragged volume to 0 — treat as mute, but remember non-zero
      this.muted = true;
    }
    if (v > 0) {
      this.lastVolumeBeforeMute = v;
    }
    this._applyVolumeUI();
    this._savePreferences();
  };

  MusicPlayer.prototype.toggleMute = function () {
    if (this.muted) {
      this.muted = false;
      var v = this.lastVolumeBeforeMute > 0 ? this.lastVolumeBeforeMute : DEFAULT_VOLUME;
      this.audio.volume = v;
      this.volume = v;
    } else {
      this.muted = true;
      this.lastVolumeBeforeMute = this.volume > 0 ? this.volume : DEFAULT_VOLUME;
      this.audio.volume = 0;
    }
    this._applyVolumeUI();
    this._savePreferences();
  };

  MusicPlayer.prototype._applyVolumeUI = function () {
    var display = this.muted ? 0 : Math.round(this.volume * 100);
    this.el.volumeSlider.value = String(display);
    this.el.volumeValue.textContent = display + '%';
    this.el.volumeSlider.style.setProperty('--vol', display + '%');

    var icon;
    if (this.muted || display === 0) {
      icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/></svg>';
      this.el.muteBtn.classList.add('is-active');
    } else if (display < 50) {
      icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>';
      this.el.muteBtn.classList.remove('is-active');
    } else {
      icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 5.93a10 10 0 0 1 0 14.14"/></svg>';
      this.el.muteBtn.classList.remove('is-active');
    }
    this.el.muteIcon.innerHTML = icon;
  };

  /* ============================================================
   * 9. PLAYLIST UI
   * ============================================================ */
  MusicPlayer.prototype._applyPlaylistUI = function () {
    var self = this;
    var html = '';
    this.playlist.forEach(function (track, i) {
      var isActive = (i === self.currentIndex);
      var isError  = !!self.trackErrors[track.src];
      html += '<li class="music-player__playlist-item' + (isActive ? ' is-active' : '') + (isError ? ' is-error' : '') + '" data-index="' + i + '" role="listitem" tabindex="0">'
            +   '<span class="music-player__playlist-item-index">' + (i + 1) + '</span>'
            +   '<span class="music-player__playlist-item-title">' + self._escapeHtml(track.title) + '</span>'
            +   (isError
                ? '<span class="music-player__playlist-item-error">File belum tersedia</span>'
                : '<span class="music-player__playlist-item-eq" aria-hidden="true">'
                +   '<span class="music-player__eq-bar"></span>'
                +   '<span class="music-player__eq-bar"></span>'
                +   '<span class="music-player__eq-bar"></span>'
                + '</span>')
            + '</li>';
    });
    this.el.playlistList.innerHTML = html;

    var items = this.el.playlistList.querySelectorAll('.music-player__playlist-item');
    Array.prototype.forEach.call(items, function (li) {
      var idx = parseInt(li.getAttribute('data-index'), 10);
      li.addEventListener('click', function (e) {
        e.preventDefault();
        self._loadTrack(idx, { autoplay: true });
      });
      li.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          self._loadTrack(idx, { autoplay: true });
        }
      });
    });
  };

  MusicPlayer.prototype.togglePlaylist = function () {
    this.isPlaylistOpen = !this.isPlaylistOpen;
    this.root.classList.toggle('is-playlist-open', this.isPlaylistOpen);
    this._savePreferences();
  };

  MusicPlayer.prototype.closePlaylist = function () {
    this.isPlaylistOpen = false;
    this.root.classList.remove('is-playlist-open');
    this._savePreferences();
  };

  MusicPlayer.prototype.openPlaylist = function () {
    this.isPlaylistOpen = true;
    this.root.classList.add('is-playlist-open');
    this._savePreferences();
  };

  /* ============================================================
   * 10. TRACK DISPLAY
   * ============================================================ */
  MusicPlayer.prototype._updateTrackDisplay = function () {
    var track = this.playlist[this.currentIndex];
    if (!track) return;
    this.el.title.textContent = track.title;
    if (this.trackErrors[track.src]) {
      this._setStatus('File audio tidak tersedia', 'is-error');
    } else {
      this._setStatus('');
    }
  };

  MusicPlayer.prototype._setStatus = function (msg, cls) {
    this.el.status.textContent = msg || '';
    this.el.status.className = 'music-player__track-status' + (cls ? ' ' + cls : '');
  };

  /* ============================================================
   * 11. SEEK
   * ============================================================ */
  MusicPlayer.prototype._seekToClientX = function (clientX) {
    var rect = this.el.progress.getBoundingClientRect();
    var x = clientX - rect.left;
    var pct = (x / rect.width);
    pct = Math.max(0, Math.min(1, pct));
    this.el.fill.style.width = (pct * 100) + '%';
    var dur = this.audio.duration;
    if (isFinite(dur) && dur > 0) {
      this.audio.currentTime = pct * dur;
      this.el.current.textContent = this._formatTime(this.audio.currentTime);
      this.el.progress.setAttribute('aria-valuenow', String(Math.round(pct * 100)));
    }
  };

  /* ============================================================
   * 12. AUTOPLAY
   * ============================================================ */
  MusicPlayer.prototype._tryAutoplay = function () {
    var self = this;
    // Try immediately (Chrome allows if there is previous user engagement
    // stored in the browser; Firefox/Safari usually block)
    var p = this.audio.play();
    if (p && typeof p.then === 'function') {
      p.then(function () {
        self.isAutoplayBlocked = false;
        self._hideAutoplayPrompt();
      }).catch(function () {
        self.isAutoplayBlocked = true;
        self._showAutoplayPrompt();
      });
    }
  };

  MusicPlayer.prototype._showAutoplayPrompt = function () {
    this.root.classList.add('is-autoplay-blocked');
    this.isAutoplayBlocked = true;
  };

  MusicPlayer.prototype._hideAutoplayPrompt = function () {
    this.root.classList.remove('is-autoplay-blocked');
    this.isAutoplayBlocked = false;
  };

  MusicPlayer.prototype._attachFirstInteractionHandler = function () {
    var self = this;
    function onFirstInteract() {
      if (self.firstInteractionHandled) return;
      self.firstInteractionHandled = true;
      // Only auto-resume if user has not explicitly paused via the player UI
      // AND autoplay was blocked at startup
      if (self.isAutoplayBlocked && self.audio.paused) {
        self.play();
      }
      document.removeEventListener('click',      onFirstInteract);
      document.removeEventListener('touchstart', onFirstInteract);
      document.removeEventListener('keydown',   onFirstInteract);
    }
    document.addEventListener('click',      onFirstInteract, { passive: true });
    document.addEventListener('touchstart', onFirstInteract, { passive: true });
    document.addEventListener('keydown',    onFirstInteract);
  };

  /* ============================================================
   * 13. COLLAPSE / EXPAND
   * ============================================================ */
  MusicPlayer.prototype._setCollapsed = function (collapsed) {
    this.isCollapsed = collapsed;
    this.root.classList.toggle('is-collapsed', collapsed);
    this._savePreferences();
  };

  /* ============================================================
   * 14. LOCAL STORAGE
   * ============================================================ */
  MusicPlayer.prototype._restorePreferences = function () {
    try {
      var v = parseFloat(localStorage.getItem(LS.volume));
      if (!isNaN(v)) { this.volume = Math.max(0, Math.min(1, v)); }
      var m = localStorage.getItem(LS.muted);
      if (m !== null) { this.muted = (m === '1' || m === 'true'); }
      var t = parseInt(localStorage.getItem(LS.currentTrack), 10);
      if (!isNaN(t) && t >= 0 && t < this.playlist.length) { this.currentIndex = t; }
      var pm = localStorage.getItem(LS.playMode);
      if (pm && MODE_LABELS[pm]) { this.playMode = pm; }
      var po = localStorage.getItem(LS.playlistOpen);
      if (po !== null) { this.isPlaylistOpen = (po === '1' || po === 'true'); }
      var col = localStorage.getItem(LS.collapsed);
      if (col !== null) { this.isCollapsed = (col === '1' || col === 'true'); }
    } catch (e) { /* localStorage disabled */ }
  };

  MusicPlayer.prototype._savePreferences = function () {
    try {
      localStorage.setItem(LS.volume,       String(this.volume));
      localStorage.setItem(LS.muted,         this.muted ? '1' : '0');
      localStorage.setItem(LS.currentTrack,  String(this.currentIndex));
      localStorage.setItem(LS.playMode,      this.playMode);
      localStorage.setItem(LS.playlistOpen, this.isPlaylistOpen ? '1' : '0');
      localStorage.setItem(LS.collapsed,    this.isCollapsed ? '1' : '0');
    } catch (e) { /* ignore */ }
  };

  MusicPlayer.prototype._startPositionSaver = function () {
    var self = this;
    if (this.positionSaveTimer) { clearInterval(this.positionSaveTimer); }
    this.positionSaveTimer = window.setInterval(function () {
      try {
        if (isFinite(self.audio.currentTime) && self.audio.currentTime > 0) {
          localStorage.setItem(LS.position, String(self.audio.currentTime));
        }
      } catch (e) {}
    }, 1500);

    // Restore last position (helps when navigating between pages)
    try {
      var last = parseFloat(localStorage.getItem(LS.position));
      if (!isNaN(last) && last > 0) {
        this._pendingResumePos = last;
        var onMeta = function () {
          if (isFinite(self.audio.duration) && self.audio.duration > 0 &&
              self._pendingResumePos < self.audio.duration) {
            try { self.audio.currentTime = self._pendingResumePos; } catch (e) {}
          }
          self.audio.removeEventListener('loadedmetadata', onMeta);
        };
        self.audio.addEventListener('loadedmetadata', onMeta);
      }
    } catch (e) {}
  };

  /* ============================================================
   * 15. HELPERS
   * ============================================================ */
  MusicPlayer.prototype._resolveUrl = function (src) {
    if (/^https?:\/\//.test(src) || src.indexOf('data:') === 0) return src;
    // Resolve relative to current document URL
    try {
      return new URL(src, document.baseURI).href;
    } catch (e) {
      return src;
    }
  };

  MusicPlayer.prototype._formatTime = function (sec) {
    if (!isFinite(sec) || isNaN(sec) || sec < 0) return '00:00';
    var m = Math.floor(sec / 60);
    var s = Math.floor(sec % 60);
    return (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
  };

  MusicPlayer.prototype._escapeHtml = function (s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[c];
    });
  };

  /* Shuffle helper — picks a different index from `exclude` */
  MusicPlayer.prototype._shuffleTo = function (excludeIndex, _direction) {
    if (this.playlist.length <= 1) {
      this._loadTrack(0, { autoplay: true });
      return;
    }
    var idx;
    var attempts = 0;
    do {
      idx = Math.floor(Math.random() * this.playlist.length);
      attempts++;
    } while (idx === excludeIndex && attempts < 12);
    this._loadTrack(idx, { autoplay: true });
  };

  /* ============================================================
   * 16. PUBLIC API
   * ============================================================ */
  MusicPlayer.prototype.togglePlay    = MusicPlayer.prototype.togglePlay;
  MusicPlayer.prototype.destroy       = function () {
    try {
      if (this.positionSaveTimer) { clearInterval(this.positionSaveTimer); }
      if (this.audio) {
        this.audio.pause();
        this.audio.removeAttribute('src');
        try { this.audio.load(); } catch (e) {}
        // Remove listeners by replacing node — simplest & safest
      }
      if (this.root && this.root.parentNode) {
        this.root.parentNode.removeChild(this.root);
      }
    } catch (e) {}
    if (instance === this) { instance = null; }
  };

  /* ============================================================
   * 17. BOOT — only ONE instance per page load
   * ============================================================ */
  function boot() {
    if (instance) {
      // already initialized — prevent double audio
      return instance;
    }
    try {
      return new MusicPlayer();
    } catch (e) {
      // Never let music player break the rest of the site
      if (window.console && console.warn) {
        console.warn('Music Player init failed:', e);
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  // Expose minimal public API
  window.MusicPlayer = {
    init: boot,
    get instance() { return instance; },
    play:    function () { if (instance) instance.play(); },
    pause:   function () { if (instance) instance.pause(); },
    toggle:  function () { if (instance) instance.togglePlay(); },
    next:    function () { if (instance) instance.next(); },
    prev:    function () { if (instance) instance.prev(); },
    destroy: function () { if (instance) instance.destroy(); }
  };
})();
