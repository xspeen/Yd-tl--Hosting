🎥 YT-DLP UNLIMITED DOWNLOADER API

Self-Hosted yt-dlp Backend with No Rate Limits

<p align="center">
  <img src="https://iili.io/q5iESa9.jpg" alt="yt-dlp API Logo" width="900"/>
</p>

<p align="center">
  <a href="https://github.com/xspeen/Yd-tl--Hosting">
    <img src="https://img.shields.io/badge/GitHub-xspeen%2FYd--tl--Hosting-181717?style=for-the-badge&logo=github&logoColor=white"/>
  </a>
  <a href="https://yd-tl-hosting.onrender.com">
    <img src="https://img.shields.io/badge/Live%20API-yd--tl--hosting.onrender.com-46E3B7?style=for-the-badge&logo=render&logoColor=white"/>
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-3.0-royalblue?style=flat-square&logo=github"/>
  <img src="https://img.shields.io/badge/License-MIT-emerald?style=flat-square&logo=opensourceinitiative"/>
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/yt--dlp-FF0000?style=flat-square&logo=youtube&logoColor=white"/>
  <img src="https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=black"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-ONLINE-success?style=flat-square"/>
  <img src="https://img.shields.io/badge/Total%20Downloads-1+-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Data%20Served-1.38MB+-orange?style=flat-square"/>
  <img src="https://img.shields.io/badge/Supported%20Sites-1000%2B-brightgreen?style=flat-square"/>
</p>

---

📋 PROJECT OVERVIEW

YT-DLP UNLIMITED DOWNLOADER is a production-ready FastAPI backend that provides a REST API for yt-dlp. Deployed on Render with zero rate limits and unlimited downloads.

Repository

```
🔗 https://github.com/xspeen/Yd-tl--Hosting
```

Live API Endpoint

```
🌐 https://yd-tl-hosting.onrender.com
```

Current Status

```json
{
  "status": "online",
  "service": "yt-dlp Unlimited Downloader",
  "version": "3.0",
  "supported_platforms": "1000+",
  "limits": "UNLIMITED - No rate limits, no restrictions",
  "stats": {
    "total_downloads": 1,
    "total_bytes": 1382558,
    "start_time": "2026-03-11T19:31:39.648439"
  },
  "active_downloads": 1,
  "endpoints": {
    "/": "This info",
    "/health": "Health check",
    "/info": "GET - Get video information",
    "/formats": "GET - List available formats",
    "/download": "POST - Download video",
    "/stream/{task_id}": "GET - Stream download progress",
    "/cancel/{task_id}": "POST - Cancel download",
    "/stats": "GET - Download statistics"
  }
}
```

---

🚀 QUICK START

Test the API

```bash
curl https://yd-tl-hosting.onrender.com/health
```

Get Video Info

```bash
curl "https://yd-tl-hosting.onrender.com/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Download Video

```bash
curl -X POST "https://yd-tl-hosting.onrender.com/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --output video.mp4
```

Download Audio Only

```bash
curl -X POST "https://yd-tl-hosting.onrender.com/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&audio_only=true" \
  --output audio.mp3
```

---

📦 INSTALLATION & DEPLOYMENT

Clone Repository

```bash
git clone https://github.com/xspeen/Yd-tl--Hosting.git
cd Yd-tl--Hosting
```

Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py
# Server will start at http://localhost:8000
```

Docker Deployment

```bash
docker build -t yt-dlp-api .
docker run -d -p 8000:8000 yt-dlp-api
```

Deploy to Render

https://render.com/images/deploy-to-render-button.svg

---

🔧 CROSS-PLATFORM USAGE

Termux 📱

```bash
pkg update && pkg upgrade -y
pkg install curl -y

# Download video
curl -X POST "https://yd-tl-hosting.onrender.com/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --output video.mp4

# Download audio
curl -X POST "https://yd-tl-hosting.onrender.com/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&audio_only=true" \
  --output audio.mp3
```

Kali Linux / Ubuntu / Debian 🐧

```bash
sudo apt update && sudo apt install curl jq -y

# Get formatted JSON info
curl -s "https://yd-tl-hosting.onrender.com/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" | jq .

# Download with specific quality
curl -X POST "https://yd-tl-hosting.onrender.com/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&format_id=137" \
  --output video.mp4
```

Windows PowerShell 🪟

```powershell
# Download video
curl.exe -X POST "https://yd-tl-hosting.onrender.com/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o video.mp4

# Download audio
curl.exe -X POST "https://yd-tl-hosting.onrender.com/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&audio_only=true" -o audio.mp3

# Get video info
curl.exe -s "https://yd-tl-hosting.onrender.com/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" | ConvertFrom-Json
```

macOS 🍎

```bash
brew install curl jq

curl -s "https://yd-tl-hosting.onrender.com/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" | jq .

curl -X POST "https://yd-tl-hosting.onrender.com/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --output video.mp4
```

Arch Linux 🏹

```bash
sudo pacman -S curl jq

curl -X POST "https://yd-tl-hosting.onrender.com/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --output video.mp4
```

Parrot OS 🦜

```bash
sudo apt update && sudo apt install curl jq -y

curl -X POST "https://yd-tl-hosting.onrender.com/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --output video.mp4
```

---

🐍 PYTHON USAGE

