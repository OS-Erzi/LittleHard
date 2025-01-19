from discord import Embed, Interaction, InputTextStyle, PermissionOverwrite, Thread, TextChannel
from discord.ui import Modal, InputText

from core import settings

class InviteModal(Modal):
    def __init__(self):
        super().__init__(timeout=None, title="Заявка на HARD LIVE")
        
        self.add_item(InputText(label="Ваш ник", max_length=50, style=InputTextStyle.short))
        self.add_item(InputText(label="Ваши планы на сервер", max_length=4000, style=InputTextStyle.long))
        self.add_item(InputText(label="Дюпать можно?", max_length=3, style=InputTextStyle.short))
    
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
