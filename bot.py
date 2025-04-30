import discord
from discord.ext import commands
import os
import asyncio
from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))
BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID"))

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.voice_states = True
intents.message_content = True  # Necesario si usás comandos de texto

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="2.783.128 Players in Warzone"
    ))
    print(f'✅ Bot conectado como {bot.user}')

async def load_extensions():
    await bot.load_extension("cogs.warzone")
    await bot.load_extension("cogs.premium_commands")
    synced = await bot.tree.sync()
    print(f"✅ Comandos slash sincronizados: {len(synced)}")

async def main():
    keep_alive()  # Activa el servidor Flask para Render
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())
