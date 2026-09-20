# VideoGrab — Streaming Downloads

## 1. Overview

VideoGrab uses the existing `yt-dlp` download engine and exposes it through a FastAPI web API.

The web application is designed so that downloaded media is **not permanently stored on the server**.

The current download flow is:

```text
Browser
   │
   │ POST /api/download
   ▼
FastAPI
   │
   ▼
VideoService
   │
   ▼
Temporary directory
   │
   ▼
VideoDownloader
   │
   ▼
yt-dlp
   │
   ▼
Downloaded media file
   │
   ▼
StreamingResponse
   │
   ▼
Browser
   │
   ▼
User's device
   │
   ▼
Temporary directory deleted
```

The temporary file exists only long enough to complete the download and stream the resulting file to the browser.

---

# 2. Design Goals

The streaming implementation has the following goals:

* Reuse the existing `VideoDownloader`.
* Avoid permanent server-side media storage.
* Avoid loading an entire video into RAM.
* Stream the resulting file to the browser in chunks.
* Automatically remove temporary files after streaming.
* Preserve the existing `/api/download` endpoint.
* Allow the browser to save the resulting file to the user's normal download location.

---

# 3. Project Structure

The relevant backend structure is:

```text
videograb/
├── backend/
│   ├── app/
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
│   └── requirements.txt
│
├── videograb/
│   └── downloader.py
│
└── docs/
    └── streaming-downloads.md
```

---

# 4. Components

## 4.1 React Frontend

The frontend collects:

* Video URL
* Quality
* Output type

It sends a request to:

```text
POST /api/download
```

The response contains the downloaded media.

---

## 4.2 FastAPI

FastAPI provides the HTTP API.

The main download route is:

```text
POST /api/download
```

The route receives the request and delegates the actual download to `VideoService`.

---

## 4.3 VideoService

`VideoService` is responsible for:

1. Creating a temporary directory.
2. Creating a `VideoDownloader`.
3. Running the existing downloader.
4. Finding the resulting media file.
5. Returning the temporary directory and file path.
6. Cleaning up the temporary directory if the download fails.

File:

```text
backend/app/services/video_service.py
```

---

## 4.4 VideoDownloader

`VideoDownloader` remains the core download engine.

It handles:

* yt-dlp
* quality selection
* audio-only downloads
* subtitles
* cookies
* proxies
* output formatting
* FFmpeg post-processing

The web API does not replace this component.

Instead:

```text
FastAPI
   │
   ▼
VideoService
   │
   ▼
VideoDownloader
   │
   ▼
yt-dlp
```

This keeps the existing CLI and web application based on the same download engine.

---

# 5. Temporary Directory Lifecycle

A temporary directory is created for each download.

Example:

```text
/tmp/videograb-a8x3k91p/
```

The downloaded file may look like:

```text
/tmp/videograb-a8x3k91p/video.mp4
```

The directory remains available while FastAPI streams the file.

After streaming finishes:

```text
/tmp/videograb-a8x3k91p/
```

is removed.

---

# 6. Why `mkdtemp()` Is Used

The original implementation used:

```python
TemporaryDirectory(prefix="videograb-").name
```

This was problematic because only the directory name was retained while the `TemporaryDirectory` object itself could be destroyed.

The new implementation uses:

```python
temp_dir = Path(
    tempfile.mkdtemp(prefix="videograb-")
)
```

This gives the application explicit control over the directory lifecycle.

The directory can later be removed with:

```python
shutil.rmtree(
    temp_dir,
    ignore_errors=True,
)
```

---

# 7. VideoService Contract

The new service returns two paths:

```python
tuple[Path, Path]
```

The values are:

```text
temporary directory
downloaded file
```

Example:

```python
temp_dir, file_path = service.download(...)
```

For example:

```text
temp_dir
└── /tmp/videograb-x7k91a/

file_path
└── /tmp/videograb-x7k91a/example.mp4
```

---

# 8. StreamingResponse

The API uses FastAPI's:

```python
StreamingResponse
```

instead of:

```python
FileResponse
```

The streaming response reads the file incrementally.

The implementation uses:

```python
chunk_size = 1024 * 1024
```

which equals:

```text
1 MB
```

