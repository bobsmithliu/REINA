from discord.ext import commands
import datetime


class Authentication(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @commands.dm_only()
    async def rule_acknowledged(self, ctx):
        user_id = ctx.author.id

        nananijiguild = self.bot.get_guild(336277820684763148)
        if nananijiguild.get_member(user_id) is None:
            await ctx.send("Unsupported operation.")
            return

        new_member_role = nananijiguild.get_role(663581221967757313)
        if new_member_role not in nananijiguild.get_member(user_id).roles:
            await ctx.send("You are already a member!")
            return

        await nananijiguild.get_member(user_id).remove_roles(new_member_role,
                                                             reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                                                                 datetime.datetime.utcnow()))
        await ctx.send(
            "You now should have access to the rest of the server. If not, please DM one of the Moderators. ")


def setup(bot):
    bot.add_cog(Authentication(bot))
