from discord import Embed, Color, ApplicationContext, Option, ChannelType, abc
from discord.ext import commands

from structs.button import InviteButton, QuestionsButton

from core import ProjectType, settings

class ButtonAction(commands.Cog):
    def __init__(self, client: ProjectType):
        self.client = client

    @commands.slash_command(name="заявки", description="Установить канал для принятия заявок на сервер")
    @commands.has_guild_permissions(administrator=True)
    async def set_channel_for_invites(
        self, 
        ctx: ApplicationContext,
        channel: Option(abc.GuildChannel, name="канал", description="Текстовый канал или ветка форума", 
                        channel_types=[ChannelType.text, ChannelType.public_thread, ChannelType.private_thread, ChannelType.news, ChannelType.news_thread],
                        required=True) #type: ignore
        ):
        await ctx.response.defer(ephemeral=True)
        embed = Embed(
            color=0xff5858, 
            title="Подать заявку Hard Live", 
            description="Нажмите снизу на кнопку \"Подать заявку\"\nНапишите свой ник, и расскажите планы на наш сервер"
        )
        
        await channel.send(embed=embed, view=InviteButton())
        await ctx.followup.send(f"Канал для заявок успешно установлен: {channel.mention}", ephemeral=True)


    @commands.slash_command(name="вопросы", description="Установить канал для создания вопросов по серверу")
    @commands.has_guild_permissions(administrator=True)
    async def set_channel_for_questions(
        self, 
        ctx: ApplicationContext,
        channel: Option(abc.GuildChannel, name="канал", description="Текстовый канал или ветка форума", 
                        channel_types=[ChannelType.text, ChannelType.public_thread, ChannelType.private_thread, ChannelType.news, ChannelType.news_thread],
                        required=True) #type: ignore
        ):
        await ctx.response.defer(ephemeral=True)
        embed = Embed(
            color=0xff5858, 
            title="Задать вопрос по Hard Live",
            description="Нажмите на кнопку \"Задать вопрос\" ниже.\nЗадайте интересующий вас вопрос администрации проекта."
        )
        
        await channel.send(embed=embed, view=QuestionsButton())
        await ctx.followup.send(f"Канал для вопрсов успешно установлен: {channel.mention}", ephemeral=True)

def setup(client):
    client.add_cog(ButtonAction(client))