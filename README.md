# 🎬 VideoGrab — Universal Video Downloader

[![CI](https://github.com/Ogwusearch/videograb/actions/workflows/ci.yml/badge.svg)](https://github.com/Ogwusearch/videograb/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red)](https://github.com/yt-dlp/yt-dlp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)](https://github.com/Ogwusearch/videograb)
[![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen)](https://github.com/Ogwusearch/videograb)

> Download videos from **YouTube**, **X (Twitter)**, **Instagram**, **Snapchat**,
> **TikTok**, **Facebook**, **Vimeo**, **Reddit**, **Twitch**, and **1000+ more sites** —
> all from one elegant command-line tool.

---

## ✨ Features

- 🌐 **1000+ supported sites** via yt-dlp
- 🎞 **Quality presets** — best, 1080p, 720p, 480p, 360p
- 🔊 **Audio extraction** — MP3, M4A, WAV, FLAC
- 📋 **Batch downloading** — one URL per line in a text file
- 🍪 **Cookie support** — for private/authenticated content
- 🌍 **Proxy support** — bypass geo-restrictions
- 💬 **Subtitles** — download alongside video
- 📊 **Rich terminal UI** — progress bars, tables, colours
- 🤖 **Interactive mode** — menu-driven, no flags needed
- 📝 **Download logging** — full history at `~/.videograb/logs/`
- ⚡ **vget.sh** — single-command shell automation script
- 🧪 **Full test suite** — pytest with mocked yt-dlp

---

## 📦 Requirements

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.10+ | Required |
| yt-dlp | latest | Auto-installed |
| rich | 13.0+ | Auto-installed |
| ffmpeg | any | **Highly recommended** |

### Install ffmpeg

| OS | Command |
|----|---------|
| Ubuntu / Debian | `sudo apt install ffmpeg` |
| macOS | `brew install ffmpeg` |
| Arch Linux | `sudo pacman -S ffmpeg` |
| Windows | [Download from ffmpeg.org](https://ffmpeg.org/download.html) → add to PATH |

> **Why ffmpeg?** Without it, video and audio tracks can't be merged — you may get video-only or audio-only files for some platforms.

---

## ⚡ Quick Start

### Option 1 — Clone & Auto-Setup (recommended)

```bash
git clone https://github.com/Ogwusearch/videograb.git
cd videograb
bash setup.sh          # scaffolds, creates venv, installs everything
```

### Option 2 — Manual install

```bash
git clone https://github.com/Ogwusearch/videograb.git
cd videograb
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
videograb --interactive
```

### Option 3 — No install needed

```bash
pip install yt-dlp rich
python -m videograb.cli https://youtu.be/dQw4w9WgXcQ
```

---

## 🚀 Usage

### Interactive Mode _(easiest)_

```bash
videograb
videograb --interactive
```

### Single Video

```bash
videograb https://youtu.be/dQw4w9WgXcQ
videograb https://youtu.be/dQw4w9WgXcQ -q 1080p
videograb https://youtu.be/dQw4w9WgXcQ -q 720p -o ~/Desktop/
```

### Audio Only (MP3)

```bash
videograb https://youtu.be/dQw4w9WgXcQ --audio
```

### Show Metadata Only

```bash
videograb https://youtu.be/dQw4w9WgXcQ --info
```

### Batch Download

```bash
videograb --batch urls.txt
videograb --batch urls.txt -q 720p -o ~/Videos/
```

### Authenticated Content _(Instagram, private X posts)_

```bash
# Option 1 — pull cookies directly from browser
videograb <URL> --cookies-browser chrome

# Option 2 — use exported cookies.txt file
videograb <URL> --cookies cookies.txt
```

### Geo-Restricted Content

```bash
videograb <URL> --proxy socks5://127.0.0.1:1080
videograb <URL> --proxy http://proxyserver:8080
```

### With Subtitles

```bash
videograb <URL> --subtitles
```

---

## ⚡ vget.sh — Shell Automation Script

For quick use without activating venv every time:

```bash
# One-time setup — make it a global command
chmod +x vget.sh
sudo cp vget.sh /usr/local/bin/vget

# Use from anywhere
vget https://youtu.be/TCiRk89axWM
vget https://youtu.be/TCiRk89axWM -q 720p
vget https://youtu.be/TCiRk89axWM --audio
vget --batch urls.txt
vget --batch urls.txt -q 1080p -o ~/Videos
vget --info https://youtu.be/TCiRk89axWM
vget --update                          # update yt-dlp to latest
vget --log                             # show download history
vget                                   # interactive menu
```

---

## 🎛 All CLI Options

| Flag | Short | Description |
|------|-------|-------------|
| `--output DIR` | `-o` | Directory to save files (default: `~/Videos/VideoGrab`) |
| `--quality PRESET` | `-q` | `best` `1080p` `720p` `480p` `360p` `worst` |
| `--audio` | | Extract audio only (MP3) |
| `--cookies FILE` | | Netscape format cookies.txt |
| `--cookies-browser` | | Pull cookies from `chrome` `firefox` `edge` `safari` `brave` |
| `--proxy URL` | | Proxy e.g. `socks5://127.0.0.1:1080` |
| `--subtitles` | | Download subtitles (English) |
| `--batch FILE` | | Text file with one URL per line |
| `--info` | | Print metadata only, don't download |
| `--verbose` | `-v` | Full yt-dlp debug output |
| `--interactive` | `-i` | Launch interactive menu |
| `--version` | `-V` | Print version and exit |

---

## 🌐 Supported Platforms

| Platform | Notes |
|----------|-------|
| **YouTube** | Videos, Shorts, Playlists, Live streams |
| **X / Twitter** | Public video tweets & GIFs |
| **Instagram** | Reels, Posts _(needs cookies for private)_ |
| **Snapchat** | Spotlight & Stories |
| **TikTok** | Public videos |
| **Facebook** | Public videos & Reels |
| **Vimeo** | Public videos |
| **Reddit** | v.redd.it video posts |
| **Twitch** | VODs & Clips |
| **Dailymotion** | Public videos |
| **Bilibili** | Public videos |
| **Rumble** | Public videos |
| **SoundCloud** | Audio tracks |
| **1000+ more** | Powered by yt-dlp |

---

## 🍪 Downloading Private / Login-Required Content

### Method 1 — Browser extension _(easiest)_

1. Install **[Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)** (Chrome) or **[cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)** (Firefox)
2. Log in to the platform
3. Click the extension → Export → save as `cookies.txt`
4. Run: `videograb <URL> --cookies cookies.txt`

### Method 2 — Pull directly from browser _(no extension)_

```bash
videograb <URL> --cookies-browser chrome
# Also: firefox, edge, safari, brave, chromium
```

---

## 📁 Batch File Format

```text
# YouTube
https://youtu.be/dQw4w9WgXcQ
https://youtu.be/TCiRk89axWM

# X / Twitter
https://x.com/user/status/1234567890

# Instagram (needs --cookies)
https://www.instagram.com/reel/ABCXYZ/

# Snapchat
https://www.snapchat.com/spotlight/abc123
```

```bash
videograb --batch urls.txt --cookies cookies.txt -q 720p -o ~/Downloads/
```

---

## 🗂 Project Structure

```
videograb/
├── videograb/                   # Main package
│   ├── __init__.py              # Version & metadata
│   ├── cli.py                   # CLI entry point & interactive mode
│   ├── config.py                # Config, quality presets, platform patterns
│   ├── detector.py              # URL → platform detection
│   ├── downloader.py            # Core yt-dlp engine
│   ├── display.py               # Rich UI — progress bars, tables, banners
│   └── logger.py                # Logging (~/.videograb/logs/)
├── tests/
│   ├── test_config.py
│   ├── test_detector.py         # 12 parametrized platform tests
│   └── test_downloader.py       # Mocked yt-dlp unit tests
├── scripts/
│   ├── batch_example.txt
│   └── export_cookies.md
├── docs/
├── .github/workflows/ci.yml     # CI — Python 3.10, 3.11, 3.12
├── vget.sh                      # Shell automation script
├── setup.sh                     # Full auto-setup script
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── Makefile
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🧪 Running Tests

```bash
# All tests
pytest tests/ -v

# With HTML coverage report
pytest tests/ -v --cov=videograb --cov-report=html
open htmlcov/index.html

# Single file
pytest tests/test_detector.py -v
```

---

## 🛠 Development

```bash
pip install -e ".[dev]"   # install with dev extras

make format    # black formatter
make lint      # flake8 linter
make test      # pytest
make clean     # remove build artifacts
```

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `videograb: command not found` | `pip install -e .` inside the project folder |
| `ffmpeg not found` | Install ffmpeg and add to PATH |
| Login / private content fails | `--cookies-browser chrome` or `--cookies cookies.txt` |
| Video unavailable / region-locked | Try `--proxy socks5://127.0.0.1:1080` |
| No audio in downloaded file | Install ffmpeg |
| Instagram keeps failing | Export fresh cookies from browser |
| YouTube errors | `pip install -U yt-dlp` — YouTube changes frequently |
| Exit code 128 | Open a fresh terminal: `cd ~/projects/videograb && source .venv/bin/activate` |
| `pip install -e .` fails | `pip install --upgrade pip setuptools wheel` first, then retry |

---

## ⚠️ Disclaimer

This tool is for **personal use only**. Always respect:
- Platform Terms of Service
- Copyright laws in your country
- Content creator rights

**Only download content you have explicit permission to download.**

---

## 👤 Author

**Ogwusearch**
- GitHub: [@Ogwusearch](https://github.com/Ogwusearch)

---

## 📄 License

MIT — see [LICENSE](LICENSE)

---

<div align="center">

Made with ❤️ by [Ogwusearch](https://github.com/Ogwusearch) · Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp)

⭐ **Star this repo if it helped you!**

</div>
