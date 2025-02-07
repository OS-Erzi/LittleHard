from discord import Embed, ButtonStyle, InputTextStyle, Interaction, ComponentType, TextChannel, ChannelType
from discord.ui import InputText, Button, Modal, View, Select

from .button import UrlButton

class EmbedGenerator(View):
    def __init__(self, sponsor_url: str):
        super().__init__(timeout=None)
        self.embed = Embed(color=0x2b2d31)
        self.sponsor_url = sponsor_url

        self.setup_buttons()

    #Установка
    def setup_buttons(self) -> None:
        self.author_button = Button(label="Автор", custom_id="author", row=1)
        self.author_button.callback = self.create_embed_callback
        self.title_button = Button(label="Заголовок", custom_id="title", row=1)
        self.title_button.callback = self.create_embed_callback
        self.content_button = Button(label="Контент ембеда", custom_id="description", row=1)
        self.content_button.callback = self.create_embed_callback

        self.add_field_button = Button(label="Добавить поле", custom_id="add_field", row=2)
        self.add_field_button.callback = self.add_field_callback
        self.clear_fields_button = Button(label="Очистить все поля", custom_id="clear_fields", row=2)
        self.clear_fields_button.callback = self.clear_fields_callback
        self.remove_last_field_button = Button(label="Удалить последнее поле", custom_id="remove_last_field", row=2)
        self.remove_last_field_button.callback = self.remove_last_field_callback

        self.add_item(self.author_button)
        self.add_item(self.title_button)
        self.add_item(self.content_button)

        self.add_item(self.add_field_button)
        self.add_item(self.clear_fields_button)
        self.add_item(self.remove_last_field_button)

        self.thumbnail_button = Button(label="Мини-Картинка", custom_id="thumbnail", row=3)
        self.thumbnail_button.callback = self.create_embed_callback
        self.image_button = Button(label="Картинка", custom_id="image", row=3)
        self.image_button.callback = self.create_embed_callback
        self.footer_button = Button(label="Футер", custom_id="footer", row=3)
        self.footer_button.callback = self.create_embed_callback

        self.add_item(self.thumbnail_button)
        self.add_item(self.image_button)
        self.add_item(self.footer_button)

        self.send_button = Button(label="Отправить эмбед", emoji="<:arrow:1187170092480462921>", custom_id="send_embed", row=4, style=ButtonStyle.green)
        self.send_button.callback = self.send_callback

        self.add_item(self.send_button)

    def start_embed(self):
        embed = Embed(color=0x2b2d31, description="Воспользуйтесь кнопками для настройки")
        return embed

    #Эмбед
    def get_request_content(self, custom_id: str) -> dict:
        content_list = {
            "content": {
                "title": "Контент вне эмбеда",
                "label": "Содержание",
                "placeholder": "Так же вы можете использовать упоминания\n<#id-канала><@id-юзера><@&id-роли>"
            },
            "author": {
                "title": "Автор эмбеда",
                "label": "Содержание",
                "placeholder": "Администрация"
            },
            "title": {
                "title": "Заголовок эмбеда",
                "label": "Содержание",
                "placeholder": "Название"
            },
            "description": {
                "title": "Описание эмбеда",
                "label": "Содержание",
                "placeholder": ""
            },
            "thumbnail": {
                "title": "Мини-картинка",
                "label": "Ссылка",
                "placeholder": "https://..../...."
            },
            "image": {
                "title": "Картинка",
                "label": "Ссылка",
                "placeholder": "https://..../...."
            },
            "footer": {
                "title": "Нижняя строка",
                "label": "Содержание",
                "placeholder": "С любовью к вам"
            }
        }
        return content_list[custom_id]

    async def create_embed_callback(self, interaction: Interaction):
        custom_id = interaction.custom_id
        content = self.get_request_content(custom_id)
        
        await interaction.response.send_modal(
            GetContentForEmbed(
                title=content["title"], 
                label=content["label"], 
                placeholder=content["placeholder"], 
                custom_id=custom_id, 
                embed=self.embed
            )
        )

    async def add_field_callback(self, interaction: Interaction):
        await interaction.response.send_modal(
            AddFieldModal(embed=self.embed)
        )

    async def clear_fields_callback(self, interaction: Interaction):
        self.embed.clear_fields()
        await interaction.response.edit_message(embed=self.embed)

    async def remove_last_field_callback(self, interaction: Interaction):
        if self.embed.fields:
            self.embed.remove_field(-1)  # Удаляет последнее поле
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message("Нет полей для удаления", ephemeral=True)

    #Управление
    async def send_callback(self, interaction: Interaction):
        await interaction.response.defer()
        self.content = f"||{interaction.guild.default_role}||"
        view = Get_Channel(self.content, self.embed, self.sponsor_url, self)
        view.self_button()
        embed = view.self_embed()
        await interaction.edit_original_response(embed=embed, view=view)

