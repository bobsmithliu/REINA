import datetime
import os

import discord
import pytz
from discord.ext import commands
from textblob import TextBlob
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

from Modules.General import General
from Modules.Mods import Mods
from Modules.Roles import Roles
from Modules.Pronouns import Pronouns
from Modules.MyHelp import MyHelp
from Modules.Authentication import Authentication
from Modules.Checks import check_if_bot_spam
from Modules import CONSTANT

BOT_DESCRIPTION = '''
R.E.I.N.A. 2.10

Roles and Entertainment Information and Notification Agent

Licensed under WTFPL

Use >help [command] to see the help text of a specific command. 

Use bot only in #bot spam
'''

bot = commands.Bot(command_prefix='>', description=BOT_DESCRIPTION, case_insensitive=True, help_command=MyHelp())
scheduler = AsyncIOScheduler()
REACTIONABLES = {}
COUNTER_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


@bot.listen()
async def on_ready():
    print('Ready!')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(">help"))

    if scheduler.state == 0:
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


@bot.listen()
async def on_reaction_add(reaction, user):
    if reaction.message.id in REACTIONABLES and user.id != bot.user.id:
        bot_msg = await reaction.message.channel.fetch_message(reaction.message.id)

        if REACTIONABLES[reaction.message.id]["user"] == user.id:  # is the user reacted the user sent the message
            if REACTIONABLES[reaction.message.id]["category"] == "subscription" and reaction.emoji in COUNTER_EMOJIS:
                reaction_index = COUNTER_EMOJIS.index(reaction.emoji)

                if reaction_index < len(REACTIONABLES[reaction.message.id]["operable"]):  # verify reaction
                    role = reaction.message.guild.get_role(REACTIONABLES[reaction.message.id]["operable"][reaction_index])

                    if REACTIONABLES[reaction.message.id]["type"] == "add":
                        await user.add_roles(role)
                    elif REACTIONABLES[reaction.message.id]["type"] == "remove":
                        await user.remove_roles(role)
                    await bot_msg.edit(content="Subscription configured. ", embed=None)

            await bot_msg.clear_reactions()
            await asyncio.sleep(5)
            await bot_msg.delete()
            del REACTIONABLES[reaction.message.id]


async def prompt_keisanchuu(bot_b, t_minus):
    now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

    tv_radio_channel = bot.get_channel(465158208978157588)
    keisanchuu_role = tv_radio_channel.guild.get_role(641112458291052584)

    await tv_radio_channel.trigger_typing()

    alert_embed = discord.Embed(title="Keisanchu Reminder",
                                type='rich',
                                description="Hey guys! Time now is `{}`, The next episode of 22/7 {} is airing in **{} minutes**.\n"
                                            "You can watch it at:".format(now.strftime('%Y-%m-%d %H:%M %Z'),
                                                                          keisanchuu_role.mention, t_minus))

    alert_embed.add_field(name="Link 1", value="https://www.zhanqi.tv/873082427")
    alert_embed.add_field(name="Link 2", value="https://ok.ru/videoembed/2261404032759")
    alert_embed.add_field(name="Link 3", value="https://vk.com/videos-177082369")
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
                                description="Hey guys! Time now is `{}`, This week's {} Plus will start in **{} minutes**. \n\n"
                                            "If it's your first time viewing, you will be directed to a page requesting some simple demographics info. \n"
                                            "Fill out the form as best you can and click the bottom button to proceed to the stream.".format(now.strftime('%Y-%m-%d %H:%M %Z'), radio_role.mention, t_minus))

    alert_embed.add_field(name='You can watch it at',
                          value='http://www.uniqueradio.jp/agplayerf/player3.php')
    alert_embed.set_footer(text='R.E.I.N.A. scheduled message.', icon_url=bot_b.user.avatar_url)
    alert_embed.set_image(url='https://pbs.twimg.com/media/EUcZFgcUUAA43Rp?format=jpg&name=small')

    await tv_radio_channel.send(content=radio_role.mention, embed=alert_embed)


