import discord
from discord.ext import commands, tasks
import os
import random
from dotenv import load_dotenv
from keep_alive import keep_alive

# Charger les variables d'environnement
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Important !

bot = commands.Bot(command_prefix='!', intents=intents)

# Messages d’hydratation automatique
MESSAGES = [
    "🫧 Hé toi, hydratation check ! Va boire un bon verre d’eau maintenant 💦",
    "🌿 Boire de l’eau c’est pas négociable, c’est sacré.",
    "🥤 Troublemode : ACTIVÉ → Bouteille d’eau dans la main, go !",
    "🕒 T’as survécu une heure de plus, célèbre ça avec un verre d’eau.",
    "🌙 Même les boss de FromSoftware boivent… et toi ?",
]

# Réponses piquantes pour la commande !hydrate
HYDRATE_REPLIES = [
    "🧃 Tu veux un rappel perso ? Va boire ou je t’arrose moi-même.",
    "💢 Lève-toi et bois, flemmard·e ! Tu crois que c’est optionnel ?",
    "🥵 Tu transpires le sel, bois de l’eau avant d’être un crouton.",
    "😈 Tu veux un fouet ou tu bois gentiment ?",
]

# Dictionnaire des moods
MOODS = {
    "chaos": "🌪️ Mode Chaos activé. Attache ta gourde.",
    "mystique": "🔮 Les astres disent : hydrate-toi.",
    "aigri": "🙄 Encore une heure, encore un verre. Tu veux une médaille ?",
    "spm": "💢 T’as intérêt à boire si tu veux pas t’évanouir en hurlant.",
    "UwU": "🌸 OwO bois de l'eau senpaiiii~",
}

@bot.event
async def on_ready():
    print(f"{bot.user} est en ligne 🌊")
    send_water_reminder.start()

# Rappel automatique chaque heure
@tasks.loop(hours=1)
async def send_water_reminder():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        message = random.choice(MESSAGES)
        await channel.send(f"<@&{ROLE_ID}> {message}")

# Commande !hydrate
@bot.command()
async def hydrate(ctx):
    reply = random.choice(HYDRATE_REPLIES)
    await ctx.send(f"{ctx.author.mention} {reply}")

# Commande !mood
@bot.command()
async def mood(ctx, mode: str = None):
    if not mode:
        await ctx.send("🌀 Précise un mood : chaos, mystique, aigri, spm ou UwU.")
        return
    mood = MOODS.get(mode.lower())
    if mood:
        await ctx.send(f"{ctx.author.mention} {mood}")
    else:
        await ctx.send("❌ Ce mood n’existe pas. Essaie : chaos, mystique, aigri, spm, UwU.")

# Lancer le serveur web pour Render
keep_alive()

# Lancer le bot
bot.run(TOKEN)
N)
