# ⚡ ClipCraft

Turn long videos and live streams into viral, captioned vertical clips (9:16) ready for YouTube Shorts, Instagram Reels, and TikTok. **100% Free and Open Source** — run it locally on your own machine with ₹0 subscription fees.

Paste a YouTube, Twitch, or Kick link (or upload an MP4/MOV) and **ClipCraft** automatically transcribes speech, scouts the highest-retention hooks with AI, auto-reframes to vertical 9:16, burns word-by-word animated subtitles, and schedules/posts them to your social accounts.

---

## ✨ Features

- **⚡ Instant AI Moment Scouting**: Transcribes audio with Whisper and uses fast reasoning models (Groq 120B, Ollama, Gemini, or OpenAI) to pinpoint high-retention hooks and punchlines.
- **📱 9:16 Vertical Reframing**: Auto-centers speakers with customizable layout modes (Full frame + blurred fill, Zoomed fill, or Center crop).
- **🎨 Dynamic Animated Captions**: Word-by-word highlighted captions with viral typography presets:
  - `Bounce`: Energetic pop-in word animation.
  - `Hype`: Bold, high-contrast karaoke style.
  - `Clean`: Minimalist sleek text.
- **🔴 Livestream Recording & Clipping**: Connect to live YouTube, Twitch, or Kick streams to automatically buffer and extract viral highlights in real-time.
- **🚀 Multi-Creator Workspaces & Social Hub**: Organize clips across multiple YouTube channels, Instagram accounts, and TikTok pages with automated posting queues and daily rate limits.
- **💻 100% Local-First & Privacy Preserving**: Video rendering (FFmpeg) and speech transcription run directly on your own computer. Your videos are never uploaded to third-party SaaS servers.

---

## 🚀 Quick Start (Run Locally in 3 Minutes)

### 1. Requirements
- **Python 3.10+**
- **FFmpeg**:
  - *Windows*: `winget install Gyan.FFmpeg`
  - *Mac*: `brew install ffmpeg`
  - *Linux*: `sudo apt install ffmpeg`

### 2. Clone & Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ClipCraft.git
cd ClipCraft

# Create and activate virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Mac / Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch ClipCraft Studio
```bash
python -m studio.server
```
Open **`http://localhost:8765`** in your browser!

### 4. Connect Your Free AI Key (Optional but Recommended)
In the ClipCraft dashboard:
1. Navigate to **Settings → AI**.
2. Select **Groq** (or Gemini / Ollama).
3. Paste a free key from [console.groq.com/keys](https://console.groq.com/keys) (₹0 cost).
4. Select `openai/gpt-oss-120b` or click **Save and test**.

---

## 🛠️ Tech Stack
- **Backend**: FastAPI, Uvicorn, SQLite, SQLAlchemy.
- **Video & Audio Processing**: FFmpeg, Whisper (sherpa-onnx / faster-whisper), Pillow.
- **Downloader**: yt-dlp.
- **Frontend**: Lightweight, zero-build reactive Web Studio with Obsidian Dark UI.

---

## 📄 License
Released under the permissive [MIT License](LICENSE). Free for personal and commercial use.
