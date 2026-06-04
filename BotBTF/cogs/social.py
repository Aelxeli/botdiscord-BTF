import discord
from discord.ext import commands
import random

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = [
            "Sim, com certeza! ✨",
            "Minhas fontes dizem que sim. ✅",
            "Provavelmente... 🤔",
            "Não conte com isso. ❌",
            "Minha resposta é não. 🛑",
            "Pergunte novamente mais tarde... 😴",
            "Melhor não te dizer agora... 🤐",
            "Sinais apontam que sim! 💎",
            "Muito duvidoso. 🤨",
            "Sem dúvida! 🚀"
        ]

    @commands.command(name="8ball", aliases=["vidente", "bola8"])
    async def eight_ball(self, ctx, *, question):
        """Faz uma pergunta para a bola 8 mágica."""
        response = random.choice(self.responses)
        
        embed = discord.Embed(
            title="🔮 Bola 8 Mágica",
            color=self.bot.color_purple
        )
        embed.add_field(name="Sua Pergunta:", value=question, inline=False)
        embed.add_field(name="Minha Resposta:", value=response, inline=False)
        embed.set_footer(text=f"Solicitado por {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, ctx):
        """Verifica a latência do bot."""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Latência: **{latency}ms**")

    @commands.command(name="invite", aliases=["convite", "convidar"])
    async def invite(self, ctx):
        """Gera o link de convite oficial do Botequinho com todas as permissões."""
        url = "https://discord.com/oauth2/authorize?client_id=1510124945018192003&permissions=8&response_type=code&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fbotequinho&integration_type=0&scope=application_identities.write+applications.commands.permissions.update+sdk.social_layer_presence+gateway.connect+openid+role_connections.write+relationships.write+activities.write+applications.store.update+applications.builds.upload+rpc.activities.write+rpc.video.write+rpc.voice.read+bot+guilds.members.read+identify+connections+sdk.social_layer+account.global_name.update+dm_channels.messages.read+presences.read+activities.invites.write+voice+applications.entitlements+applications.builds.read+webhook.incoming+rpc.screenshare.read+rpc.voice.write+rpc+guilds.channels.read+guilds+identify.premium+email+guilds.join+gdm.join+rpc.notifications.read+rpc.video.read+rpc.screenshare.write+messages.read+applications.commands+activities.read+relationships.read+dm_channels.read+presences.write+dm_channels.messages.write+payment_sources.country_code+lobbies.write"
        
        embed = discord.Embed(
            title="📥 Convite Oficial - Botequinho",
            description=f"Para me adicionar ao seu servidor com todas as permissões necessárias, clique [AQUI]({url}).\n\n**Configuração:** Administrador (ID: 8) + Scopes Avançados",
            color=self.bot.color_blue
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text="Botequinho BTF - Link de Autorização")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Social(bot))