class GetContentForEmbed(Modal):
    def __init__(self, title: str, label: str, placeholder: str, custom_id: str, embed: Embed):
        super().__init__(title=title)
        self.custom_id = custom_id
        self.embed = embed
        self.add_item(InputText(label=label, placeholder=placeholder, style=InputTextStyle.long, custom_id=self.custom_id))

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        new_content = self.children[0].value
        
        match interaction.custom_id:
            case "author":
                self.embed.set_author(name=new_content)
            case "title":
                self.embed.title = new_content
            case "description":
                self.embed.description = new_content
            case "thumbnail":
                self.embed.set_thumbnail(url=new_content)
            case "image":
                self.embed.set_image(url=new_content)
            case "footer":
                self.embed.set_footer(text=new_content)

        try:
            await interaction.edit_original_response(embed=self.embed)
        except:
            pass

class AddFieldModal(Modal):
    def __init__(self, embed: Embed):
        super().__init__(title="Добавить поле")
        self.embed = embed
        self.add_item(InputText(label="Название", placeholder="Введите название поля", custom_id="field_name"))
        self.add_item(InputText(label="Значение", placeholder="Введите значение поля", custom_id="field_value", style=InputTextStyle.long))
        self.add_item(InputText(label="Inline", placeholder="True или False", custom_id="field_inline"))

    async def callback(self, interaction: Interaction):
        name = self.children[0].value
        value = self.children[1].value
        inline = self.children[2].value.lower() == 'true'

        self.embed.add_field(name=name, value=value, inline=inline)

        await interaction.response.edit_message(embed=self.embed)

class Get_Channel(View):
    def __init__(self, content: str, embed: Embed, sponsor_url: str, back: EmbedGenerator):
        super().__init__(timeout=None)
        self.sponsor_url = sponsor_url
        self.content = content
        self.embed = embed

        self.backer = back

        self.channel_select = Select(
            select_type=ComponentType.channel_select,
            channel_types=[
                ChannelType.text, 
                ChannelType.public_thread, 
                ChannelType.private_thread, 
                ChannelType.news, 
                ChannelType.news_thread
            ],
            placeholder="Список каналов отправки", min_values=1, max_values=1, custom_id="select_channel"
        )
        self.channel_select.callback = self.channel_select_callback

        self.back_creator = Button(label="Назад", style=ButtonStyle.danger, emoji="<:x_left:1186671627941970041>", custom_id="back_creator")
        self.back_creator.callback = self.back_creator_callback
        
        self.back_button = Button(label="Назад", style=ButtonStyle.danger, emoji="<:x_left:1186671627941970041>", custom_id="back_button")
        self.back_button.callback = self.back_button_callback

    #Установка
    def self_embed(self):
        embed = Embed(color=0x2b2d31, description="Выберите канал отправки.")
        return (embed)

    #Обновление кнопок
    def self_button(self):
        self.clear_items()
        self.add_item(self.channel_select)
        self.add_item(self.back_creator)
    
    def button_back(self):
        self.clear_items()
        self.add_item(self.back_button)

    async def channel_select_callback(self, interaction: Interaction):
        await interaction.response.defer()
        channel = interaction.guild.get_channel(int(interaction.data["values"][0]))
        if isinstance(channel, TextChannel):
            e = Embed(color=0x2b2d31, description="В течении нескольких секунд эмбед будет отправлен")
            await interaction.edit_original_response(embed=e, view=None)
            await channel.send(content=self.content, embed=self.embed, view=UrlButton(self.sponsor_url, "Переходник"))
        else:
            embed = Embed(color=0x2b2d31, description="Невозможно отправить сообщение в этот канал")
            self.button_back()
            await interaction.edit_original_response(embed=embed, view=self)

    async def back_button_callback(self, interaction: Interaction):
        await interaction.response.defer()
        self.self_button()
        embed = self.self_embed()
        await interaction.edit_original_response(view=self, embed=embed)

    async def back_creator_callback(self, interaction: Interaction):
        await interaction.response.defer()
        await interaction.edit_original_response(embed=self.embed, view=self.backer)
