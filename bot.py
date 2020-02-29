import asyncio

import discord
from discord.ext import commands
import datetime
import pytz
import time
import bs4
import aiohttp

import TOKEN


bot_description = '''
R.E.I.N.A. 1.17

Roles and Entertainment Information and Notification Agent

Open source at: https://github.com/Skk-nsmt/REINA
'''
bot = commands.Bot(command_prefix='>', description=bot_description, case_insensitive=True)

# -----------------------------------
# |                                 |
# |       Below are constants       |
# |                                 |
# -----------------------------------

jptz = pytz.timezone('Asia/Tokyo')
universaltz = pytz.timezone('UTC')
pacifictz = pytz.timezone('America/Los_Angeles')
centraltz = pytz.timezone('America/Chicago')
easterntz = pytz.timezone('America/New_York')

sub_roles_id = {
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
    'Sally': 466162519447437312,
    'Uta': 659171909723750405
}
main_roles_id = {
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
    'Sally': 466159611179958273,
    'Uta': 659171144028520475
}
acceptable_roles = ['Tamago', 'Tsubomi', 'Ainacchi', 'Rettan', 'Mikami', 'Moe', 'Ayaka', 'Reinyan', 'Reika',
                    'Chiharun', 'Nicole', 'Meimei', 'Miu', 'Nagomin', 'Akane', 'Kanaeru', 'Miyako', 'Mizzy',
                    'Jun', 'Ruri', 'Sakura', 'Sally', 'Uta']
stream_links = {
    'Chiharu': ['Hokaze Chiharu', 'https://www.showroom-live.com/digital_idol_2', discord.Color.red()],
    'Ruri': ['Umino Ruri', 'https://www.showroom-live.com/digital_idol_4', discord.Color.green()],
    'Mei': ['Hanakawa Mei', 'https://www.showroom-live.com/digital_idol_7', discord.Color.blue()],
    'Uta': ['Kawase Uta', 'https://www.showroom-live.com/kawaseuta', discord.Color.blue()],
    'Reina': ['Miyase Reina', 'https://www.showroom-live.com/digital_idol_9', discord.Color.dark_magenta()],
    'Sally': ['Amaki Sally', 'https://www.showroom-live.com/digital_idol_11', discord.Color.gold()],
    'Aina': ['Takeda Aina', 'https://www.showroom-live.com/digital_idol_15', discord.Color.teal()],
    'Kanae': ['Shirosawa Kanae', 'https://www.showroom-live.com/digital_idol_18', discord.Color.purple()],
    'Urara': ['Takatsuji Urara', 'https://www.showroom-live.com/digital_idol_19', discord.Color.from_rgb(230, 136, 242)],
    'Moe': ['Suzuhana Moe', 'https://www.showroom-live.com/digital_idol_20', discord.Color.magenta()],
    'Mizuha': ['Kuraoka Mizuha', 'https://www.showroom-live.com/digital_idol_21', discord.Color.orange()],
    'Nagomi': ['Saijo Nagomi', 'https://www.showroom-live.com/digital_idol_22', discord.Color.from_rgb(220, 248, 250)],
    'Nananiji': ['Group Stream', 'https://www.showroom-live.com/nanabunno', discord.Color.blue()]
}

# Constants ends here

# Checking functions


def check_if_bot_spam():
    async def predicate(ctx):
        bot_channel = ctx.guild.get_channel(336287198510841856)
        return ctx.channel == bot_channel
    return commands.check(predicate)


def check_if_role_or_bot_spam():
    async def predicate(ctx):
        bot_channel = ctx.guild.get_channel(336287198510841856)
        role_channel = discord.utils.get(ctx.guild.channels, name='roles')
        return ctx.channel == bot_channel or ctx.channel == role_channel
    return commands.check(predicate)


@bot.listen()
async def on_ready():
    print('Ready!')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(">help"))


