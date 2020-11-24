import ssl
import logging

from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
from engineio.payload import Payload

Payload.max_decode_packets = 1000000

app = Flask(__name__)
sio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

mem = {}

@app.route("/")
def index():
    return "Server is open"

@sio.on("message")
def message(message):
    emit("message", message)


@sio.on("connection")
def connection(json):
    roomId = json["roomId"]

    join_room(roomId)
    emit("message", json["message"])

@sio.on("send")
def send(json):
    print("------------------------------------------------------------")

    roomId = json["roomId"]
    address = json["address"]
    image = json["image"]

    mem[address] = image

    print(address+mem[address][:30]+"...")
    cmem = mem.copy()

    cmem.pop(address)
    try:
        print(cmem.popitem()[1][:30]+"...")
    except:
        print("NO HAVE CONNECTION WITH OTHER DEVICE")

    emit("image", {"image":image}, room=roomId, broadcast=True, include_self=False)


if __name__ == '__main__':
    from OpenSSL import SSL

    context = SSL.Context(SSL.SSLv23_METHOD)  ## SSL.Context(SSL.SSLv23_METHOD)
    cert = 'future.crt'
    pkey = 'future.key'
    context.use_privatekey_file(pkey)
    context.use_certificate_file(cert)
    sio.run(app, host="0.0.0.0", port=5000) # , ssl_context=(cert, pkey)