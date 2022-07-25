import discord
from discord.ext import commands
import youtube_dl
import asyncio
import keep_alive

client = commands.Bot(command_prefix="?", intents = discord.Intents.all())
songs = []
play_next_song = asyncio.Event()

options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
ydl_options = {'format': "bestaudio"}

"""
async def audio_player_task():
  while True:
    play_next_song.clear()
    current = await songs.get()
    current.start()
    await play_next_song.wait()

def toggle_next():
  client.loop.call_soon_threadsafe(play_next_song.set)
"""

@client.command()
async def join(ctx):
  if ctx.author.voice is None:
    await ctx.send("Please join a voice channel and try again.")
  voice_channel = ctx.author.voice.channel
  if ctx.voice_client is None:
    await voice_channel.connect()
  else: 
    await ctx.voice_client.move_to(voice_channel)

@client.command()
async def stop(ctx):
  await ctx.voice_client.disconnect()

@client.command()
async def play(ctx, *val):
  await ctx.invoke(client.get_command('join'))
  ctx.voice_client.stop()
  
  vc = ctx.voice_client

  with youtube_dl.YoutubeDL(ydl_options) as ydl:
    query = " ".join(val)
    info = ydl.extract_info("ytsearch:%s" % query, download=False)['entries'][0]
    url2 = info['formats'][0]['url']
    source = await discord.FFmpegOpusAudio.from_probe(url2, **options)
    vc.play(source)

keep_alive.keep_alive()
client.run("Insert Discord Bot Key here")
