import discord
import os
import asyncio
import random
from discord.ext import commands, tasks
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Listes des messages selon les moods
REMINDER_MESSAGES = [
    "🫧 Hé toi, hydratation check ! Va boire un bon verre d’eau maintenant 💦",
    "🌿 Boire de l’eau c’est pas négociable, c’est sacré.",
    "🥤 Troublemode : ACTIVÉ → Bouteille d’eau dans la main, go !",
    "🕒 T’as survécu une heure de plus, célèbre ça avec un verre d’eau.",
    "🌙 Même les boss de FromSoftware boivent… et toi ?",
]

HYDRATE_RESPONSES = [
    "💧 *Encore toi ?* T’as pas compris que c’est pas optionnel ?",
    "🫠 Tu veux te transformer en raisin sec ? Bois. Maintenant.",
    "💦 L’eau, c’est la base. Tu crois que Miyazaki carbure à quoi ?",
    "😤 C’est pas une option, c’est un ordre. BOUA !",
    "🥵 T’as chaud ? C’est ton karma qui brûle. Va boire."
]

TROUBLE_ALCOOL_RESPONSES = [
    "⚠️ Trouble Alert : Alcoolémie détectée. On t’a dit de boire de l’eau, pas du Pinot Noir. Repose ce verre, Jean-Michel Sommelière du dimanche. 🥴",
    "🚨 Hydrobot t’observe. Ce n’est PAS un verre d’eau, ce truc rouge. 🍷",
    "🤡 Encore un verre et je t’envoie la SPA pour ton foie."
]

VERREDEVIN_RESPONSES = [
    "🍷 Santé ! On trinque à tes reins qui pleurent et à ton foie qui envoie sa lettre de démission.",
    "🍷 T’as le droit à ton petit moment Dionysiaque. Mais hydrate-toi après, hein, Troublinette. 💧",
    "🍷 Un verre ok. Deux ? Bon. Trois ? Je déclenche les sirènes."
]

@bot.event
async def on_ready():
    print(f"{bot.user} est en ligne ✨")
    send_water_reminder.start()

@tasks.loop(hours=1)
async def send_water_reminder():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        message = random.choice(REMINDER_MESSAGES)
        await channel.send(f"<@&{ROLE_ID}> {message}")

@bot.command()
async def hydrate(ctx):
    response = random.choice(HYDRATE_RESPONSES)
    await ctx.send(f"{ctx.author.mention} {response}")

@bot.command()
async def troublealcoolique(ctx):
    response = random.choice(TROUBLE_ALCOOL_RESPONSES)
    await ctx.send(f"{ctx.author.mention} {response}")

@bot.command()
async def verredevin(ctx):
    response = random.choice(VERREDEVIN_RESPONSES)
    await ctx.send(f"{ctx.author.mention} {response}")

keep_alive()
bot.run(TOKEN)
