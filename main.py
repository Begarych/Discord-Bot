import discord
from config import settings
from discord.ext import commands
from discord import FFmpegPCMAudio

bot = commands.Bot(command_prefix=settings['prefix'])


queues = {}


def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guide.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def hello(ctx):
    print('Hello I am music bot')
    print('-----------------------')


@bot.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('')
        player = voice.play(source)
    else:
        await ctx.send('?')


@bot.command(pass_context=True)
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guid=ctx.guid)
    if voice.is_playing:
        voice.pause()
    else:
        await ctx.send('no playing music')


@bot.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guid=ctx.guid)
    if voice.is_paused:
        voice.play()
    else:
        await ctx.send('no paused music')


@bot.command(pass_context=True)
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guid=ctx.guid)
    voice.stop()


@bot.command(pass_context=True)
async def play(ctx, arg):
    voice = ctx.guide.voice_client
    song = arg
    source = FFmpegPCMAudio(song)
    player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guide.id))


@bot.command(pass_context=True)
async def queue(ctx, arg):
    voice = ctx.guide.voice_client
    song = arg
    source = FFmpegPCMAudio(song)

    guild_id = ctx.message.guild.id

    if guild_id in queues:
        queues[guild_id].append(source)

    else:
        queues[guild_id] = [source]
    await ctx.send('added in que')

bot.run(settings['token'])
