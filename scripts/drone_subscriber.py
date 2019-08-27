#!/usr/bin/env python3

#====================================Art by Ankit=====================================#

import rospy
import mavros
import numpy as np
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode
from std_msgs.msg import Float32
from geometry_msgs.msg import Vector3

# callback method for state sub
current_state = State()
offb_set_mode = SetMode
def state_cb(state):
    global current_state
    current_state = state
estimate = Vector3()

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %f %f %f" ,data.x,data.y, data.z)
    global estimate
    estimate = data


pos = PoseStamped()
def pos_cb(cur):
    global pos
    pos = cur

object_data = rospy.Subscriber('chatter', Vector3, callback)
local_pos_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
state_sub = rospy.Subscriber('mavros/state', State, state_cb)
current_pos_sub = rospy.Subscriber('mavros/local_position/pose', PoseStamped, pos_cb)
arming_client = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
set_mode_client = rospy.ServiceProxy('mavros/set_mode', SetMode)

pose = PoseStamped()
pose.pose.position.x = 0
pose.pose.position.y = 0
pose.pose.position.z = 2

def position_control():

    rospy.init_node('offb_node', anonymous=True)
    prev_state = current_state
    rate = rospy.Rate(20.0) # MUST be more then 2Hz

    # send a few setpoints before starting
    for i in range(100):
        local_pos_pub.publish(pose)
        rate.sleep()

    # wait for FCU connection
    while not current_state.connected:
        rate.sleep()

    last_request = rospy.get_rostime()
    while not rospy.is_shutdown():
        now = rospy.get_rostime()
        if current_state.mode != "OFFBOARD" and (now - last_request > rospy.Duration(5.)):
            set_mode_client(base_mode=0, custom_mode="OFFBOARD")
            last_request = now
        else:
            if not current_state.armed and (now - last_request > rospy.Duration(5.)):
               arming_client(True)
               last_request = now

        # older versions of PX4 always return success==True, so better to check Status instead
        if prev_state.armed != current_state.armed:
            rospy.loginfo("Vehicle armed: %r" % current_state.armed)
        if prev_state.mode != current_state.mode:
            rospy.loginfo("Current mode: %s" % current_state.mode)
        prev_state = current_state

        # Update timestamp and publish pose
        pose.header.stamp = rospy.Time.now()
        pose.pose.position.x = pos.pose.position.x + estimate.x
        pose.pose.position.y = pos.pose.position.y - estimate.z
        if(pos.pose.position.z > 2):
            pose.pose.position.z = pos.pose.position.z + estimate.y
        else:
            pose.pose.position.z = 2
        local_pos_pub.publish(pose)
        rate.sleep()

if __name__ == '__main__':
    try:
        position_control()
    except rospy.ROSInterruptException:
        pass
