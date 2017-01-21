from discord.ext import commands
import discord.utils
import dbaseConn
import discord
import random

bot = commands.Bot(command_prefix = ';')

class normalCommands: 
    def __init__(self,bot):
        self.bot = bot

    @bot.command()
    async def stats(self):
        """ stats about the bot """
        await self.bot.say("```I\'m being used in "+str(len(self.bot.servers))+' servers by '+str(len(list(self.bot.get_all_members())))+' users```')

    @bot.command(hidden=True)
    async def flip(self):
        """ ayyyyyy """
        x = bool(random.randrange(0,2))
        message = await self.bot.say('.')
        await self.bot.edit_message(message,'\\')
        await self.bot.edit_message(message,'-')
        await self.bot.edit_message(message,'/')
        await self.bot.edit_message(message,'-')
        if x == True:
            await self.bot.edit_message(message,'Heads !')
        else:
            await self.bot.edit_message(message,'Tails !')

    @bot.command()
    async def invite(self):
        """ post invite link """
        rl = 'https://discordapp.com/oauth2/authorize?client_id=232810583123165186&scope=bot&permissions=317844529'
        msg = discord.Embed (
                title = 'Invite Link',
                description = 'Invite me to yer server with this >.<',
                image = self.bot.user.avatar_url,
                url = rl 
            ).set_author(name = self.bot.user.name,url = rl, icon_url = self.bot.user.avatar_url )
        await self.bot.say(embed=msg)

    @bot.command()
    async def yass(self):
        """ says yass in dank way """
        await self.bot.say('```yass```')

    @bot.command()
    async def sass(self):
        """ says sass in dank way """
        await self.bot.say('```sass```')

    @bot.command(pass_context=True)
    async def swag(self,ctx,message='swag'):
        """ tells who the swaggest swagger is """
        await self.bot.say('<@'+ctx.message.author.id+'> u sweg beatch')

    @bot.group(pass_context=True)
    async def todo(self,ctx):
        """ add, show or remove items from your todo list """
        if ctx.invoked_subcommand is None:
            await self.bot.say('type `;help todo` to see the list of commands that can be used with `;todo`')

    @todo.command(pass_context=True)
    async def add(self,ctx,*,message):
        """ Add an item to the todo  list """
        dbaseConn.insertTodo(ctx.message.author.id,message)
        await self.bot.say('<@'+str(ctx.message.author.id)+'> '+message+' has  been added to your todo list')

    @todo.command(pass_context=True)
    async def show(self,ctx,message='str'):
        """ show  your todo list """
        f = dbaseConn.showTodo(ctx.message.author.id)
        if bool(f): 
            await self.bot.say('<@'+str(ctx.message.author.id)+'> your todo has the following items: ')
            for v in [i for i, x in enumerate(f)]:
                await self.bot.say(str(v+1)+'. '+f[v]+'\n')
        else:
            await self.bot.say('your todo list is empty')

    @todo.command(pass_context=True)
    async def remove(self,ctx,message : int):
        """ remove  items from todo list """
        f = dbaseConn.showTodo(ctx.message.author.id)
        f.pop((int(message)-1))
        dbaseConn.insertTodo(ctx.message.author.id,f)

def setup(bot):
    bot.add_cog(normalCommands(bot))
