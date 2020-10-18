# bot.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='=')

@bot.command(name='talk', help='Say something to the bot.')
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

bot.run(TOKEN)
