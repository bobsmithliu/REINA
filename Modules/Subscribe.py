import asyncio

import discord
from discord.ext import commands


from Modules.Checks import check_if_bot_spam
from Modules import CONSTANT


class Subscribe(commands.Cog):
    def __init__(self, b_bot: commands.Bot):
        self.bot: commands.Bot = b_bot
        self.REACTIONABLES: dict = {}
        self.COUNTER_EMOJIS: list[str] = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        if reaction.message.id in self.REACTIONABLES and user.id != self.bot.user.id:
            bot_msg: discord.Message = await reaction.message.channel.fetch_message(reaction.message.id)

            if self.REACTIONABLES[reaction.message.id]["user"] == user.id:
                # is the user reacted the user sent the message
                if self.REACTIONABLES[reaction.message.id]["category"] == "subscription" and reaction.emoji in self.COUNTER_EMOJIS:
                    reaction_index: int = self.COUNTER_EMOJIS.index(reaction.emoji)

                    if reaction_index < len(self.REACTIONABLES[reaction.message.id]["operable"]):  # verify reaction
                        role: discord.Role = reaction.message.guild.get_role(
                            self.REACTIONABLES[reaction.message.id]["operable"][reaction_index])

                        if self.REACTIONABLES[reaction.message.id]["type"] == "add":
                            await user.add_roles(role)
                        elif self.REACTIONABLES[reaction.message.id]["type"] == "remove":
                            await user.remove_roles(role)
                        await bot_msg.edit(content="Subscription configured. ", embed=None)

                del self.REACTIONABLES[reaction.message.id]
                await asyncio.sleep(5)
                await bot_msg.delete()

    @commands.command()
    @check_if_bot_spam()
    async def subscribe(self, ctx: commands.Context) -> None:
        """
        Subscribe to a regular program's notification.
        """
        user_roles: list[discord.Role] = ctx.author.roles
        subscribable_roles: list[discord.Role] = [ctx.guild.get_role(x) for x in CONSTANT.SUBSCRIBABLE]

        user_subscribed: list[discord.Role] = list(set(user_roles) & set(subscribable_roles))

        # get subscribe-able roles
        user_subscribable: list[discord.Role] = list(set(subscribable_roles) - set(user_subscribed))

        if len(user_subscribable) == 0:
            await ctx.send("Since you subscribed to all programs, you have no programs you can subscribe to. ")
            return

        description_str: str = ""
        for emoji, role in zip(self.COUNTER_EMOJIS, user_subscribable):
            description_str += "{} {}\n".format(emoji, role.name)

        # make embed
        sub_embed: discord.Embed = discord.Embed(title="Choose a reaction to subscribe", colour=discord.Color.red(),
                                                 description=description_str)
        sub_embed.set_author(name="You can subscribe to the following program(s)")
        sub_embed.set_footer(text="Note: you must react to the message within 60 seconds. ")

        sub_msg: discord.Message = await ctx.send(embed=sub_embed)

        # add reactions
        for _, emoji in zip(user_subscribable, self.COUNTER_EMOJIS):
            await sub_msg.add_reaction(emoji)

        self.REACTIONABLES[sub_msg.id] = {
            "category": "subscription",
            "type": "add",
            "user": ctx.author.id,
            "operable": [role.id for role in user_subscribable]
        }

        await asyncio.sleep(60)
        if sub_msg.id in self.REACTIONABLES:
            await sub_msg.delete()
            del self.REACTIONABLES[sub_msg.id]

    @commands.command()
    @check_if_bot_spam()
    async def unsubscribe(self, ctx: commands.Context):
        """
        Unsubscribe to a regular program's notification.
        """
        user_roles: list[discord.Role] = ctx.author.roles
        subscribable_roles: list[discord.Role] = [ctx.guild.get_role(x) for x in CONSTANT.SUBSCRIBABLE]

        user_subscribed: list[discord.Role] = list(set(user_roles) & set(subscribable_roles))

        if len(user_subscribed) == 0:
            await ctx.reply("Since you subscribed to no program, you have no programs to unsubscribe to. ")
            return

        description_str: str = ""
        for index, role in enumerate(user_subscribed):
            description_str += "{}. {}\n".format(index + 1, role.name)

        # make embed
        sub_embed: discord.Embed = discord.Embed(title="Choose a reaction to unsubscribe", colour=discord.Color.red(),
                                                 description=description_str)
        sub_embed.set_author(name="You can unsubscribe to the following program(s)")
        sub_embed.set_footer(text="Note: you must react to this message within 60 seconds. ")

        sub_msg: discord.Message = await ctx.send(embed=sub_embed)

        # add reactions
        for _, emoji in zip(user_subscribed, self.COUNTER_EMOJIS):
            await sub_msg.add_reaction(emoji)

        self.REACTIONABLES[sub_msg.id] = {
            "category": "subscription",
            "type": "remove",
            "user": ctx.author.id,
            "operable": [role.id for role in user_subscribed]
        }

        await asyncio.sleep(60)
        if sub_msg.id in self.REACTIONABLES:
            await sub_msg.delete()
            del self.REACTIONABLES[sub_msg.id]

    @subscribe.error
    @unsubscribe.error
    async def command_error(self, ctx, error):
        bot_channel: discord.TextChannel = ctx.guild.get_channel(336287198510841856)
        if isinstance(error, commands.CheckFailure):
            await ctx.send('Please proceed with your action at {}.'.format(bot_channel.mention))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Incorrect number of arguments.')