@bot.listen()
async def on_message(message):
    # don't respond to ourselves
    if message.author == bot.user:
        return
    if 'reina' in message.content.lower() and 'cute' in message.content.lower():
        await message.add_reaction('♥️')


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

    @hi.error
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
        Sally, Sakura, Ruri, Jun, Mizzy, Miyako, Kanaeru, Akane, Nagomin, Miu, Meimei, Uta, Nicole, Chiharun, Reika, Reinyan, Ayaka, Moe, Mikami, Rettan, Yuki, Ainacchi, Tsubomi, Tamago
        """
        role_name = role_name.capitalize()

        if role_name in acceptable_roles:
            if role_type == 'main':
                role_ids = [role.id for role in ctx.author.roles]
                main_roles = list(set(role_ids) & set(main_roles_id.values()))

                role = ctx.guild.get_role(main_roles_id[role_name])

                if role in ctx.author.roles:
                    await ctx.send("You already have that role!")
                elif main_roles:
                    await ctx.send("You can't have more than one main role!")
                else:
                    await ctx.author.add_roles(role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(datetime.datetime.utcnow()))
                    await ctx.send("Role added.")
            elif role_type == 'sub':
                role = ctx.guild.get_role(sub_roles_id[role_name])

                if role in ctx.author.roles:
                    await ctx.send("You already have that role!")
                else:
                    await ctx.author.add_roles(role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(datetime.datetime.utcnow()))
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
        Sally, Sakura, Ruri, Jun, Mizzy, Miyako, Kanaeru, Akane, Nagomin, Miu, Meimei, Uta, Nicole, Chiharun, Reika, Reinyan, Ayaka, Moe, Mikami, Rettan, Yuki, Ainacchi, Tsubomi, Tamago
        """
        role_name = role_name.capitalize()

        if role_name in acceptable_roles:
            if role_type == 'main':
                role = ctx.guild.get_role(main_roles_id[role_name])
            elif role_type == 'sub':
                role = ctx.guild.get_role(sub_roles_id[role_name])
            else:
                await ctx.send("Illegal operation.")
                return

            if role not in ctx.author.roles:
                await ctx.send("You don't have that role!")
            else:
                await ctx.author.remove_roles(role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                    datetime.datetime.utcnow()))
                await ctx.send("Role removed.")

        else:
            await ctx.send("Illegal role name.")

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


class Kuraten(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @check_if_bot_spam()
    async def sub_kuraten(self, ctx):
        """
        Subscribe to Kuraten! notifications.
        """
        kuraten_role = ctx.guild.get_role(641113337186222080)
        if kuraten_role in ctx.author.roles:
            await ctx.send("You already have that role!")
        else:
            await ctx.author.add_roles(kuraten_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(datetime.datetime.utcnow()))
            await ctx.send("You have subscribed to Kuraten! notifications.")

    @commands.command()
    @check_if_bot_spam()
    async def unsub_kuraten(self, ctx):
        """
        Unsubscribe to Kuraten! notifications.
        """
        kuraten_role = ctx.guild.get_role(641113337186222080)
        if kuraten_role not in ctx.author.roles:
            await ctx.send("You don't have that role!")
        else:
            await ctx.author.remove_roles(kuraten_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(datetime.datetime.utcnow()))
            await ctx.send("You have unsubscribed to Kuraten! notifications.")

    @sub_kuraten.error
    @unsub_kuraten.error
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
            await ctx.author.add_roles(anime_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(datetime.datetime.utcnow()))
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
            await ctx.author.remove_roles(anime_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(datetime.datetime.utcnow()))
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


class Keisanchuu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @check_if_bot_spam()
    async def sub_keisanchuu(self, ctx):
        """
        Subscribe to 22/7 Keisanchuu notifications.
        """
        keisanchuu_role = ctx.guild.get_role(641112458291052584)
        if keisanchuu_role in ctx.author.roles:
            await ctx.send("You already have that role!")
        else:
            await ctx.author.add_roles(keisanchuu_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                datetime.datetime.utcnow()))
            await ctx.send("You have subscribed to 22/7 Keisanchuu notifications.")

    @commands.command()
    @check_if_bot_spam()
    async def unsub_keisanchuu(self, ctx):
        """
        Unsubscribe to 22/7 Keisanchuu notifications.
        """
        keisanchuu_role = ctx.guild.get_role(641112458291052584)
        if keisanchuu_role not in ctx.author.roles:
            await ctx.send("You don't have that role!")
        else:
            await ctx.author.remove_roles(keisanchuu_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                datetime.datetime.utcnow()))
            await ctx.send("You have unsubscribed to 22/7 Keisanchuu notifications.")

    @sub_keisanchuu.error
    @unsub_keisanchuu.error
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


