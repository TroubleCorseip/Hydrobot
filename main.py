import discord
from discord.ext import commands, tasks
import os
import random
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

MESSAGES = [
    "🫧 Hé toi, hydratation check ! Va boire un bon verre d’eau maintenant 💦",
    "🌿 Boire de l’eau c’est pas négociable, c’est sacré.",
    "🥤 Troublemode : ACTIVÉ → Bouteille d’eau dans la main, go !",
    "🕒 T’as survécu une heure de plus, célèbre ça avec un verre d’eau.",
    "🌙 Même les boss de FromSoftware boivent… et toi ?",
]

@bot.event
async def on_ready():
    print(f"{bot.user} est en ligne ✨")
    send_water_reminder.start()

@tasks.loop(hours=1)
async def send_water_reminder():
    now = datetime.now()
    if 7 <= now.hour < 23:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            message = random.choice(MESSAGES)
            await channel.send(f"<@&{ROLE_ID}> {message}")

@bot.command()
async def hydrate(ctx):
    phrases = [
        "🚨 Tu savais que 73% de ton sel est constitué d'eau ? BOIS !",
        "💧Pas d’eau, pas de skill. C’est la base.",
        "🧠 Tu veux rivaliser avec les boss de Sekiro ? Commence par t’hydrater.",
        "👀 Même Lara Croft pense que t’as l’air desséché·e."
    ]
    await ctx.send(f"{ctx.author.mention} {random.choice(phrases)}")

@bot.command()
async def mood(ctx):
    moods = [
        "😈 Mode Chaos : déclenché. Prépare-toi à faire n’importe quoi.",
        "✨ Mode Mystique : intuition x1000. Lis entre les lignes aujourd’hui.",
        "😒 Mode Aigri : ne pas déranger. Tu grognes au moindre bruit.",
        "🔥 Mode SPM : éruption volcanique imminente.",
        "🐾 Mode UwU : tout est doux, tout est mignon."
    ]
    await ctx.send(f"{ctx.author.mention} {random.choice(moods)}")

keep_alive()
bot.run(TOKEN)
