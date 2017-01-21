from pymongo import errors as pymongoErrors
from pymongo import MongoClient
import os

client = MongoClient()
db = client.uberKewl

os.popen('mongod')

def insertTodo(userID,todoList):
    try:
        cursor = db.todo.find_one({"_id":userID})
        if bool(cursor):
#   If it is a string, aka if user is adding an item
            if type(todoList) == str:
                db.todo.update(
                        {
                            "_id":userID
                        },
                        {
                            '$push' : {
                                "todo":todoList
                                }
                        }
                )
#   If the script is updating the value, i.e used in deleting the values
            else:
                db.todo.update(
                    {
                        "_id":userID
                    },
                    {
                        "_id":userID,
                        "todo":todoList
                    }
                )
#   Creating the list for the user for the first time
        else:
            t = []
            t.append(todoList)
            db.todo.insert_one(
                    {
                        "_id":userID,
                        "todo":t
                    }
            )
    except pymongoErrors.DuplicateKeyError:
        pass

def showTodo(userID):
    try:
        cursor = ((db.todo.find({"_id":userID},{"todo":1,"_id":0})))
        for val in cursor:
            pass 
        return val["todo"]
    except (TypeError,UnboundLocalError):
        return None

def insertMod(serverID,compID,userID):
     try:
        cursor = db.mod.find_one({"_id":serverID})
        userList = [compID,userID]
        if bool(cursor):
            db.mod.update(
                    {
                        "_id" : serverID
                    },
                    {
                        '$push' : {
                            "userList" : userList 
                            }
                    }
            )
        else:
            t = []
            t.append(userList)
            db.mod.insert_one(
                    {
                        "_id":serverID,
                        "userList":t
                    }
            )
     except pymongoErrors.DuplicateKeyError:
        pass

def removeMod(serverID,newList):
    try:
        cursor = db.mod.find_one({"_id":serverID})
        db.mod.update (
                {
                    "_id":serverID
                },
                {
                    "userList":newList
                }
        )
    except (TypeError,UnboundLocalError):
        pass

def showMod(serverID):
    try:
        cursor = ((db.mod.find({"_id":serverID},{"userList":1,"_id":0})))
        for val in cursor:
            pass 
        return val["userList"]
    except (TypeError,UnboundLocalError):
        return None

def insertAdmin(serverID,roleID,roleName):
     try:
        cursor = db.admin_lst.find_one({"_id":serverID})
        role = (roleID,roleName)
        if bool(cursor):
            db.admin_lst.update(
                    {
                        "_id" : serverID
                    },
                    {
                        '$push' : {
                            "role" : role
                            }
                    }
            )
        else:
            t = []
            t.append(role)
            db.admin_lst.insert_one(
                    {
                        "_id":serverID,
                        "role":t
                    }
            )
     except pymongoErrors.DuplicateKeyError:
        pass

def removeAdmin(serverID,newList):
    try:
        cursor = db.admin_lst.find_one({"_id":serverID})
        db.admin_lst.update (
                {
                    "_id":serverID
                },
                {
                    "role":newList
                }
        )
    except (TypeError,UnboundLocalError):
        pass

def showAdmin(serverID):
    try:
        cursor = ((db.admin_lst.find({"_id":serverID},{"role":1,"_id":0})))
        for val in cursor:
            pass 
        return val["role"]
    except (TypeError,UnboundLocalError):
        return None
