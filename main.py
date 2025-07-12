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
bot = commands.Bot(command_prefix='!', intents=intents)

# ---------------------- MODES D’HUMEUR ----------------------
MOODS = {
    "default": [
        "🫧 Hé toi, hydratation check ! Va boire un bon verre d’eau maintenant 💦",
        "🌿 Boire de l’eau c’est pas négociable, c’est sacré.",
        "🥤 Troublemode : ACTIVÉ → Bouteille d’eau dans la main, go !",
        "🕒 T’as survécu une heure de plus, célèbre ça avec un verre d’eau.",
        "🌙 Même les boss de FromSoftware boivent… et toi ?",
    ],
    "chaos": [
        "💥 VA BOIRE ou j’envoie des gremlins dans tes canalisations.",
        "⚡ Une goutte de plus, une neurone de sauvée. Vas-y.",
        "🔥 Ce message s’autodétruira si tu bois pas dans 10 secondes.",
    ],
    "mystique": [
        "🔮 Une entité t’observe et attend que tu boives… maintenant.",
        "🌙 Les étoiles murmurent : hydratation ou damnation.",
        "✨ Ta destinée dépend de cette gorgée sacrée.",
    ],
    "aigri": [
        "🙄 Encore à sécher comme une plante oubliée ? Tsss.",
        "💧 Même les gens pas drôles ont besoin d’eau.",
        "😒 Bois. Pas pour moi. Pour ton cerveau en fin de vie.",
    ],
    "UwU": [
        "✨ OwO bois un ptit verre d’eau, pwetty pwease ? ✨",
        "💦 Hii~ le botou veut que tu t’hydwates~",
        "🥺 T’as pas envie que j’cwise en sec, hein ? Bois~",
    ],
    "spm": [
        "🩸 T’as pas envie de mourir déshydratée en phase lutéale non ?",
        "💀 Ta fatigue, ton humeur, tes larmes ? Bois un verre d’eau.",
        "⚠️ Alerte rouge : hydratation vitale. T’as le droit de pleurer après.",
    ],
    "sass": [
        "👑 Tu veux régner ? Bois d’abord.",
        "💅 L’eau ? C’est le secret des queens. Et t’en es une.",
        "🧊 Tu veux être glaciale et irrésistible ? Commence par un verre d’eau.",
    ]
}

current_mood = "default"
manual_count = {}

# ---------------------- COMMANDES ----------------------
@bot.event
async def on_ready():
    print(f"{bot.user} est en ligne ✨")
    send_water_reminder.start()

@bot.command()
async def hydrate(ctx):
    global manual_count
    user = ctx.author
    message = random.choice(MOODS.get(current_mood, MOODS["default"]))
    await ctx.send(f"{user.mention} {message}")

    # Statistiques
    manual_count[user.name] = manual_count.get(user.name, 0) + 1

@bot.command()
async def mood(ctx, *, mood_type):
    global current_mood
    mood_type = mood_type.lower()
    if mood_type in MOODS:
        current_mood = mood_type
        await ctx.send(f"🌡️ Hydrobot est maintenant en humeur **{mood_type}**.")
    else:
        await ctx.send(f"❌ Humeur inconnue. Les humeurs disponibles sont : {', '.join(MOODS.keys())}")

@bot.command()
async def hydrostats(ctx):
    global manual_count
    total = sum(manual_count.values())
    leaderboard = sorted(manual_count.items(), key=lambda x: x[1], reverse=True)
    ranking = "\n".join([f"{i+1}. {name} : {count} fois" for i, (name, count) in enumerate(leaderboard)])
    await ctx.send(f"📊 **Hydrostats** :\nTotal de rappels manuels : {total}\n\n**Classement** :\n{ranking if ranking else 'Aucune donnée 🫠'}")

# ---------------------- RAPPEL AUTO ----------------------
@tasks.loop(hours=1)
async def send_water_reminder():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        message = random.choice(MOODS.get(current_mood, MOODS["default"]))
        await channel.send(f"<@&{ROLE_ID}> {message}")

# ---------------------- KEEP ALIVE ----------------------
keep_alive()

bot.run(TOKEN)
