import datetime

import discord
import pytz
from discord.ext import commands
from textblob import TextBlob
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

import TOKEN
from Modules.Default import Default
from Modules.Mods import Mods
from Modules.Roles import Roles
from Modules.MyHelp import MyHelp
from Modules.Checks import check_if_bot_spam, check_if_role_or_bot_spam
from Modules import CONSTANT

BOT_DESCRIPTION = '''
R.E.I.N.A. 2.02

Roles and Entertainment Information and Notification Agent

Licensed under WTFPL
'''

PRIVACY = '''
```
Privacy Policy

Using this bot (Discord unique user name: R.E.I.N.A. #3681, "this bot") means that you have read and understood this document.

The developer of this bot has made every possible effort to minimize data collection. However, to keep this bot operable responsively, some non-sensitive data will be collected in a non-permanent way. No data is ever stored permanently.

This bot will collect your messages and user information (meta-data included) sent to 22/7 Discord server (http://discord.gg/NxZ3W7Z, "this server") to a server operated by Amazon Web Services in its cache: a non-permanent storage system, for command processing. The bot only collects the most recent 1000 messages sent in this server. Your messages and information will be delete from the cache after a short period of time. 

If, in any way, you are not comfortable about how your data is collected and used, please immediately contact this bot's developer: Skk#9753. 
```
'''

bot = commands.Bot(command_prefix='>', description=BOT_DESCRIPTION, case_insensitive=True, help_command=MyHelp())
scheduler = AsyncIOScheduler()
REACTIONABLES = {}
COUNTER_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟", "🇦", "🇧", "🇨", "🇩", "🇪",
                  "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹"]


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


@bot.listen()
async def on_reaction_add(reaction, user):
    if reaction.message.id in REACTIONABLES and user.id != bot.user.id:
        bot_msg = await reaction.message.channel.fetch_message(reaction.message.id)

        if REACTIONABLES[reaction.message.id]["user"] == user.id:  # is the user reacted the user sent the message
            if REACTIONABLES[reaction.message.id]["category"] == "subscription" and reaction.emoji in COUNTER_EMOJIS:
                reaction_index = COUNTER_EMOJIS.index(reaction.emoji)

                if reaction_index < len(REACTIONABLES[reaction.message.id]["operatables"]):  # verify reaction
                    role = reaction.message.guild.get_role(REACTIONABLES[reaction.message.id]["operatables"][reaction_index])

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
                                description="Hey guys! Time now is `{}`, This week's {} Plus will start in **{} minutes**. \n\n"
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
    async def privacy(self, ctx):
        """
        Read this bot's privacy policy.
        """
        await ctx.send(PRIVACY)

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


class Subscribe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @check_if_bot_spam()
    async def subscribe(self, ctx):
        """
        Subscribe to a regular program notification.
        """
        user_roles = ctx.author.roles
        subscribeable_roles = [ctx.guild.get_role(x) for x in CONSTANT.SUBSCRIBEABLES]

        user_subscribed = list(set(user_roles) & set(subscribeable_roles))

        # get subscribe-able roles
        user_subscribeable = list(set(subscribeable_roles) - set(user_subscribed))

        if len(user_subscribeable) == 0:
            bot_msg = await ctx.send("You have no programs to subscribe to. ")
            await asyncio.sleep(3)
            await ctx.message.delete()
            await bot_msg.delete()
            return

        description_str = ""
        for emoji, role in zip(COUNTER_EMOJIS, user_subscribeable):
            description_str += "{} {}\n".format(emoji, role.name)

        # make embed
        sub_embed = discord.Embed(title="Choose a reaction to subscribe",
                                  colour=discord.Color.red(),
                                  description=description_str)
        sub_embed.set_author(name="You can subscribe to the following program(s)")
        sub_embed.set_footer(text="Note: you must react to the message within 60 seconds. ")

        sub_msg = await ctx.send(embed=sub_embed)

        # add reactions
        for _, emoji in zip(user_subscribeable, COUNTER_EMOJIS):
            await sub_msg.add_reaction(emoji)

        REACTIONABLES[sub_msg.id] = {
            "category": "subscription",
            "type": "add",
            "user": ctx.author.id,
            "operatables": [role.id for role in user_subscribeable]
        }

        await asyncio.sleep(3)
        await ctx.message.delete()
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
        subscribeable_roles = [ctx.guild.get_role(x) for x in CONSTANT.SUBSCRIBEABLES]

        user_subscribed = list(set(user_roles) & set(subscribeable_roles))

        if len(user_subscribed) == 0:
            bot_msg = await ctx.send("You have no programs to unsubscribe to. ")
            await asyncio.sleep(3)
            await ctx.message.delete()
            await bot_msg.delete()
            return

        description_str = ""
        for index, role in enumerate(user_subscribed):
            description_str += "{}. {}\n".format(index + 1, role.name)

        # make embed
        sub_embed = discord.Embed(title="Choose a reaction to unsubscribe",
                                  colour=discord.Color.red(),
                                  description=description_str)
        sub_embed.set_author(name="You can unsubscribe to the following program(s)")
        sub_embed.set_footer(text="Note: you must react to the message within 60 seconds. ")

        sub_msg = await ctx.send(embed=sub_embed)

        # add reactions
        for _, emoji in zip(user_subscribed, COUNTER_EMOJIS):
            await sub_msg.add_reaction(emoji)

        REACTIONABLES[sub_msg.id] = {
            "category": "subscription",
            "type": "remove",
            "user": ctx.author.id,
            "operatables": [role.id for role in user_subscribed]
        }

        await asyncio.sleep(3)
        await ctx.message.delete()
        await asyncio.sleep(60)
        if sub_msg.id in REACTIONABLES:
            await sub_msg.delete()
            del REACTIONABLES[sub_msg.id]


bot.load_extension("Modules.Authentication")
new_member_loaded = True

bot.add_cog(Default(bot))
bot.add_cog(Roles(bot))
bot.add_cog(Mods(bot))
bot.add_cog(Special(bot))
bot.add_cog(Subscribe(bot))
bot.run(TOKEN.TOKEN)
