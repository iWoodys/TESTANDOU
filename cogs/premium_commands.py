import discord
from discord import app_commands
from discord.ext import commands
from firebase_admin import firestore
from premium import is_premium, set_premium, get_premium_expiry
import os

db = firestore.client()

BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID"))

class PremiumCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /premium_info
    @app_commands.command(name="premium_info", description="Muestra tu estado premium.")
    async def premium_info(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        expiry = get_premium_expiry(user_id)

        if not expiry:
            await interaction.response.send_message("🪙 No sos usuario premium actualmente.", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"✨ Sos premium hasta: **{expiry}** (UTC)", ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(PremiumCommands(bot))

