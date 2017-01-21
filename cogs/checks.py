from discord.ext import commands
import discord.utils
import dbaseConn

def checkAdmin(user):
    try:
        List = dbaseConn.showAdmin(user.server.id)
    except AttributeError:
        return False

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

def isAdmin():
    return commands.check(lambda ctx: checkAdmin(ctx.message))
