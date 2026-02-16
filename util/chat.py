import json
from uuid import uuid4

from pymongo import MongoClient
import html
import uuid

from util.response import Response

mongo_client = MongoClient("localhost")
db = mongo_client["cse312"]
chat_collection = db["chat"]

def find_user(request, res):
    if request.cookies.get("session"):
        session_id = request.cookies.get("session")
        session_id = session_id.split(';')[0]
        chats = list(chat_collection.find({"session": session_id}))
        if chats == []:
            session_id = str(uuid.uuid4())
            user_id = "Joey" + str(uuid.uuid4())
            res.cookies({"session": session_id + "; HTTPOnly; Max-Age=7200"})
            return user_id, session_id
        else:
            user_id = chats[0]["author"]
            return user_id, session_id
    else:
        user_id = "Joey" + str(uuid.uuid4())
        session_id = str(uuid.uuid4())
        res.cookies({"session": session_id + "; HTTPOnly; Max-Age=7200"})
        return user_id, session_id

def create_chat(request, handler):
    res = Response()
    user_id, session_id = find_user(request, res)
    content = json.loads(request.body.decode("utf-8")).get("content")
    content = html.escape(content)
    chat_collection.insert_one({"author" : str(user_id), "id" : str(uuid.uuid4()), "content" : str(content), "updated" : False, "session" : str(session_id)})
    res.text("Message sent successfully")
    handler.request.sendall(res.to_data())
    return

def get_chat(request, handler):
    res = Response()
    jason = list(chat_collection.find({}, {"_id" : 0, "session" : 0}))
    res.json({"messages" : jason})
    handler.request.sendall(res.to_data())
    return
