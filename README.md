# 🎬 VideoGrab — Universal Video Downloader

[![CI](https://github.com/Ogwusearch/videograb/actions/workflows/ci.yml/badge.svg)](https://github.com/Ogwusearch/videograb/actions)

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red)](https://github.com/yt-dlp/yt-dlp)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)](https://github.com/Ogwusearch/videograb)

---

> Download supported online media through a CLI or web interface powered by **yt-dlp**.

VideoGrab combines a Python command-line downloader with a **React + FastAPI web application**.

The project is designed around a shared download engine so both interfaces use the same core functionality.

```text
                         VideoGrab
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
       CLI Application              Web Application
             │                             │
             │                     React Frontend
             │                             │
             │                         FastAPI
             │                             │
             └──────────────┬──────────────┘
                            │
                            ▼
                    VideoDownloader
                            │
                            ▼
                          yt-dlp
```

---

# ✨ Features

## CLI

* 🌐 Support for many sites through yt-dlp
* 🎞 Quality presets
* 🔊 Audio extraction
* 📋 Batch downloads
* 🍪 Cookie support
* 🌍 Proxy configuration
* 💬 Subtitle downloads
* 📊 Rich terminal interface
* 🤖 Interactive mode
* 📝 Download logging
* ⚡ `vget.sh` automation
* 🧪 Automated tests

## Web Application

* 🌐 React frontend
* ⚡ Vite development environment
* 🚀 FastAPI backend
* 🎞 Video quality selection
* 🔊 Audio-only downloads
* 📡 HTTP file streaming
* 🗑 Temporary server-side files
* 🧹 Automatic temporary-file cleanup
* 📥 Browser downloads
* 🔌 REST API
* 📚 Automatic FastAPI API documentation

---

# 🏗 Architecture

VideoGrab uses a shared downloader engine.

```text
┌─────────────────────────────────────┐
│             Frontend                │
│          React + Vite               │
│                                     │
│       http://127.0.0.1:5173        │
└──────────────────┬──────────────────┘
                   │
                   │ HTTP
                   ▼
┌─────────────────────────────────────┐
│              Backend                │
│              FastAPI                │
│                                     │
│       http://127.0.0.1:8127        │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│           VideoService              │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│         VideoDownloader             │
│                                     │
│            yt-dlp                   │
└──────────────────┬──────────────────┘
                   │
                   ▼
             Temporary File
                   │
                   ▼
          StreamingResponse
                   │
                   ▼
                Browser
                   │
                   ▼
             User's Device
                   │
                   ▼
          Temporary File Deleted
```

---

# 📡 Web Download Streaming

The web application does not permanently store downloaded media.

The current lifecycle is:

```text
Source
  │
  ▼
yt-dlp
  │
  ▼
Temporary server directory
  │
  ▼
Downloaded media file
  │
  ▼
FastAPI StreamingResponse
  │
  ▼
Browser
  │
  ▼
User's device
  │
  ▼
Temporary server directory deleted
```

Temporary directories use names similar to:

```text
/tmp/videograb-xxxxx/
```

The resulting file is streamed in chunks rather than loading the entire media file into memory.

The current stream size is approximately:

```text
1 MB per chunk
```

After the response finishes, the temporary directory is removed.

### Important

Streaming does not mean the server uses zero disk space.

The current architecture temporarily stores the completed media file on the server before streaming it:

```text
Source
   ↓
Temporary server file
   ↓
Browser
```

It is **temporary storage**, not permanent media storage.

---

# 🌐 Web Application

## Frontend

Technology:

```text
React
Vite
JavaScript
Lucide React
```

Development server:

```text
http://127.0.0.1:5173
```

The frontend provides:

* URL input
* Quality selection
* Video download
* Audio download
* Download status
* Error handling
* Browser download handling

---

# ⚡ Backend

Technology:

```text
Python
FastAPI
Pydantic
Uvicorn
yt-dlp
```

Development server:

```text
http://127.0.0.1:8127
```

API documentation:

```text
http://127.0.0.1:8127/docs
```

Health endpoint:

```text
GET /api/health
```

Download endpoint:

```text
POST /api/download
```

Information endpoint:

```text
POST /api/info
```

---

# 📡 API

## Health

```http
GET /api/health
```

Example:

```json
{
  "status": "ok",
  "service": "videograb-api"
}
```

---

## Video Information

```http
POST /api/info
```

Request:

```json
{
  "url": "https://example.com/video"
}
```

The endpoint returns information detected through the existing VideoGrab/yt-dlp engine.

---

## Download

```http
POST /api/download
```

Request:

```json
{
  "url": "https://example.com/video",
  "quality": "best",
  "audio_only": false
}
```

Parameters:

| Parameter    | Type    | Default  | Description       |
| ------------ | ------- | -------- | ----------------- |
| `url`        | URL     | Required | Source URL        |
| `quality`    | string  | `best`   | Requested quality |
| `audio_only` | boolean | `false`  | Extract audio     |

The response is streamed to the browser as a downloadable file.

---

# 📁 Project Structure

```text
videograb/
│
├── videograb/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── detector.py
│   ├── downloader.py
│   ├── display.py
│   └── logger.py
│
├── backend/
│   ├── __init__.py
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── schemas.py
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   ├── info.py
│   │   │   └── download.py
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       └── video_service.py
│   │
│   ├── data/
│   │   ├── tmp/
│   │   └── downloads/
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── tests/
│   ├── test_config.py
│   ├── test_detector.py
│   └── test_downloader.py
│
├── scripts/
│   ├── batch_example.txt
│   └── export_cookies.md
│
├── docs/
│   ├── streaming-downloads.md
│   └── ...
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── vget.sh
├── setup.sh
├── start-backend.sh
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

# 📦 Requirements

## CLI

| Requirement | Version | Notes              |
| ----------- | ------- | ------------------ |
| Python      | 3.10+   | Required           |
| yt-dlp      | Current | Downloader engine  |
| Rich        | 13+     | Terminal interface |
| FFmpeg      | Current | Recommended        |

## Web Application

| Component        | Technology |
| ---------------- | ---------- |
| Frontend         | React      |
| Build tool       | Vite       |
| Backend          | FastAPI    |
| Server           | Uvicorn    |
| Downloader       | yt-dlp     |
| Media processing | FFmpeg     |

---

# 🎬 FFmpeg

FFmpeg is strongly recommended because some media sources provide separate video and audio streams that need to be merged.

## Ubuntu / Debian

```bash
sudo apt install ffmpeg
```

## macOS

```bash
brew install ffmpeg
```

## Arch Linux

```bash
sudo pacman -S ffmpeg
```

## Windows

Install FFmpeg and make sure it is available through `PATH`.

Verify:

```bash
ffmpeg -version
```

---

# ⚡ Quick Start

## Clone

```bash
git clone https://github.com/Ogwusearch/videograb.git

cd videograb
```

---

# 🐍 CLI Setup

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install:

```bash
pip install -r requirements.txt
pip install -e .
```

Verify:

```bash
videograb --version
```

---

# 🌐 Web Application Setup

## Backend

From the project root:

```bash
source .venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

Start the backend:

```bash
./start-backend.sh
```

Backend:

```text
http://127.0.0.1:8127
```

API documentation:

```text
http://127.0.0.1:8127/docs
```

---

# ⚛️ Frontend

Open another terminal:

```bash
cd /home/ogwu/workspace/videograb/frontend
```

Install dependencies:

```bash
npm install
```

Start Vite:

```bash
npm run dev -- --host 127.0.0.1 --port 5173
```

Open:

```text
http://127.0.0.1:5173
```

---

# 🔧 Frontend Environment

Create:

```text
frontend/.env.development
```

with:

```env
VITE_API_BASE_URL=http://127.0.0.1:8127
```

Example production configuration:

```env
VITE_API_BASE_URL=https://your-api-domain.example
```

Environment files containing secrets should not be committed.

---

# 🚀 CLI Usage

## Interactive Mode

```bash
videograb
```

or:

```bash
videograb --interactive
```

---

## Single Video

```bash
videograb <URL>
```

Example:

```bash
videograb <URL>
```

Specify quality:

```bash
videograb <URL> -q 1080p
```

Specify output directory:

```bash
videograb <URL> -q 720p -o ~/Videos/
```

---

# 🔊 Audio Only

```bash
videograb <URL> --audio
```

The audio extraction pipeline uses FFmpeg where required.

---

# 📋 Metadata

```bash
videograb <URL> --info
```

This displays available media information without starting a normal download.

---

# 📦 Batch Downloads

Create:

```text
urls.txt
```

with one URL per line:

```text
https://example.com/video1
https://example.com/video2
https://example.com/video3
```

Run:

```bash
videograb --batch urls.txt
```

With quality:

```bash
videograb --batch urls.txt -q 720p
```

With an output directory:

```bash
videograb --batch urls.txt -o ~/Videos/
```

---

# 🎛 CLI Options

| Flag                | Short | Description           |
| ------------------- | ----- | --------------------- |
| `--output DIR`      | `-o`  | Output directory      |
| `--quality PRESET`  | `-q`  | Quality preset        |
| `--audio`           |       | Extract audio         |
| `--cookies FILE`    |       | Cookies file          |
| `--cookies-browser` |       | Browser cookie source |
| `--proxy URL`       |       | Proxy URL             |
| `--subtitles`       |       | Download subtitles    |
| `--batch FILE`      |       | Batch URL file        |
| `--info`            |       | Show metadata         |
| `--verbose`         | `-v`  | Verbose output        |
| `--interactive`     | `-i`  | Interactive mode      |
| `--version`         | `-V`  | Show version          |

---

# ⚡ vget.sh

`vget.sh` provides a convenient shell wrapper.

Make it executable:

```bash
chmod +x vget.sh
```

Install globally:

```bash
sudo cp vget.sh /usr/local/bin/vget
```

Use:

```bash
vget <URL>
```

Examples:

```bash
vget <URL>

vget <URL> -q 720p

vget <URL> --audio

vget --batch urls.txt

vget --info <URL>
```

---

# 🌐 Supported Platforms

VideoGrab uses yt-dlp as its extraction engine.

Support depends on the current yt-dlp extractor implementations and individual platform changes.

Examples of supported services include:

| Platform    | Examples                                |
| ----------- | --------------------------------------- |
| YouTube     | Videos, Shorts, playlists, live content |
| X / Twitter | Public media                            |
| Instagram   | Public supported media                  |
| Snapchat    | Supported public media                  |
| TikTok      | Supported public media                  |
| Facebook    | Supported public media                  |
| Vimeo       | Public videos                           |
| Reddit      | Supported video posts                   |
| Twitch      | Supported VODs and clips                |
| Dailymotion | Public videos                           |
| Bilibili    | Supported public videos                 |
| Rumble      | Supported public videos                 |
| SoundCloud  | Supported audio                         |

For the current extractor list, refer to the yt-dlp project.

---

# 🍪 Cookies and Authentication

The CLI can use cookies supplied by the user for content they are authorized to access.

Example:

```bash
videograb <URL> --cookies cookies.txt
```

Browser cookie extraction can also be configured where supported:

```bash
videograb <URL> --cookies-browser chrome
```

Supported browser choices depend on the installed yt-dlp version and local environment.

Never commit cookies or authentication files to Git.

Add them to `.gitignore` when appropriate.

---

# 🌍 Proxy Configuration

The CLI supports proxy configuration:

```bash
videograb <URL> --proxy socks5://127.0.0.1:1080
```

or:

```bash
videograb <URL> --proxy http://proxyserver:8080
```

Use proxy services only where you are authorized to do so and in accordance with applicable laws and service terms.

---

# 💬 Subtitles

Request subtitles with:

```bash
videograb <URL> --subtitles
```

Subtitle availability depends on the source platform.

---

# 🧪 Testing

Run all tests:

```bash
pytest tests/ -v
```

Run coverage:

```bash
pytest tests/ -v --cov=videograb --cov-report=html
```

Open the generated report:

```bash
open htmlcov/index.html
```

Linux users may use:

```bash
xdg-open htmlcov/index.html
```

Run an individual test file:

```bash
pytest tests/test_detector.py -v
```

---

# 🛠 Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Format:

```bash
make format
```

Lint:

```bash
make lint
```

Test:

```bash
make test
```

Clean build artifacts:

```bash
make clean
```

---

# 🐛 Troubleshooting

| Problem                        | Solution                                                  |
| ------------------------------ | --------------------------------------------------------- |
| `videograb: command not found` | Activate `.venv` and run `pip install -e .`               |
| `ffmpeg not found`             | Install FFmpeg and verify it is on `PATH`                 |
| `fastapi` cannot be imported   | Activate `.venv` and install `backend/requirements.txt`   |
| Pylance cannot find FastAPI    | Select `.venv/bin/python` as the VS Code interpreter      |
| Backend port is busy           | Check the process using port `8127`                       |
| Frontend cannot reach API      | Check `VITE_API_BASE_URL`                                 |
| CORS error                     | Verify the backend allows the frontend origin             |
| No audio                       | Verify FFmpeg installation                                |
| yt-dlp failure                 | Update yt-dlp                                             |
| Authentication failure         | Verify the supplied cookies are current and authorized    |
| Temporary files remain         | Check active/interrupted downloads and `/tmp/videograb-*` |

Update yt-dlp:

```bash
python -m pip install -U yt-dlp
```

---

# 🔍 Backend Diagnostics

Check the Python interpreter:

```bash
python -c "import sys; print(sys.executable)"
```

Expected:

```text
/home/ogwu/workspace/videograb/.venv/bin/python
```

Check FastAPI:

```bash
python -c "import fastapi; print(fastapi.__version__)"
```

Check Starlette:

```bash
python -c "import starlette; print(starlette.__version__)"
```

Check the API:

```bash
curl http://127.0.0.1:8127/api/health
```

---

# 🧹 Temporary Download Storage

Web downloads use temporary directories.

Typical location:

```text
/tmp/videograb-*/
```

These files are removed after the streaming response finishes.

The project should not treat:

```text
backend/data/downloads/
```

as permanent user media storage.

Downloaded media should not be committed to Git.

---

# 🔐 Security Considerations

Before exposing the downloader publicly, additional controls should be implemented.

Recommended controls include:

* Request rate limiting
* Concurrent download limits
* Download timeouts
* Temporary disk quotas
* Cleanup after interrupted requests
* Input validation
* Logging
* Monitoring
* Resource limits
* Abuse protection

Video downloading and media processing can consume substantial CPU, memory, bandwidth, and disk resources.

---

# 🚀 Deployment

The intended initial deployment architecture is:

```text
                         Internet
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
      Cloudflare Pages                 Render
             │                             │
             ▼                             ▼
      React / Vite                    FastAPI
                                            │
                                            ▼
                                         yt-dlp
                                            │
                                            ▼
                                    Temporary storage
                                            │
                                            ▼
                                         Browser
```

GitHub stores the application source code.

The web frontend and API are deployed separately.

The backend should use the hosting platform's assigned `$PORT` and bind to:

```text
0.0.0.0
```

Local development uses:

```text
127.0.0.1:5173
127.0.0.1:8127
```

Production configuration should use the actual deployed frontend and backend domains.

---

# 📚 Documentation

Additional documentation is stored in:

```text
docs/
```

Current documentation includes:

```text
docs/
├── streaming-downloads.md
└── ...
```

The streaming documentation describes:

* Temporary-file lifecycle
* `VideoService`
* `StreamingResponse`
* Chunked file transfer
* Browser downloads
* Automatic cleanup
* Storage considerations
* Production considerations

---

# 🧭 Development Roadmap

## Phase 1 — CLI

* [x] yt-dlp integration
* [x] Quality presets
* [x] Audio extraction
* [x] Batch downloads
* [x] Interactive CLI
* [x] Rich terminal UI
* [x] Tests

## Phase 2 — API

* [x] FastAPI application
* [x] Health endpoint
* [x] Video information endpoint
* [x] Download endpoint
* [x] Pydantic request schemas

## Phase 3 — Web Frontend

* [x] React
* [x] Vite
* [x] URL input
* [x] Quality selector
* [x] Audio/video selection
* [x] API integration
* [x] Browser download

## Phase 4 — Streaming

* [x] Temporary download directory
* [x] Chunked file streaming
* [x] `StreamingResponse`
* [x] Browser download headers
* [x] Automatic cleanup

## Phase 5 — Production Hardening

* [ ] Rate limiting
* [ ] Concurrent job limits
* [ ] Download timeouts
* [ ] Resource limits
* [ ] Improved cleanup
* [ ] Production logging
* [ ] Monitoring
* [ ] Abuse protection

## Phase 6 — Deployment

* [ ] GitHub CI validation
* [ ] Backend deployment
* [ ] Frontend deployment
* [ ] Production CORS configuration
* [ ] Production environment variables
* [ ] Domain configuration
* [ ] End-to-end production testing

---

# ⚠️ Responsible Use

VideoGrab should only be used to download media when the user has the necessary rights or permission to do so.

Users are responsible for complying with:

* Applicable copyright law
* Platform terms of service
* Content licenses
* Privacy requirements
* Creator rights

Do not use VideoGrab to bypass access controls or download content you are not authorized to access.

---

# 👤 Author

**Ogwusearch**

GitHub:

https://github.com/Ogwusearch

---

# 📄 License

MIT License.

See:

```text
LICENSE
```

---

<div align="center">

Made with ❤️ by **Ogwusearch**

Powered by **yt-dlp**

⭐ Star the repository if it is useful to you.

</div>
