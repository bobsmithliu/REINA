import discord
from discord.ext import commands


def check_if_bot_spam():
    async def predicate(ctx):
        bot_channel = ctx.guild.get_channel(336287198510841856)
        return ctx.channel == bot_channel

    return commands.check(predicate)


def check_if_role_or_bot_spam():
    async def predicate(ctx):
        bot_channel = ctx.guild.get_channel(336287198510841856)
        role_channel = discord.utils.get(ctx.guild.channels, name='roles')
        return ctx.channel == bot_channel or ctx.channel == role_channel

    return commands.check(predicate)