```python
import requests

BASE_URL = "https://yd-tl-hosting.onrender.com"

def get_video_info(url):
    """Get video metadata"""
    response = requests.get(f"{BASE_URL}/info", params={"url": url})
    return response.json()

def download_video(url, output="video.mp4", audio_only=False):
    """Download video or audio"""
    params = {"url": url}
    if audio_only:
        params["audio_only"] = "true"
    
    response = requests.post(f"{BASE_URL}/download", params=params, stream=True)
    
    with open(output, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"✅ Downloaded: {output} ({len(response.content) / 1024 / 1024:.2f} MB)")

# Example
info = get_video_info("https://youtu.be/dQw4w9WgXcQ")
print(f"📹 Title: {info['title']}")
print(f"⏱️ Duration: {info['duration']} seconds")
print(f"👤 Uploader: {info['uploader']}")

download_video("https://youtu.be/dQw4w9WgXcQ", "video.mp4")
download_video("https://youtu.be/dQw4w9WgXcQ", "audio.mp3", audio_only=True)
```

---

📊 SUPPORTED PLATFORMS

<p align="center">
  <img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"/>
  <img src="https://img.shields.io/badge/TikTok-000000?style=for-the-badge&logo=tiktok&logoColor=white"/>
  <img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white"/>
  <img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white"/>
  <img src="https://img.shields.io/badge/Twitter-1D9BF0?style=for-the-badge&logo=twitter&logoColor=white"/>
  <img src="https://img.shields.io/badge/Vimeo-1AB7EA?style=for-the-badge&logo=vimeo&logoColor=white"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Reddit-FF4500?style=for-the-badge&logo=reddit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pinterest-BD081C?style=for-the-badge&logo=pinterest&logoColor=white"/>
  <img src="https://img.shields.io/badge/Dailymotion-0A0A0A?style=for-the-badge&logo=dailymotion&logoColor=white"/>
  <img src="https://img.shields.io/badge/Twitch-9146FF?style=for-the-badge&logo=twitch&logoColor=white"/>
  <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/>
</p>

➕ And 1000+ more websites! Powered by yt-dlp

---

📁 REPOSITORY STRUCTURE

```
📦 Yd-tl--Hosting
├── 📄 main.py                 # FastAPI application
├── 📄 requirements.txt        # Python dependencies
├── 📄 Dockerfile              # Docker configuration
├── 📄 render.yaml             # Render deployment config
├── 📄 .gitignore              # Git ignore rules
└── 📄 README.md               # This documentation
```

---

🔧 CONFIGURATION

Environment Variables

Variable Description Default
PORT Server port 8000

Render Deployment

```yaml
# render.yaml
services:
  - type: web
    name: yt-dlp-api
    runtime: docker
    plan: free
    dockerfilePath: ./Dockerfile
```

---

⏱️ PERFORMANCE NOTES

· First request: 30-50 seconds (Render cold start)
· Subsequent requests: 2-5 seconds
· Keep alive: Use cron-job.org to ping /health every 15 minutes

---

📊 LIVE STATISTICS

```bash
curl https://yd-tl-hosting.onrender.com/stats
```

```json
{
  "stats": {
    "total_downloads": 1,
    "total_bytes": 1382558,
    "start_time": "2026-03-11T19:31:39.648439"
  },
  "active_downloads": 1
}
```

---

🤝 CONTRIBUTING

1. 🍴 Fork the repository
2. 🌿 Create feature branch (git checkout -b feature/amazing)
3. 💾 Commit changes (git commit -m 'Add amazing feature')
4. 📤 Push to branch (git push origin feature/amazing)
5. ✅ Open a Pull Request

---

📜 LICENSE

```
MIT License

Copyright (c) 2026 XSPEEN

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

📞 SUPPORT & CONTACT

<p align="center">
  <a href="https://github.com/xspeen/Yd-tl--Hosting">
    <img src="https://img.shields.io/badge/Repository-GitHub-181717?style=for-the-badge&logo=github"/>
  </a>
  <a href="https://github.com/xspeen/Yd-tl--Hosting/issues">
    <img src="https://img.shields.io/badge/Report%20Issue-GitHub-red?style=for-the-badge&logo=github"/>
  </a>
  <a href="https://t.me/xspeen_chatter">
    <img src="https://img.shields.io/badge/Contact-Telegram-26A5E4?style=for-the-badge&logo=telegram"/>
  </a>
</p>

<p align="center">
  <img src="https://yd-tl-hosting.onrender.com/stats" width="0" height="0"/>
</p>

---

<p align="center">
  <img src="https://iili.io/q5iESa9.jpg" width="100"/>
  <br/>
  <strong>⚡ Created by XSPEEN</strong>
  <br/>
  <a href="https://github.com/xspeen">github.com/xspeen</a>
  <br/><br/>
  <sub>📦 Repository: <a href="https://github.com/xspeen/Yd-tl--Hosting">github.com/xspeen/Yd-tl--Hosting</a></sub>
  <br/>
  <sub>🌐 Live API: <a href="https://yd-tl-hosting.onrender.com">yd-tl-hosting.onrender.com</a></sub>
  <br/><br/>
  <sub>© 2026 YT-DLP Unlimited Downloader. All rights reserved.</sub>
</p>
