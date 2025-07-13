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
import random

@bot.command()
async def hydrostats(ctx):
    messages = [
        "📊 Statistiques indisponibles pour l’instant. Mais t’as bu combien de verres aujourd’hui, hein ?",
        "📉 Stats en pause… comme ton envie de te lever de ton fauteuil.",
        "📈 T’es en haut du classement, ou au fond du tonneau ? Mystère.",
    ]
    await ctx.send(random.choice(messages))

@bot.command()
async def troublealcoolique(ctx):
    messages = [
        f"🍷 {ctx.author.mention}, une lampée de vin et tu oublies que t’as encore pas fini Sekiro.",
        f"🥃 {ctx.author.mention}, tu verses un verre pour chaque mort sur Elden Ring ? Le foie est en PLS.",
        f"🍺 {ctx.author.mention}, boire pour oublier que Leno existe ? Validé.",
        f"🍹 {ctx.author.mention}, encore un verre et t’arrives à battre Artorias les yeux fermés.",
    ]
    await ctx.send(random.choice(messages))

@bot.command()
async def verredevin(ctx):
    messages = [
        f"🍇 {ctx.author.mention}, un verre de vin c’est un verre d’eau en plus… en plus joyeux.",
        f"🍷 {ctx.author.mention}, tu veux l’aération du nez à l’ancienne ? Tire une gorgée.",
        f"🧛 {ctx.author.mention}, le vin c’est du sang de boss FromSoftware filtré par l’émotion. Santé.",
    ]
    await ctx.send(random.choice(messages))

@bot.command()
async def calimero(ctx):
    messages = [
        f"😭 {ctx.author.mention}, *encore* mort à un millimètre de vie du boss ? Oui, c’est injuste.",
        f"🖤 {ctx.author.mention} est en mode 'je boude dans la bonfire zone'.",
        f"🎭 {ctx.author.mention}, t’as perdu contre un mob nul ? Viens, on pleure ensemble sur une save corrompue.",
        f"💢 {ctx.author.mention}, 'LIFE IS PAIN' édition spéciale FromSoft, servi chaud dans ton mug Calimero™️.",
    ]
    await ctx.send(random.choice(messages))

keep_alive()
bot.run(TOKEN)
