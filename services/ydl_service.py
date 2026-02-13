import asyncio
import os
import uuid
from typing import Optional
from yt_dlp import YoutubeDL
from core.config import config
import logging

logger = logging.getLogger(__name__)

class YDLService:
    def __init__(self):
        # Basic settings for all services
        self.base_opts = {
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'restrictfilenames': True,
            'max_filesize': 200 * 1024 * 1024,  # limit 200MB
            'verbose': True, # Add verbose logging for yt-dlp
        }

    async def download_video(self, url: str, extra_opts: dict = None) -> Optional[str]:
        """
        A universal download method.
        Returns the file path or None if an error occurs..
        """
        # Use video title as file name. yt-dlp's restrictfilenames option will sanitize it.
        file_path_template = os.path.join(config.DOWNLOADS_DIR, "%(title)s.%(ext)s")
        
        ydl_opts = self.base_opts.copy()
        ydl_opts['outtmpl'] = file_path_template
        if extra_opts:
            ydl_opts.update(extra_opts)

        # We run synchronous yt-dlp in a separate thread to avoid hanging the bot.
        try:
            return await asyncio.to_thread(self._sync_download, url, ydl_opts)
        except Exception as e:
            logger.error(f"Ошибка скачивания: {e}", exc_info=True)
            return None

    def _sync_download(self, url: str, opts: dict) -> str:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # yt-dlp 2023.01.06 and later will return info['filepath']
            # which is the path to the final processed file.
            return info.get('filepath') or ydl.prepare_filename(info)

# Create one instance of the service for use in the bot
ydl_service = YDLService()