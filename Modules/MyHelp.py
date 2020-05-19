from discord.ext.commands.help import DefaultHelpCommand


class MyHelp(DefaultHelpCommand):
    def command_not_found(self, string):
        return 'Nope'
