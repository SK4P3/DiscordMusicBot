import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.ext.commands import Bot
import yt_dlp as youtube_dl
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

bot = Bot(command_prefix='!', intents=intents)


def get_youtube_video_info(url):

    ydl_opts = {
        'format': 'bestaudio/best',  # Choose the best quality audio format
        'quiet': True,  # Suppress verbose output
        'no_warnings': True,  # Suppress warnings
        'default_search': 'auto',  # Auto search for URLs that are not direct YouTube URLs
        # You can add more options as per your requirements
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)
            return info_dict
        except Exception as e:
            print(f"Error occurred: {e}")
            return None


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command(name='join', help='Joins a voice channel')
async def join(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()

    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command()
async def play(ctx, url):

    if not ctx.voice_client:
        await join(ctx)

    if not ctx.voice_client:
        await ctx.send("I am not connected to a voice channel.")
        return

    ctx.voice_client.stop()

    ffmpeg_opts = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    video_info = get_youtube_video_info(url)
    video_url = video_info.get('url')

    ctx.voice_client.play(FFmpegPCMAudio(video_url, **ffmpeg_opts))


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.event
async def on_message(message):
    print(message)
    await bot.process_commands(message)


if __name__ == '__main__':
    bot.run(token)
