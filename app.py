import discord
from discord import app_commands
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Register slash commands here
        self.tree.add_command(move_to)
        await self.tree.sync()

    async def on_ready(self):
        print(f'Bot connected as {self.user}')
        print(f'Connected to the following guilds:')
        for guild in self.guilds:
            print(f'- {guild.name} (id: {guild.id})')

# Initialize the bot
bot = MyBot()

# Slash command to move a message to another channel
@bot.tree.command(name="moveto", description="Move a message to another channel")
@app_commands.describe(channel_name="The name of the channel to move the message to")
async def move_to(interaction: discord.Interaction, channel_name: str):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return

    reference = interaction.message.reference
    if reference is None:
        await interaction.response.send_message("You need to reply to a message to move it.", ephemeral=True)
        return

    # Get the message being replied to
    msg_id = reference.message_id
    original_message = await interaction.channel.fetch_message(msg_id)

    # Find the target channel by name
    target_channel = discord.utils.get(interaction.guild.channels, name=channel_name)

    if target_channel is None:
        await interaction.response.send_message(f"Channel '{channel_name}' not found.", ephemeral=True)
        return

    # Send the original message content to the target channel
    await target_channel.send(f"Moved message from {original_message.author.mention}:\n{original_message.content}")

    # Optionally, delete the original message
    await original_message.delete()

    await interaction.response.send_message(f"Message moved to {channel_name}.", ephemeral=True)

# Run the bot with your token
bot.run(os.getenv('MOVE_IT_TOKEN'))
