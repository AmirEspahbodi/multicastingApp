import cv2, socket, base64, numpy as np
import struct

def TV(MCAST_GRP, MCAST_PORT, BUFFER_SIZE=65535):
    print("starting channels ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((MCAST_GRP, MCAST_PORT))
        
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    print("chanel started!")
    while True:
        packet,_ = sock.recvfrom(BUFFER_SIZE)
        data = base64.b16decode(packet,' /')
        npdata = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(npdata, 1)
        
        cv2.imshow("client recv video ...", frame)
        key = cv2.waitKey(1) & 0xFF
        if (key==ord('q')):
            sock.close()
            pass

