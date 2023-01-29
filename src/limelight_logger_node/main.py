#!/usr/bin/env python3

import rospy
from threading import Thread

import cv2
import numpy

from sensor_msgs.msg import Image

def ros_func():

    limelight_addresses = rospy.get_param("/hmi_agent_node/drive_fwd_back_axis_id", [])

    limelight_capture = cv2.VideoCapture('http://10.1.95.11:5800')

    limelight_image_publisher = rospy.Publisher(name="/LimelightImage", data_class=Image, queue_size=10, tcp_nodelay=True)

    rate = rospy.Rate(20)

    while not rospy.is_shutdown():

        return_code, frame = limelight_capture.read()

        image_message = Image()
        image_message.header.stamp = rospy.get_rostime()
        image_message.width = frame.shape[1]
        image_message.height = frame.shape[0]
        image_message.encoding = "rgb8"
        image_message.header.frame_id = "limelight"
        image_message.data = list(numpy.array(frame).flatten())

        limelight_image_publisher.publish(image_message)

        rate.sleep()


def ros_main(node_name):
    rospy.init_node(node_name)

    t1 = Thread(target=ros_func)
    t1.start()

    rospy.spin()

    t1.join(5)
