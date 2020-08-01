from discord.ext import commands
from Modules import CONSTANT
import asyncio

from Modules.Checks import check_if_role_or_bot_spam


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @check_if_role_or_bot_spam()
    async def role(self, ctx, role_type, *role_names):
        """
        Add a role.

        role_type: Use 'main' or 'sub' to indicate which type of role you want. Your main role will control your nametag colour.
        role_names: The name of the roles you want to add, names are not case-sensitive, you can enter as many names as you want to.

        E.g.: ">role main Sally" will add Sally as your main role and make your nametag yellow.
        E.g.: ">role sub Mizzy" will add Mizzy as a sub role without affecting your nametag colour.

        If you enter >role main with more than one role name, you will get the first valid role you entered in the sequence.

        Only the following roles may be added:
        Sally, Sakura, Ruri, Jun, Mizzy, Miyako, Kanaeru, Akane, Nagomin, Miu, Meimei, Uta, Nicole, Chiharun, Reika, Reinyan, Ayaka, Moe, Mikami, Rettan, Yuki, Ainacchi, Tsubomi, Tamago, Gouda, Kaoruko, Nana, Miko, Komiya, Aida, Mukai
        """
        role_names = [x.capitalize() for x in role_names]
        result_msgs = []

        for role_name in role_names:
            if role_name in CONSTANT.ROLEABLES:
                if role_type == 'main':
                    role_ids = [role.id for role in ctx.author.roles]
                    main_roles = list(set(role_ids) & set(CONSTANT.MAIN_ROLES_ID.values()))

                    role = ctx.guild.get_role(CONSTANT.MAIN_ROLES_ID[role_name])

                    if role in ctx.author.roles:
                        result_msgs.append("You already have that role!")
                    elif main_roles:
                        result_msgs.append("You can't have more than one main role!")
                    else:
                        await ctx.author.add_roles(role)
                        result_msgs.append("Role added.")
                    break
                elif role_type == 'sub':
                    role = ctx.guild.get_role(CONSTANT.SUB_ROLES_ID[role_name])

                    if role in ctx.author.roles:
                        result_msgs.append("You already have that role!")
                    else:
                        await ctx.author.add_roles(role)
                        result_msgs.append("Role added.")
                else:
                    await ctx.send("Illegal operation.")
                    break
            else:
                result_msgs.append("Illegal role name. Type `>help role` for a list of acceptable role names. ")
        final_msg = ""
        for name, result in zip(role_names, result_msgs):
            final_msg += "**{}**: {} \n".format(name, result)

        await ctx.send(final_msg)

    @commands.command()
    @check_if_role_or_bot_spam()
    async def unrole(self, ctx, role_type, *role_names):
        """
        Delete a role.

        role_type: Use 'main' or 'sub' to indicate which type of role you wish to delete. If you delete your main role, your nametag colour will change to that of your highest sub role until you add a new main role.
        role_name: The name of the role you want to delete. (Case-insensitive)

        E.g.: ">unrole main Sally" will remove Sally as your main role. If, say, you have Meimei as a sub role, your nametag colour will then be light blue until you add a new main role.

        Only the following roles may be deleted:
        Sally, Sakura, Ruri, Jun, Mizzy, Miyako, Kanaeru, Akane, Nagomin, Miu, Meimei, Uta, Nicole, Chiharun, Reika, Reinyan, Ayaka, Moe, Mikami, Rettan, Yuki, Ainacchi, Tsubomi, Tamago, Gouda, Kaoruko, Nana, Miko, Komiya, Aida, Mukai
        """
        role_names = [x.capitalize() for x in role_names]
        result_msgs = []

        if role_type != "main" and role_type != "sub":
            print(role_type)
            await ctx.send("Illegal operation.")
        else:
            for role_name in role_names:
                if role_name in CONSTANT.ROLEABLES:
                    if role_type == 'main':
                        role = ctx.guild.get_role(CONSTANT.MAIN_ROLES_ID[role_name])
                    else:
                        role = ctx.guild.get_role(CONSTANT.SUB_ROLES_ID[role_name])

                    if role not in ctx.author.roles:
                        result_msgs.append("You don't have that role!")
                    else:
                        await ctx.author.remove_roles(role)
                        result_msgs.append("Role removed.")
                else:
                    result_msgs.append("Illegal role name. Type `>help unrole` for a list of acceptable role names. ")
            final_msg = ""
            for name, result in zip(role_names, result_msgs):
                final_msg += "**{}**: {} \n".format(name, result)

            await ctx.send(final_msg)

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
