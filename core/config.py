from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, field_validator
from typing import List

class Settings(BaseSettings):

    BOT_TOKEN: SecretStr
    BOT_USERNAME: str
    
    # А list of channels to which the user must subscribe
    CHANNEL_ID_1: str
    CHANNEL_ID_2: str

    @property
    def channels(self) -> List[str]:
        return [self.CHANNEL_ID_1, self.CHANNEL_ID_2]
    
    # Path to the folder for temporary files

    DOWNLOADS_DIR: str = "downloads"

    CAPTION_TEMPLATE: str = "[Скачать любую песню или видео🎧](https://t.me/{username})"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

config = Settings()