from discord.ext import commands
import discord.utils
import dbaseConn
import discord
import asyncio
from cogs import checks

client = discord.Client()
bot = commands.Bot(command_prefix = ';')

class adminCommands:
    def __init__(self,bot):
        self.bot = bot

	def getMute(message):
            Roles = message.server.roles
            for role in Roles:
                if role.name == 'redMute' or role.name == 'AethexMuted':
                    return role
            else:
                newRole = self.bot.create_role (
                        message.server,
                        name = 'redMute',
                        colour = discord.Colour(int(0x71368a)),
                        permissions = discord.Permissions(0)
                )
                return newRole 
    
        self.getMute = getMute

    @bot.group(pass_context=True)
    async def admin(self,ctx):
        """ admin commands """
        if ctx.invoked_subcommand is None:
            await self.bot.say('type `;help admin` to see the list of commands that can be used with `;admin`')

    @admin.command(pass_context=True,name='add')
    @checks.isAdmin()
    async def _add(self,ctx,message:discord.Role):
        dbaseConn.insertAdmin(ctx.message.server.id,message.id,message.name)
        await self.bot.say('role added to the admin list')

    @admin.command(pass_context=True,name='show')
    @checks.isAdmin()
    async def _show(self,ctx):
        """ shows your admin list, works only for admins """
        f = dbaseConn.showAdmin(ctx.message.server.id)
        if bool(f): 
            await self.bot.say('This servers admin list has the following roles: ')
            for x in range(len(f)):
                await self.bot.say(str(x+1)+'. '+str(f[x][1]))
        else:
            await self.bot.say('your admin list is empty')

    @admin.command(pass_context=True,name='remove')
    @checks.isAdmin()
    async def _remove(self,ctx,message : int):
         """ remove  roles from admin list, works only for admins """
         f = dbaseConn.showAdmin(ctx.message.server.id)
         f.pop((int(message)-1))
         dbaseConn.removeAdmin(ctx.message.server.id,f)
         await self.bot.say("You don't have the perms m8")

    @bot.command(pass_context=True)
    async def mod(self,ctx,message : discord.Member):
        """ register a complain against a user """
        dbaseConn.insertMod(ctx.message.server.id,str(ctx.message.mentions[0]),str(ctx.message.author))
        await self.bot.delete_message(ctx.message)

    @bot.command(pass_context=True)
    @checks.isAdmin()
    async def show(self,ctx):
        """ shows members , works only for admins"""
        f = dbaseConn.showMod(ctx.message.server.id)  
        await self.bot.say('wait up yo!')
        for x in range(len(f)):
            await self.bot.say(str(x+1)+'. '+f[x][0]+str(' was ratted out by ')+f[x][1])

    @bot.command(pass_context=True)
    @checks.isAdmin()
    async def remove(self,ctx, message : int):
        """ removes members , works only for admins"""
        f = dbaseConn.showMod(ctx.message.server.id)  
        await self.bot.say('wait up yo!')
        f.pop(int(message)-1)
        dbaseConn.removeMod(ctx.message.server.id,f) 

    @bot.group(pass_context=True,name='voice')
    async def voice(self,ctx):
        """ admin voice commands """
        if ctx.invoked_subcommand is None:
            await self.bot.say('type `;help voice` to see the list of commands that can be used with `;voice`')

    @voice.command(pass_context=True)
    @checks.isAdmin()
    async def deafen(self,ctx,message : discord.Member):
        """ deafen a member in the voice channel , works only for admins """
        try:
            await self.bot.server_voice_state(ctx.message.mentions[0],mute=True, deafen=True)
            await self.bot.say('deafened '+str(ctx.message.mentions[0]))
        except discord.errors.Forbidden:
            await self.bot.say("I don't have the permissions to perform this operation")

    @voice.command(pass_context=True)
    @checks.isAdmin()
    async def undeafen(self,ctx,message : discord.Member):
        """ undeafen a member in the voice channel , works only for admins """
        try:
            await self.bot.server_voice_state(ctx.message.mentions[0], mute=False, deafen=False)
            await self.bot.say('Undeafened '+str(ctx.message.mentions[0]))
        except discord.errors.Forbidden:
            await self.bot.say('I don\'t have the permissions to perform this operation')

    @voice.command(pass_context=True,name='mute')
    @checks.isAdmin()
    async def _mute(self,ctx,message : discord.Member):
        """ mute a member in the voice channel , works only for admins """
        try:
            await self.bot.server_voice_state(ctx.message.mentions[0],mute=True, deafen=False)
            await self.bot.say('Muted '+str(ctx.message.mentions[0]))
        except discord.errors.Forbidden:
            await self.bot.say("I don't have the permissions to perform this operation")

    @voice.command(pass_context=True,name='unmute')
    @checks.isAdmin()
    async def _unmute(self,ctx,message : discord.Member):
        """ unmute a member in the voice channel , works only for admins """
        try:
            await self.bot.server_voice_state(ctx.message.mentions[0], mute=False, deafen=False)
            await self.bot.say('Unmuted '+str(ctx.message.mentions[0]))
        except discord.errors.Forbidden:
            await self.bot.say('I don\'t have the permissions to perform this operation')
    
    @bot.group(pass_context=True,name='chat')
    async def chat(self,ctx):
        """ admin chat commands """
        if ctx.invoked_subcommand is None:
            await self.bot.say('type `;help chat` to see the list of commands under `;chat`')
	
    @chat.command(pass_context=True)
    @checks.isAdmin()
    async def mute(self,ctx,message):
        """ mute a user in the server """
        try:
            try:
                muteRole = await self.getMute(ctx.message)
            except TypeError:
                muteRole = self.getMute(ctx.message)
            await self.bot.add_roles(ctx.message.mentions[0],muteRole)
            await self.bot.say('user muted')
        except discord.errors.Forbidden:
            await self.bot.say("I don't have the permissions to perform this operation")

    @chat.command(pass_context=True)
    @checks.isAdmin()
    async def unmute(self,ctx,message):
        """ unmute a user in the server """
        try:
            muteRole = self.getMute(ctx.message)
            await self.bot.remove_roles(ctx.message.mentions[0],muteRole)
            await self.bot.say('user unmuted')
        except discord.errors.Forbidden:
            await self.bot.say("I don't have the permissions to perform this operation")

def setup(bot):
    bot.add_cog(adminCommands(bot))
