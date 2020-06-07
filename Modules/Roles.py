from discord.ext import commands
from Modules import CONSTANT
import datetime
import asyncio

from Modules.Checks import check_if_role_or_bot_spam


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @check_if_role_or_bot_spam()
    async def role(self, ctx, role_type, role_name):
        """
        Add a role.

        role_type: Use 'main' or 'sub' to indicate which type of role you want. Your main role will control your nametag colour.
        role_name: The name of your role. (Case-insensitive)

        E.g.: ">role main Sally" will add Sally as your main role and make your nametag yellow.
        E.g.: ">role sub Mizzy" will add Mizzy as a sub role without affecting your nametag colour.

        Only the following roles may be added:
        Sally, Sakura, Ruri, Jun, Mizzy, Miyako, Kanaeru, Akane, Nagomin, Miu, Meimei, Uta, Nicole, Chiharun, Reika, Reinyan, Ayaka, Moe, Mikami, Rettan, Yuki, Ainacchi, Tsubomi, Tamago, Gouda, Kaoruko, Nana, Miko

        Note: >role/unrole main <role_name> has been deprecated, use >main_role for a smarter configurator.
        """
        role_name = role_name.capitalize()

        if role_name in CONSTANT.ROLEABLES:
            if role_type == 'main':
                role_ids = [role.id for role in ctx.author.roles]
                main_roles = list(set(role_ids) & set(CONSTANT.MAIN_ROLES_ID.values()))

                role = ctx.guild.get_role(CONSTANT.MAIN_ROLES_ID[role_name])

                if role in ctx.author.roles:
                    await ctx.send("You already have that role!")
                elif main_roles:
                    await ctx.send("You can't have more than one main role!")
                else:
                    await ctx.author.add_roles(role)
                    await ctx.send("Role added.")
            elif role_type == 'sub':
                role = ctx.guild.get_role(CONSTANT.SUB_ROLES_ID[role_name])

                if role in ctx.author.roles:
                    await ctx.send("You already have that role!")
                else:
                    await ctx.author.add_roles(role)
                    await ctx.send("Role added.")
            else:
                await ctx.send("Illegal operation.")
        else:
            await ctx.send("Illegal role name. Type `>help role` for a list of acceptable role names. ")

    @commands.command()
    @check_if_role_or_bot_spam()
    async def unrole(self, ctx, role_type, role_name):
        """
        Delete a role.

        role_type: Use 'main' or 'sub' to indicate which type of role you wish to delete. If you delete your main role, your nametag colour will change to that of your highest sub role until you add a new main role.
        role_name: The name of your role. (Case-insensitive)

        E.g.: ">unrole main Sally" will remove Sally as your main role. If, say, you have Meimei as a sub role, your nametag colour will then be light blue until you add a new main role.

        Only the following roles may be deleted:
        Sally, Sakura, Ruri, Jun, Mizzy, Miyako, Kanaeru, Akane, Nagomin, Miu, Meimei, Uta, Nicole, Chiharun, Reika, Reinyan, Ayaka, Moe, Mikami, Rettan, Yuki, Ainacchi, Tsubomi, Tamago, Gouda, Kaoruko, Nana, Miko

        Note: >role/unrole main <role_name> has been deprecated, use >main_role for a smarter configurator.
        """
        role_name = role_name.capitalize()

        if role_name in CONSTANT.ROLEABLES:
            if role_type == 'main':
                role = ctx.guild.get_role(CONSTANT.MAIN_ROLES_ID[role_name])
            elif role_type == 'sub':
                role = ctx.guild.get_role(CONSTANT.SUB_ROLES_ID[role_name])
            else:
                await ctx.send("Illegal operation.")
                return

            if role not in ctx.author.roles:
                await ctx.send("You don't have that role!")
            else:
                await ctx.author.remove_roles(role)
                await ctx.send("Role removed.")

        else:
            await ctx.send("Illegal role name. Type `>help unrole` for a list of acceptable role names. ")

    @role.error
    @unrole.error
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
