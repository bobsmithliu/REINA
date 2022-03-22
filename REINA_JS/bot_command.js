// Const declaration
const { SlashCommandBuilder } = require('@discordjs/builders');
const { REST } = require('@discordjs/rest');
const { Routes } = require('discord-api-types/v9');
const { clientId, guildId, token } = require('./config.json');

const commands = [
	new SlashCommandBuilder().setName('help').setDescription('This command would reply all available commands and parameters of the bot'),
	new SlashCommandBuilder().setName('role').setDescription('Add role.'),
]
	.map(command => command.toJSON());

const rest = new REST({ version:'9' }).setToken(token);

rest.put(Routes.applicationGuildCommand(clientId, guildId), { body:commands })
	.then(() => console.log('Successfully registered applciation commands.'))
	.catch(console.error);