class Mods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @commands.has_any_role('Moderators', 'Disciplinary Committee')
    async def protect(self, ctx):
        """
        (Mod-only command) Do mystery things.
        Note: this is an on-off switch command.
        """
        global new_member_loaded

        if new_member_loaded:
            bot.unload_extension("authentication")
            new_member_loaded = False
            await ctx.send("Unloaded. ")
        else:
            bot.load_extension("authentication")
            new_member_loaded = True
            await ctx.send("Loaded. ")

    @commands.command()
    @commands.has_any_role('Moderators', 'Disciplinary Committee')
    @check_if_bot_spam()
    async def announce(self, ctx, person, date, planned_time):
        """
        (Mod-only command) Make stream announcements.

        Make stream announcements at #227 streams.

        person: use members' first name, or use "Nananiji" for Nananiji Room stream.
        date: use either "today" or "tomorrow" to indicate whether the stream is happening today or tomorrow.
        planned_time: "<two_digit_hour>:<two_digit_minute>" format in 24Hr standard.

        Please note that when executing the command, the stream will need to be happening TODAY in Japan.
        """
        stream_channel = discord.utils.get(ctx.guild.channels, name='227-streams')
        await stream_channel.trigger_typing()

        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.62 Safari/537.36",
            'Referer': "https://www.showroom-live.com"
        }

        if person in stream_links:
            now = datetime.datetime.now(jptz)

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(stream_links[person][1], headers=headers) as r:
                        if r.status == 200:
                            page = bs4.BeautifulSoup(await r.text(), "html.parser")

                parsed_time = time.strptime(planned_time, "%H:%M")

                stream_time = jptz.localize(datetime.datetime(year=now.year,
                                                              month=now.month,
                                                              day=now.day,
                                                              hour=parsed_time.tm_hour,
                                                              minute=parsed_time.tm_min))

                if date == "tomorrow":
                    stream_time = stream_time + datetime.timedelta(days=1)
                else:
                    pass

                announcement_embed = discord.Embed(title="**{}**".format(stream_links[person][0]),
                                                   type='rich',
                                                   description='{}'.format(stream_links[person][1]),
                                                   color=stream_links[person][2])

                announcement_embed.add_field(name='Japan Time',
                                             value='{}'.format(stream_time.strftime("%Y-%m-%d %I:%M%p")))
                announcement_embed.add_field(name='Universal Time',
                                             value='{}'.format(stream_time.astimezone(universaltz).strftime("%Y-%m-%d %I:%M%p")))
                announcement_embed.add_field(name='Eastern Time',
                                             value='{}'.format(stream_time.astimezone(easterntz).strftime("%Y-%m-%d %I:%M%p")))
                announcement_embed.add_field(name='Central Time',
                                             value='{}'.format(stream_time.astimezone(centraltz).strftime("%Y-%m-%d %I:%M%p")))
                announcement_embed.add_field(name='Pacific Time',
                                             value='{}'.format(stream_time.astimezone(pacifictz).strftime("%Y-%m-%d %I:%M%p")))

                announcement_embed.set_author(name='Upcoming Stream',
                                              icon_url="https://www.showroom-live.com/assets/img/v3/apple-touch-icon.png")
                announcement_embed.set_image(url=page.find("meta", attrs={"property": "og:image"})['content'])

                announcement_embed.set_footer(text='Sent by {}'.format(ctx.author.display_name),
                                              icon_url=ctx.author.avatar_url)

                stream_msg = await stream_channel.send(embed=announcement_embed)

                await stream_msg.pin()
            except ValueError:
                await ctx.send("Something happened, please report it to the developer. ")

        else:
            await ctx.send("Illegal name.")

    @announce.error
    @protect.error
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


bot.load_extension("authentication")
new_member_loaded = True

bot.add_cog(Default(bot))
bot.add_cog(Roles(bot))
bot.add_cog(Kuraten(bot))
bot.add_cog(Keisanchuu(bot))
bot.add_cog(Anime(bot))
bot.add_cog(Mods(bot))
bot.run(TOKEN.TOKEN)