class Subscribe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @check_if_bot_spam()
    async def subscribe(self, ctx):
        """
        Subscribe to a regular program's notification.
        """
        user_roles = ctx.author.roles
        subscribable_roles = [ctx.guild.get_role(x) for x in CONSTANT.SUBSCRIBABLE]

        user_subscribed = list(set(user_roles) & set(subscribable_roles))

        # get subscribe-able roles
        user_subscribable = list(set(subscribable_roles) - set(user_subscribed))

        if len(user_subscribable) == 0:
            bot_msg = await ctx.send("Since you subscribed to all programs, you have no programs you can subscribe to. ")
            return

        description_str = ""
        for emoji, role in zip(COUNTER_EMOJIS, user_subscribable):
            description_str += "{} {}\n".format(emoji, role.name)

        # make embed
        sub_embed = discord.Embed(title="Choose a reaction to subscribe",
                                  colour=discord.Color.red(),
                                  description=description_str)
        sub_embed.set_author(name="You can subscribe to the following program(s)")
        sub_embed.set_footer(text="Note: you must react to the message within 60 seconds. ")

        sub_msg = await ctx.send(embed=sub_embed)

        # add reactions
        for _, emoji in zip(user_subscribable, COUNTER_EMOJIS):
            await sub_msg.add_reaction(emoji)

        REACTIONABLES[sub_msg.id] = {
            "category": "subscription",
            "type": "add",
            "user": ctx.author.id,
            "operable": [role.id for role in user_subscribable]
        }

        await asyncio.sleep(60)
        if sub_msg.id in REACTIONABLES:
            await sub_msg.delete()
            del REACTIONABLES[sub_msg.id]

    @commands.command()
    @check_if_bot_spam()
    async def unsubscribe(self, ctx):
        """
        Unsubscribe to a regular program's notification.
        """
        user_roles = ctx.author.roles
        subscribable_roles = [ctx.guild.get_role(x) for x in CONSTANT.SUBSCRIBABLE]

        user_subscribed = list(set(user_roles) & set(subscribable_roles))

        if len(user_subscribed) == 0:
            bot_msg = await ctx.send("Since you subscribed to no program, you have no programs to unsubscribe to. ")
            return

        description_str = ""
        for index, role in enumerate(user_subscribed):
            description_str += "{}. {}\n".format(index + 1, role.name)

        # make embed
        sub_embed = discord.Embed(title="Choose a reaction to unsubscribe",
                                  colour=discord.Color.red(),
                                  description=description_str)
        sub_embed.set_author(name="You can unsubscribe to the following program(s)")
        sub_embed.set_footer(text="Note: you must react to this message within 60 seconds. ")

        sub_msg = await ctx.send(embed=sub_embed)

        # add reactions
        for _, emoji in zip(user_subscribed, COUNTER_EMOJIS):
            await sub_msg.add_reaction(emoji)

        REACTIONABLES[sub_msg.id] = {
            "category": "subscription",
            "type": "remove",
            "user": ctx.author.id,
            "operable": [role.id for role in user_subscribed]
        }

        await asyncio.sleep(60)
        if sub_msg.id in REACTIONABLES:
            await sub_msg.delete()
            del REACTIONABLES[sub_msg.id]

    @subscribe.error
    @unsubscribe.error
    async def command_error(self, ctx, error):
        bot_channel = ctx.guild.get_channel(336287198510841856)
        if isinstance(error, commands.CheckFailure):
            await ctx.send('Please proceed your action at {}.'.format(bot_channel.mention))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Incorrect number of arguments.')


bot.add_cog(General(bot))
bot.add_cog(Roles(bot))
bot.add_cog(Mods(bot))
bot.add_cog(Subscribe(bot))
bot.add_cog(Authentication(bot))
bot.add_cog(Pronouns(bot))
bot.run(os.getenv('DISCORD_TOKEN'))
