import discord
from discord.ext import commands
import random
from MusicBot.db_service import DBService
from MusicBot.configs import CHAMPIONS

class CommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = DBService()
        print('[Command Cog] Initialized')

    @commands.command(name="leaguechamp", aliases=["LeagueChamp", "lc"], help="rolls a random league of legends champion")
    async def leaguechamp(self, ctx, role: str = ''):
        if role == '':
            role = random.choice(['Top', 'Jungle', 'Mid', 'ADC', 'Support'])
            
        role:str = role.lower()
        if role not in CHAMPIONS:
            await ctx.send(f'Invalid role: {role}')
            return

        champ = random.choice(CHAMPIONS[role])
        await ctx.send(f'Your champion is: **{champ}**')
        
    
   
    
