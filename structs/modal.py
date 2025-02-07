from discord import Embed, Interaction, InputTextStyle, PermissionOverwrite, Thread, TextChannel
from discord.ui import Modal, InputText

from .button import UrlButton

from .button import UrlButton

from core import settings

class InviteModal(Modal):
    def __init__(self):
        super().__init__(timeout=None, title="Заявка на HARD LIVE")
        
        self.add_item(InputText(label="Ваш ник", max_length=50, style=InputTextStyle.short))
        self.add_item(InputText(label="Ваши планы на сервер", max_length=2000, style=InputTextStyle.long))
        self.add_item(InputText(label="Ваши планы на сервер", max_length=2000, style=InputTextStyle.long))
        self.add_item(InputText(label="Дюпать можно?", max_length=3, style=InputTextStyle.short))
        self.add_item(InputText(label="Откуда вы узнали о нашем проекте?", max_length=250, style=InputTextStyle.short))
        self.add_item(InputText(label="Откуда вы узнали о нашем проекте?", max_length=250, style=InputTextStyle.short))
    
    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        category = interaction.guild.get_channel(settings.channelsid.CATEGORY_FOR_INVITE_CHANNEL)

        overwrites = {
            interaction.guild.default_role: PermissionOverwrite(read_messages=False),
            interaction.user: PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel = await category.create_text_channel(name=self.children[0].value, overwrites=overwrites)

        embed = Embed(color=0x2b2d31, title=f"Заявка от {self.children[0].value}")
        embed.add_field(name="Планы на сервер.", value=self.children[1].value, inline=False)
        embed.add_field(name="Можно ли дюпать.", value=f"Ответ: {self.children[2].value}", inline=False)
        embed.add_field(name="Узнал о проекте:", value=self.children[3].value, inline=True)
        embed.add_field(name="Узнал о проекте:", value=self.children[3].value, inline=True)


        await channel.send(interaction.user.mention, embed=embed)

class QuestionsModal(Modal):
    def __init__(self):
        super().__init__(timeout=None, title="Задать вопрос")
        
        self.add_item(InputText(label="Заголовок:", placeholder="Максимум 100 символов", max_length=100, style=InputTextStyle.short))
        self.add_item(InputText(label="Содержание:", placeholder="Максимум 2.000 символов", max_length=2000, style=InputTextStyle.long))
    #
    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        label = self.children[0].value
        question = self.children[1].value
        user = interaction.user

        try:
            if isinstance(interaction.channel, Thread):
                # Если это ветка форума, создаем новую ветку
                forum_channel = interaction.channel.parent
                thread = await forum_channel.create_thread(
                    name=label,
                    content=question,
                    auto_archive_duration=10080  # 7 дней
                )
            elif isinstance(interaction.channel, TextChannel):
                # Если это текстовый канал, создаем новый канал в той же категории
                category = interaction.channel.category
                overwrites = {
                    interaction.guild.default_role: PermissionOverwrite(read_messages=False),
                    interaction.user: PermissionOverwrite(read_messages=True, send_messages=True)
                }
                new_channel = await category.create_text_channel(name=self.children[0].value, overwrites=overwrites)
                thread = new_channel
        finally:
            embed = Embed(
                color=0x2b2d31,
                description=f"Вопрос задал - {user.mention}"
            ).set_footer(text=f"id: {user.id}")
            await thread.send(embed=embed)

class MediaRequestModal(Modal):
    def __init__(self):
        super().__init__(timeout=None, title="Задать вопрос")
        
        self.add_item(
            InputText(
                label="Какой контент планируете снимать у нас?", 
                max_length=2000, style=InputTextStyle.long)
            )
        self.add_item(
            InputText(
                label="Площадка для вашего контента",
                placeholder="Youtube/Twitch/...",
                max_length=2000, style=InputTextStyle.short)
            )
        self.add_item(
            InputText(
                label="Сколько у вас подписчиков/фоловеров.",
                placeholder="от 100+ / от 25+",
                max_length=8, style=InputTextStyle.short)
            )
        self.add_item(
            InputText(
                label="Ссылка на канал.",
                placeholder="Поле для ссылки",
                max_length=1000, style=InputTextStyle.short)
            )
    
    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        category = interaction.guild.get_channel(settings.channelsid.CATEGORY_FOR_MEDIA_CHANNEL)

        overwrites = {
            interaction.guild.default_role: PermissionOverwrite(read_messages=False),
            interaction.user: PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel = await category.create_text_channel(name=interaction.user.display_name, overwrites=overwrites)

        chi = self.children

        embed = Embed(color=0x2b2d31, title=f"Заявка")
        embed.set_author(name=interaction.user, url=interaction.user, icon_url=interaction.user.display_avatar.url)

        embed.add_field(name=chi[0].label, value=f"> {chi[0].value}", inline=False)
        embed.add_field(name=chi[1].label, value=f"> {chi[1].value}", inline=True)
        embed.add_field(name=chi[2].label, value=f"> {chi[2].value}", inline=True)
        embed.set_image(url=settings.images.INVISIBLE_URL)

        try:
            await channel.send(interaction.user.mention, embed=embed, view=UrlButton(chi[3].value, "Канал"))
        except:
            embed.add_field(name=chi[3].label, value=chi[3].value, inline=False)
            await channel.send(interaction.user.mention, embed=embed)
