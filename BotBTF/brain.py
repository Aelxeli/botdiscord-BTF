import discord
import os
import sys
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Força o console a usar UTF-8 no Windows para evitar erros de caractere (emojis)
if sys.platform == "win32":
    import subprocess
    subprocess.call('chcp 65001', shell=True)

# Carrega variáveis de ambiente (.env)
base_path = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_path, '.env'))
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", "/")

class BTFBot(commands.Bot):
    def __init__(self):
        # ATENÇÃO: Para o bot ler comandos com prefixo (como ! ou /),
        # você PRECISA ativar a opção "Message Content Intent" no Discord Developer Portal!
        intents = discord.Intents.default()
        intents.message_content = True # Habilita a leitura de mensagens para comandos
        intents.members = True         # Habilita o rastreio de membros para XP e Rank

        super().__init__(
            command_prefix="/",
            intents=intents,
            help_command=None
        )
        self.color_purple = 0x9b59b6
        self.color_blue = 0x3498db

    async def setup_hook(self):
        print("--- Carregando Cogs ---")
        cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    print(f"[OK] {filename}")
                except Exception as e:
                    print(f"[ERRO] {filename}: {e}")
        print("--- Pronto! ---\n")

    async def on_message(self, message):
        # Ignora mensagens de outros bots
        if message.author.bot:
            return
        
        # Tenta processar comandos
        await self.process_commands(message)

    async def on_ready(self):
        print(f"Bot Online: {self.user}")
        await self.change_presence(activity=discord.Game(name="/help"))

async def main():
    if not TOKEN:
        print("ERRO: DISCORD_TOKEN não encontrado no .env")
        return
    bot = BTFBot()
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
