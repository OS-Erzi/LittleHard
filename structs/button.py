from discord import Interaction, ButtonStyle
from discord.ui import button, View, Button

from .modal import InviteModal, QuestionsModal

class InviteButton(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Подать заявку", style=ButtonStyle.green, custom_id="modal")
    async def button1_callback(self, button: Button, interaction: Interaction):
        await interaction.response.send_modal(InviteModal())

class QuestionsButton(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Задать вопрос", style=ButtonStyle.green, custom_id="question_modal")
    async def button2_callback(self, button: Button, interaction: Interaction):
        await interaction.response.send_modal(QuestionsModal())
