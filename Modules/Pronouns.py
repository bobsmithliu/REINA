import discord
from discord.ext import commands

from Modules import CONSTANT
from Modules.Checks import check_if_role_or_bot_spam


class Pronouns(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command()
    @check_if_role_or_bot_spam()
    async def pronoun(self, ctx: commands.Context, choice: str):
        """Give yourself a pronoun role.

        choice: the pronoun you wish to get.

        Available choices are "they", "she", "he", "ask".

        "Ask" means you want people to ask you what your pronoun is.
        You can only have one pronoun.

        Example:
            >pronoun they
        """
        if choice not in CONSTANT.PRONOUNABLES:
            await ctx.reply("Illegal choice. ")
            return

        role_ids: list[int] = [role.id for role in ctx.author.roles]
        pronoun_roles: list[int] = list(set(role_ids) & set(CONSTANT.PRONOUNS.values()))

        if pronoun_roles:
            await ctx.reply("You already have a pronoun, to remove your pronoun role, use `>clear_pronoun`. ")
            return

        role: discord.Role = ctx.guild.get_role(CONSTANT.PRONOUNS[choice])
        if role in ctx.author.roles:
            await ctx.reply("You already have that pronoun. ")
            return

        await ctx.author.add_roles(role)
        await ctx.reply("Pronoun given. ")

    @commands.command()
    @check_if_role_or_bot_spam()
    async def clear_pronoun(self, ctx: commands.Context):
        """
        Clear any pronoun you currently have.
        """
        role_ids: list[int] = [role.id for role in ctx.author.roles]
        pronoun_roles: list[int] = list(set(role_ids) & set(CONSTANT.PRONOUNS.values()))

        if pronoun_roles:
            role: discord.Role = ctx.guild.get_role(pronoun_roles[0])
            await ctx.author.remove_roles(role)
            await ctx.reply("Pronoun removed.")
        else:
            await ctx.reply("You don't have any pronouns. ")
