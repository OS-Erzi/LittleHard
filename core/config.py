from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import BaseModel, Field, HttpUrl


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

class BotSettings(EnvBaseSettings):
    TOKEN: str
    LOAD_TITLE: str
    BOT_DESCRIPTION: str

class ChannelsId(EnvBaseSettings):
    CATEGORY_FOR_INVITE_CHANNEL: int
    CATEGORY_FOR_MEDIA_CHANNEL: int

class ImagesCfg(EnvBaseSettings):
    INVISIBLE_URL: HttpUrl

class Settings(BaseModel):
    bot: BotSettings = Field(default_factory=BotSettings)
    channelsid: ChannelsId = Field(default_factory=ChannelsId)

    images: ImagesCfg = Field(default_factory=ImagesCfg)

def get_settings() -> Settings:
    return Settings()