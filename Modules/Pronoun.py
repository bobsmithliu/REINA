from discord.ext import commands
from Modules import CONSTANT
from Modules.Checks import check_if_bot_spam

import asyncio


class Pronouns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @check_if_bot_spam()
    async def pronoun(self, ctx, choice):
        """Give yourself a pronoun role.

        Available choices are "they", "she", "he", "ask".
        "Ask" means you want people to ask you what your pronoun is.
        You can only have one pronoun.

        Example: >pronoun they
        """
        if choice not in CONSTANT.PRONOUNABLES:
            await ctx.send("Illegal choice. ")
            return

        role_ids = [role.id for role in ctx.author.roles]
        pronoun_roles = list(set(role_ids) & set(CONSTANT.PRONOUNS.values()))

        if pronoun_roles:
            await ctx.send("You already have a pronoun, to remove your pronoun role, use `>clear_pronoun`. ")
            return

        role = ctx.guild.get_role(CONSTANT.PRONOUNS[choice])
        if role in ctx.author.roles:
            await ctx.send("You already have that pronoun. ")
            return

        await ctx.author.add_roles(role)
        await ctx.send("Pronoun given. ")

    @commands.command()
    @check_if_bot_spam()
    async def clear_pronoun(self, ctx):
        """Clear any pronoun you currently have.
        """
        role_ids = [role.id for role in ctx.author.roles]
        pronoun_roles = list(set(role_ids) & set(CONSTANT.PRONOUNS.values()))

        if pronoun_roles:
            role = ctx.guild.get_role(pronoun_roles[0])
            await ctx.author.remove_roles(role)
            await ctx.send("Pronoun removed.")
        else:
            await ctx.send("You don't have any pronouns. ")

    @pronoun.error
    @clear_pronoun.error
    async def command_error(self, ctx, error):
        bot_channel = ctx.guild.get_channel(336287198510841856)
        if isinstance(error, commands.CheckFailure):
            message = await ctx.send('Please proceed your action at {} (deletion in 5s)'.format(bot_channel.mention))
            await asyncio.sleep(1)
            for i in range(4, 0, -1):
                await message.edit(
                    content="Please proceed your action at {} (deletion in {}s)".format(bot_channel.mention, i))
                await asyncio.sleep(1)
            await message.delete()
            await ctx.message.delete()
