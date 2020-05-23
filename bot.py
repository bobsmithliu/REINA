import datetime

import discord
import pytz
from discord.ext import commands
from textblob import TextBlob
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import TOKEN
from Modules.Default import Default
from Modules.Keisanchuu import Keisanchuu
from Modules.Mods import Mods
from Modules.Roles import Roles
from Modules.Wariraji import Wariraji
from Modules.MyHelp import MyHelp
from Modules.Checks import check_if_bot_spam

BOT_DESCRIPTION = '''
R.E.I.N.A. 1.25

Roles and Entertainment Information and Notification Agent

Licensed under WTFPL
'''

bot = commands.Bot(command_prefix='>', description=BOT_DESCRIPTION, case_insensitive=True, help_command=MyHelp())
scheduler = AsyncIOScheduler()


@bot.listen()
async def on_ready():
    print('Ready!')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(">help"))

    scheduler.add_job(prompt_keisanchuu, "cron", day_of_week='sat', hour=22, minute=30, args=[bot, 30])
    scheduler.add_job(prompt_keisanchuu, "cron", day_of_week='sat', hour=22, minute=55, args=[bot, 5])
    scheduler.add_job(prompt_radio, "cron", day_of_week='sat', hour=15, minute=30, args=[bot, 30])
    scheduler.add_job(prompt_radio, "cron", day_of_week='sat', hour=15, minute=55, args=[bot, 5])

    print("Background Task Setup finished. ")

    scheduler.start()
    print("Scheduler started. ")


@bot.listen()
async def on_message(message):
    # don't respond to ourselves
    if message.author == bot.user:
        return
    if "reina" in message.content.lower().split():
        text = TextBlob(message.content.lower())
        if text.polarity >= 0.3:
            await message.add_reaction('♥️')
        if text.polarity <= -0.3:
            await message.add_reaction('💔')


@bot.listen()
async def on_member_join(member):
    new_member_role = bot.get_channel(465158208978157588).guild.get_role(663581221967757313)
    await member.add_roles(new_member_role)


async def prompt_keisanchuu(bot_b, t_minus):
    now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

    tv_radio_channel = bot.get_channel(465158208978157588)
    keisanchuu_role = tv_radio_channel.guild.get_role(641112458291052584)

    await tv_radio_channel.trigger_typing()

    alert_embed = discord.Embed(title="Keisanchu Reminder",
                                type='rich',
                                description="**Hey guys!** Time now is `{}`, The next episode of 22/7 {} is airing in **{} minutes**.\n"
                                            "You can watch it at:".format(now.strftime('%Y-%m-%d %H:%M %Z'),
                                                                          keisanchuu_role.mention, t_minus))

    alert_embed.add_field(name="Link 1", value="https://vk.com/videos-177082369")
    alert_embed.add_field(name="Link 2", value="https://ok.ru/videoembed/1977861545719")
    alert_embed.set_image(url="https://www.nanabunnonijyuuni.com/assets/img/tv/img_tv_visual.jpg")

    alert_embed.set_footer(text='R.E.I.N.A. scheduled message.', icon_url=bot_b.user.avatar_url)

    await tv_radio_channel.send(content=keisanchuu_role.mention, embed=alert_embed)


async def prompt_radio(bot_b, t_minus):
    now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

    tv_radio_channel = bot_b.get_channel(465158208978157588)
    radio_role = tv_radio_channel.guild.get_role(694627966495490078)

    await tv_radio_channel.trigger_typing()
    alert_embed = discord.Embed(title='Warikirenai Plus Radio Reminder',
                                type='rich',
                                description="**Hey guys!** Time now is `{}`, This week's {} Plus will start in **{} minutes**. \n\n"
                                            "If it's your first time viewing, you will be directed to a page requesting some simple demographics info. \n"
                                            "Fill out the form as best you can and click the bottom button to proceed to the stream.".format(
                                    now.strftime('%Y-%m-%d %H:%M %Z'), radio_role.mention, t_minus))

    alert_embed.add_field(name='You can watch it at',
                          value='http://www.uniqueradio.jp/agplayerf/player3.php')
    alert_embed.set_footer(text='R.E.I.N.A. scheduled message.', icon_url=bot_b.user.avatar_url)
    alert_embed.set_image(url='https://pbs.twimg.com/media/EUcZFgcUUAA43Rp?format=jpg&name=small')

    await tv_radio_channel.send(content=radio_role.mention, embed=alert_embed)


class Special(commands.Cog):
    def __init__(self, cog_bot):
        self.bot = cog_bot
        self._last_member = None

    @commands.command()
    @check_if_bot_spam()
    @commands.has_any_role('Moderators', 'Disciplinary Committee')
    async def protect(self, ctx):
        """
        (Mod-only command) Do mystery things.
        Note: this is an on-off switch command.
        """
        global new_member_loaded

        if new_member_loaded:
            bot.unload_extension("Modules.Authentication")
            new_member_loaded = False
            await ctx.send("Unloaded. ")
        else:
            bot.load_extension("Modules.Authentication")
            new_member_loaded = True
            await ctx.send("Loaded. ")


bot.load_extension("Modules.Authentication")
new_member_loaded = True

bot.add_cog(Default(bot))
bot.add_cog(Roles(bot))
bot.add_cog(Wariraji(bot))
bot.add_cog(Keisanchuu(bot))
bot.add_cog(Mods(bot))
bot.add_cog(Special(bot))
bot.run(TOKEN.TOKEN)
