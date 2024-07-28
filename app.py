import discord
from discord.ext import commands
import os

# Create intents and enable the ones you need
intents = discord.Intents.default()
intents.messages = True  # Enable the intent to receive message events
intents.message_content = True  # Enable access to message content

# Initialize the bot with the desired command prefix and intents
bot = commands.Bot(command_prefix='/', intents=intents)

# Event that triggers when the bot is ready
@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

# Command to move a message to another channel
@bot.command()
@commands.has_permissions(manage_messages=True)
async def moveTo(ctx, channel_name: str):
    # Check if the message is a reply
    if ctx.message.reference is None:
        await ctx.send("You need to reply to a message to move it.")
        return

    # Get the message being replied to
    msg_id = ctx.message.reference.message_id
    original_message = await ctx.channel.fetch_message(msg_id)

    # Find the target channel by name
    target_channel = discord.utils.get(ctx.guild.channels, name=channel_name)

    if target_channel is None:
        await ctx.send(f"Channel '{channel_name}' not found.")
        return

    # Send the original message content to the target channel
    await target_channel.send(f"Moved message from {original_message.author.mention}:\n{original_message.content}")

    # Optionally, delete the original message
    await original_message.delete()

# Run the bot with your token
bot.run(os.getenv('MOVE_IT_TOKEN'))
