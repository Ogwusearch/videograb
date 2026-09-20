import { useState } from "react";
import {
  Download,
  Link,
  Loader2,
  Music,
  Video,
  CheckCircle,
  AlertCircle,
} from "lucide-react";

const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8127";
  
function App() {
  const [url, setUrl] = useState("");
  const [quality, setQuality] = useState("best");
  const [format, setFormat] = useState("video");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const getInfo = async () => {
    if (!url.trim()) {
      setError("Enter a video URL.");
      return null;
    }

    setLoading(true);
    setError("");
    setMessage("");

    try {
      const response = await fetch(`${API_BASE}/api/info`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to read video information.");
      }

      return data;
    } catch (err) {
      setError(err.message || "Unable to connect to VideoGrab API.");
      return null;
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!url.trim()) {
      setError("Enter a video URL.");
      return;
    }

    setLoading(true);
    setError("");
    setMessage("");

    try {
      const response = await fetch(`${API_BASE}/api/download`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url,
          quality,
          audio_only: format === "audio",
        }),
      });

      if (!response.ok) {
        let detail = "Download failed.";

        try {
          const data = await response.json();
          detail = data.detail || detail;
        } catch {
          // Response was not JSON.
        }

        throw new Error(detail);
      }

      const blob = await response.blob();

      const contentDisposition = response.headers.get(
        "content-disposition"
      );

      let filename = format === "audio"
        ? "videograb-audio.mp3"
        : "videograb-video.mp4";

      if (contentDisposition) {
        const match = contentDisposition.match(
          /filename="?([^"]+)"?/i
        );

        if (match?.[1]) {
          filename = match[1];
        }
      }

      const downloadUrl = window.URL.createObjectURL(blob);
      const anchor = document.createElement("a");

      anchor.href = downloadUrl;
      anchor.download = filename;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();

      window.URL.revokeObjectURL(downloadUrl);

      setMessage("Download sent to your browser.");
    } catch (err) {
      setError(err.message || "Download failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">
            <Download size={21} />
          </div>

          <span>VideoGrab</span>
        </div>

        <a
          href="https://github.com/Ogwusearch/videograb"
          target="_blank"
          rel="noreferrer"
          className="github-link"
        >
          GitHub
        </a>
      </header>

      <main className="main">
        <section className="hero">
          <div className="hero-badge">
            Universal video downloader
          </div>

          <h1>
            Download videos.
            <br />
            <span>Keep them yours.</span>
          </h1>

          <p className="hero-description">
            Paste a video URL, choose your quality, and download it
            directly to your device.
          </p>
        </section>

        <section className="download-card">
          <label className="field-label">
            Video URL
          </label>

          <div className="url-input">
            <Link size={20} />

            <input
              type="url"
              value={url}
              onChange={(event) => {
                setUrl(event.target.value);
                setError("");
                setMessage("");
              }}
              placeholder="https://youtube.com/watch?v=..."
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  handleDownload();
                }
              }}
            />
          </div>

          <div className="options">
            <div className="option">
              <label className="field-label">
                Quality
              </label>

              <select
                value={quality}
                onChange={(event) =>
                  setQuality(event.target.value)
                }
              >
                <option value="best">Best available</option>
                <option value="1080p">1080p</option>
                <option value="720p">720p</option>
                <option value="480p">480p</option>
                <option value="360p">360p</option>
              </select>
            </div>

            <div className="option">
              <label className="field-label">
                Format
              </label>

              <div className="format-buttons">
                <button
                  type="button"
                  className={
                    format === "video"
                      ? "format-button active"
                      : "format-button"
                  }
                  onClick={() => setFormat("video")}
                >
                  <Video size={17} />
                  Video
                </button>

                <button
                  type="button"
                  className={
                    format === "audio"
                      ? "format-button active"
                      : "format-button"
                  }
                  onClick={() => setFormat("audio")}
                >
                  <Music size={17} />
                  MP3
                </button>
              </div>
            </div>
          </div>

          {error && (
            <div className="status error">
              <AlertCircle size={18} />
              {error}
            </div>
          )}

          {message && (
            <div className="status success">
              <CheckCircle size={18} />
              {message}
            </div>
          )}

          <button
            type="button"
            className="download-button"
            onClick={handleDownload}
            disabled={loading}
          >
            {loading ? (
              <>
                <Loader2 className="spin" size={20} />
                Processing...
              </>
            ) : (
              <>
                <Download size={20} />
                Download
              </>
            )}
          </button>

          <p className="storage-note">
            Downloads are delivered to your browser and saved using
            your device's normal download settings.
          </p>
        </section>

        <section className="platforms">
          <span>YouTube</span>
          <span>X</span>
          <span>Instagram</span>
          <span>TikTok</span>
          <span>Facebook</span>
          <span>Vimeo</span>
          <span>Reddit</span>
          <span>+ more</span>
        </section>
      </main>

      <footer>
        <span>VideoGrab</span>
        <span>Open source downloader</span>
      </footer>
    </div>
  );
}

export default App;