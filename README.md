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

---

## ⚙️ Configuration & Upstream Features
If you prefer a file (or run a server), the same settings can go in `.env`:

```ini
PEAKCUT_AI_PROVIDER=groq
PEAKCUT_AI_MODELS=openai/gpt-oss-120b
PEAKCUT_AI_KEY=your-key-here
```

| `PEAKCUT_AI_PROVIDER` | Service | Where to get a key |
|---|---|---|
| `groq` | Groq (Recommended, ₹0) | https://console.groq.com/keys |
| `gemini` | Google Gemini | https://aistudio.google.com/apikey |
| `openai` | OpenAI | https://platform.openai.com/api-keys |
| `xai` | Grok (xAI) | https://console.x.ai |
| `openrouter` | OpenRouter | https://openrouter.ai/keys |
| `anthropic` | Claude | https://console.anthropic.com |
| `ollama` | Local Ollama | https://ollama.com |
| `custom` | OpenAI-compatible endpoint | |

### Videos in Arabic & Multilingual
Speech models can be managed directly in **Settings → Speech models**. Supports Arabic, English, and multilingual Hinglish.

## Settings

Everything is set through environment variables, normally in a `.env` file next to this README.
[`.env.example`](.env.example) lists every setting with a short explanation. The ones that matter first:

| Setting | What it is for |
|---|---|
| `PEAKCUT_AI_PROVIDER`, `PEAKCUT_AI_MODELS`, `PEAKCUT_AI_KEY` | The AI that picks clips and writes titles (or set it in the dashboard) |
| `PEAKCUT_ACCOUNTS` | `1` makes everyone sign in. Use it on any server other people can reach |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | Optional: Sign in with Google, and connecting YouTube |
| `PEAKCUT_SMTP_*`, `PEAKCUT_MAIL_FROM` | Optional: confirmation and password emails |
| `PEAKCUT_DATA` | Where videos, clips and the database are kept (default `./data`) |

`.env`, the `secrets/` folder and all user data are ignored by git. Keep keys there, never in the code.

## Admins

This only matters with accounts switched on (`PEAKCUT_ACCOUNTS=1`); without them you are the owner and can do
everything. An account is an admin only when the database says so. No email address is special in the code and no web request
can change a role. Do it on the machine that runs PeakCut:

```bash
python -m studio.admin grant you@example.com
```

`revoke` and `list` work the same way. The admin dashboard is at `/admin` and answers "not found" to everyone else.

## How it is built

| Part | What it is |
|---|---|
| `studio/` | The server: FastAPI, the clip pipeline, live recording, accounts |
| `studio/ai.py` | The only file that talks to an AI service. Add a provider here |
| `web/` | The pages: landing, sign-in, the app, the admin dashboard (plain HTML, CSS and JavaScript, no build step) |
| `tests/` | Tests that run against a throwaway copy of the app |
| `deploy/`, `Dockerfile`, `docker-compose.yml` | One-server deployment with PostgreSQL and automatic HTTPS |

Video work is done with `ffmpeg` and `yt-dlp`. Speech is transcribed with `sherpa-onnx` and NVIDIA's Parakeet
model (English) and FastConformer Arabic model, both released by NVIDIA under the Creative Commons Attribution 4.0
licence (CC-BY-4.0). The Arabic model was converted for sherpa-onnx with `tools/export_arabic_model.py`.
Data is kept per user: accounts in the database (SQLite on your own computer, PostgreSQL on a server), videos and
clips in each user's own folder. [AGENTS.md](AGENTS.md) is a short map of the code for contributors and AI coding
assistants.

## Where your videos and clips are kept

Everything PeakCut keeps is in one folder: videos, clips, recordings, creators, settings and the speech model. By
default it is the `data` folder inside PeakCut. **Settings, Storage** shows the folder and how much room its drive
has, opens it in one click, and lets you move it to another drive: choose the new folder, and PeakCut moves
everything there the next time it starts. If the drive is nearly full, PeakCut says so and stops taking new videos
until there is room. (`PEAKCUT_DATA` in `.env` still works and takes priority.)

## Updating

PeakCut checks GitHub once a minute while it runs. When a newer version is out, the dashboard shows a notice
within a minute or two (no restart needed), with what changed
and how to update: ask your AI coding assistant to do it (the notice has a sentence to paste), or run
`git pull && pip install -r requirements.txt` in the PeakCut folder and restart it (with Docker:
`git pull && docker compose up -d --build`). Your `.env`, keys and clips are not touched. Only the two commit ids
are sent to GitHub; set `PEAKCUT_UPDATE_CHECK=0` to turn the check off.

## Deploy

[DEPLOY.md](DEPLOY.md) walks through a single server with Docker: the app, PostgreSQL, and Caddy for HTTPS.

```bash
docker compose up -d --build
```

## How it behaves under load

- The page asks the server one small question every few seconds. When nothing has changed, the answer comes
  straight from memory.
- Each person's videos wait in their own line and the lines take turns, so one person cannot hold everyone up.
- The server measures its own processor, memory and disk every second. Extra videos and recordings start only
  while there is room, wait briefly when it is nearly full, and continue the moment it frees up.
- There are no limits on upload size, video length, recordings, creators or storage unless you set them in
  `.env`. Five videos can be sent at once. Request sizes are always capped, so junk can't fill the memory.

## Tests

```bash
python tests/run.py
```

This starts a copy of the app on a spare port with an empty temporary data folder, runs the permission, abuse and
queue tests against it, then removes it. It needs no keys and never touches real data.

## Security

- With sign-in off, PeakCut listens on this computer only (`127.0.0.1`), refuses changes sent by other websites,
  and only answers to its own address. Do not expose it to the internet that way: turn accounts on.
- Passwords are stored only as salted scrypt hashes. Sessions are random tokens stored hashed; cookies are HTTP-only.
- Every route works out who is asking from the session, never from the request, so users only reach their own data.
- Only known video sites are fetched, and text from videos is treated as data when it is shown to the AI.
- Found a problem? Please report it privately through the repository's security advisories instead of opening a
  public issue.

## Using it responsibly

Clip videos you made, or have permission to use. You are responsible for the rights to what you download, clip and
post, and for following the terms of the sites you fetch from and post to.

## Licence

[MIT](LICENSE). Caption fonts in `studio/fonts/` (Anton, Archivo Black, Poppins) are under the SIL Open Font
License; the licence texts are in the same folder.
