from discord.ext.commands.help import DefaultHelpCommand


class MyHelp(DefaultHelpCommand):
    def command_not_found(self, string):
        return 'There is no such command, type `>help` to see a list of available commands. '
