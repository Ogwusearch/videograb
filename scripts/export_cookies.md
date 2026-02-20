# How to Export Browser Cookies

Some platforms (Instagram, private X posts, Snapchat) require authentication.

## Method 1 — Browser Extension

1. Install **Get cookies.txt LOCALLY** (Chrome) or **cookies.txt** (Firefox)
2. Log in to the platform
3. Click the extension → Export → Save as `cookies.txt`
4. Run: `videograb <URL> --cookies cookies.txt`

## Method 2 — yt-dlp built-in (no extension needed)

```bash
videograb <URL> --cookies-browser chrome
# Options: chrome, firefox, edge, safari, chromium, brave, opera, vivaldi
```

## Method 3 — Manual export via curl

```bash
# After logging in via browser, inspect network requests and grab Cookie header
# Then create cookies.txt in Netscape format
```
