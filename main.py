import asyncio
import random
import discord
from discord import FFmpegPCMAudio
from discord.ext.commands import Bot
from dotenv import load_dotenv
import os

from utils import format_time, get_youtube_video_info

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
bot = Bot(command_prefix='!', intents=intents)

song_queue = []

ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}


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

    video_info = get_youtube_video_info(url)
    if video_info is None:
        await ctx.send("Could not retrieve video information.")
        return

    song_queue.append(video_info)

    if len(song_queue) > 1 or ctx.voice_client.is_playing():
        await ctx.send(
            f"Added to Queue!\nThere are currently {len(song_queue)} songs in queue. Use !list to get more information."
        )

    if not ctx.voice_client.is_playing():
        await play_from_queue(ctx)


@bot.command(name="playnow")
async def play_now(ctx, url):
    if not ctx.voice_client:
        await ctx.send("I am not connected to a voice channel.")
        return

    video_info = get_youtube_video_info(url)
    if video_info is None:
        await ctx.send("Could not retrieve video information.")
        return

    song_queue.insert(0, video_info)
    ctx.voice_client.stop()


async def play_from_queue(ctx):
    while len(song_queue) > 0:
        video_info = song_queue.pop(0)
        video_url = video_info["url"]

        source = FFmpegPCMAudio(video_url, **ffmpeg_opts)
        ctx.voice_client.play(source)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def shuffle(ctx):
    if len(song_queue) > 1:
        random.shuffle(song_queue)
        await ctx.send("Queue shuffled!")
    else:
        await ctx.send("Not enough songs in the queue to shuffle.")


@bot.command(name="list")
async def list_queue(ctx):
    if len(song_queue) > 0:
        msg = f"There are currently {len(song_queue)} songs in queue.\n"
        for i, song in enumerate(song_queue):
            msg += str(i+1)+". "
            msg += song["title"] + " - "
            msg += format_time(int(song["formats"][0]["fragments"][0]["duration"]))
            msg += "\n"
        await ctx.send(msg)
    else:
        await ctx.send("No songs in queue.")


@bot.command()
async def skip(ctx):
    await ctx.send("Skipped!")
    ctx.voice_client.stop()


@bot.command()
async def clear(ctx):
    global song_queue
    song_queue = []
    ctx.voice_client.stop()
    await ctx.send("Cleared Queue!")


@bot.event
async def on_message(message):
    print(message)
    await bot.process_commands(message)


if __name__ == '__main__':
    # print(get_youtube_video_info("https://www.youtube.com/watch?v=Hhok9PNV_zc"))
    bot.run(token)
