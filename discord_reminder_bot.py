import asyncio
from datetime import datetime
import discord
from discord.ext import commands, tasks
from flask import Flask
import os
from threading import Thread


# --- Flask Keep-Alive Setup ---
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Discord Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = 1328854763000823851

member1 = "<@1063175341608275988>"  # Logan
member2 = "<@446875072381059073>" # Lane
member3 = "<@163724371263750144>" # Caleb

rotation = [member2, member3, member1]
reminder_enabled = True

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print("Bot is ready.")
    reminder.start()

@tasks.loop(minutes=1)
async def reminder():
    now = datetime.now()
    if now.weekday() == 4 and now.hour == 10 and now.minute == 0 and reminder_enabled:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("@everyone Don’t forget status reports today")

            week_num = now.isocalendar()[1]
            assigned = rotation[week_num % len(rotation)]

            await channel.send(f"Also {assigned} has the team report for this week")

# --- Start Everything ---
keep_alive()  # Start Flask server for pinging
bot.run(os.getenv("DISCORD_TOKEN"))  # Start Discord bot
