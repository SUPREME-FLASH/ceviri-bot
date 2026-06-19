import discord
from discord.ext import commands
from deep_translator import GoogleTranslator

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Kullanıcıların dil tercihlerini tutan sözlük
user_languages = {}

@bot.event
async def on_ready():
    print(f"{bot.user} aktif!")

# Kullanıcı kendi dilini ayarlıyor: !dil en
@bot.command()
async def dil(ctx, lang_code):
    user_languages[ctx.author.id] = lang_code
    await ctx.send(f"✅ Dil tercihin kaydedildi: **{lang_code}**")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)

    # Kullanıcının hedef dili
    target_lang = user_languages.get(message.author.id, "tr")

    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(message.content)

        # Embed mesaj oluştur
        embed = discord.Embed(
            title="🌐 Otomatik Çeviri",
            description=f"**{message.author.display_name}** için çeviri yapıldı",
            color=0x3498db
        )
        embed.add_field(name="📥 Orijinal Mesaj", value=message.content, inline=False)
        embed.add_field(name=f"📤 Çevrilen ({target_lang})", value=translated, inline=False)
        embed.set_footer(text="Çeviri sistemi aktif")

        await message.channel.send(embed=embed)

    except Exception as e:
        await message.channel.send(f"Hata oluştu: {e}")

import os
bot.run(os.getenv("TOKEN"))

