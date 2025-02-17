import discord
from discord.ext import commands
import random
from MusicBot.db_service import DBService

class token_cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = DBService()
        print('[Token Cog] Initialized')

    @commands.command(name="roll", aliases=["dr"], help="starts a deathroll game")
    async def roll(self, ctx, max_roll: int = 1000):
        roll = random.randint(1, max_roll)
        await ctx.send(f'{ctx.author.name} : **{roll}** [0, {max_roll}]')
    
    @commands.command(name="flip", aliases=["coin"], help="flips a coin")
    async def flip(self, ctx):
        flip = random.choice(['Heads', 'Tails'])
        await ctx.send(f'{ctx.author.name} : **{flip}**')
    
    @commands.command(name='points', aliases=['point', 'pts'], help='Displays the points of the user')
    async def points(self, ctx):
        num_pts = self.db.get_points(ctx.guild.id, ctx.author.id)
        if num_pts is None:
            await ctx.send('No points found')
            return
        await ctx.send(f'{ctx.author.name} has {num_pts} points')

    @commands.command(name='give', aliases=['gift'], help='Gives points to another user')
    async def give(self, ctx, user: discord.Member, points: int):
        if points < 0:
            await ctx.send('Cannot give negative points')
            return
        num_pts = self.db.get_points(ctx.guild.id, ctx.author.id)
        if num_pts < points:
            await ctx.send('Not enough points')
            return
        
        self.db.add_points(ctx.guild.id, user.id, points)
        self.db.add_points(ctx.guild.id, ctx.author.id, -points)
        await ctx.send(f'{ctx.author.name} gave {points} points to {user.name}')

    @commands.command(name='kick', aliases=[], help='Gives points to another user')
    async def kick(self, ctx,  user: discord.Member):
        if user == ctx.author:
            await ctx.send('Cannot kick yourself')
            return

        num_pts = self.db.get_points(ctx.guild.id, ctx.author.id)
        if num_pts <= 500:
            await ctx.send('Not enough points')
            return
        
        self.db.update_points(ctx.guild.id, ctx.author.id, -1000)
        
        print(f'Kicking {user.name}')
        await ctx.guild.kick(user)

    @commands.command(name='dc', aliases=[], help='Gives points to another user')
    async def dc(self, ctx,  user: discord.Member):
        if user == ctx.author:
            await ctx.send('Cannot kick yourself')
            return

        num_pts = self.db.get_points(ctx.guild.id, ctx.author.id)
        if num_pts <= 100:
            await ctx.send('Not enough points')
            return
        
        self.db.update_points(ctx.guild.id, ctx.author.id, -100)
        
        print(f'Kicking {user.name}')
        await user.move_to(None)
    
