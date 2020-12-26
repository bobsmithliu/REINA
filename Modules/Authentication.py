from discord.ext import commands
import datetime


class Authentication(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.is_protection_on = False

    @commands.command()
    @commands.dm_only()
    async def rule_acknowledged(self, ctx):
        if self.is_protection_on:
            ctx.send("Unfortunately, the moderators of 22/7 server have turned on the server protection protocol, "
                     "new members may not join at this time. Please wait until the restriction is lifted. ")
        else:
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

    @commands.command()
    @commands.has_any_role('Moderators')
    async def protect(self, ctx):
        """
        Do mysterious things.
        Note: this is an on/off switch command.
        """
        self.is_protection_on = not self.is_protection_on
        ctx.send("Protection is {}".format(self.is_protection_on))
