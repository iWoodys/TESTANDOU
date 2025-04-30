import discord
from discord import app_commands
from discord.ext import commands
from firebase_admin import firestore
from premium import is_premium, set_premium, get_premium_expiry
import os

db = firestore.client()

# Reemplaza con tu ID real
BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID"))

class PremiumCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /add_load
    @app_commands.command(name="add_load", description="Agrega un nuevo loadout.")
    @app_commands.describe(nombre="Nombre del arma", datos="Detalles del loadout")
    async def add_load(self, interaction: discord.Interaction, nombre: str, datos: str):
        user_id = str(interaction.user.id)
        server_id = str(interaction.guild.id)

        # Referencia a los loadouts del usuario
        user_ref = db.collection("loadouts").document(server_id).collection("users").document(user_id)
        doc = user_ref.get()

        loadouts = doc.to_dict().get("loadouts", {}) if doc.exists else {}

        if not is_premium(user_id) and len(loadouts) >= 5:
            await interaction.response.send_message(
                "❌ Alcanzaste el límite de 5 loadouts. Hazte premium para guardar más.",
                ephemeral=True
            )
            return

        loadouts[nombre] = {"data": datos}

        user_ref.set({"loadouts": loadouts}, merge=True)

        await interaction.response.send_message(
            f"✅ Loadout **{nombre}** guardado correctamente.",
            ephemeral=True
        )

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
