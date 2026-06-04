import discord
from discord.ext import commands
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def notify_action(self, ctx, title, description, target=None):
        """Função utilitária para sinalizar ações no chat com identidade visual BTF."""
        embed = discord.Embed(
            title=title,
            description=description,
            color=self.bot.color_purple,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        if target:
            embed.set_thumbnail(url=target.display_avatar.url)
        embed.set_footer(text=f"Ação por {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        
        await ctx.send(embed=embed)

    @commands.command(name="clear", aliases=["limpar", "purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        """Limpa uma quantidade específica de mensagens no chat."""
        await ctx.channel.purge(limit=amount + 1)
        await self.notify_action(ctx, "🧹 Chat Limpo", f"Foram removidas **{amount}** mensagens deste canal.")

    @commands.command(name="slowmode", aliases=["lento"])
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        """Define o modo lento para o canal atual."""
        await ctx.channel.edit(slowmode_delay=seconds)
        status = f"definido para **{seconds}s**" if seconds > 0 else "desativado"
        await self.notify_action(ctx, "⏳ Modo Lento", f"O modo lento foi {status}.")

    @commands.command(name="kick", aliases=["expulsar"])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Não informado"):
        """Expulsa um membro do servidor."""
        await member.kick(reason=reason)
        await self.notify_action(ctx, "👢 Membro Expulso", f"**{member.mention}** foi removido do servidor.\n**Motivo:** {reason}", target=member)

    @commands.command(name="ban", aliases=["banir"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Não informado"):
        """Bane um membro do servidor."""
        await member.ban(reason=reason)
        await self.notify_action(ctx, "🔨 Membro Banido", f"**{member.mention}** foi banido permanentemente.\n**Motivo:** {reason}", target=member)

    @commands.command(name="mute", aliases=["silenciar", "timeout"])
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int = 10, *, reason="Não informado"):
        """Silencia um membro usando o sistema de timeout do Discord."""
        duration = datetime.timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await self.notify_action(ctx, "🔇 Membro Silenciado", f"**{member.mention}** foi silenciado por **{minutes} minutos**.\n**Motivo:** {reason}", target=member)

    @commands.command(name="unmute", aliases=["dessilenciar"])
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason="Não informado"):
        """Remove o silêncio de um membro."""
        await member.timeout(None, reason=reason)
        await self.notify_action(ctx, "🔊 Silêncio Removido", f"O silêncio de **{member.mention}** foi removido.", target=member)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description="❌ Você não tem permissão para usar este comando!", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(description="❌ Membro não encontrado!", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description=f"❌ Argumento faltando! Use `{ctx.prefix}help {ctx.command}`", color=0xff0000)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
