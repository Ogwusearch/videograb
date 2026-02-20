"""
Rich-powered terminal UI helpers.
Falls back gracefully if rich is not installed.
"""

import re
import sys

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import (
        Progress, SpinnerColumn, BarColumn,
        TextColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn,
    )
    from rich.prompt import Prompt, Confirm
    from rich import print as rprint
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

console = Console() if HAS_RICH else None


# ── Banner ───────────────────────────────────────────────────

def print_banner():
    if HAS_RICH:
        console.print(Panel.fit(
            "[bold cyan]🎬 VideoGrab[/bold cyan]  —  Universal Video Downloader\n"
            "[dim]YouTube • X/Twitter • Instagram • Snapchat • Any Website[/dim]",
            border_style="cyan",
        ))
    else:
        print("=" * 57)
        print("  🎬  VideoGrab — Universal Video Downloader")
        print("  YouTube | X/Twitter | Instagram | Snapchat | Websites")
        print("=" * 57)


# ── Generic print ────────────────────────────────────────────

def cprint(msg: str):
    if HAS_RICH:
        console.print(msg)
    else:
        print(re.sub(r"\[.*?\]", "", msg))


# ── Info table ───────────────────────────────────────────────

def print_info(info: dict):
    if "error" in info:
        cprint(f"[bold red]❌ {info['error']}[/bold red]")
        return

    if HAS_RICH:
        t = Table(show_header=False, box=None, padding=(0, 1))
        t.add_column(style="dim cyan")
        t.add_column()
        rows = [
            ("📺 Title",    info.get("title", "N/A")),
            ("👤 Uploader", info.get("uploader", "N/A")),
            ("⏱  Duration", info.get("duration_string", "N/A")),
            ("📅 Date",     info.get("upload_date", "N/A")),
            ("👁  Views",   f"{info.get('view_count', 0):,}" if info.get("view_count") else "N/A"),
            ("🎞  Formats", str(len(info.get("formats", [])))),
            ("🔗 URL",      info.get("webpage_url", "N/A")),
        ]
        for k, v in rows:
            t.add_row(k, str(v))
        console.print(t)
    else:
        for key, val in [
            ("Title", info.get("title")), ("Uploader", info.get("uploader")),
            ("Duration", info.get("duration_string")), ("Date", info.get("upload_date")),
        ]:
            print(f"  {key}: {val}")


# ── Progress hook for yt-dlp ─────────────────────────────────

def make_progress_hook(task_name: str = "Downloading"):
    """Returns a yt-dlp progress hook that renders a Rich progress bar."""
    _progress = None
    _task     = None

    def hook(d: dict):
        nonlocal _progress, _task

        if d["status"] == "downloading" and HAS_RICH:
            if _progress is None:
                _progress = Progress(
                    SpinnerColumn(),
                    TextColumn("[bold cyan]{task.description}"),
                    BarColumn(),
                    DownloadColumn(),
                    TransferSpeedColumn(),
                    TimeRemainingColumn(),
                    transient=True,
                )
                _progress.start()
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                _task = _progress.add_task(task_name, total=total)

            downloaded = d.get("downloaded_bytes", 0)
            total      = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            _progress.update(_task, completed=downloaded, total=total)

        elif d["status"] == "finished":
            if _progress:
                _progress.stop()
                _progress = None
            fname = d.get("filename", "")
            cprint(f"✅ Saved: [bold green]{fname}[/bold green]")

        elif d["status"] == "error":
            if _progress:
                _progress.stop()
                _progress = None
            cprint("[bold red]❌ Error during download[/bold red]")

    return hook


# ── Batch results summary ────────────────────────────────────

def print_batch_summary(results: dict):
    ok_count   = len(results["success"])
    fail_count = len(results["failed"])
    cprint(f"\n[bold]Results:[/bold] ✅ {ok_count} succeeded  ❌ {fail_count} failed")
    if results["failed"]:
        cprint("[bold red]Failed URLs:[/bold red]")
        for u in results["failed"]:
            cprint(f"  • {u}")
