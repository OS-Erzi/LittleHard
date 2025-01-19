from discord import Intents, CustomActivity

from .base import ProjectType
from core import settings

def start_loader():
    intents = Intents.all()
    activity = CustomActivity(name=settings.bot.BOT_DESCRIPTION)
    bot = ProjectType(intents=intents, activity=activity, command_prefix="!")
    bot.run(settings.bot.TEST_TOKEN)