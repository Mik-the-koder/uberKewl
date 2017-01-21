from discord.ext import commands
import discord.utils
import discord
import asyncio

client = discord.Client()
bot = commands.Bot(command_prefix = ';')

finger = """
```
.                     /´¯/)
                    ,/¯../
                   /..../
             /´¯/'...'/´¯¯`·¸
          /'/.../..../......./¨¯\\
        ('(...´...´.... ¯~/'....')
         \.................'..../
          ''...\.......... _.·´
            \..............(
              \.............\\
x
```
"""

class shataCommands:
    def __init__(self,bot):
        self.bot = bot

    @bot.command()
    async def shrug(self):
        """ ¯\\_(₹.₹)_/¯ """
        await self.bot.say('¯\\\_(₹.₹)\_/¯')

    @bot.group(pass_context=True)
    async def sexyvoice(self,ctx):
        """ super sexy voice in the voice channel """
        if ctx.invoked_subcommand is None:
            await self.bot.say('type `;help sexyvoice` to see the list of commands that can be used with `;sexyvoice`')

    @sexyvoice.command(pass_context=True)
    async def start(self,ctx):
        """ Start the super sexy voice in the voice channel ;) """
        if ctx.message.author.voice_channel is None:
            await self.bot.say('join a voice channel first')
            return
        try:
            voice = await self.bot.join_voice_channel(ctx.message.author.voice_channel)
        except discord.errors.ClientException as e:
            voice = self.bot.voice_client_in(ctx.message.server)
        player  = voice.create_ffmpeg_player('videoplayback.m4a')
##        player = await voice.create_ytdl_player('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        player.start()

    @sexyvoice.command(pass_context=True)
    async def stop(self,ctx):
        """ Stop the super sexy voice in the voice channel :( """
        if not self.bot.is_voice_connected(ctx.message.server):
            await self.bot.say('not in a voice channel m8')
            return
        await self.bot.voice_client_in(ctx.message.server).disconnect()

    @bot.command(pass_context=True)
    async def flipoff(self,ctx):
        """ flips off """
        if ctx.message.mentions:
            finger1 = finger.replace('x',' \t\t\t\t'+str(ctx.message.mentions[0]))
        else:
            finger1 = finger.replace('x',' \t\t\t\t'+str(ctx.message.author))
        await self.bot.say(finger1)

def setup(bot):
    bot.add_cog(shataCommands(bot))
