from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import BaseModel, Field
from os import getenv

from typing import List, Dict, Tuple
from random import randint

class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

class BotSettings(EnvBaseSettings):
    TOKEN: str
    LOAD_TITLE: str
    BOT_DESCRIPTION: str

class ChannelsId(EnvBaseSettings):
    CATEGORY_FOR_INVITE_CHANNEL: int

class Settings(BaseModel):
    bot: BotSettings = Field(default_factory=BotSettings)
    channelsid: ChannelsId = Field(default_factory=ChannelsId)

def get_settings() -> Settings:
    return Settings()