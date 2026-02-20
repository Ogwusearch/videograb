# 🎬 VideoGrab — Universal Video Downloader

[![CI](https://github.com/yourname/videograb/actions/workflows/ci.yml/badge.svg)](https://github.com/yourname/videograb/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Download videos from **YouTube**, **X (Twitter)**, **Instagram**, **Snapchat**,
**TikTok**, **Facebook**, **Vimeo**, **Reddit**, **Twitch**, and 1000+ more sites.

---

## 📦 Requirements

- Python 3.10+
- `ffmpeg` (recommended for best quality merging)

Install ffmpeg:

| OS | Command |
|----|---------|
| macOS | `brew install ffmpeg` |
| Ubuntu/Debian | `sudo apt install ffmpeg` |
| Windows | [Download from ffmpeg.org](https://ffmpeg.org/download.html) |

---

## ⚡ Quick Start

```bash
git clone https://github.com/yourname/videograb.git
cd videograb
pip install -e ".[dev]"     # installs as CLI tool + dev deps
videograb --interactive      # launch interactive mode
```

Or without installing:
```bash
pip install -r requirements.txt
python -m videograb.cli https://youtu.be/dQw4w9WgXcQ
```

---

## 🚀 Usage

### Interactive Mode
```bash
videograb
videograb --interactive
```

### Single URL
```bash
videograb <URL>
videograb <URL> -q 720p
videograb <URL> --audio          # MP3 extraction
videograb <URL> --info           # Metadata only
```

### Batch Download
```bash
videograb --batch scripts/batch_example.txt
videograb --batch urls.txt -o ~/Videos/ -q 1080p
```

### Authenticated Content (Instagram, private posts)
```bash
# Option 1 — cookies file
videograb <URL> --cookies cookies.txt

# Option 2 — pull from browser directly
videograb <URL> --cookies-browser chrome
```

---

## 🎛 All Options

| Flag | Description |
|------|-------------|
| `-o DIR` | Output directory |
| `-q QUALITY` | `best`, `1080p`, `720p`, `480p`, `360p`, `worst` |
| `--audio` | Extract audio as MP3 |
| `--cookies FILE` | Netscape cookies.txt |
| `--cookies-browser` | `chrome`, `firefox`, `edge`, `safari` |
| `--proxy URL` | Proxy (e.g. `socks5://127.0.0.1:1080`) |
| `--subtitles` | Download subtitles |
| `--batch FILE` | File with one URL per line |
| `--info` | Show metadata without downloading |
| `-v` | Verbose output |
| `-i` | Interactive mode |

---

## 🗂 Project Structure

```
videograb/
├── videograb/
│   ├── __init__.py       # Package metadata
│   ├── cli.py            # CLI entry point & interactive mode
│   ├── config.py         # Global config & constants
│   ├── detector.py       # Platform detection from URL
│   ├── downloader.py     # Core yt-dlp download engine
│   ├── display.py        # Rich terminal UI helpers
│   └── logger.py         # Logging setup
├── tests/
│   ├── test_config.py
│   ├── test_detector.py
│   └── test_downloader.py
├── scripts/
│   ├── batch_example.txt
│   └── export_cookies.md
├── docs/
├── .github/workflows/ci.yml
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .env.example
└── README.md
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
pytest tests/ -v --cov=videograb --cov-report=html
```

---

## ⚠️ Disclaimer

For personal use only. Respect platform Terms of Service and copyright laws.
Only download content you have permission to download.

---

## 📄 License

MIT — see [LICENSE](LICENSE)
