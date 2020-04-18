import asyncio
import datetime

from discord.ext import commands

from Modules.Checks import check_if_bot_spam


class Wariraji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @check_if_bot_spam()
    async def sub_wariraji(self, ctx):
        """
        Subscribe to Warikirenai Radio Plus notifications.
        """
        radio_role = ctx.guild.get_role(694627966495490078)
        if radio_role in ctx.author.roles:
            await ctx.send("You already have that role!")
        else:
            await ctx.author.add_roles(radio_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                datetime.datetime.utcnow()))
            await ctx.send("You have subscribed to Warikirenai Radio Plus notifications.")

    @commands.command()
    @check_if_bot_spam()
    async def unsub_wariraji(self, ctx):
        """
        Unsubscribe to Warikirenai Radio Plus notifications.
        """
        radio_role = ctx.guild.get_role(694627966495490078)
        if radio_role not in ctx.author.roles:
            await ctx.send("You don't have that role!")
        else:
            await ctx.author.remove_roles(radio_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                datetime.datetime.utcnow()))
            await ctx.send("You have unsubscribed to Warikirenai Radio Plus notifications.")

    @sub_wariraji.error
    @unsub_wariraji.error
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