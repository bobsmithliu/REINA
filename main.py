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
        # self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_member_join(self, member):
        new_member_role = self.get_channel(465158208978157588).guild.get_role(663581221967757313)
        await member.add_roles(new_member_role)

    # async def my_background_task(self):
    #     await self.wait_until_ready()
    #     while not self.is_closed():
    #         now = datetime.datetime.now(jptz)


client = MyClient()
client.run(TOKEN.TOKEN)
