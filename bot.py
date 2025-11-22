
import discord
from discord.ext import commands
import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("MTQ0MTc2MTQ3NDMyNTM4NTI1OA.GE4Jb5.wbP5Wo3ZE9ZNfgTQINe98VY_O13hT4C2mf2hOM")
LOADOUT_CHANNEL_ID = int(os.getenv("1441762137591517244"))
COMMAND_PREFIX = "!"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# Battlefield Infinity (battlefinity.gg) loadout çekme fonksiyonu
def fetch_loadout(weapon_name):
    url = f"https://battlefinity.gg/?s={weapon_name.replace(' ', '+')}"
    print("Checking URL:", url)

    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Silah ismi
    title = soup.find("h2", class_="post-title")
    if not title:
        return None

    weapon_title = title.text.strip()

    # Silah resmi
    img = soup.find("img")
    image_url = img["src"] if img else None

    # İçerik açıklaması
    content = soup.find("div", class_="post-excerpt")
    description = content.text.strip() if content else "Açıklama bulunamadı."

    return weapon_title, image_url, description


@bot.event
async def on_ready():
    print(f"BF6 Loadout Bot Online: {bot.user}")


@bot.command(name="loadout")
async def loadout(ctx, *, weapon: str):
    if ctx.channel.id != LOADOUT_CHANNEL_ID:
        return await ctx.send("Bu komut sadece belirlenen loadout kanalında kullanılabilir.")

    await ctx.send(f"🔍 **{weapon}** için loadout aranıyor...")

    data = fetch_loadout(weapon)
    if not data:
        return await ctx.send("❌ Loadout bulunamadı.")

    title, image_url, desc = data

    embed = discord.Embed(
        title=f"🔫 {title} - BF6 Loadout",
        description=desc,
        color=discord.Color.green()
    )

    if image_url:
        embed.set_image(url=image_url)

    await ctx.send(embed=embed)


bot.run(TOKEN)
