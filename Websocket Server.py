from websocket_server import WebsocketServer
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if message == "ping":
        server.send_message(client, "pong")
    elif message =="bg":
        print("bg")
        GPIO.output(22, True)
        GPIO.output(27, False)
    elif message =="fg":
        print("fg")
        GPIO.output(22, False)
        GPIO.output(27, True)
    elif message =="s":
        print("s")
        GPIO.output(27, False)
        GPIO.output(22, False)
    elif message =="l":
        print("l")
        GPIO.output(17, True)
        GPIO.output(23, False)
    elif message =="r":
        print("r")
        GPIO.output(17, False)
        GPIO.output(23, True)
    elif message =="c":
        print("c")
        GPIO.output(17, False)
        GPIO.output(23, False)
    elif len(message) > 200:
        message = message[:200] + '..'
    else:
        print("Client(%d) said: %s" % (client['id'], message))


PORT = 9001
server = WebsocketServer(9001, '0.0.0.0')
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
try:
    server.run_forever()
except:
    GPIO.cleanup()
