from discord.ext import commands
import random
import asyncio

from Modules import CONSTANT
from Modules.Checks import check_if_bot_spam

PRIVACY = '''
```
Privacy Policy

Using this bot (Discord unique user name: R.E.I.N.A. #3681, "this bot") means that you have read and understood this document.

The developer of this bot has made every possible effort to minimize data collection. However, to keep this bot operable responsively, some non-sensitive data will be collected in a non-permanent way. No data is ever stored permanently.

This bot will collect your messages and user information (meta-data included) sent to 22/7 Discord server (http://discord.gg/NxZ3W7Z, "this server") to a server operated by Amazon Web Services in its cache: a non-permanent storage system, for command processing. 
The bot only collects the most recent 1000 messages sent in this server. Your messages and information will be deleted from the cache after a short period of time. 

If, in any way, you are not comfortable with how your data is collected and used, please immediately contact this bot's developer: Skk#8086. 
```
'''


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
        random_song = random.choice(list(CONSTANT.LYRICS.keys()))
        random_lyrics = "\n> ".join(("> " + random.choice(CONSTANT.LYRICS[random_song])).split("\n"))

        await ctx.send("*{}* \nーー *「{}」*".format(random_lyrics, random_song))

    @commands.command()
    @check_if_bot_spam()
    async def privacy(self, ctx):
        """
        Read this bot's privacy policy.
        """
        await ctx.send(PRIVACY)

    @commands.command()
    @check_if_bot_spam()
    async def should_i(self, ctx, *prompts):
        """
        Let the bot help you to decide what you should do.
        [prompts...]: a list of things that you want the bot to decide for you, surround each option with a pair of quotation marks.

        Example: >should_i "eat" "sleep"
        Example: >should_i "AAA" "BBB" "CCC" "DDD"
        """
        await ctx.send("You should {}. ".format(random.choice(prompts)))

    @hi.error
    @rand_lyrics.error
    @should_i.error
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
