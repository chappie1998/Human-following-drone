#!/usr/bin/env python3

#====================================Art by Ankit=====================================#

import argparse
import cv2
import dlib
import socket
import numpy as np
import rospy
from geometry_msgs.msg import Vector3
from std_msgs.msg import Float32


# drag and select the roi
def drag_and_select(event, x, y, flags, param):
    global dragging, roi_selected, startX, startY, endX, endY

    if event == cv2.EVENT_LBUTTONDOWN:
        (startX, startY) = (x, y)
        roi_selected = False
        dragging = True
    elif event == cv2.EVENT_LBUTTONUP:
        roi_selected = True
        dragging = False

    (endX, endY) = x, y

WIN_NAME = 'window'
WIN_WIDTH = int(800)
WIN_HEIGHT = int(600)

roi_selected = False
startX, startY, endX, endY = 0,0,0,0
dragging = False
tracker = dlib.correlation_tracker()
tracking = False
skip_frames = 0
pause_frames = False

cv2.namedWindow(WIN_NAME)
cv2.setMouseCallback(WIN_NAME, drag_and_select)

#video receiver setup
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


flag = 0
area0 = 0
area1 = 0
track_flag = False
while True:
    stream_bytes += connection.read(1024)
    first = stream_bytes.find(b'\xff\xd8')
    last = stream_bytes.find(b'\xff\xd9')
    if first != -1 and last != -1:
        jpg = stream_bytes[first:last + 2]
        stream_bytes = stream_bytes[last + 2:]
        if not pause_frames:
            skip_frames -= 1
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            if frame is None:
                break
            if skip_frames > 0:
                continue

            frame = cv2.resize(frame, (WIN_WIDTH, WIN_HEIGHT), cv2.INTER_AREA)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            draw_frame = frame.copy()

            if roi_selected:
                # track if roi is selected and tracking is turned on
                if tracking:
                    tracker.update(rgb)
                    pos = tracker.get_position()

                    startX = int(pos.left())
                    startY = int(pos.top())
                    endX = int(pos.right())
                    endY = int(pos.bottom())
                    cv2.rectangle(draw_frame, (startX, startY), (endX, endY), (0,255,0), 2)
                    cv2.putText(draw_frame, 'object', (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
                    data = Vector3()
                    if(track_flag == True):
                        data.x = (((startX + endX)/2)-400)/(endX-startX)
                        data.y = (((startY + endY)/2)-300)/(endY-startY)
                        area1 = ((endX - startX)*(endY - startY))
                        data.z = (area1-area0)/area0
                        pub = rospy.Publisher('chatter', Vector3, queue_size=10)
                        rospy.init_node('talker', anonymous=True)
                        rate = rospy.Rate(10)
                        rospy.loginfo(data)
                        pub.publish(data)

        if dragging == True:
            # draw the bounding box if dragging
            draw_frame = frame.copy()
            cv2.rectangle(draw_frame, (startX, startY), (endX, endY), (0,255,0), 2)
            cv2.putText(draw_frame, 'object', (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

        cv2.putText(draw_frame, 'Tracking: ' + str(tracking), (10, WIN_HEIGHT - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
        cv2.imshow(WIN_NAME, draw_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('s'):
            skip_frames = 100
        # toggle pause
        if key == ord('p'):
            if pause_frames is True:
                pause_frames = False
            else:
                pause_frames = True
        # toggle tracking
        if key == ord('t'):
            if tracking == False:
                if roi_selected:
                    tracking = True
                    rect = dlib.rectangle(startX, startY, endX, endY)
                    tracker.start_track(rgb, rect)
                    track_flag = True
                    area0 = (endX - startX)*(endY - startY)
            elif tracking == True:
                tracking = False

cv2.destroyAllWindows()
connection.close()
server_socket.close()

if __name__ == '__main__':
    try:
        None
    except rospy.ROSInterruptException:
        pass
