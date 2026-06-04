import discord

# Cores baseadas na logo BTF (Neon Purple/Blue)
BTF_PURPLE = 0x9b59b6
BTF_BLUE = 0x3498db
BTF_DARK = 0x2c3e50

def get_embed(title=None, description=None, color=BTF_PURPLE):
    embed = discord.Embed(title=title, description=description, color=color)
    return embed

async def set_bot_logo(bot, image_path):
    """
    Função utilitária para mudar a logo do bot.
    Requer que o bot esteja logado.
    """
    with open(image_path, 'rb') as f:
        await bot.user.edit(avatar=f.read())
