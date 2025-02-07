import discord
from discord.ext import commands
import os
import asyncio

from music import music_cog

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

with open('token.txt', 'r') as file:
    token = file.read()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')



async def main():
    async with bot:
        await bot.add_cog(music_cog(bot))
        await bot.start(token)


if __name__ == '__main__':
    asyncio.run(main())