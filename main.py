# Version avec sauvegarde des stats dans un fichier JSON et modes d'humeur dynamiques

import discord
from discord.ext import commands, tasks
import os
import random
import asyncio
from keep_alive import keep_alive
from dotenv import load_dotenv
from datetime import datetime
import json

# Charger les variables d’environnement
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))

# Initialisation du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Fichier de stats
STATS_FILE = "hydro_stats.json"
if os.path.exists(STATS_FILE):
    with open(STATS_FILE, "r") as f:
        stats = json.load(f)
else:
    stats = {
        "hydrate_count": 0,
        "manual_hydrate_calls": {},
        "monthly_calls": {},
        "current_mood": "doux"
    }

def save_stats():
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)

# Dictionnaire des humeurs
MOODS = {
    "doux": [
        "🌸 Une petite gorgée d'eau et tout ira mieux.",
        "🍃 Respire, bois, recommence.",
        "💧 Hydrate-toi, t’es précieux.se."
    ],
    "rigolo": [
        "🤣 Si tu bois pas d'eau, c’est ton corps qui va faire un bug Windows.",
        "🤡 Une gorgée d’eau pour chaque neurone encore connecté.",
        "🍺 Pas de panique, c’est juste de l’eau. (T'es pas un gremlin hein ?)"
    ],
    "agressif": [
        "🔪 Bois. De. L’eau. Ou je t’hydrate moi-même.",
        "⚠️ T’as 5 secondes pour boire sinon j’arrive avec une bassine.",
        "💢 Tu veux déshydrater comme une vieille figue ? Non ? Alors BOIS."
    ],
    "sass": [
        "💅 Une reine s’hydrate. T’es pas une vieille chips.",
        "👑 Bois comme si ton teint dépendait de ça (spoiler : il dépend de ça).",
        "✨ L’eau c’est le skincare du cœur."
    ],
    "badass": [
        "🔥 Même Artorias aurait bu de l’eau là.",
        "💀 Les vrais champions boivent entre deux claques de boss.",
        "🗡️ Bois de l’eau. Puis brise des chaînes."
    ],
    "chaos": [
        "🌀 Le monde brûle, mais toi tu vas boire un verre d’eau comme si de rien n’était.",
        "💣 Et si tu buvais une gorgée pour chaque pensée intrusive ? Challenge accepté.",
        "🎲 Gloire au hasard, hydratation incluse."
    ],
    "mystique": [
        "🔮 L’eau est mémoire. Honore ton corps, élève ton âme.",
        "🌕 Une gorgée d’eau sous la lune, un pacte avec toi-même.",
        "🧿 Hydrate-toi. Les guides t’observent."
    ],
    "aigri": [
        "🙄 Encore un rappel. Ouais. Bois de l’eau si t’y tiens tant que ça.",
        "😒 Tu vas pas exploser de joie, mais au moins t’es pas sec comme un vieux cactus.",
        "😑 Voilà, bois. Moi je m’en fous hein."
    ],
    "spm": [
        "😩 T’as mal, t’es à cran, mais tu vas BOIRE cette foutue eau.",
        "🫠 Eau + chocolat + plaid = combo vital. Vas-y.",
        "🌪️ Avant de crier ou pleurer, bois. Après, fais-toi plaisir."
    ],
    "uwu": [
        "🥺 pwease dwink wawa ou je cwy...", 
        "🌸 watertime uwu", 
        "✨ hydwation is impowtant~" 
    ]
}

@bot.event
async def on_ready():
    print(f"{bot.user} est en ligne ✨")
    send_water_reminder.start()

@tasks.loop(hours=1)
async def send_water_reminder():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        stats["hydrate_count"] += 1
        save_stats()
        mood = stats.get("current_mood", "doux")
        message = random.choice(MOODS[mood])
        await channel.send(f"<@&{ROLE_ID}> {message}")

@bot.command()
async def hydrate(ctx):
    user = ctx.author.name
    today = datetime.now().strftime("%Y-%m")
    stats["manual_hydrate_calls"][user] = stats["manual_hydrate_calls"].get(user, 0) + 1
    if today not in stats["monthly_calls"]:
        stats["monthly_calls"][today] = {}
    stats["monthly_calls"][today][user] = stats["monthly_calls"][today].get(user, 0) + 1
    save_stats()
    message = random.choice([
        f"🔔 {user}, t'as soif de victoire ou de calcium ? Peu importe, bois.",
        f"🩷 {user}, même les queens s’hydratent. Allez hop.",
        f"🥤 {user}, chaque gorgée = un pas vers la grandeur.",
        f"💦 {user} fait 'glou glou' comme un champion. T'as mérité un bisou astral."
    ])
    await ctx.send(f"<@&{ROLE_ID}> {message}")

@bot.command()
async def hydrostats(ctx):
    msg = f"📊 Total de rappels envoyés : {stats['hydrate_count']}\n"
    if stats["manual_hydrate_calls"]:
        msg += "👥 Classement général des buveurs :\n"
        sorted_users = sorted(stats["manual_hydrate_calls"].items(), key=lambda x: x[1], reverse=True)
        for i, (user, count) in enumerate(sorted_users, 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "💧"
            msg += f"{emoji} {user} : {count} fois\n"
    else:
        msg += "Personne n’a encore utilisé `!hydrate` manuellement 🪠"
    await ctx.send(msg)

@bot.command()
async def topmois(ctx):
    today = datetime.now().strftime("%Y-%m")
    if today in stats["monthly_calls"]:
        msg = f"📅 Classement pour {today} :\n"
        sorted_month = sorted(stats["monthly_calls"][today].items(), key=lambda x: x[1], reverse=True)
        for i, (user, count) in enumerate(sorted_month, 1):
            emoji = "🏆" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "💧"
            msg += f"{emoji} {user} : {count} fois\n"
    else:
        msg = "Aucun appel ce mois-ci 🛌"
    await ctx.send(msg)

@bot.command()
async def mood(ctx, *, mood_choice):
    if mood_choice in MOODS:
        stats["current_mood"] = mood_choice
        save_stats()
        await ctx.send(f"🎭 Humeur changée pour : **{mood_choice}**")
    else:
        await ctx.send(f"❌ Humeur inconnue. Choisis parmi : {', '.join(MOODS.keys())}")

keep_alive()
bot.run(TOKEN)
