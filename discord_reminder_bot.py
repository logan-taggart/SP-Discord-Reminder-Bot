import asyncio
from datetime import datetime
import discord
from discord.ext import commands, tasks
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = 1356176312556847159

member1 = "<@1063175341608275988>"
member2 = "Lane"
member3 = "Caleb"

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

        await asyncio.sleep(60)


bot.run(os.getenv("DISCORD_TOKEN"))