import discord
from discord.ext import commands
import asyncio
import queue
import MusicBot.download_music as download_music
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

with open('token.txt', 'r') as file:
    token = file.read()
# Create a queue to manage songs
song_queue = queue.Queue()

# Create an event to signal when a song finishes
song_finished = asyncio.Event()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def play(ctx, url):
    if ctx.author.voice:
        voice_channel = ctx.author.voice.channel
        if not ctx.voice_client:
            await voice_channel.connect()
        voice_client = ctx.voice_client

        # Set the file name to the next available song number
        if not os.path.exists('song_' + str(song_queue.qsize() + 1) + '.mp3'):
            file_name = 'song_' + str(song_queue.qsize() + 1)
        else: 
            file_name = file_name = 'song_' + str(song_queue.qsize() + 2
                                                  )
        await download_music.download(url, f'music/{file_name}')

        # Add the song to the queue
        song_queue.put(f'music/{file_name}.mp3')

        # Play the song if not already playing
        if not voice_client.is_playing():
            await play_next_song(ctx, voice_client)
        else:
            await ctx.send('Added to the queue!')
    else:
        await ctx.send('You are not in a voice channel!')

async def play_next_song(ctx, voice_client):
    while not song_queue.empty():
        song = song_queue.get()
        audio_source = discord.FFmpegPCMAudio(song, executable='bin/ffmpeg.exe')
        voice_client.play(audio_source, after=lambda e: song_finished.set())
        await ctx.send(f'Now playing: {song}')
        
        # Wait for the song to finish
        await song_finished.wait()
        song_finished.clear()
    else:
        await ctx.send('Queue is empty!')

@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send('Skipped the current song.')
    else:
        await ctx.send('No song is currently playing.')

        
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('Disconnected from the voice channel')
    else:
        await ctx.send('I am not in a voice channel!')

bot.run(token)