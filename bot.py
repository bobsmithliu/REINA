import discord
from discord.ext import commands
import datetime

TOKEN = '[REDACTED]'

reina = discord.Game("Roles and Entertainment Information and Notification Agent")
bot_description = '''
R.E.I.N.A. 1.02

Roles and Entertainment Information and Notification Agent

Open-source at: https://github.com/Skk-nsmt/REINA
'''
bot = commands.Bot(command_prefix='>', description=bot_description)
sub = {
    'Tamago': 497370840824807424,
    'Tsubomi': 497369993428729856,
    'Ainacchi': 466163376779689985,
    'Yuki': 497369955181002765,
    'Rettan': 466163341031637002,
    'Mikami': 497369641241411584,
    'Moe': 466163363756638209,
    'Ayaka': 466163285318828032,
    'Reinyan': 466163253232402432,
    'Reika': 466163208315731968,
    'Chiharun': 466163143983366145,
    'Nicole': 466163118695776266,
    'Meimei': 466163049217261570,
    'Miu': 466162997971255296,
    'Nagomin': 466162947807248386,
    'Akane': 466162927758737409,
    'Kanaeru': 466162902349643786,
    'Miyako': 466162830371192832,
    'Mizzy': 466162802692980737,
    'Jun': 466162727598161931,
    'Ruri': 466162700880183307,
    'Sakura': 466162595817193482,
    'Sally': 466162519447437312
}
main = {
    'Tamago': 497370864254320670,
    'Tsubomi': 497370023397163008,
    'Ainacchi': 466160683185340426,
    'Yuki': 497369857042677768,
    'Rettan': 466160640428343298,
    'Mikami': 497369717175222284,
    'Moe': 466160644341628929,
    'Ayaka': 466160548128620554,
    'Reinyan': 466160517044502578,
    'Reika': 466160400405102593,
    'Chiharun': 466160373855420418,
    'Nicole': 466160288564117515,
    'Meimei': 466160266451877892,
    'Miu': 466160184725864448,
    'Nagomin': 466160116534607875,
    'Akane': 466160086583083008,
    'Kanaeru': 466160011996037122,
    'Miyako': 466159974125404171,
    'Mizzy': 466159885629784064,
    'Jun': 466159852532531210,
    'Ruri': 466159773604249611,
    'Sakura': 466159732235829249,
    'Sally': 466159611179958273
}
acceptable_roles = ['Tamago', 'Tsubomi', 'Ainacchi', 'Rettan', 'Mikami', 'Moe', 'Ayaka', 'Reinyan', 'Reika',
                    'Chiharun', 'Nicole', 'Meimei', 'Miu', 'Nagomin', 'Akane', 'Kanaeru', 'Miyako', 'Mizzy',
                    'Jun', 'Ruri', 'Sakura', 'Sally']


@bot.listen()
async def on_ready():
    print('Ready!')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=reina)


