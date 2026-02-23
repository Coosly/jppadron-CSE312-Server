import json
from uuid import uuid4

from pymongo import MongoClient
import html
import uuid

from util.response import Response
from util.database import chat_collection

def find_user(request, res):
    if request.cookies.get("session"):
        session_id = request.cookies.get("session")
        session_id = session_id.split(';')[0]
        chats = list(chat_collection.find({"session": session_id}))
        if chats == []:
            session_id = str(uuid.uuid4())
            user_id = "Joey" + str(uuid.uuid4())
            res.cookies({"session": session_id + "; HTTPOnly; Max-Age=7200"})
            return user_id, session_id, ""
        else:
            user_id = chats[0]["author"]
            nickname = chats[0]["nickname"]
            return user_id, session_id, nickname
    else:
        user_id = "Joey" + str(uuid.uuid4())
        session_id = str(uuid.uuid4())
        res.cookies({"session": session_id + "; HTTPOnly; Max-Age=7200"})
        return user_id, session_id, ""

def create_chat(request, handler):
    res = Response()
    user_id, session_id, nickname = find_user(request, res)
    content = json.loads(request.body.decode("utf-8")).get("content")
    content = html.escape(content)
    chat_collection.insert_one({"author" : str(user_id), "id" : str(uuid.uuid4()), "content" : str(content), "updated" : False, "session" : str(session_id), "reactions" : {}, "nickname" : str(nickname)})
    res.text("Message created successfully")
    res.text("Message sent successfully")
    handler.request.sendall(res.to_data())
    return

def get_chat(request, handler):
    res = Response()
    jason = list(chat_collection.find({}, {"_id" : 0, "session" : 0}))
    res.json({"messages" : jason})
    handler.request.sendall(res.to_data())
    return

def update_chat(request, handler):
    res = Response()
    user_id, session_id, _ = find_user(request, res)
    content = json.loads(request.body.decode("utf-8")).get("content")
    content = html.escape(content)
    id = request.path.split("/")[3]
    if session_id == chat_collection.find_one({"id": id}).get("session"):
        chat_collection.update_one({"id": id}, {"$set" : {"content" : content, "updated" : True}})
        res.text("Message updated successfully")
        handler.request.sendall(res.to_data())
        return
    else:
        res.set_status(403, "Forbidden")
        handler.request.sendall(res.to_data())
        return

def delete_chat(request, handler):
    res = Response()
    user_id, session_id, _ = find_user(request, res)
    id = request.path.split("/")[3]
    if session_id == chat_collection.find_one({"id": id}).get("session"):
        chat_collection.delete_one({"id": id})
        res.text("Message deleted successfully")
        handler.request.sendall(res.to_data())
        return
    else:
        res.set_status(403, "Forbidden")
        handler.request.sendall(res.to_data())
        return

def add_reaction(request, handler):
    res = Response()
    session_id = request.cookies.get("session")
    id = request.path.split("/")[3]
    emoji = json.loads(request.body.decode("utf-8")).get("emoji")
    emoji = html.escape(emoji)
    if emoji in chat_collection.find_one({"id": id}).get("reactions"):
        if session_id in chat_collection.find_one({"id": id}).get("reactions").get(emoji):
            res.set_status(403, "Forbidden")
            handler.request.sendall(res.to_data())
            return
        else:
            chat_collection.update_one({"id": id}, {"$push": {f"reactions.{emoji}": session_id}})
            res.text("Emoji added successfully")
            handler.request.sendall(res.to_data())
            return
    else:
        chat_collection.update_one({"id": id}, {"$push" : {f"reactions.{emoji}" : session_id}})
        res.text("Emoji added successfully")
        handler.request.sendall(res.to_data())
        return

def delete_reaction(request, handler):
    res = Response()
    session_id = request.cookies.get("session")
    id = request.path.split("/")[3]
    emoji = json.loads(request.body.decode("utf-8")).get("emoji")
    emoji = html.escape(emoji)
    if session_id in chat_collection.find_one({"id": id}).get("reactions").get(emoji):
        chat_collection.update_one({"id": id}, {"$pull": {f"reactions.{emoji}": session_id}})
        chat_collection.update_one({"id": id, f"reactions.{emoji}": {"$size": 0}}, {"$unset": {f"reactions.{emoji}": ""}})
        res.text("Emoji removed successfully")
        handler.request.sendall(res.to_data())
    else:
        res.set_status(403, "Forbidden")
        handler.request.sendall(res.to_data())
        return


def set_nickname(request, handler):
    res = Response()
    session_id = request.cookies.get("session")
    nickname = json.loads(request.body.decode("utf-8")).get("nickname")
    nickname = html.escape(nickname)
    chat_collection.update_many({"session": session_id}, {"$set": {"nickname": nickname}})
    res.text("Nickname set successfully")
    handler.request.sendall(res.to_data())

