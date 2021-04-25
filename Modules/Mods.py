import datetime
import time

import discord
import pytz
from discord.ext import commands

from Modules import CONSTANT
from Modules.CONSTANT import SHOWROOM_ALERT_ROLES
from Modules.Checks import check_if_bot_spam

JP_TZ: pytz.UTC = pytz.timezone('Asia/Tokyo')
UNIVERSAL_TZ: pytz.UTC = pytz.timezone('UTC')
PACIFIC_TZ: pytz.UTC = pytz.timezone('America/Los_Angeles')
CENTRAL_TZ: pytz.UTC = pytz.timezone('America/Chicago')
EASTERN_TZ: pytz.UTC = pytz.timezone('America/New_York')

TIMEZONES = [
    ("Japan Time", JP_TZ),
    ("Universal Time", UNIVERSAL_TZ),
    ("Pacific Time", PACIFIC_TZ),
    ("Central Time", CENTRAL_TZ),
    ("Eastern Time", EASTERN_TZ)]

TIME_FORMAT_STRING: str = "%Y-%m-%d %I:%M%p"


class Mods(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command()
    @commands.has_any_role('Moderators', 'Disciplinary Committee')
    @check_if_bot_spam()
    async def announce_sr(self, ctx: commands.Context, person: str, date: str, planned_time: str):
        """
        (Mod-only command) Make Showroom stream announcements.

        Make Showroom stream announcements at #227-streams.

        <person>: use member's first name, or use "Nananiji" for Nananiji Room stream on Showroom.
        <date>: use either "today" or "tomorrow" to indicate whether the stream is happening today or tomorrow.
        <planned_time>: "<two_digit_hour>:<two_digit_minute>" format in 24-hour standard.
        <unpin_time>: Unpin the announcement embed after this many seconds,
                    default value is an hour (3600 seconds), must be an integer.

        Valid first names are:
            Sally, Ruri, Mizzy, Kanaeru, Nagomin, Uta, Reinyan, Moe, Rettan, Ainacchi
        """
        stream_channel: discord.TextChannel = ctx.guild.get_channel(336281736633909258)

        if person in CONSTANT.SHOWROOM_STREAM_LINKS:
            role_to_ping: discord.Role = ctx.guild.get_role(SHOWROOM_ALERT_ROLES[person])

            await stream_channel.trigger_typing()
            now: datetime.datetime = datetime.datetime.now(JP_TZ)

            try:
                parsed_time = time.strptime(planned_time, "%H:%M")
            except ValueError:
                await ctx.reply("Time cannot be parsed. ")
                return

            stream_time = JP_TZ.localize(datetime.datetime(year=now.year,
                                                           month=now.month,
                                                           day=now.day,
                                                           hour=parsed_time.tm_hour,
                                                           minute=parsed_time.tm_min))

            if date == "tomorrow":
                stream_time = stream_time + datetime.timedelta(days=1)

            announcement_embed = discord.Embed(title="**{}**".format(CONSTANT.SHOWROOM_STREAM_LINKS[person][0]),
                                               type='rich',
                                               description='{}'.format(CONSTANT.SHOWROOM_STREAM_LINKS[person][1]),
                                               color=CONSTANT.SHOWROOM_STREAM_LINKS[person][2])

            for tz in TIMEZONES:
                announcement_embed.add_field(name=tz[0],
                                             value=stream_time.astimezone(tz[1]).strftime(TIME_FORMAT_STRING))

            announcement_embed.set_author(name='Upcoming Showroom Stream',
                                          icon_url="https://www.showroom-live.com/assets/img/v3/apple-touch-icon.png")

            # get local image
            img_file: discord.File = discord.File("assets/" + CONSTANT.SHOWROOM_STREAM_LINKS[person][3],
                                                  filename=CONSTANT.SHOWROOM_STREAM_LINKS[person][3])

            announcement_embed.set_image(url="attachment://" + CONSTANT.SHOWROOM_STREAM_LINKS[person][3])

            announcement_embed.set_footer(text='Sent by {}'.format(ctx.author.display_name),
                                          icon_url=ctx.author.avatar_url)

            await stream_channel.send(content=role_to_ping.mention, embed=announcement_embed)
            await ctx.reply("Success. ")

        else:
            await ctx.reply("Illegal name.")

    @commands.command()
    @commands.has_any_role('Moderators', 'Disciplinary Committee')
    @check_if_bot_spam()
    async def announce_insta(self, ctx: commands.Context, person: str, date: str, planned_time: str):
        """
        (Mod-only command) Make Instagram stream announcements.

        Make Instagram stream announcements at #227-streams.

        person: use members' first name.
        date: use either "today" or "tomorrow" to indicate whether the stream is happening today or tomorrow.
        planned_time: "<two_digit_hour>:<two_digit_minute>" format in 24-hour standard.

        Valid first names are:
            Chiharu, Reina, Sally, Aina, Kanae, Urara, Moe
        """
        stream_channel = ctx.guild.get_channel(336281736633909258)

        if person in CONSTANT.INSTAGRAM_STREAM_LINKS:
            await stream_channel.trigger_typing()
            now = datetime.datetime.now(JP_TZ)

            try:
                parsed_time = time.strptime(planned_time, "%H:%M")
            except ValueError:
                await ctx.reply("Time cannot be parsed. ")
                return

            stream_time = JP_TZ.localize(datetime.datetime(year=now.year,
                                                           month=now.month,
                                                           day=now.day,
                                                           hour=parsed_time.tm_hour,
                                                           minute=parsed_time.tm_min))

            if date == "tomorrow":
                stream_time = stream_time + datetime.timedelta(days=1)

            announcement_embed = discord.Embed(title="**{}**".format(CONSTANT.INSTAGRAM_STREAM_LINKS[person][0]),
                                               type='rich',
                                               description='{}'.format(CONSTANT.INSTAGRAM_STREAM_LINKS[person][1]),
                                               color=CONSTANT.INSTAGRAM_STREAM_LINKS[person][2])

            for tz in TIMEZONES:
                announcement_embed.add_field(name=tz[0],
                                             value=stream_time.astimezone(tz[1]).strftime(TIME_FORMAT_STRING))

            announcement_embed.set_author(name='Upcoming Instagram Stream',
                                          icon_url="https://instagram.com/static/images/ico/apple-touch-icon-180x180-precomposed.png/c06fdb2357bd.png")

            announcement_embed.set_footer(text='Sent by {}'.format(ctx.author.display_name),
                                          icon_url=ctx.author.avatar_url)

            await stream_channel.send(embed=announcement_embed)
            await ctx.reply("Success. ")
        else:
            await ctx.reply("You've put an illegal name or this person does not have an Instagram account yet. ")

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.MissingAnyRole):
            await ctx.reply("You are not in the list of privileged users, "
                            "this incident will be reported. (https://xkcd.com/838/)")
