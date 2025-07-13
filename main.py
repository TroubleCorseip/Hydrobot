import discord
from discord.ext import commands, tasks
import os
import random
from dotenv import load_dotenv
from keep_alive import keep_alive
import datetime

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
    "💧 Une gorgée d'eau pour chaque fois que t’as soupiré aujourd’hui.",
    "👊 Le skill ça passe aussi par une bonne hydratation.",
    "📣 Ceci est un rappel semi-automatisé. Bois. Maintenant. Merci."
]

user_hydration_count = {}
monthly_hydration = {}
last_mood_messages = {}
active_moods = {}

@bot.event
async def on_ready():
    print(f"{bot.user} est en ligne ✨")
    send_water_reminder.start()

@tasks.loop(hours=1)
async def send_water_reminder():
    now = datetime.datetime.now().time()
    if now >= datetime.time(23, 0) or now < datetime.time(7, 0):
        return
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        message = random.choice(MESSAGES)
        await channel.send(f"<@&{ROLE_ID}> {message}")

@bot.command()
async def hydrate(ctx):
    user = ctx.author
    user_hydration_count[user.name] = user_hydration_count.get(user.name, 0) + 1
    month = datetime.datetime.now().strftime("%Y-%m")
    if month not in monthly_hydration:
        monthly_hydration[month] = {}
    monthly_hydration[month][user.name] = monthly_hydration[month].get(user.name, 0) + 1

    sassy_messages = [
        f"{user.mention} 💦 C’est pas trop tôt, tu comptes survivre ou dessécher ?",
        f"{user.mention} T’as mis assez de temps à réagir, hein ? Bois maintenant !",
        f"{user.mention} Je t’ai vu. Tu boudes ta bouteille ? Mauvais plan.",
        f"{user.mention} Go boire ou je hurle à la lune."
    ]
    await ctx.send(random.choice(sassy_messages))

@bot.command()
async def mood(ctx, *, mood_type=None):
    moods = {
        "uwu": "🐾 Mode UwU : tout est doux, tout est mignon.",
        "spm": "🔥 Mode SPM : éruption volcanique imminente.",
        "aigri": "💀 Mode Aigri : râler est une forme d’art.",
        "chaos": "🧨 Mode Chaos : les lois de la logique n'ont plus cours.",
        "mystique": "✨ Mode Mystique : intuition x1000. Lis entre les lignes aujourd’hui.",
        "sass": "👠 Mode Sass : tout est jugé, avec style."
    }
    user_id = ctx.author.id
    if mood_type and mood_type.lower() in moods:
        if user_id in last_mood_messages:
            try:
                await last_mood_messages[user_id].delete()
            except:
                pass
        message = await ctx.send(f"{ctx.author.mention} {moods[mood_type.lower()]}")
        last_mood_messages[user_id] = message
        active_moods[user_id] = mood_type.lower()
    else:
        await ctx.send("🌀 Mood inconnu. Essaie : `!mood uwu`, `spm`, `aigri`, `chaos`, `mystique`, `sass`…")

@bot.command()
async def hydrostats(ctx):
    total = sum(user_hydration_count.values())
    stats_msg = f"📊 Total de rappels enregistrés : **{total}**\n"
    top_users = sorted(user_hydration_count.items(), key=lambda x: x[1], reverse=True)[:5]
    if top_users:
        stats_msg += "🥇 Top buveurs :\n"
        for user, count in top_users:
            stats_msg += f"- {user} : {count} verres\n"
    user_id = ctx.author.id
    if user_id in active_moods:
        stats_msg += f"\n🎭 Ton mood actuel : **{active_moods[user_id]}**"
    await ctx.send(stats_msg)

@bot.command()
async def topmois(ctx):
    month = datetime.datetime.now().strftime("%Y-%m")
    if month in monthly_hydration:
        top_users = sorted(monthly_hydration[month].items(), key=lambda x: x[1], reverse=True)[:5]
        msg = f"🏆 Classement hydratation - {month} :\n"
        for user, count in top_users:
            msg += f"- {user} : {count} verres\n"
        await ctx.send(msg)
    else:
        await ctx.send("Aucune donnée pour ce mois.")

@bot.command()
async def troublealcoolique(ctx):
    messages = [
        "🍷 Encore un verre ? T’es sûr ? Bon… santé, soldat de l’apéro !",
        "🥂 Tu carbures à quoi là ? L’élixir du dragon ancestral ?",
        "🫣 On dirait un build foi/alcool, c’est puissant mais instable."
    ]
    await ctx.send(random.choice(messages))

@bot.command()
async def verredevin(ctx):
    messages = [
        "🍇 Un petit rouge pour oublier les boss impossibles ? Santé.",
        "🍷 Lara Croft aurait survécu à tout, mais un bon vin lui aurait fait plaisir aussi.",
        "🧛‍♀️ C’est pas du sang, c’est juste un très vieux millésime."
    ]
    await ctx.send(random.choice(messages))

@bot.command()
async def calimero(ctx):
    messages = [
        "😭 J’ai raté mon esquive, j’ai plus d’estus, j’ai mal au cœur.",
        "😩 Pourquoi tout le monde meurt sauf moi quand je veux farmer tranquille ?",
        "🫠 Y a des jours où même mon cheval dans Elden Ring veut pas coopérer."
    ]
    await ctx.send(random.choice(messages))

keep_alive()
bot.run(TOKEN)
