#!/usr/bin/env python3

import tf2_ros
import rospy
from threading import Thread
from sensor_msgs.msg import Image

import cv2
import numpy as np
import rosbag

from frc_robot_utilities_py_node.frc_robot_utilities_py import *
from frc_robot_utilities_py_node.RobotStatusHelperPy import RobotStatusHelperPy, Alliance, RobotMode


def ros_func():
    global hmi_updates
    global robot_status

    cap = cv2.VideoCapture('http://10.1.95.11:5800')
    bag = rosbag.Bag('limelight_video.bag', 'w')

    rate = rospy.Rate(20)
    # Put your code in the appropriate sections in this if statement/while loop
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        cv2.imwrite('limelight_last_img.jpg', frame)

        stamp = roslib.rostime.Time.from_sec(time.time())
        ros_img = Image()
        ros_img.header.stamp = stamp
        ros_img.width = frame.shape[0]
        ros_img.height = frame.shape[1]
        ros_img.encoding = "rgb8"
        ros_img.header.frame_id = "limelight"
        ros_img.data = frame

        bag.write(ros_img, stamp)

        rate.sleep()

    bag.close()

def ros_main(node_name):
    rospy.init_node(node_name)
    register_for_robot_updates()

    t1 = Thread(target=ros_func)
    t1.start()

    rospy.spin()

    t1.join(5)
