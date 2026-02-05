# 📥 Multi-Platform Video Downloader Bot
### A powerful, asynchronous Telegram bot designed to download video and audio content from various social media platforms. Built with a focus on speed, modularity, and ease of use.

## ✨ Features
**YouTube:** Download videos (up to 720p) or convert them directly to MP3 audio.

**TikTok:** High-quality video downloads without watermarks.

**Instagram:** Save Reels and Feed videos instantly.

**Pinterest:** Download video content from pins.

**Subscription Middleware:** Restrict access to the bot until the user joins your specified Telegram channels.

**Robust Logging:** Clean logs with terminal output for real-time monitoring and file-based logging for errors.

## 🛠 Tech Stack
**Language:** Python 3.10+ (Tested on 3.14)

**Framework:** Aiogram 3.x

**Core Engine:** yt-dlp

**Media Processing:** FFmpeg

**Configuration:** Pydantic-settings (Environment-based)

## 🚀 Installation & Setup
**1. Prerequisites (Arch Linux Example)**
Ensure FFmpeg is installed on your system for media merging and audio conversion:
```Bash
sudo pacman -S ffmpeg
```
**2. Clone and Install**
```
git clone https://github.com/yourusername/savegram-bot.git
cd savegram-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**3. Environment Configuration**
Create a `.env` file in the root directory:


```
BOT_TOKEN=your_telegram_bot_token
BOT_USERNAME=@YourBotUsername
CHANNEL_ID_1=-100123456789
CHANNEL_ID_2=@your_public_channel
DOWNLOADS_DIR=downloads
```
**4. Running the Bot**

```python
python main.py
```
## 📁 Project Structure

```Plaintext
├── core/               # Configuration and Logger initialization
├── handlers/           # Platform-specific logic (YouTube, TikTok, etc.)
├── middlewares/        # Subscription check logic
├── services/           # Global YDLService for media handling
├── logs/               # Log files (errors.log)
├── downloads/          # Temporary storage (auto-cleaned)
└── main.py             # Application entry point
```
## 🛡 License
Distributed under the **MIT License.** See LICENSE for more information.

## 🤝 Support
If you encounter any issues or have feature requests, please open an Issue or contact the maintainer.

## Created with ❤️ for the open-source community.