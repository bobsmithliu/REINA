import asyncio
import datetime

import discord
import pytz
import schedule

import TOKEN


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    # TODO: Generalize prompting
    async def prompt_keisanchuu(self, t_minus):
        now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

        tv_radio_channel = self.get_channel(465158208978157588)
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

        alert_embed.set_footer(text='R.E.I.N.A. scheduled message.', icon_url=self.user.avatar_url)

        await tv_radio_channel.send(content=keisanchuu_role.mention, embed=alert_embed)

    async def prompt_radio(self, t_minus):
        now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

        tv_radio_channel = self.get_channel(465158208978157588)
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
        alert_embed.set_footer(text='R.E.I.N.A. scheduled message.', icon_url=self.user.avatar_url)
        alert_embed.set_image(url='https://pbs.twimg.com/media/EUcZFgcUUAA43Rp?format=jpg&name=small')

        await tv_radio_channel.send(content=radio_role.mention, embed=alert_embed)

    async def my_background_task(self):
        await self.wait_until_ready()

        schedule.every().saturday.at("22:30").do(self.prompt_keisanchuu, 30)
        schedule.every().saturday.at("22:55").do(self.prompt_keisanchuu, 5)
        schedule.every().saturday.at("15:30").do(self.prompt_radio, 30)
        schedule.every().saturday.at("15:55").do(self.prompt_radio, 5)

        print("Background Task engaged.")

        while not self.is_closed():
            schedule.run_pending()
            await asyncio.sleep(1)

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_member_join(self, member):
        new_member_role = self.get_channel(465158208978157588).guild.get_role(663581221967757313)
        await member.add_roles(new_member_role)


client = MyClient()
client.run(TOKEN.TOKEN)
