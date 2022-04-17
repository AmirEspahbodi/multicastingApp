import cv2, imutils, socket, base64
import os
from time import sleep

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())



def STV(MCAST_GRP, VIDEO_PATH, MCAST_PORT=5007, MULTICAST_TTL=2, JPEG_QUALITY=30, WIDTH=400, BUFFER_SIZE=65535):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    info(f"starting MCAST CHANNEL {MCAST_GRP} ... ")
    while True:
        # Reduce the load of CPU.
        sleep(0.1)
        vid  = cv2.VideoCapture(VIDEO_PATH)
        print(f"video opened, MCAST_GRP = {MCAST_GRP}")
        while (vid.isOpened()):
            _,frame = vid.read()
            frame = imutils.resize(frame, width=WIDTH)
            encoded,buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
            message = base64.b16encode(buffer)
            sock.sendto(message, (MCAST_GRP, MCAST_PORT))
            
            #cv2.imshow("server transfering video ...", frame)
            key = cv2.waitKey(1) & 0xFF
            if (key==ord('q')):
                sock.close()
                pass
