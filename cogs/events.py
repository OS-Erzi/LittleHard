from discord import (
    ApplicationContext, 
    DiscordException,
    HTTPException,
    Forbidden,
    NotFound,
    Embed, 
    Color
)

from discord.ext import commands

from core import ProjectType

from structs.button import InviteButton, QuestionsButton

class Events(commands.Cog):
    def __init__(self, client: ProjectType):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.client.add_view(InviteButton())
        self.client.add_view(QuestionsButton())

    @commands.Cog.listener()
    async def on_application_command_error(self, context: ApplicationContext, error: DiscordException):
        match error:
            case Forbidden():
                embed = Embed(
                    color=Color.red(),
                    title="Ошибка доступа",
                    description="У бота недостаточно прав для выполнения этого действия."
                )
            case NotFound():
                embed = Embed(
                    color=Color.red(),
                    title="Объект не найден",
                    description="Запрошенный ресурс не найден. Проверьте правильность введенных данных."
                )
            case HTTPException():
                embed = Embed(
                    color=Color.red(),
                    title="Ошибка HTTP",
                    description="Произошла ошибка при отправке запроса к Discord API."
                )
            case commands.CommandOnCooldown():
                embed = Embed(
                    color=Color.orange(),
                    title="Команда на перезарядке",
                    description=f"Пожалуйста, подождите {error.retry_after:.2f} секунд перед повторным использованием."
                )
            case commands.MissingPermissions():
                embed = Embed(
                    color=Color.red(),
                    title="Недостаточно прав",
                    description="У вас недостаточно прав для выполнения этой команды."
                )
            case commands.MissingRequiredArgument():
                embed = Embed(
                    color=Color.yellow(),
                    title="Отсутствует обязательный аргумент",
                    description=f"Пропущен обязательный аргумент: {error.param.name}"
                )
            case _:
                embed = Embed(
                    color=Color.red(),
                    title="Неизвестная ошибка",
                    description=f"Произошла непредвиденная ошибка: {str(error)}"
                )

        await context.respond(embed=embed, ephemeral=True)


def setup(client):
    client.add_cog(Events(client))