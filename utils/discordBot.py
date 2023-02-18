import discord
from dotenv import load_dotenv
import os

from utils.chatgpt import chatgpt
load_dotenv()


class aclient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)
        self.activity = discord.Activity(type=discord.ActivityType.watching, name="/chat")


async def send_message(message, user_message):
    try:
        user_id = message.user.id
        response = '> **' + user_message + '** - <@' + str(user_id) + '> \n\n'
        response = f'{response} {chatgpt.get_response(user_id, user_message)}'
        await message.channel.send(response)
    except Exception:
        await message.channel.send('> **Error: Something went wrong, please try again later!**')


def run():
    client = aclient()

    @client.event
    async def on_ready():
        await client.tree.sync()

    @client.tree.command(name="chat", description="Have a chat with ChatGPT")
    async def chat(interaction: discord.Interaction, *, message: str):
        if interaction.user == client.user:
            return
        await send_message(interaction, message)

    @client.tree.command(name="reset", description="Reset ChatGPT conversation history")
    async def reset(interaction: discord.Interaction):
        user_id = interaction.user.id
        chatgpt.clean_history(user_id)
        await interaction.channel.send(f'> Reset ChatGPT conversation history < - <@{user_id}>')

    client.run(os.getenv('DISCORD_TOKEN'))
