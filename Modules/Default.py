from discord.ext import commands
import random
import asyncio

from Modules import CONSTANT
from Modules.Checks import check_if_bot_spam, check_if_tv_or_streams_or_bot_spam


class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @check_if_bot_spam()
    async def hi(self, ctx):
        """
        Let R.E.I.N.A. greet you!
        """
        await ctx.send("Hi! {}".format(ctx.author.display_name))

    @commands.command()
    @check_if_bot_spam()
    async def rand_lyrics(self, ctx):
        """
        Print out random lyrics from 22/7 songs.
        """
        random_song = random.choice(list(CONSTANT.lyrics.keys()))
        random_lyrics = "\n> ".join(("> " + random.choice(CONSTANT.lyrics[random_song])).split("\n"))

        await ctx.send("*{}* \nーー *「{}」*".format(random_lyrics, random_song))

    @hi.error
    @rand_lyrics.error
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
