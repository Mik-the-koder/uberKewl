from discord.ext import commands
import discord.utils
import dbaseConn
import discord
import logging
import random
import json

help_attrs = dict(hidden=True)
client = discord.Client ()
description = ''' uberKewl: A uber kewl bot written primarily to flip a coin. Has some extra stuff that you may find useful >.<'''
bot = commands.Bot(command_prefix = ';',pm_help = True, description = description, help_attrs=help_attrs)

logger = logging.getLogger('discord')
logger.setLevel(logging.CRITICAL)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

initial_extensions = [
    'cogs.normalCommands',
    'cogs.shataCommands',
    'cogs.adminCommands',
]

@bot.event
async def on_ready ():
    await bot.change_presence(game=discord.Game(name='prefix is ;'),status=discord.Status.online)
    print ('ready \a')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower().find('uberkewl') != -1:
        await bot.send_typing(message.channel)
        await bot.send_message(message.channel,'yes')
    if message.content.lower().find(';help') != -1:
        await bot.send_typing(message.channel)
        await bot.send_message(message.channel,"Help is on it's way! Check your messages !!")
    await bot.process_commands(message)

@bot.event
async def on_command_error(exception, context):
    message = context.message
    try:
       f = open('debugCMD.txt','a')
       f.write(
               "COMMAND **{}** IN **{}** ({}) by {} ({}) exception in {} [{}]\n\n".format
               (
                   message.content, 
                   message.server.name,
                   message.server.id,
                   message.author.name,
                   message.author.id,
                   type(exception),
                   exception
                )
       )
       f.close()
    except AttributeError:
       f = open('debugCMD.txt','a')
       f.write(
               "COMMAND {} DirectMessage by {} ({}) exception in {} [{}]\n\n".format
               (
                   message.content, 
                   message.author.name,
                   message.author.id,
                   type(exception),
                   exception
                )
            )
       f.close()

def loadCreds():
    with open('creds.json') as f:
        return json.load(f)

if __name__ == '__main__':
    creds = loadCreds()
    token = creds['token']
    
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    bot.run(token)
