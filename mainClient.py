import socket
import json
from MCASTClient import TV
from multiprocessing import Process


DEST_HOST = '192.168.243.97'
DEST_PORT = 5005
BUFF_SIZE = 65535

print("commands:\n",
      "/q: quit current tv\n",
      "/chu: update channels\n",
      "/ch: current channels\n",
      "/sch: select channels\n"
      )

CHANNELS = None
CURRENT_CHANEL = None

def updateChannels():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((DEST_HOST, DEST_PORT))
        sock.send(b'ch')
        channels_data = sock.recv(BUFF_SIZE)
        channels = json.loads(channels_data)
        print(channels)
        global CHANNELS
        CHANNELS = channels

def StartChanel(chid):
    if (chid not in CHANNELS["channels"]):
        print(f"channel with id={chid} does not exist")
        return
    else:
        global CURRENT_CHANEL
        if CURRENT_CHANEL:
            CURRENT_CHANEL.terminate()
        CURRENT_CHANEL = Process(target=TV, args=(CHANNELS[chid]["MCAST_IP"], 5007)) # here
        CURRENT_CHANEL.start()

def closeChannel():
    global CURRENT_CHANEL
    if CURRENT_CHANEL:
        CURRENT_CHANEL.terminate()
        CURRENT_CHANEL=None

if __name__ == "__main__":
    while True:
        command = input("command: ")
        if command == '/q':
            closeChannel()
        elif command == '/chu':
            updateChannels()
        elif command == '/ch':
            print(CHANNELS)
        elif command == '/sch':
            chid = input("enter channel ID: ")
            StartChanel(chid)
