import asyncio
import os
import uuid
from typing import Optional
from yt_dlp import YoutubeDL
from core.config import config

class YDLService:
    def __init__(self):
        # Basic settings for all services
        self.base_opts = {
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'restrictfilenames': True,
            'max_filesize': 50 * 1024 * 1024,  # limit 50MB
        }

    async def download_video(self, url: str, extra_opts: dict = None) -> Optional[str]:
        """
        A universal download method.
        Returns the file path or None if an error occurs..
        """
        # Create a unique file name to avoid conflicts
        file_id = str(uuid.uuid4())
        file_path = os.path.join(config.DOWNLOADS_DIR, f"{file_id}.%(ext)s")

        # We combine basic settings with custom ones (for a specific social network)
        ydl_opts = self.base_opts.copy()
        ydl_opts['outtmpl'] = file_path
        if extra_opts:
            ydl_opts.update(extra_opts)

        # We run synchronous yt-dlp in a separate thread to avoid hanging the bot.
        try:
            return await asyncio.to_thread(self._sync_download, url, ydl_opts)
        except Exception as e:
            print(f"Ошибка скачивания: {e}")
            return None

    def _sync_download(self, url: str, opts: dict) -> str:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)

# Create one instance of the service for use in the bot
ydl_service = YDLService()