class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def hi(self, ctx):
        """
        Let R.E.I.N.A. greet you!
        """
        await ctx.send("Hi! {}".format(ctx.author.display_name))

    @commands.command()
    async def role(self, ctx, main_role, role_name):
        """
        Add a role.

        main_role: Use 'main' or 'sub' to indicate which type of role you want. Your main role will control your nametag colour.
        role_name: The name of your role.

        E.g.: ">role main Sally" will add Sally as your main role and make your nametag yellow.
        E.g.: ">role sub Mizzy" will add Mizzy as a sub role without affecting your nametag colour.

        Only the following roles may be added:
        Sally, Sakura, Ruri, Jun, Mizzy, Miyako, Kanaeru, Akane, Nagomin, Miu, Meimei, Nicole, Chiharun, Reika, Reinyan, Ayaka, Moe, Mikami, Rettan, Yuki, Ainacchi, Tsubomi, Tamago
        """
        if role_name in acceptable_roles:
            if main_role == 'main':
                role_ids = [role.id for role in ctx.author.roles]
                main_roles = list(set(role_ids) & set(main.values()))

                role = ctx.guild.get_role(main[role_name])

                if role in ctx.author.roles:
                    await ctx.send("You already have that role!")
                elif main_roles:
                    await ctx.send("You can't have more than one main role!")
                else:
                    await ctx.author.add_roles(role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(datetime.datetime.utcnow()))
                    await ctx.send("Role added.")
            elif main_role == 'sub':
                role = ctx.guild.get_role(sub[role_name])

                if role in ctx.author.roles:
                    await ctx.send("You already have that role!")
                else:
                    await ctx.author.add_roles(role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(datetime.datetime.utcnow()))
                    await ctx.send("Role added.")
            else:
                await ctx.send("Illegal operation.")
        else:
            await ctx.send("Illegal role name.")

    @commands.command()
    async def unrole(self, ctx, main_role, role_name):
        """
        Delete a role.

        main_role: Use 'main' or 'sub' to indicate which type of role you wish to delete. If you delete your main role, your nametag colour will change to that of your highest sub role until you add a new main role.
        role_name: The name of your role.

        E.g.: ">unrole main Sally" will remove Sally as your main role. If, say, you have Meimei as a sub role, your nametag colour will then be light blue until you add a new main role.

        Only the following roles may be deleted:
        Sally, Sakura, Ruri, Jun, Mizzy, Miyako, Kanaeru, Akane, Nagomin, Miu, Meimei, Nicole, Chiharun, Reika, Reinyan, Ayaka, Moe, Mikami, Rettan, Yuki, Ainacchi, Tsubomi, Tamago
        """
        if role_name in acceptable_roles:
            if main_role == 'main':
                role = ctx.guild.get_role(main[role_name])

                if role not in ctx.author.roles:
                    await ctx.send("You don't have that role!")
                else:
                    await ctx.author.remove_roles(role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(datetime.datetime.utcnow()))
                    await ctx.send("Role removed.")
            elif main_role == 'sub':
                role = ctx.guild.get_role(sub[role_name])

                if role not in ctx.author.roles:
                    await ctx.send("You don't have that role!")
                else:
                    await ctx.author.remove_roles(role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                        datetime.datetime.utcnow()))
                    await ctx.send("Role removed.")
            else:
                await ctx.send("Illegal operation.")
        else:
            await ctx.send("Illegal role name.")

    @commands.command(aliases=["subkuraten"])
    async def subKuraten(self, ctx):
        """
        Subscribe to Kuraten! notifications.
        """
        kuraten_role = ctx.guild.get_role(641113337186222080)
        if kuraten_role in ctx.author.roles:
            await ctx.send("You already have that role!")
        else:
            await ctx.author.add_roles(kuraten_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(datetime.datetime.utcnow()))
            await ctx.send("You have subscribed to Kuraten! notifications.")

    @commands.command(aliases=["unsubkuraten"])
    async def unsubKuraten(self, ctx):
        """
        Unsubscribe to Kuraten! notifications.
        """
        kuraten_role = ctx.guild.get_role(641113337186222080)
        if kuraten_role not in ctx.author.roles:
            await ctx.send("You don't have that role!")
        else:
            await ctx.author.remove_roles(kuraten_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(datetime.datetime.utcnow()))
            await ctx.send("You have unsubscribed to Kuraten! notifications.")

    @commands.command(aliases=["subkeisanchuu"])
    async def subKeisanchuu(self, ctx):
        """
        Subscribe to 22/7 Keisanchuu notifications.
        """
        keisanchuu_role = ctx.guild.get_role(641112458291052584)
        if keisanchuu_role in ctx.author.roles:
            await ctx.send("You already have that role!")
        else:
            await ctx.author.add_roles(keisanchuu_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(datetime.datetime.utcnow()))
            await ctx.send("You have subscribed to 22/7 Keisanchuu notifications.")

    @commands.command(aliases=["unsubkeisanchuu"])
    async def unsubKeisanchuu(self, ctx):
        """
        Unsubscribe to 22/7 Keisanchuu notifications.
        """
        keisanchuu_role = ctx.guild.get_role(641112458291052584)
        if keisanchuu_role not in ctx.author.roles:
            await ctx.send("You don't have that role!")
        else:
            await ctx.author.remove_roles(keisanchuu_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(datetime.datetime.utcnow()))
            await ctx.send("You have unsubscribed to 22/7 Keisanchuu notifications.")


bot.add_cog(Default(bot))
bot.run(TOKEN)
