import discord
from discord.ext import commands

from Modules.CONSTANT import SHOWROOM_ALERT_ROLEABLES, SHOWROOM_ALERT_ROLES
from Modules.Checks import check_if_bot_spam


class Showroom(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command(aliases=["sr"])
    @check_if_bot_spam()
    async def showroom(self, ctx: commands.Context, person: str) -> None:
        """
        Enable Showroom ping for a certain person.

        <person>: the number of the person you want to enable pings for.

        Example:
            ">showroom ruri"
            will turn on Ruri's Showroom ping
            Every time a Moderator announces an upcoming Ruri showroom stream, you will be informed.

        Valid names are:
            Sally, Ruri, Mizzy, Kanaeru, Nagomin, Uta, Reinyan, Moe, Rettan, Ainacchi
        """
        person: str = person.capitalize()

        if person in SHOWROOM_ALERT_ROLEABLES:
            role: discord.Role = ctx.guild.get_role(SHOWROOM_ALERT_ROLES[person])

            if role in ctx.author.roles:
                await ctx.reply("You have already turned on alert for {}".format(person))
                return
            else:
                await ctx.author.add_roles(role)
                await ctx.reply("Turned on Showroom stream ping for {}".format(person))
                return
        else:
            await ctx.reply("Invalid name. Read `>help showroom` for a list of valid names. ")

    @commands.command(aliases=["unsr"])
    @check_if_bot_spam()
    async def unshowroom(self, ctx: commands.Context, person: str) -> None:
        """
        Opt-out from this person's Showroom ping.

        <person>: the person you want to opt-out from.

        Example:
            ">unshowroom ruri"
            will turn off Ruri's Showroom ping
            Every time a Moderator announces an upcoming Ruri showroom stream, you will NOT be informed.

        Valid names are:
            Sally, Ruri, Mizzy, Kanaeru, Nagomin, Uta, Reinyan, Moe, Rettan, Ainacchi
        """
        person: str = person.capitalize()

        if person in SHOWROOM_ALERT_ROLEABLES:
            role: discord.Role = ctx.guild.get_role(SHOWROOM_ALERT_ROLES[person])

            if role in ctx.author.roles:
                await ctx.author.remove_roles(role)
                await ctx.reply("{}'s Showroom ping turned off. ".format(person))
            else:
                await ctx.reply("You have not turned on {}'s Showroom ping. ".format(person))
        else:
            await ctx.reply("Invalid name. Read `>unhelp showroom` for a list of valid names. ")
