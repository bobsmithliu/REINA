import discord
import asyncio
import datetime
import pytz

import TOKEN

jptz = pytz.timezone('Asia/Tokyo')


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_member_join(self, member):
        new_member_role = self.get_channel(465158208978157588).guild.get_role(663581221967757313)
        await member.add_roles(new_member_role)

    async def my_background_task(self):
        await self.wait_until_ready()
        radio_channel = self.get_channel(465158208978157588)  # channel ID goes here
        anime_channel = discord.utils.get(self.guilds[0].channels, name="anime-spoilers")
        print("now sending timed message to channel {} ({}) and {} ({})".format(radio_channel.name, radio_channel.id, anime_channel.name, anime_channel.id))
        print("Background Task engaged.")
        while not self.is_closed():
            now = datetime.datetime.now(jptz)

            # =================== KURATEN =====================

            kuraten_role = radio_channel.guild.get_role(641113337186222080)
            anime_role = radio_channel.guild.get_role(668634086172131378)

            # Kuraten 30 min alert
            if now.weekday() == 6 and now.hour == 10 and now.minute == 30 and now.second == 0:
                await radio_channel.trigger_typing()
                alert_embed = discord.Embed(title='Kuraten! Reminder',
                                            type='rich',
                                            description="**Hey guys!** Time now is `{}`, This week's {} will start in **30 minutes**. \n\n"
                                                        "If it's your first time viewing, you will be directed to a page requesting some simple demographics info. \n"
                                                        "Fill out the form as best you can and click the bottom button to proceed to the stream.".format(now.strftime('%Y-%m-%d %H:%M %Z'), kuraten_role.mention))

                alert_embed.add_field(name='You can watch it at', value='http://www.uniqueradio.jp/agplayerf/player3.php')
                alert_embed.set_footer(text='R.E.I.N.A. scheduled message.', icon_url=self.user.avatar_url)
                alert_embed.set_image(url='https://pbs.twimg.com/media/ELy19GhUUAEfzIP?format=jpg&name=medium')

                await radio_channel.send(content=kuraten_role.mention, embed=alert_embed)
            else:
                await asyncio.sleep(0.2)

            # Kuraten 5 min alert
            if now.weekday() == 6 and now.hour == 10 and now.minute == 55 and now.second == 0:
                await radio_channel.trigger_typing()

                alert_embed = discord.Embed(title='Kuraten! Reminder',
                                            type='rich',
                                            description="**Hey guys!** Time now is `{}`, This week's {} will start in **5 minutes**. \n\n"
                                                        "If it's your first time viewing, you will be directed to a page requesting some simple demographics info. \n"
                                                        "Fill out the form as best you can and click the bottom button to proceed to the stream.".format(now.strftime('%Y-%m-%d %H:%M %Z'), kuraten_role.mention))

                alert_embed.add_field(name='You can watch it at', value='http://www.uniqueradio.jp/agplayerf/player3.php')
                alert_embed.set_footer(text='R.E.I.N.A. scheduled message.', icon_url=self.user.avatar_url)
                alert_embed.set_image(url='https://pbs.twimg.com/media/ELy19GhUUAEfzIP?format=jpg&name=medium')

                await radio_channel.send(content=kuraten_role.mention, embed=alert_embed)
            else:
                await asyncio.sleep(0.2)

            # ======================= ANIME =========================

            # Anime 30 min alert
            if now.weekday() == 5 and now.hour == 22 and now.minute == 30 and now.second == 0:
                await anime_channel.trigger_typing()

                alert_embed = discord.Embed(title='Anime Reminder',
                                            type='rich',
                                            description="**Hey guys!** Time now is `{}`, This week's 22/7 anime will start in **30 minutes**. \n"
                                                        "You can watch it at: ".format(now.strftime('%Y-%m-%d %H:%M %Z')))

                alert_embed.add_field(name='Link 1', value='https://vk.com/videos-177082369')
                alert_embed.add_field(name='Link 2', value='https://ok.ru/videoembed/1461556485879')
                alert_embed.set_footer(text='R.E.I.N.A. scheduled message.', icon_url=self.user.avatar_url)
                alert_embed.set_image(url='https://www.nanabunnonijyuuni.com/assets/img/top/main/img_tv_anime.jpg')

                await anime_channel.send(content=anime_role.mention, embed=alert_embed)
            else:
                await asyncio.sleep(0.2)

            # Anime 5 min alert
            if now.weekday() == 5 and now.hour == 22 and now.minute == 55 and now.second == 0:
                await anime_channel.trigger_typing()

                alert_embed = discord.Embed(title='Anime Reminder',
                                            type='rich',
                                            description="**Hey guys!** Time now is `{}`, This week's 22/7 anime will start in **5 minutes**. \n"
                                                        "You can watch it at: ".format(now.strftime('%Y-%m-%d %H:%M %Z')))

                alert_embed.add_field(name='Link 1', value='https://vk.com/videos-177082369')
                alert_embed.add_field(name='Link 2', value='https://ok.ru/videoembed/1461556485879')
                alert_embed.set_footer(text='R.E.I.N.A. scheduled message.', icon_url=self.user.avatar_url)
                alert_embed.set_image(url='https://www.nanabunnonijyuuni.com/assets/img/top/main/img_tv_anime.jpg')

                await anime_channel.send(content=anime_role.mention, embed=alert_embed)
            else:
                await asyncio.sleep(0.2)


client = MyClient()
client.run(TOKEN.TOKEN)
