import discord
from discord.ext import commands
from pprint import pprint

from MusicBot.db_service import DBService


class event_cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = DBService()
        print('[Event Cog] Initialized')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        print(f'{member} has joined the server')
        self.db.add_guild(member.guild.id, member.guild.name)
        self.db.add_user(member.guild.id, member.id, member.name)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
        print(f'{member} has joined the voice channel')
        self.db.add_guild(member.guild.id, member.guild.name)
        self.db.add_user(member.guild.id, member.id, member.name)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f'[BOT] Joined {guild.name} with {guild.member_count} members')
        self.db.add_guild(guild.id, guild.name)
        for member in guild.members:
            self.db.add_user(guild.id, member.id, member.name)
