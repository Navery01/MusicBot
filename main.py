import discord
from discord.ext import commands, tasks
import os
import asyncio

from MusicBot.music import music_cog
from MusicBot.event_cog import event_cog
from MusicBot.token_cog import token_cog
from MusicBot.trivia_cog import trivia_cog
from MusicBot.db_service import DBService

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

with open('token.txt', 'r') as file:
    token = file.read()

@tasks.loop(hours=1)
async def update_database():
    DBService().restart()

@bot.event
async def on_ready():
    update_database.start()
    print(f'Logged in as {bot.user.name}')

async def main():
    async with bot:
        await bot.add_cog(music_cog(bot))
        await bot.add_cog(event_cog(bot))
        await bot.add_cog(token_cog(bot))
        await bot.add_cog(trivia_cog(bot))
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())