The server therefore does not need to load an entire large video into memory.

---

# 9. File Streaming

The streaming function is:

```python
def iter_file(
    file_path: Path,
    chunk_size: int = 1024 * 1024,
):
    with file_path.open("rb") as file:
        while chunk := file.read(chunk_size):
            yield chunk
```

The flow is:

```text
video.mp4
   │
   ├── 1 MB
   ├── 1 MB
   ├── 1 MB
   ├── 1 MB
   └── ...
        │
        ▼
     Browser
```

This is preferable to:

```python
file.read()
```

for potentially large media files.

---

# 10. Browser Download Headers

The API sends:

```http
Content-Disposition: attachment
```

This tells the browser that the response should be treated as a downloadable file.

The filename is taken from the resulting media file:

```python
headers={
    "Content-Disposition": (
        f'attachment; filename="{file_path.name}"'
    )
}
```

For example:

```text
example.mp4
```

or:

```text
example.mp3
```

---

# 11. Cleanup

The response uses a background task:

```python
BackgroundTask(
    cleanup_temp_directory,
    temp_dir,
)
```

The cleanup function is:

```python
def cleanup_temp_directory(temp_dir: Path) -> None:
    shutil.rmtree(
        temp_dir,
        ignore_errors=True,
    )
```

The lifecycle becomes:

```text
Download
   │
   ▼
Temporary file created
   │
   ▼
StreamingResponse starts
   │
   ▼
File streamed
   │
   ▼
Response finishes
   │
   ▼
Background cleanup
   │
   ▼
Temporary directory removed
```

---

# 12. Error Handling

If the downloader fails:

```python
if not success:
    raise RuntimeError("Download failed")
```

The service cleans up the temporary directory:

```python
shutil.rmtree(
    temp_dir,
    ignore_errors=True,
)
```

The API then converts the exception into an HTTP error:

```python
raise HTTPException(
    status_code=400,
    detail=str(exc),
)
```

This prevents failed downloads from being intentionally retained.

---

# 13. Download API

## Endpoint

```http
POST /api/download
```

## Request

Example:

```json
{
  "url": "https://example.com/video",
  "quality": "best",
  "audio_only": false
}
```

## Parameters

| Parameter    | Type    | Default  | Description                    |
| ------------ | ------- | -------- | ------------------------------ |
| `url`        | URL     | required | Source media URL               |
| `quality`    | string  | `best`   | Requested quality              |
| `audio_only` | boolean | `false`  | Extract audio instead of video |

---

# 14. Successful Response

The response is a streamed binary file.

For example:

```http
HTTP/1.1 200 OK
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="video.mp4"
```

The browser receives the media as a download.

---

# 15. Frontend Flow

The frontend sends:

```text
POST /api/download
```

The backend:

```text
1. Creates temporary directory
2. Runs yt-dlp
3. Locates output file
4. Starts streaming
```

The frontend receives:

```text
HTTP response
      │
      ▼
Blob
      │
      ▼
Browser download
```

The browser controls where the user ultimately saves the downloaded file.

---

# 16. Storage Model

VideoGrab does not use a permanent media-storage directory for web downloads.

Instead:

```text
Server
└── temporary media
       │
       ▼
    browser
       │
       ▼
User's device
```

This is different from:

```text
Server
└── downloads/
      ├── video1.mp4
      ├── video2.mp4
      ├── video3.mp4
      └── ...
```

The second model would cause server storage to continually grow.

The streaming design avoids that persistent accumulation.

---

# 17. Memory Model

The application does not intentionally load the entire resulting video into RAM.

Instead:

```text
Disk
 │
 ├── 1 MB
 ├── 1 MB
 ├── 1 MB
 └── ...
      │
      ▼
   Browser
```

This is important for large media files.

However, the server still needs enough disk space to hold the temporary downloaded file before and during streaming.

---

# 18. Disk Usage

Streaming does **not** mean zero server disk usage in the current architecture.

The current implementation is:

```text
Source
   ↓
Temporary server file
   ↓
Browser
```

Therefore a 500 MB video can temporarily require approximately 500 MB of server disk space.

After the response completes:

```text
temporary file → deleted
```

