import socket
import json
from multiprocessing import Process



def get_chennels():
    return {
        "channels": ["1", "2", "3"],
        "1": {
            "name": "channel 1",
            "movie-name":"COSTA RICA IN 4K 60fps HDR ULTRA HD",
            "MCAST_IP": "224.1.1.1",
            "MCAST_PORT": 5007,
        },
        "2":{
            "name": "channel 2",
            "movie-name":"Real 16K HDR 60FPS Dolby Vision",
            "MCAST_IP": "224.1.1.2",
            "MCAST_PORT": 5007,
        },
        "3":{
            "name": "channel 3",
            "movie-name":"The UNIVERSE in 4K 60fps",
            "MCAST_IP": "224.1.1.3",
            "MCAST_PORT": 5007,
        },
    }

def send_channels(addr):
    channels_data = json.dumps(get_chennels())
    try:
        conn.sendall(bytes(channels_data, 'ascii'))
    except BaseException:
        pass


if __name__ == '__main__':
    HOST = '192.168.243.97'
    PORT = 5005
    BUFF_SIZE = 65535
    from MCASTServer import STV
    
    # Run multicast channels on different processors
    channel1 = Process(target=STV, args=('224.1.1.1', 'movies/COSTA_RICA_IN_4K_60fps_HDR_ULTRA_HD__LXb3EKWsInQ_298.mp4', 5007, 2), kwargs={"JPEG_QUALITY":30})
    channel1.start()
    
    channel2 = Process(target=STV, args=('224.1.1.2', 'movies/Real_16K_HDR_60FPS_Dolby_Vision_62uLFAExx-k_299.mp4', 5007, 2), kwargs={"JPEG_QUALITY":30})
    channel2.start()
    
    channel3 = Process(target=STV, args=('224.1.1.3', 'movies/The_UNIVERSE_in_4K_60fps-EL2XOIVzvlU-22.mp4', 5007, 2), kwargs={"JPEG_QUALITY":30})
    channel3.start()

    # start TCP server
    print("start tcp server ...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print("server start ...")
        while True:
            conn, addr = sock.accept()
            with conn:
                od = conn.recv(BUFF_SIZE)
                if (od == b'ch'):
                    send_channels(addr)
