import discord
from discord.ext import commands

from Modules import CONSTANT
from Modules.Checks import check_if_role_or_bot_spam


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @check_if_role_or_bot_spam()
    async def role(self, ctx: commands.Context, role_type: str, *role_names):
        """
        Add a role.

        <role_type>: Use 'main', 'sub', or 'unit' to indicate which type of role you want.
        Your main role will control your nametag colour.

        [role_names...]: The name of the roles you want to add, names are not case-sensitive.
        You can enter as many names as you want to.

        Examples:
            ">role main Sally"
            --- will add Sally as your main role and make your nametag yellow.

            ">role sub Mizzy"
            --- will add Mizzy as a sub role without affecting your nametag colour.

        Unit examples:
            >role unit Cider
            >role unit Bench
            >role unit Keikoto

        Unit roles work the same as sub roles, you can have many of them.

        You can enter multiple role names for this command.
        If you enter ">role main" with more than one role name, you will get the first valid role you entered.

        Examples:
            ">role sub Sally Sakura Ruri Jun"
            --- will add all these four sub roles to you.
            ">role main Sally Sakura Ruri Jun"
            --- will only add Sally as the main role, if you had Sally as your main role, the operation does nothing.

        Only the following roles may be added for 'main' and 'sub' roles:
            Sally, Sakura, Ruri, Jun, Mizzy, Miyako, Kanaeru, Akane,
            Nagomin, Miu, Meimei, Uta, Nicole, Chiharun, Reika,
            Reinyan, Ayaka, Moe, Mikami, Rettan, Yuki, Ainacchi, Tsubomi,
            Tamago, Gouda, Kaoruko, Nana, Miko, Komiya, Aida, Mukai

        Only the following roles may be added for 'unit' roles:
            >> Hareta Hi no Bench (use the word "Bench" to add),
            >> Keikoto saisei keikaku (use the word "Keikoto"),
            >> Ki no Nuketa Cider (use the word "Cider")
        """
        role_names: list[str] = [x.capitalize() for x in role_names]

        if not role_names:
            await ctx.reply("Missing required arguments. ")

        result_msgs: list[str] = []

        for role_name in role_names:
            if role_name in CONSTANT.ROLEABLES:
                if role_type == 'main':
                    if role_name in CONSTANT.UNIT_ROLES_ID:
                        result_msgs.append("You indicated main roles, but you entered an invalid role name. ")
                    else:
                        role_ids: list[int] = [role.id for role in ctx.author.roles]
                        main_roles = list(set(role_ids) & set(CONSTANT.MAIN_ROLES_ID.values()))

                        role: discord.Role = ctx.guild.get_role(CONSTANT.MAIN_ROLES_ID[role_name])

                        if role in ctx.author.roles:
                            result_msgs.append("You already have that role!")
                        elif main_roles:
                            result_msgs.append("You can't have more than one main role!")
                        else:
                            await ctx.author.add_roles(role)
                            result_msgs.append("Role added.")
                        break
                elif role_type == 'sub':
                    if role_name in CONSTANT.UNIT_ROLES_ID:
                        result_msgs.append("You indicated sub roles, but you entered an invalid role name. ")
                    else:
                        role: discord.Role = ctx.guild.get_role(CONSTANT.SUB_ROLES_ID[role_name])

                        if role in ctx.author.roles:
                            result_msgs.append("You already have that role!")
                        else:
                            await ctx.author.add_roles(role)
                            result_msgs.append("Role added.")
                elif role_type == 'unit':
                    if role_name in CONSTANT.MAIN_ROLES_ID.keys() or role_name in CONSTANT.SUB_ROLES_ID.keys():
                        result_msgs.append("You indicated unit roles, but you entered an invalid role name. ")
                    else:
                        role: discord.Role = ctx.guild.get_role(CONSTANT.UNIT_ROLES_ID[role_name])

                        if role in ctx.author.roles:
                            result_msgs.append("You already have that role!")
                        else:
                            await ctx.author.add_roles(role)
                            result_msgs.append("Role added.")
                else:
                    await ctx.reply("Illegal operation.")
                    break
            else:
                result_msgs.append("Illegal role name. Type `>help role` for a list of acceptable role names. ")
        final_msg: str = ""
        for name, result in zip(role_names, result_msgs):
            final_msg += "**{}**: {} \n".format(name, result)

        await ctx.reply(final_msg)

    @commands.command()
    @check_if_role_or_bot_spam()
    async def unrole(self, ctx: commands.Context, role_type: str, *role_names):
        """
        Delete a role.

        <role_type>: Use 'main' or 'sub' to indicate which type of role you wish to delete.
        If you delete your main role, your nametag colour will change to that of your highest sub role
        until you add a new main role.

        [role_names...]: The name of the role you want to delete, names are not case-sensitive.
        You can enter as many names as you want to.

        Example:
            ">unrole main Sally"
            --- will remove Sally as your main role.
            --- If you have Meimei as a sub role, your nametag colour will then be light blue
            until you add a new main role.

        Multiple role deletion works similarly as >role does, for more help, send ">help role".
        """
        role_names: list[str] = [x.capitalize() for x in role_names]

        if not role_names:
            await ctx.reply("Missing required argument. ")

        result_msgs: list[str] = []

        for role_name in role_names:
            if role_name in CONSTANT.ROLEABLES:
                if role_type == 'main':
                    if role_name in CONSTANT.MAIN_ROLES_ID.keys():
                        role: discord.Role = ctx.guild.get_role(CONSTANT.MAIN_ROLES_ID[role_name])
                    else:
                        result_msgs.append("Illegal role name for main roles. ")
                        continue
                elif role_type == 'sub':
                    if role_name in CONSTANT.SUB_ROLES_ID.keys():
                        role: discord.Role = ctx.guild.get_role(CONSTANT.SUB_ROLES_ID[role_name])
                    else:
                        result_msgs.append("Illegal role name for sub roles. ")
                        continue
                elif role_type == 'unit':
                    if role_name in CONSTANT.UNIT_ROLES_ID.keys():
                        role: discord.Role = ctx.guild.get_role(CONSTANT.UNIT_ROLES_ID[role_name])
                    else:
                        result_msgs.append("Illegal role name for unit roles. ")
                        continue
                else:
                    await ctx.send("Invalid selection. ")
                    return

                if role not in ctx.author.roles:
                    result_msgs.append("You don't have that role!")
                else:
                    await ctx.author.remove_roles(role)
                    result_msgs.append("Role removed.")
            else:
                result_msgs.append("Illegal role name. Type `>help unrole` for a list of acceptable role names. ")
        final_msg: str = ""
        for name, result in zip(role_names, result_msgs):
            final_msg += "**{}**: {} \n".format(name, result)

        await ctx.reply(final_msg)
