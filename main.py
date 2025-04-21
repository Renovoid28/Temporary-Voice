import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
VC_CATEGORY_ID = int(os.getenv("VC_CATEGORY_ID"))
VC_TRIGGER_ID = int(os.getenv("VC_TRIGGER_ID"))

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
temp_channels = {}

@bot.event
async def on_ready():
    print(f"Bot aktif sebagai {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.id == VC_TRIGGER_ID:
        guild = member.guild
        category = guild.get_channel(VC_CATEGORY_ID)
        new_channel = await guild.create_voice_channel(
            name=f"{member.name}'s VC",
            category=category
        )
        temp_channels[member.id] = new_channel.id
        await member.move_to(new_channel)

    if before.channel and before.channel.id in temp_channels.values():
        if len(before.channel.members) == 0:
            await before.channel.delete()
            for uid, cid in list(temp_channels.items()):
                if cid == before.channel.id:
                    del temp_channels[uid]

bot.run(TOKEN)
