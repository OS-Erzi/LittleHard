from discord import Embed, ApplicationContext, Option, ChannelType, abc, SlashCommandGroup, Message
from discord.ext import commands

import re
import aiohttp

from structs.button import InviteButton, QuestionsButton, UrlButton
from structs.embedgen import EmbedGenerator

from core import ProjectType

class ButtonAction(commands.Cog):
    def __init__(self, client: ProjectType):
        self.client = client

    def validate_invite_link(self, url: str):
        if not re.match(r'https?://(?:www\.)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?', url):
            return False
        return True

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

    sponsor = SlashCommandGroup("спонсор")

    @sponsor.command(name="добавить", description="Добавить эмбед с кнопкой спонсора в канал")
    @commands.has_guild_permissions(administrator=True)
    async def send_sponsor_embed(
        self, 
        ctx: ApplicationContext, 
        sponsor_url: Option(str, name="ссылка-на-сервер", description="Полная ссылка-приглашение спонсора", required=True), #type: ignore
        ):
        if not self.validate_invite_link(str(sponsor_url)):
            raise commands.BadArgument("ValidateInviteUrl")
        
        view = EmbedGenerator(sponsor_url)
        embed = view.start_embed()
        await ctx.respond(embed=embed, view=view, ephemeral=True)

    @sponsor.command(name="ссылка", description="Изменить ссылку в кнопке")
    @commands.has_guild_permissions(administrator=True)
    async def edit_url_in_button(
        self,
        ctx: ApplicationContext ,
        message_url: Option(str, name="сообщение", description="Ссылка на сообщение с кнопкой"), #type: ignore
        new_url: Option(str, name="спонсор", description="Новая ссылка для кнопки") #type: ignore
        ):
        try:
            # Разбор URL сообщения
            _, channel_id, message_id = message_url.split('/')[-3:]
            channel_id = int(channel_id)
            message_id = int(message_id)

            # Получение канала и сообщения
            channel = ctx.guild.get_channel(channel_id)
            if not channel:
                await ctx.respond("Канал не найден.", ephemeral=True)
                return

            message: Message = await channel.fetch_message(message_id)
            if not message:
                await ctx.respond("Сообщение не найдено.", ephemeral=True)
                return

            # Проверка наличия кнопок в сообщении
            if not message.components:
                await ctx.respond("В указанном сообщении нет кнопок.", ephemeral=True)
                return

            # Создание новой View с обновленной кнопкой
            view = UrlButton(new_url)

            # Обновление сообщения с новой View
            await message.edit(view=view)
            await ctx.respond("Ссылка в кнопке успешно обновлена.", ephemeral=True)

        except ValueError:
            await ctx.respond("Неверный формат ссылки на сообщение.", ephemeral=True)
        except Exception as e:
            await ctx.respond(f"Произошла ошибка: {str(e)}", ephemeral=True)
        

def setup(client):
    client.add_cog(ButtonAction(client))