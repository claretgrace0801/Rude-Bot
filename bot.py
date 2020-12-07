# bot.py
import os
import random
import sys
import asyncio
import time

from gtts import gTTS
import discord
from discord.ext import commands,tasks
from dotenv import load_dotenv
from time import sleep
from discord import opus

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='=', intents=intents)

#global variables
threshold = 400
minutes = 5

mute_toggles = {}
active_time = {}

async def check_inactivity():
    # print(time.time())
    bot_channels = bot.voice_clients
    # print(bot_channels)
    t = time.time()
    sec = minutes*60
    for vc in bot_channels:
        if (t - active_time[vc.guild.id]) > sec:
            await vc.disconnect() 

async def check_often():
    while True:
        # print(time.time())
        await check_inactivity()
        await asyncio.sleep(minutes*60)

async def update_toggles():
    global mute_toggles
    for guild in bot.guilds:
        for member in guild.members:
            if member.id not in mute_toggles:
                mute_toggles[member.id] = False

async def update_active_time():
    global active_time
    for guild in bot.guilds:
        if guild.id not in active_time:
            active_time[guild.id] = 0.0

@bot.listen('on_ready')
async def initialisation():
    await update_toggles()
    await update_active_time()
    # print(mute_toggles)
    print("CONNECTED")

@bot.listen('on_guild_join')
async def guild_join():
    # update mute toggles
    await update_toggles()
    await update_active_time()

@bot.listen('on_member_join')
async def mem_join():
    await update_toggles()

@bot.command(name='rude', help="Don't do this. The bot will insult you.")
async def talk_rude(ctx):
    name = ctx.message.author.name
    insults = [
        f"I have no interest in talking to you, {name}",
        f"I'm stuck here talking to {name}. What has my life come to.",
        f"Don't you have anything else to do other than talking to me, {name}. I mean I'm not even a real person.",
        f"You talking to a bot makes your lack of friends evident, {name}.",
        f"Sorry, I don't think talking to you is worth my time, {name}"
    ]

    response = random.choice(insults)
    await ctx.send(response)

async def text_to_speech(message, content):
    global active_time
    active_time[message.guild.id] = time.time()
    if len(content) > 400:
        return
    # tts_engine = tts.sapi.Sapi()
    # tts_engine.create_recording("playing.wav", content)
    tts_var = gTTS(content, lang_check=False)
    tts_var.save('playing.mp3')

    bot_channels = bot.voice_clients
    voice_c = message.author.voice

    if voice_c != None:
        vc = None
        voice_channel = voice_c.channel
        bot_channels_channels = [channel.channel for channel in bot_channels]
        print(bot_channels_channels)
        if voice_channel not in bot_channels_channels:
            try:
                vc = await voice_channel.connect()
            except:
                chan = [val for val in bot_channels if val.channel in message.guild.voice_channels][0]
                await chan.disconnect()
                vc = await voice_channel.connect()
        # elif voice_channel != bot_channels[0].channel:
            # await bot_channels[0].disconnect()
            # vc = await voice_channel.connect()
        else:
            vc = [val for val in bot_channels if val.channel in message.guild.voice_channels][0]
        
        # await message.channel.send(f"Saying what {ctx.message.author.name} told me to say.")
        vc.play(discord.FFmpegPCMAudio("./playing.mp3"))
        
        # Sleep while audio is playing.
        while vc.is_playing():
            sleep(.1)
        # await vc.disconnect()
    
    else:
        await message.channel.send("You are not in a voice channel.")
    # Delete command after the audio is done playing.
    
    # os.system("rm playing.mp3")

tts_help_string = "Text to speech.\nYou can also use it in the following ways:\n=say Hello there\n= Hello there\nsay Hello there\nIf you are muted, it will speak whatever you type."

@bot.command(name='say', help=tts_help_string, aliases=[''])
async def tts(ctx, *args):
    sentence = " ".join(args[:])
    await text_to_speech(ctx.message, sentence)
    

@bot.listen('on_message')
async def talk_it(message):
    # global mute_toggles
    m = message.author.voice.mute or message.author.voice.self_mute
    d = message.author.voice.deaf or message.author.voice.self_deaf
    
    invoke_com = 'say'
    if (message.content.split(' '))[0] == invoke_com:
        await text_to_speech(message, message.content[len(invoke_com)+1:])

    elif m and not d and len(message.content) < threshold and message.content[0] != '=' and mute_toggles[message.author.id]:
        await text_to_speech(message, message.content)
    # elif m and not d and len(message.content) < threshold and message.content[0] != '=':
    #     await text_to_speech(message, message.content)


@bot.command(name='auto', help='Set to true/false to enable/disable mute-speech\nSet to True if you want every message to be spoken out while you are muted.')
async def mspeech(ctx, arg):
    global mute_toggles
    if arg == 'true' or arg == 'True':
        mute_toggles[ctx.message.author.id] = True
        await ctx.send(f"Mute speech is on for {ctx.message.author.name}.")
    elif arg == 'false' or arg == 'False':
        mute_toggles[ctx.message.author.id] = False
        await ctx.send(f"Mute speech is off for {ctx.message.author.name}.")
    else:
        await ctx.send(f"{arg} is not a valid option")

bot.loop.create_task(check_often())
bot.run(TOKEN)


