from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

# def http_consumer(message):
#     # Make standard HTTP response - access ASGI path attribute directly
#     response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
#     # Encode that response into message format (ASGI)
#     for chunk in AsgiHandler.encode_response(response):
#         message.reply_channel.send(chunk)

##Connected to websocket.connect
@channel_session
def ws_connect(message):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Work out room name from path (ignore slashes)
    room = message.content['path'].strip("/")
    # Save room in session and add us to the group
    message.channel_session['room'] = room
    Group("chat-%s" % room).add(message.reply_channel)

# Connected to websocket.receive
@channel_session
def ws_message(message):
    Group("chat-%s" % message.channel_session['room']).send({
        "text": message['text'],
    })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
