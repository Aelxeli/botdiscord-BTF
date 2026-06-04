import discord
from discord.ext import commands

class Notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Em um sistema real, isso seria salvo no banco de dados
        self.special_keywords = ["importante", "ajuda", "btf", "admin"]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content_lower = message.content.lower()
        for keyword in self.special_keywords:
            if keyword in content_lower:
                # Notifica em um canal de logs (se configurado) ou apenas destaca
                # Por agora, vamos apenas simular uma reação ou resposta especial
                # Idealmente, o bot enviaria um alerta para os moderadores
                pass

    @commands.command(name="notify", aliases=["notificar"])
    @commands.has_permissions(administrator=True)
    async def notify_all(self, ctx, *, text):
        """Envia uma notificação especial em formato de anúncio."""
        embed = discord.Embed(
            title="📢 AVISO ESPECIAL BTF",
            description=text,
            color=0xff0000 # Vermelho para destaque
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url if self.bot.user else None)
        embed.set_footer(text="BTF Notification System")
        
        await ctx.send("@everyone", embed=embed)

async def setup(bot):
    await bot.add_cog(Notifications(bot))
