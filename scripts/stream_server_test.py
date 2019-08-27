
#====================================Art by Ankit=====================================#

import numpy as np
import cv2
import

host = "192.168.43.113"
port = 8000
server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(0)
connection, client_address = server_socket.accept()
connection = connection.makefile('rb')
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

# need bytes here
stream_bytes = b' '
while True:
    stream_bytes += connection.read(1024)
    first = stream_bytes.find(b'\xff\xd8')
    last = stream_bytes.find(b'\xff\xd9')
    if first != -1 and last != -1:
        jpg = stream_bytes[first:last + 2]
        stream_bytes = stream_bytes[last + 2:]
        image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('image', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
connection.close()
server_socket.close()
