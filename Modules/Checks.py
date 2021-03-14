import discord
from discord.ext import commands


class IncorrectChannel(commands.CommandError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def check_if_bot_spam():
    async def predicate(ctx: commands.Context):
        bot_channel: discord.TextChannel = ctx.guild.get_channel(336287198510841856)
        if ctx.channel != bot_channel:
            raise IncorrectChannel()
        else:
            return True

    return commands.check(predicate)


def check_if_role_or_bot_spam():
    async def predicate(ctx: commands.Context):
        bot_channel: discord.TextChannel = ctx.guild.get_channel(336287198510841856)
        role_channel: discord.TextChannel = discord.utils.get(ctx.guild.channels, name='roles')
        if ctx.channel != bot_channel and ctx.channel != role_channel:
            raise IncorrectChannel()
        else:
            return True

    return commands.check(predicate)