The server does not retain the file permanently.

---

# 19. Important Difference: File Streaming vs Direct Proxying

Current architecture:

```text
Source
   ↓
yt-dlp
   ↓
temporary file
   ↓
FastAPI StreamingResponse
   ↓
Browser
```

A future direct-proxy architecture could be:

```text
Source
   ↓
yt-dlp / source stream
   ↓
FastAPI
   ↓
Browser
```

The second architecture could reduce temporary disk usage, but it requires substantially more careful handling of:

* yt-dlp output streams
* FFmpeg processing
* fragmented media
* merged formats
* retries
* HTTP range requests
* connection failures
* client disconnects

The current temporary-file streaming implementation is therefore intentionally simpler.

---

# 20. Security Considerations

Before exposing VideoGrab publicly, the API should eventually add:

* Rate limiting
* Maximum concurrent downloads
* Download timeouts
* Maximum temporary disk usage
* Temporary-file cleanup on interrupted requests
* URL validation
* Request-size limits
* Logging and monitoring
* Protection against server resource exhaustion

A public downloader can receive many simultaneous resource-intensive requests.

---

# 21. Production Considerations

The current design is suitable for development and an initial prototype.

For production deployment, the backend should also consider:

```text
Reverse proxy
      │
      ▼
FastAPI
      │
      ├── concurrency limits
      ├── rate limiting
      ├── temporary storage limits
      └── cleanup
```

The server should not be treated as permanent media storage.

---

# 22. Testing

Start the backend:

```bash
cd /home/ogwu/workspace/videograb

source .venv/bin/activate

./start-backend.sh
```

Check the API:

```bash
curl http://127.0.0.1:8127/api/health
```

Expected:

```json
{
  "status": "ok",
  "service": "videograb-api"
}
```

Open the API documentation:

```text
http://127.0.0.1:8127/docs
```

Use the `/api/download` endpoint to test a permitted media URL.

---

# 23. Monitoring Temporary Files

During development, temporary directories can be inspected with:

```bash
ls -lah /tmp | grep videograb
```

During an active download, you may see:

```text
videograb-abc123/
```

After the response completes, it should disappear.

---

# 24. Architecture Summary

The final web download architecture is:

```text
┌───────────────────────────┐
│       React Frontend      │
│      localhost:5173       │
└─────────────┬─────────────┘
              │
              │ HTTP
              ▼
┌───────────────────────────┐
│       FastAPI Backend     │
│      localhost:8127       │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│       VideoService        │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│   Temporary Directory     │
│     /tmp/videograb-*      │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│     VideoDownloader       │
│          yt-dlp           │
└─────────────┬─────────────┘
              │
              ▼
       Downloaded File
              │
              ▼
┌───────────────────────────┐
│    StreamingResponse      │
│       1 MB chunks         │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│          Browser          │
└─────────────┬─────────────┘
              │
              ▼
       User's Device

              +

       Background Cleanup
              │
              ▼
     Temporary directory
           deleted
```

---

# 25. Implementation Status

| Component                      | Status             |
| ------------------------------ | ------------------ |
| Existing CLI downloader        | Complete           |
| yt-dlp integration             | Complete           |
| FastAPI backend                | Complete           |
| Download API                   | Complete           |
| Temporary download directory   | Implemented        |
| Chunked file streaming         | Implemented        |
| Browser download response      | Implemented        |
| Automatic cleanup              | Implemented        |
| Permanent server media storage | Not used           |
| Frontend download integration  | Existing           |
| Download progress              | Future improvement |
| Rate limiting                  | Future             |
| Concurrent-job limits          | Future             |
| Production hardening           | Future             |

---

# 26. Next Development Phase

The next logical phase is **download progress and job management**.

Instead of:

```text
Click Download
       │
       ▼
Wait
       │
       ▼
File appears
```

the application can eventually provide:

```text
Download
   │
   ├── Preparing
   ├── Downloading
   ├── Processing
   ├── Streaming
   └── Complete
```

This can later be extended with:

```text
Progress %
Download speed
Downloaded size
Estimated time remaining
Current status
Cancel button
Error details
```

The existing `VideoDownloader` already has progress-hook support, so this can be built on top of the current architecture.
