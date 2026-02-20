"""
Command-line interface entry point.
"""

import sys
import argparse
from pathlib import Path

from videograb.downloader import VideoDownloader
from videograb.detector   import detect_platform, is_valid_url
from videograb.display    import (
    print_banner, cprint, print_info,
    make_progress_hook, print_batch_summary,
)
from videograb.config     import DEFAULT_OUTPUT_DIR, QUALITY_PRESETS
from videograb            import __version__

try:
    from rich.prompt  import Prompt, Confirm
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


# ── Interactive mode ─────────────────────────────────────────

def interactive_mode():
    print_banner()
    cprint("\n[dim]Press Ctrl+C at any time to exit.[/dim]\n")

    def ask(prompt, default=None, choices=None):
        if HAS_RICH:
            return Prompt.ask(prompt, default=default, choices=choices)
        suffix = f" [{default}]" if default else ""
        return input(f"{prompt}{suffix}: ").strip() or default

    def confirm(prompt, default=False):
        if HAS_RICH:
            return Confirm.ask(prompt, default=default)
        ans = input(f"{prompt} [y/N]: ").strip().lower()
        return ans in ("y", "yes")

    output_dir    = ask("📁 Output directory", default=str(DEFAULT_OUTPUT_DIR))
    quality       = ask("🎞  Quality", default="best",
                        choices=list(QUALITY_PRESETS.keys()))
    audio_only    = confirm("🔊 Audio only (MP3)?", default=False)
    use_cookies   = confirm("🍪 Use cookies file?", default=False)
    cookies_file  = ask("   Path to cookies.txt") if use_cookies else None
    use_proxy     = confirm("🌐 Use proxy?", default=False)
    proxy         = ask("   Proxy URL (e.g. socks5://127.0.0.1:1080)") if use_proxy else None

    dl = VideoDownloader(
        output_dir=output_dir,
        quality=quality,
        audio_only=audio_only,
        cookies_file=cookies_file,
        proxy=proxy,
        on_progress=make_progress_hook(),
    )

    while True:
        try:
            url = ask("\n🔗 Enter URL (or 'quit')")
        except (KeyboardInterrupt, EOFError):
            cprint("\n\n👋 Goodbye!")
            break

        if not url or url.lower() in ("quit", "exit", "q"):
            cprint("\n👋 Goodbye!")
            break

        if not is_valid_url(url):
            cprint("[yellow]⚠  Please enter a valid URL starting with http:// or https://[/yellow]")
            continue

        platform = detect_platform(url)
        cprint(f"🔍 Platform: [bold cyan]{platform}[/bold cyan]")
        dl.download(url)


# ── Argument parser ──────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="videograb",
        description="🎬 VideoGrab — Download videos from YouTube, X, Instagram, Snapchat & more.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  videograb https://youtu.be/dQw4w9WgXcQ
  videograb https://x.com/user/status/123 -q 720p
  videograb https://www.instagram.com/reel/xxx/ --cookies cookies.txt
  videograb --batch urls.txt -o ~/Videos/
  videograb URL --info
  videograb --interactive
        """,
    )
    parser.add_argument("url",          nargs="?",  help="Video URL")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-o", "--output", default=str(DEFAULT_OUTPUT_DIR), metavar="DIR",
                        help="Output directory")
    parser.add_argument("-q", "--quality", choices=list(QUALITY_PRESETS.keys()),
                        default="best", help="Video quality preset")
    parser.add_argument("--audio",        action="store_true", help="Extract audio as MP3")
    parser.add_argument("--cookies",      metavar="FILE",      help="Cookies file (Netscape format)")
    parser.add_argument("--cookies-browser", metavar="BROWSER",
                        help="Pull cookies from browser: chrome, firefox, edge, safari")
    parser.add_argument("--proxy",        metavar="URL",       help="Proxy URL")
    parser.add_argument("--subtitles",    action="store_true", help="Download subtitles")
    parser.add_argument("--batch",        metavar="FILE",      help="File with one URL per line")
    parser.add_argument("--info",         action="store_true", help="Show info without downloading")
    parser.add_argument("-v", "--verbose",action="store_true", help="Verbose yt-dlp output")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode")
    return parser


# ── Main entry ───────────────────────────────────────────────

def main():
    parser = build_parser()
    args   = parser.parse_args()

    if args.interactive or (not args.url and not args.batch):
        interactive_mode()
        return

    print_banner()

    dl = VideoDownloader(
        output_dir      = args.output,
        quality         = args.quality,
        audio_only      = args.audio,
        cookies_file    = args.cookies,
        cookies_browser = args.cookies_browser,
        proxy           = args.proxy,
        subtitles       = args.subtitles,
        verbose         = args.verbose,
        on_progress     = make_progress_hook(),
    )

    if args.batch:
        batch_file = Path(args.batch)
        if not batch_file.exists():
            cprint(f"[bold red]❌ Batch file not found:[/bold red] {args.batch}")
            sys.exit(1)
        urls    = batch_file.read_text(encoding="utf-8").splitlines()
        results = dl.batch_download(urls)
        print_batch_summary(results)

    elif args.url:
        if not is_valid_url(args.url):
            cprint("[bold red]❌ Invalid URL. Must start with http:// or https://[/bold red]")
            sys.exit(1)

        platform = detect_platform(args.url)
        cprint(f"🔍 Platform: [bold cyan]{platform}[/bold cyan]")

        if args.info:
            info = dl.get_info(args.url)
            print_info(info)
        else:
            success = dl.download(args.url)
            sys.exit(0 if success else 1)
