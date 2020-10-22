# bot.py
import os
import random
import pyttsx3
import discord
from discord.ext import commands
from dotenv import load_dotenv
from time import sleep

engine = pyttsx3.init() # object creation

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 125)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female


print("CONNECTED")
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='=')

threshold = 400
# mute_toggles ={}
# for guild in bot.guilds:
#     for member in guild.members:
#         mute_toggles[member] = True

# for voice in voices: 
#     # to get the info. about various voices in our PC  
#     print("Voice:") 
#     print("ID: %s" %voice.id) 
#     print("Name: %s" %voice.name) 
#     print("Age: %s" %voice.age) 
#     print("Gender: %s" %voice.gender) 
#     print("Languages Known: %s" %voice.languages) 

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
    engine.save_to_file(content, 'playing.mp3')
    engine.runAndWait()
    engine.stop()
    bot_channels = bot.voice_clients
    voice_channel = message.author.voice
    # print(voice_channel)  
    if voice_channel != None:
        vc = None
        # await message.channel.send(f"Hi {vc}")
        voice_channel = voice_channel.channel
        if len(bot_channels) == 0:
            vc = await voice_channel.connect()
        elif voice_channel != bot_channels[0].channel:
            await bot_channels[0].disconnect()
            vc = await voice_channel.connect()
        else:
            vc = bot_channels[0]
        
        # await message.channel.send(f"Saying what {ctx.message.author.name} told me to say.")
        vc.play(discord.FFmpegPCMAudio(executable="../random/ffmpeg/bin/ffmpeg.exe", source="./playing.mp3"))
        
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
    m = message.author.voice.mute or message.author.voice.self_mute
    d = message.author.voice.deaf or message.author.voice.self_deaf
    
    invoke_com = 'say'
    if (message.content.split(' '))[0] == invoke_com:
        await text_to_speech(message, message.content[len(invoke_com)+1:])

    elif m and not d and len(message.content) < threshold and message.content[0] != '=':
        await text_to_speech(message, message.content)


@bot.command(name='voice', help='Set a voice for text to speech.\nAvailable voices: David, Zira')
async def voi(ctx, arg):
    voice_names = [voice.name.split(' ')[1] for voice in voices]
    if arg in voice_names:
        vid = ''
        for voice in voices:
            if voice.name.split(' ')[1] == arg:
                vid = voice.id
        engine.setProperty('voice', vid)
        await ctx.send(f"Voice set to {arg}")
    else:
        await ctx.send(f"{arg} is not an option")

# @bot.command(name='mute-speech', help='Set to true/false\nSet to True if you want every message to be spoken out while you are muted.')
# async def mspeech(ctx, arg):
#     if arg == 'true':
#         mute_toggles[ctx.message.author] = True
#         ctx.send(f"Mute speech is on.")
#     elif arg == 'false':
#         mute_toggles[ctx.message.author] = False
#         ctx.send(f"Mute speech is off.")
#     else:
#         ctx.send(f"{arg} is not a valid option")

# @bot.command(name='show-voices', help='List available voices')
# async def voice(ctx):
#     display_text = "```"
#     for voice in voices:
#         display_text += f"\n{voice.name.split(' ')[1]}"
#     display_text += "```"
#     await ctx.send(display_text)

bot.run(TOKEN)


