from discord.ext import commands
import discord.utils
import dbaseConn
import discord
import asyncio

client = discord.Client()
bot = commands.Bot(command_prefix = ';')

class adminCommands:
    def __init__(self,bot):
        self.bot = bot
        def checkAdmin(user):
            List = dbaseConn.showAdmin(user.server.id)
            userRole = user.author.roles  
            if user.author.server_permissions.administrator:
                return True
            elif True:
                for x in range(len(List)):
                    for y in userRole:
                        if y.id in List[x][0]:
                            return True
            else:
                return False

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
    
        self.checkAdmin = checkAdmin
        self.getMute = getMute

    @bot.group(pass_context=True)
    async def admin(self,ctx):
        """ admin commands """
        if self.checkAdmin(ctx.message):
            if ctx.invoked_subcommand is None:
                await self.bot.say('type `;help admin` to see the list of commands that can be used with `;admin`')
        else:
            await self.bot.say("You don't have the perms m8")

    @admin.command(pass_context=True,name='add')
    async def _add(self,ctx,message:discord.Role):
        if self.checkAdmin(ctx.message): 
            dbaseConn.insertAdmin(ctx.message.server.id,message.id,message.name)
            await self.bot.say('role added to the admin list')
        else:
            await self.bot.say("You don't have the perms m8")

    @admin.command(pass_context=True,name='show')
    async def _show(self,ctx):
        """ shows your admin list, works only for admins """
        if self.checkAdmin(ctx.message):
            f = dbaseConn.showAdmin(ctx.message.server.id)
            if bool(f): 
                await self.bot.say('This servers admin list has the following roles: ')
                for x in range(len(f)):
                    await self.bot.say(str(x+1)+'. '+str(f[x][1]))
            else:
                await self.bot.say('your admin list is empty')
        else:
            await self.bot.say("You don't have the perms m8")

    @admin.command(pass_context=True,name='remove')
    async def _remove(self,ctx,message : int):
         """ remove  roles from admin list, works only for admins """
         if self.checkAdmin(ctx.message):
             f = dbaseConn.showAdmin(ctx.message.server.id)
             f.pop((int(message)-1))
             dbaseConn.removeAdmin(ctx.message.server.id,f)
             await self.bot.say('Removed the role from the Admin list')
         else:
             await self.bot.say("You don't have the perms m8")

    @bot.command(pass_context=True)
    async def mod(self,ctx,message : discord.Member):
        """ register a complain against a user """
        dbaseConn.insertMod(ctx.message.server.id,str(ctx.message.mentions[0]),str(ctx.message.author))
        await self.bot.delete_message(ctx.message)

    @bot.command(pass_context=True)
    async def show(self,ctx):
        """ shows members , works only for admins"""
        if self.checkAdmin(ctx.message):
            f = dbaseConn.showMod(ctx.message.server.id)  
            await self.bot.say('wait up yo!')
            for x in range(len(f)):
                await self.bot.say(str(x+1)+'. '+f[x][0]+str(' was ratted out by ')+f[x][1])
        else:
             await self.bot.say("You don't have the perms m8")

    @bot.command(pass_context=True)
    async def remove(self,ctx, message : int):
        """ removes members , works only for admins"""
        if self.checkAdmin(ctx.message):
            f = dbaseConn.showMod(ctx.message.server.id)  
            await self.bot.say('wait up yo!')
            f.pop(int(message)-1)
            dbaseConn.removeMod(ctx.message.server.id,f) 
        else:
             await self.bot.say("You don't have the perms m8")

    @bot.group(pass_context=True,name='voice')
    async def voice(self,ctx):
        """ admin voice commands """
        if ctx.invoked_subcommand is None:
            await self.bot.say('type `;help voice` to see the list of commands that can be used with `;voice`')

    @voice.command(pass_context=True)
    async def deafen(self,ctx,message : discord.Member):
        """ deafen a member in the voice channel , works only for admins """
        try:
            if self.checkAdmin(ctx.message):
                await self.bot.server_voice_state(ctx.message.mentions[0],mute=True, deafen=True)
                await self.bot.say('deafened '+str(ctx.message.mentions[0]))
        except discord.errors.Forbidden:
            await self.bot.say("I don't have the permissions to perform this operation")

    @voice.command(pass_context=True)
    async def undeafen(self,ctx,message : discord.Member):
        """ undeafen a member in the voice channel , works only for admins """
        try:
            if self.checkAdmin(ctx.message):
                await self.bot.server_voice_state(ctx.message.mentions[0], mute=False, deafen=False)
                await self.bot.say('Undeafened '+str(ctx.message.mentions[0]))
        except discord.errors.Forbidden:
            await self.bot.say('I don\'t have the permissions to perform this operation')

    @voice.command(pass_context=True,name='mute')
    async def _mute(self,ctx,message : discord.Member):
        """ mute a member in the voice channel , works only for admins """
        try:
            if self.checkAdmin(ctx.message):
                await self.bot.server_voice_state(ctx.message.mentions[0],mute=True, deafen=False)
                await self.bot.say('Muted '+str(ctx.message.mentions[0]))
        except discord.errors.Forbidden:
            await self.bot.say("I don't have the permissions to perform this operation")

    @voice.command(pass_context=True,name='unmute')
    async def _unmute(self,ctx,message : discord.Member):
        """ unmute a member in the voice channel , works only for admins """
        try:
            if self.checkAdmin(ctx.message):
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
    async def mute(self,ctx,message):
        """ mute a user in the server """
        try:
            if self.checkAdmin(ctx.message):
                try:
                    muteRole = await self.getMute(ctx.message)
                except TypeError:
                    muteRole = self.getMute(ctx.message)
                await self.bot.add_roles(ctx.message.mentions[0],muteRole)
                await self.bot.say('user muted')
        except discord.errors.Forbidden:
            await self.bot.say("I don't have the permissions to perform this operation")

    @chat.command(pass_context=True)
    async def unmute(self,ctx,message):
        """ unmute a user in the server """
        try:
            if self.checkAdmin(ctx.message):
                muteRole = self.getMute(ctx.message)
                await self.bot.remove_roles(ctx.message.mentions[0],muteRole)
                await self.bot.say('user unmuted')
        except discord.errors.Forbidden:
            await self.bot.say("I don't have the permissions to perform this operation")

def setup(bot):
    bot.add_cog(adminCommands(bot))
