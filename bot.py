import datetime
import os
import sys
import traceback

import discord
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands

import Modules.Checks
from Modules.Authentication import Authentication
from Modules.General import General
from Modules.Mods import Mods
from Modules.MyHelp import MyHelp
from Modules.Pronouns import Pronouns
from Modules.Roles import Roles
from Modules.Showroom import Showroom
from Modules.Subscribe import Subscribe

# === CONSTANTS ===

TV_DESCRIPTION: str = '''
"Hey guys! Time now is `{}`, The next episode of 22/7 {} is airing in **{} minutes**.
You can watch it at:
'''

RADIO_DESCRIPTION: str = '''
Hey guys! Time now is `{}`, This week's {} Plus will start in **{} minutes**. \n\n
If it's your first time viewing, you will be directed to a page requesting some simple demographics info. \n
Fill out the form as best you can and click the bottom button to proceed to the stream.
'''

BOT_DESCRIPTION: str = '''
R.E.I.N.A. 2.17

Roles and Entertainment Information and Notification Agent

Licensed under WTFPL

Use >help [command] to see the help text of a specific command.

Use bot only in #bot spam
'''

KENZANCHUU_LINKS: [str] = [
    "https://www.zhanqi.tv/873082427",
    "https://ok.ru/videoembed/2733731028727",
    "https://vk.com/videos-177082369"
]

# === Intents Section ===

intents: discord.Intents = discord.Intents.default()
intents.members = True
intents.bans = False
intents.emojis = False
intents.integrations = False
intents.webhooks = False
intents.invites = False
intents.voice_states = False
intents.typing = False
intents.dm_typing = False
intents.guild_typing = False

member_cache_flags: discord.MemberCacheFlags = discord.MemberCacheFlags().none()
member_cache_flags.joined = True

# === Intents Section ===

bot: commands.Bot = commands.Bot(command_prefix='>', description=BOT_DESCRIPTION, case_insensitive=True,
                                 help_command=MyHelp(), intents=intents)
scheduler: AsyncIOScheduler = AsyncIOScheduler(timezone="Asia/Tokyo")


@bot.listen()
async def on_ready() -> None:
    print('Ready!')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(">help"))

    if scheduler.state == 0:
        scheduler.remove_all_jobs()

        scheduler.add_job(prompt_kenzanchuu, "cron", day_of_week='sat', hour=22, minute=30,
                          start_date=datetime.datetime(2021, 1, 9), args=[bot, 30])
        scheduler.add_job(prompt_kenzanchuu, "cron", day_of_week='sat', hour=22, minute=55,
                          start_date=datetime.datetime(2021, 1, 9), args=[bot, 5])
        scheduler.add_job(prompt_radio, "cron", day_of_week='sat', hour=15, minute=30, args=[bot, 30])
        scheduler.add_job(prompt_radio, "cron", day_of_week='sat', hour=15, minute=55, args=[bot, 5])

        print("Background Task Setup finished. ")

        scheduler.start()
        print("Scheduler started. ")


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
    print("Exception in command {}: ".format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):
        await ctx.reply('Incorrect number of arguments.')
        return

    if isinstance(error, Modules.Checks.IncorrectChannel):
        bot_channel: discord.TextChannel = ctx.guild.get_channel(336287198510841856)
        await ctx.reply('Please proceed with your action at {}.'.format(bot_channel.mention))
        return


# === Helpers ===

async def prompt_kenzanchuu(bot_b: commands.Bot, t_minus: int) -> None:
    now: datetime.datetime = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

    tv_radio_channel: discord.TextChannel = bot.get_channel(465158208978157588)
    kenzanchuu_role: discord.Role = tv_radio_channel.guild.get_role(641112458291052584)

    await tv_radio_channel.trigger_typing()

    alert_embed: discord.Embed = discord.Embed(title="Kenzanchu Reminder", type='rich',
                                               description=TV_DESCRIPTION.format(now.strftime('%Y-%m-%d %H:%M %Z'),
                                                                                 kenzanchuu_role.mention, t_minus))

    for index, item in enumerate(KENZANCHUU_LINKS, start=1):
        alert_embed.add_field(name="Link {}".format(index), value=item)

    alert_embed.set_image(url="https://nanabunnonijyuuni.com/images/4/a18/02ab0a833376c38b775887a818f8a.jpg")

    alert_embed.set_footer(text='R.E.I.N.A. scheduled message.', icon_url=bot_b.user.avatar_url)

    await tv_radio_channel.send(content=kenzanchuu_role.mention, embed=alert_embed)


async def prompt_radio(bot_b: commands.Bot, t_minus: int) -> None:
    now: datetime.datetime = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

    tv_radio_channel: discord.TextChannel = bot_b.get_channel(465158208978157588)
    radio_role: discord.Role = tv_radio_channel.guild.get_role(694627966495490078)

    await tv_radio_channel.trigger_typing()
    alert_embed: discord.Embed = discord.Embed(title='Warikirenai Plus Radio Reminder', type='rich',
                                               description=RADIO_DESCRIPTION.format(now.strftime('%Y-%m-%d %H:%M %Z'),
                                                                                    radio_role.mention, t_minus))

    alert_embed.add_field(name='You can watch it at',
                          value='http://www.uniqueradio.jp/agplayerf/player3.php')
    alert_embed.set_footer(text='R.E.I.N.A. scheduled message.', icon_url=bot_b.user.avatar_url)
    alert_embed.set_image(url='https://pbs.twimg.com/media/EUcZFgcUUAA43Rp?format=jpg&name=small')

    await tv_radio_channel.send(content=radio_role.mention, embed=alert_embed)

# === Helpers ===

bot.add_cog(General(bot))
bot.add_cog(Roles(bot))
bot.add_cog(Mods(bot))
bot.add_cog(Subscribe(bot))
bot.add_cog(Authentication(bot))
bot.add_cog(Pronouns(bot))
bot.add_cog(Showroom(bot))

bot.run(os.getenv("DISCORD_TOKEN"))
