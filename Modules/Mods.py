import asyncio
import datetime

import aiohttp
import bs4
import discord
import pytz
import time
from discord.ext import commands

from Modules import CONSTANT
from Modules.Checks import check_if_bot_spam

jptz = pytz.timezone('Asia/Tokyo')
universaltz = pytz.timezone('UTC')
pacifictz = pytz.timezone('America/Los_Angeles')
centraltz = pytz.timezone('America/Chicago')
easterntz = pytz.timezone('America/New_York')


class Mods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @commands.has_any_role('Moderators', 'Disciplinary Committee')
    @check_if_bot_spam()
    async def announce(self, ctx, person, date, planned_time):
        """
        (Mod-only command) Make stream announcements.

        Make stream announcements at #227-streams.

        person: use members' first name, or use "Nananiji" for Nananiji Room stream.
        date: use either "today" or "tomorrow" to indicate whether the stream is happening today or tomorrow.
        planned_time: "<two_digit_hour>:<two_digit_minute>" format in 24Hr standard.

        Please note that when executing the command, the stream will need to be happening TODAY in Japan.
        """
        stream_channel = ctx.guild.get_channel(336281736633909258)

        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.62 Safari/537.36",
            'Referer': "https://www.showroom-live.com"
        }

        if person in CONSTANT.stream_links:
            await stream_channel.trigger_typing()
            now = datetime.datetime.now(jptz)

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(CONSTANT.stream_links[person][1], headers=headers) as r:
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

                announcement_embed = discord.Embed(title="**{}**".format(CONSTANT.stream_links[person][0]),
                                                   type='rich',
                                                   description='{}'.format(CONSTANT.stream_links[person][1]),
                                                   color=CONSTANT.stream_links[person][2])

                announcement_embed.add_field(name='Japan Time',
                                             value='{}'.format(stream_time.strftime("%Y-%m-%d %I:%M%p")))
                announcement_embed.add_field(name='Universal Time',
                                             value='{}'.format(
                                                 stream_time.astimezone(universaltz).strftime("%Y-%m-%d %I:%M%p")))
                announcement_embed.add_field(name='Eastern Time',
                                             value='{}'.format(
                                                 stream_time.astimezone(easterntz).strftime("%Y-%m-%d %I:%M%p")))
                announcement_embed.add_field(name='Central Time',
                                             value='{}'.format(
                                                 stream_time.astimezone(centraltz).strftime("%Y-%m-%d %I:%M%p")))
                announcement_embed.add_field(name='Pacific Time',
                                             value='{}'.format(
                                                 stream_time.astimezone(pacifictz).strftime("%Y-%m-%d %I:%M%p")))

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
