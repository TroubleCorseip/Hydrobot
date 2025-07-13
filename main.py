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

last_mood_message = None  # Stocke le dernier message envoyé

@bot.command()
async def mood(ctx, *, mood_type=None):
    global last_mood_message

    moods = {
        "uwu": "🐾 Mode UwU : tout est doux, tout est mignon.",
        "spm": "🔥 Mode SPM : éruption volcanique imminente.",
        "aigri": "💀 Mode Aigri : râler est une forme d’art.",
        "chaos": "🧨 Mode Chaos : les lois de la logique n'ont plus cours.",
        "mystique": "🔮 Mode Mystique : tout est signe, tout est fluide.",
        "sass": "👠 Mode Sass : tout est jugé, avec style.",
    }

    if mood_type and mood_type.lower() in moods:
        try:
            # Supprimer le message précédent si possible
            if last_mood_message:
                await last_mood_message.delete()
        except:
            pass  # On ignore les erreurs de suppression

        message = await ctx.send(f"{ctx.author.mention} {moods[mood_type.lower()]}")
        last_mood_message = message
    else:
        await ctx.send("🌀 Mood inconnu. Essaie : `!mood uwu`, `spm`, `aigri`, `chaos`, `mystique`, `sass`…")


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
