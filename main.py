import discord
import asyncio
import datetime
import pytz

TOKEN = '[REDACTED]'

jptz = pytz.timezone('Asia/Tokyo')


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged on as', self.user)

    async def my_background_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(465158208978157588)  # channel ID goes here
        print("now sending timed message channel {}".format(channel.name))
        print("Background Task engaged.")
        while not self.is_closed():
            now = datetime.datetime.now(jptz)

            kuraten_role = channel.guild.get_role(641113337186222080)
            keisanchuu_role = channel.guild.get_role(641112458291052584)

            # Kuraten 30 min alert
            if now.weekday() == 6 and now.hour == 10 and now.minute == 30 and now.second == 0:
                await channel.trigger_typing()
                alert_embed = discord.Embed(title='Kuraten! Reminder',
                                            type='rich',
                                            description="**Hey guys!** Time now is `{}`, This week's {} will start in **30 minutes**."
                                                        "\nYou can watch it at http://www.uniqueradio.jp/agplayerf/player3.php \n\n"
                                                        "If it's your first time viewing, you will be directed to a page requesting some simple demographics info. \n"
                                                        "Fill out the form as best you can and click the bottom button to proceed to the stream.".format(now.strftime('%Y-%m-%d %H:%M %Z'), kuraten_role.mention))

                alert_embed.set_footer(text='R.E.I.N.A. scheduled message.', icon_url=self.user.avatar_url)
                alert_embed.set_image(url='https://pbs.twimg.com/media/ELy19GhUUAEfzIP?format=jpg&name=medium')

                await channel.send(embed=alert_embed)
            else:
                await asyncio.sleep(0.2)

            # Kuraten 5 min alert
            if now.weekday() == 6 and now.hour == 10 and now.minute == 55 and now.second == 0:
                await channel.trigger_typing()

                alert_embed = discord.Embed(title='Kuraten! Reminder',
                                            type='rich',
                                            description="**Hey guys!** Time now is `{}`, This week's {} will start in **5 minutes**."
                                                        "\nYou can watch it at http://www.uniqueradio.jp/agplayerf/player3.php \n\n"
                                                        "If it's your first time viewing, you will be directed to a page requesting some simple demographics info. \n"
                                                        "Fill out the form as best you can and click the bottom button to proceed to the stream.".format(now.strftime('%Y-%m-%d %H:%M %Z'), kuraten_role.mention))

                alert_embed.set_footer(text='R.E.I.N.A. scheduled message.', icon_url=self.user.avatar_url)
                alert_embed.set_image(url='https://pbs.twimg.com/media/ELy19GhUUAEfzIP?format=jpg&name=medium')

                await channel.send(embed=alert_embed)
            else:
                await asyncio.sleep(0.2)

            # Keisanchuu 30 min alert
            if now.weekday() == 5 and now.hour == 22 and now.minute == 30 and now.second == 0:
                await channel.trigger_typing()

                alert_embed = discord.Embed(title="Keisanchu Reminder",
                                            type='rich',
                                            description="**Hey guys!** Time now is `{}`, The next episode of 22/7 {} is airing in **30 minutes**.\n"
                                                        "You can watch it at:".format(now.strftime('%Y-%m-%d %H:%M %Z'), keisanchuu_role.mention))

                alert_embed.add_field(name="Link 1", value="https://vk.com/videos-177082369")
                alert_embed.add_field(name="Link 2", value="https://ok.ru/videoembed/1461556485879")

                alert_embed.set_footer(text='R.E.I.N.A. scheduled message.', icon_url=self.user.avatar_url)

                await channel.send(embed=alert_embed)
            else:
                await asyncio.sleep(0.2)

            # Keisanchuu 5 min alert
            if now.weekday() == 5 and now.hour == 22 and now.minute == 55 and now.second == 0:
                await channel.trigger_typing()

                alert_embed = discord.Embed(title="Keisanchu Reminder",
                                            type='rich',
                                            description="**Hey guys!** Time now is `{}`, The next episode of 22/7 {} is airing in **5 minutes**.\n"
                                                        "You can watch it at:".format(now.strftime('%Y-%m-%d %H:%M %Z'), keisanchuu_role.mention))

                alert_embed.add_field(name="Link 1", value="https://vk.com/videos-177082369")
                alert_embed.add_field(name="Link 2", value="https://ok.ru/videoembed/1461556485879")

                alert_embed.set_footer(text='R.E.I.N.A. scheduled message.', icon_url=self.user.avatar_url)

                await channel.send(embed=alert_embed)
            else:
                await asyncio.sleep(0.2)


client = MyClient()
client.run(TOKEN)
