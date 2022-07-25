import discord
from discord.ext import commands
import youtube_dl

bot = commands.Bot(command_prefix="?")

@bot.command()
async def play(ctx, url: str):
  voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=)
