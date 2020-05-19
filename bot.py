import discord
from discord.ext import commands
from textblob import TextBlob

import TOKEN
from Modules.Default import Default
from Modules.Keisanchuu import Keisanchuu
from Modules.Mods import Mods
from Modules.Roles import Roles
from Modules.Wariraji import Wariraji
from Modules.MyHelp import MyHelp
from Modules.Checks import check_if_bot_spam

BOT_DESCRIPTION = '''
R.E.I.N.A. 1.25

Roles and Entertainment Information and Notification Agent

Licensed under WTFPL
'''

bot = commands.Bot(command_prefix='>', description=BOT_DESCRIPTION, case_insensitive=True, help_command=MyHelp())


@bot.listen()
async def on_ready():
    print('Ready!')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(">help"))


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


class Special(commands.Cog):
    def __init__(self, cog_bot):
        self.bot = cog_bot
        self._last_member = None

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


bot.load_extension("Modules.Authentication")
new_member_loaded = True

bot.add_cog(Default(bot))
bot.add_cog(Roles(bot))
bot.add_cog(Wariraji(bot))
bot.add_cog(Keisanchuu(bot))
bot.add_cog(Mods(bot))
bot.add_cog(Special(bot))
bot.run(TOKEN.TOKEN)
