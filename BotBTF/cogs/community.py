import discord
from discord.ext import commands
import random
import asyncio

class Community(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = [
            "Valorant", "Personalizada", "BapBap", "Brawlhalla", 
            "Poker", "Sinuca", "Minecraft", "CS2", "Gartic Phone"
        ]

    @commands.command(name="game")
    async def game(self, ctx):
        """Escolhe um jogo aleatório para a galera jogar."""
        escolha = random.choice(self.games)
        embed = discord.Embed(
            title="🎮 Hora de Jogar!",
            description=f"O jogo escolhido da vez foi: **{escolha}**",
            color=self.bot.color_purple
        )
        embed.set_footer(text="Botequinho BTF - Diversão garantida")
        await ctx.send(embed=embed)

    @commands.command(name="join")
    async def join(self, ctx):
        """Faz o bot entrar em um canal de voz aleatório do servidor."""
        voice_channels = ctx.guild.voice_channels
        if not voice_channels:
            return await ctx.send("Não encontrei canais de voz neste servidor!")
        
        target_channel = random.choice(voice_channels)
        
        if ctx.voice_client:
            await ctx.voice_client.move_to(target_channel)
        else:
            await target_channel.connect()
            
        await ctx.send(f"🎤 Entrei no canal de voz: **{target_channel.name}**")

    @commands.command(name="leave")
    async def leave(self, ctx):
        """Faz o bot sair do canal de voz."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Saí da call!")
        else:
            await ctx.send("Não estou em nenhuma call no momento.")

    @commands.command(name="evento")
    async def evento(self, ctx):
        """Sorteia um evento aleatório para o servidor."""
        eventos = [
            "Noite de Cinema 🍿", 
            "Torneio Relâmpago 🏆", 
            "Karaokê no Chat de Voz 🎤", 
            "Sorteio de Cargo Especial 💎",
            "Debate Polêmico (Pizza com Abacaxi?) 🍕",
            "Guerra de Memes 🖼️"
        ]
        escolha = random.choice(eventos)
        embed = discord.Embed(
            title="🎉 Evento Aleatório",
            description=f"O evento sorteado foi: **{escolha}**",
            color=self.bot.color_blue
        )
        await ctx.send(embed=embed)

    @commands.command(name="iniciarchat")
    async def iniciarchat(self, ctx):
        """Inicia automação de mensagens do bot no canal atual."""
        if getattr(self, "automation_running", False):
            return await ctx.send("⚠️ A automação já está ativada. Use `/parechat` para encerrar.")

        self.automation_running = True
        await ctx.send("🤖 Automação de mensagens iniciada! O bot vai mandar um aviso legal a cada 5 minutos.")

        messages = [
            "🎮 Vocês poderiam jogar um vava?",
            "🍻 Callchaça hoje rapaziada?",
            "👊 Cadê a tropinha da personalizada?",
            "✨ Quem topa uma partida rapidinha agora?",
            "🔥 Tá rolando vibe boa aqui, bora colar no chat!",
            "💬 Se quiser trocar ideia ou marcar jogatina, chama aí!",
            "🎉 Tem um clima de game rolando, bora agitar essa sala!",
            "📣 Alô galera, vamos fazer esse chat ficar vivo!",
            "🎯 Quem quer montar um time agora?",
            "🎲 Bora inventar uma partida diferente hoje?",
            "👾 Se tiver alguém jogando, chama pro lobby!",
            "🤩 Hoje tá pedindo um rolezinho com a galera!",
            "💥 E aí, quem tá afim de uma rotina de memes?",
            "🎧 Tem som bom rolando? Conta aí!",
            "🌟 Vamos deixar esse chat mais animado com ideias de jogo!",
            "🚀 Hoje é dia de subir de nível, quem vem?",
            "🥳 Alô equipe, quem vai pra seca?",
            "🕹️ Partida marota pra aliviar a semana, vem?",
            "📢 Bora fazer uma call de roda de amigos?",
            "🧠 Tá afim de personalizar uma build crazy?",
            "😂 Qual foi a besteira mais engraçada que rolou hoje?",
            "🎁 Quem quer fazer sorteio de time?",
            "🛡️ Cadê os protetores do chat? Hoje é dia de lenda!",
            "🥶 Quem tá pronto pra uma rodada gelada?",
            "🤜🤛 Chama a tropa, vamos dominar essa sala!",
            "👀 Viagem rápida hoje? Quem topa?",
            "📸 Marca o amigo que nunca aparece no chat!",
            "💡 Ideia louca: versus de custom hoje de noite?",
            "📺 Alguém fazendo livestream agora?",
            "🐾 Bora contar as histórias mais épicas da semana?",
            "🌙 Hoje à noite tem vibe de jogatina sem parada!"
        ]

        while self.automation_running:
            content = random.choice(messages)
            await ctx.send(content)
            await asyncio.sleep(300)

        await ctx.send("🛑 Automação de mensagens finalizada.")

    @commands.command(name="parechat")
    async def parechat(self, ctx):
        """Para a automação de mensagens iniciada pelo bot."""
        if not getattr(self, "automation_running", False):
            return await ctx.send("❌ Nenhuma automação está ativa no momento.")

        self.automation_running = False
        await ctx.send("🛑 Automação de mensagens parada.")

    @commands.command(name="avatar")
    async def avatar(self, ctx, member: discord.Member = None):
        """Mostra o avatar de um usuário."""
        member = member or ctx.author
        embed = discord.Embed(title=f"Avatar de {member.name}", color=self.bot.color_purple)
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="userinfo")
    async def userinfo(self, ctx, member: discord.Member = None):
        """Mostra informações sobre um usuário."""
        member = member or ctx.author
        embed = discord.Embed(title=f"Info de {member.name}", color=self.bot.color_blue)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Conta criada em", value=member.created_at.strftime("%d/%m/%Y"))
        embed.add_field(name="Entrou no server", value=member.joined_at.strftime("%d/%m/%Y"))
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo")
    async def serverinfo(self, ctx):
        """Mostra informações sobre o servidor."""
        guild = ctx.guild
        embed = discord.Embed(title=f"Informações de {guild.name}", color=self.bot.color_purple)
        embed.add_field(name="Membros", value=guild.member_count)
        embed.add_field(name="Canais", value=len(guild.channels))
        embed.add_field(name="Dono", value=guild.owner.mention)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await ctx.send(embed=embed)

    @commands.command(name="escolha")
    async def escolha(self, ctx, *, opcoes):
        """O bot escolhe entre várias opções separadas por vírgula."""
        lista = [opt.strip() for opt in opcoes.split(",")]
        if len(lista) < 2:
            return await ctx.send("Por favor, forneça pelo menos duas opções separadas por vírgula!")
        await ctx.send(f"🤔 Eu escolho: **{random.choice(lista)}**")

    @commands.command(name="ajuda")
    async def ajuda(self, ctx):
        """Mostra os comandos de comunidade do Botequinho."""
        embed = discord.Embed(
            title="📖 Comandos do Botequinho BTF",
            description="Use o prefixo `/` para todos os comandos.",
            color=0xffffff
        )
        embed.add_field(name="🎮 Diversão", value="`/game`, `/evento`, `/escolha`, `/8ball`", inline=False)
        embed.add_field(name="🤖 Automação", value="`/iniciarchat`, `/parechat`", inline=False)
        embed.add_field(name="🔊 Voz", value="`/join`, `/leave`", inline=False)
        embed.add_field(name="📊 Info", value="`/avatar`, `/userinfo`, `/serverinfo`", inline=False)
        embed.add_field(name="🔗 Links", value="`/invite`", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Community(bot))
