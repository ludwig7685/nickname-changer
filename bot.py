import discord
from discord.ext import commands
import os
import asyncio
import re

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = 'MTE'
GUILD_ID = ''  # Replace with the ID of your target Discord server

# Function to modify nicknames for all users in the server
async def modify_nicknames():
    await bot.wait_until_ready()
    print("Bot is ready to modify nicknames.")
    while not bot.is_closed():
        try:
            # Get the target guild
            guild = bot.get_guild(int(GUILD_ID))
            if guild is None:
                print(f"Bot is not in the specified guild with ID: {GUILD_ID}")
                return

            # Fetch all members in the guild
            all_members = guild.members

            # Loop through all members and modify their nicknames
            for member in all_members:
                print(f"Checking nickname for user {member.name}...")
                # Check if the nickname starts with the specified prefix (ignoring additional spaces)
                if member.nick:
                    stripped_nick = re.sub(r'[^a-zA-Z0-9]', '!', member.nick.strip())
                    if stripped_nick != member.nick:  # If the nickname starts with "!" and has spaces
                        try:
                            await member.edit(nick=stripped_nick)
                            print(f"Changed nickname for user {member.name} to {stripped_nick}")
                        except discord.Forbidden:
                            print(f"Missing permissions to change nickname for user {member.name}")
                        except Exception as e:
                            print(f"An error occurred while changing nickname for user {member.name}: {e}")
                await asyncio.sleep(1)  # Add a 1-second delay before checking the next member
            await asyncio.sleep(60)  # Modify nicknames every 60 seconds
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            await asyncio.sleep(60)  # Wait before retrying in case of an error

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - {bot.user.id}")
    await modify_nicknames()  # Start the nickname modification process when the bot is ready

# Run the bot
bot.run(TOKEN)
