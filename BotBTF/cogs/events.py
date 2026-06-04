import discord
from discord.ext import commands
import asyncio

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poll", aliases=["enquete", "votar"])
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, *, question):
        """Cria uma enquete simples no chat."""
        embed = discord.Embed(
            title="📊 Enquete BTF",
            description=question,
            color=self.bot.color_purple
        )
        embed.set_footer(text=f"Enquete por {ctx.author.display_name}")
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")

    @commands.command(name="giveaway", aliases=["sorteio"])
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx, time: int, *, prize):
        """Inicia um sorteio rápido."""
        embed = discord.Embed(
            title="🎉 NOVO SORTEIO!",
            description=f"Prêmio: **{prize}**\nReaja com 🎉 para participar!",
            color=self.bot.color_blue
        )
        embed.set_footer(text=f"Termina em {time} segundos")
        g_message = await ctx.send(embed=embed)
        await g_message.add_reaction("🎉")

        await asyncio.sleep(time)

        new_message = await ctx.channel.fetch_message(g_message.id)
        users = [user async for user in new_message.reactions[0].users() if not user.bot]

        if len(users) == 0:
            await ctx.send("Ninguém participou do sorteio... 😔")
        else:
            import random
            winner = random.choice(users)
            await ctx.send(f"🎊 Parabéns {winner.mention}! Você ganhou o sorteio de **{prize}**!")

async def setup(bot):
    await bot.add_cog(Events(bot))
