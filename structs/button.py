from discord import Interaction, ButtonStyle
from discord.ui import button, View, Button

class UrlButton(View):
    def __init__(self, url: str, label: str):
        super().__init__(timeout=None)
        self.add_item(Button(label=label, url=url))

from .modal import InviteModal, MediaRequestModal, QuestionsModal

class InviteButton(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Подать заявку", style=ButtonStyle.green, custom_id="request_for_server")
    async def button1_callback(self, button: Button, interaction: Interaction):
        await interaction.response.send_modal(InviteModal())

class QuestionsButton(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Задать вопрос", style=ButtonStyle.green, custom_id="question_modal")
    async def button2_callback(self, button: Button, interaction: Interaction):
        await interaction.response.send_modal(QuestionsModal())

class MediaRequestButton(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Подать заявку", style=ButtonStyle.green, custom_id="media_request")
    async def button2_callback(self, button: Button, interaction: Interaction):
        await interaction.response.send_modal(MediaRequestModal())