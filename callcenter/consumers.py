import json

# In consumers.py
from channels import Group

# Connected to websocket.connect
def ws_add(message):
    message.reply_channel.send({"accept": True})
    Group("all-clients").add(message.reply_channel)

def ws_message(message):
    # Nothing to do here, because you only push, never receive.
    pass

# Connected to websocket.disconnect
def ws_disconnect(message):
    print("qqn se deconnecte")
    Group("all-clients").discard(message.reply_channel)

def send_message(message):
    Group("all-clients").send({"text": message})
