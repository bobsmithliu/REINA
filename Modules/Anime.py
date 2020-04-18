import asyncio
import datetime

from discord.ext import commands

from Modules.Checks import check_if_bot_spam


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @check_if_bot_spam()
    async def sub_anime(self, ctx):
        """
        Subscribe to anime notifications.
        """
        anime_role = ctx.guild.get_role(668634086172131378)
        if anime_role in ctx.author.roles:
            await ctx.send("You already have that role!")
        else:
            await ctx.author.add_roles(anime_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                datetime.datetime.utcnow()))
            await ctx.send("You have subscribed to anime notifications.")

    @commands.command()
    @check_if_bot_spam()
    async def unsub_anime(self, ctx):
        """
        Unsubscribe to anime notifications.
        """
        anime_role = ctx.guild.get_role(668634086172131378)
        if anime_role not in ctx.author.roles:
            await ctx.send("You don't have that role!")
        else:
            await ctx.author.remove_roles(anime_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                datetime.datetime.utcnow()))
            await ctx.send("You have unsubscribed to anime notifications.")

    @sub_anime.error
    @unsub_anime.error
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
