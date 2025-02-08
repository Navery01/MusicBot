import discord
from discord.ext import commands
import requests
from pprint import pprint
from MusicBot.db_service import DBService
import html
import random



class trivia_cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.current_question = None
        self.db = DBService()
        self.answer_dict = None
        self.categories = {
            'general knowledge': 9,
            'books': 10,
            'film': 11,
            'music': 12,
            'musicals and theatres': 13,
            'television': 14,
            'video games': 15,
            'board games': 16,
            'science and nature': 17,
            'computers': 18,
            'mathematics': 19,
            'mythology': 20,
            'sports': 21,
            'geography': 22,
            'history': 23,
            'politics': 24,
            'art': 25,
            'celebrities': 26,
            'animals': 27,
            'vehicles': 28,
            'comics': 29,
            'gadgets': 30,
            'anime and manga': 31,
            'cartoons and animations': 32
        }

        self.difficulties = {   
            'Easy': 'easy',
            'Medium': 'medium',
            'Hard': 'hard'
        }

        print('[Trivia Cog] Initialized')


    def get_question(self, category: str | int = 9, difficulty: str = 'medium') -> dict:
        cat =  category if category.isdigit() else self.categories[category.lower()]
        self.base_url = f'https://opentdb.com/api.php?amount=1&category={cat}&difficulty={difficulty}&type=multiple'
        response = requests.get(self.base_url)
        response.encoding = 'utf-8'  # Ensure proper encoding
        data = response.json()
        question = data['results'][0]
        pprint(question)
        return question
    
    @commands.command(name='trivia', aliases=['t'], help='Starts a trivia game')
    async def trivia(self, ctx, difficulty: str = 'medium', *category):
        category = ' '.join(category) if category else 'General Knowledge'
        self.current_question = self.get_question(category=category, difficulty=difficulty)

        answer_choices = self.current_question["incorrect_answers"] + [self.current_question["correct_answer"]]
        random.shuffle(answer_choices)

        self.answer_dict = {i: html.unescape(answer) for i, answer in enumerate(answer_choices)}
        retval = ''
        for i, answer in self.answer_dict.items():
            retval += f'{i+1}) {answer} \n'

        await ctx.send(f'***{html.unescape(self.current_question["question"])}***')
        await ctx.send(f'**{retval}**')
    
    @commands.command(name='answer', aliases=['ans'], help='Answers the current trivia question')
    async def answer(self, ctx, *answer: str):
        diff_val = {'easy': 10, 'medium': 25, 'hard': 50}

        if self.current_question is None:
            await ctx.send('Use !trivia for a new question')
            return

        answer = ' '.join(answer)
        if answer.isdigit():
            answer = self.answer_dict[int(answer)-1]
        guild_id = ctx.guild.id
        user_id = ctx.author.id
        
        if answer.lower() == self.current_question['correct_answer'].lower():
            award_points = diff_val[self.current_question['difficulty'].lower()]
            await ctx.send(f'{ctx.author.mention} has answered the {self.current_question["difficulty"]} question correctly! **+{award_points}** points!')
            self.db.update_points(guild_id, user_id, award_points)
            total_points = self.db.get_points(guild_id, user_id)
            await ctx.send(f'New balance: {total_points} points!')
        else:
            await ctx.send('Incorrect!')
            await ctx.send(f'The correct answer was: {self.current_question["correct_answer"]}')
        self.reset()

    @commands.command(name='categories', aliases=['cat'], help='All the categories available for trivia')
    async def categories(self, ctx):
        categories = '\n' + '\n'.join(f'{v}. {k}' for k, v in self.categories.items())
        await ctx.send(f'Categories: **{categories}**')

    def reset(self):
        self.current_question = None
        self.answer_dict = None


if __name__ == '__main__':
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='!', intents=intents)

    trivia_cog = trivia_cog(bot)
    question = trivia_cog.get_question('Sports', 'hard')