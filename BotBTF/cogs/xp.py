import discord
from discord.ext import commands
from utils.db import init_db, update_user_xp, get_user_data, get_leaderboard
import random

class XP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await init_db()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        # Ganha entre 5 e 15 de XP por mensagem
        xp_gain = random.randint(5, 15)
        leveled_up, new_level = await update_user_xp(message.author.id, message.guild.id, xp_gain)

        if leveled_up:
            embed = discord.Embed(
                title="✨ Level Up!",
                description=f"Parabéns {message.author.mention}! Você subiu para o **nível {new_level}**!",
                color=self.bot.color_purple
            )
            embed.set_thumbnail(url=message.author.display_avatar.url)
            await message.channel.send(embed=embed)

    @commands.command(name="rank", aliases=["level", "xp"])
    async def rank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        data = await get_user_data(member.id, ctx.guild.id)
        
        if not data:
            xp, level = 0, 1
        else:
            xp, level = data

        embed = discord.Embed(
            title=f"Rank de {member.display_name}",
            color=self.bot.color_blue
        )
        embed.add_field(name="Nível", value=str(level), inline=True)
        embed.add_field(name="XP Total", value=str(xp), inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="BTF Bot - Sistema de XP", icon_url=self.bot.user.display_avatar.url if self.bot.user else None)
        
        await ctx.send(embed=embed)

    @commands.command(name="leaderboard", aliases=["lb", "top"])
    async def leaderboard(self, ctx):
        top_users = await get_leaderboard(ctx.guild.id)
        
        if not top_users:
            return await ctx.send("Ninguém ganhou XP ainda neste servidor!")

        description = ""
        for i, (user_id, xp, level) in enumerate(top_users, 1):
            user = self.bot.get_user(user_id)
            user_name = user.name if user else f"ID: {user_id}"
            description += f"**{i}. {user_name}** - Nível {level} ({xp} XP)\n"

        embed = discord.Embed(
            title=f"🏆 Leaderboard - {ctx.guild.name}",
            description=description,
            color=self.bot.color_purple
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(XP(bot))
