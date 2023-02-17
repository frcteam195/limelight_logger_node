#!/usr/bin/env python3

import rospy
from threading import Thread

import cv2
import numpy

from sensor_msgs.msg import Image

def ros_func():

    limelight_front_capture = cv2.VideoCapture('http://10.1.95.11:5800')
    limelight_back_capture = cv2.VideoCapture('http://10.1.95.12:5800')

    limelight_front_image_publisher = rospy.Publisher(name="/LimelightFrontImage", data_class=Image, queue_size=100)
    limelight_back_image_publisher = rospy.Publisher(name="/LimelightBackImage", data_class=Image, queue_size=100)

    rate = rospy.Rate(50)

    while not rospy.is_shutdown():

        try:
            return_code, frame = limelight_front_capture.read()

            if return_code:
                image_message = Image()
                image_message.header.stamp = 0
                image_message.width = frame.shape[1]
                image_message.height = frame.shape[0]
                image_message.encoding = "rgb8"
                image_message.header.frame_id = "limelight"
                image_message.data = list(numpy.array(frame).flatten())

                limelight_front_image_publisher.publish(image_message)
        except:
            pass

        try:
            return_code, frame = limelight_back_capture.read()

            if return_code:

                image_message = Image()
                image_message.header.stamp = rospy.get_rostime()
                image_message.width = frame.shape[1]
                image_message.height = frame.shape[0]
                image_message.encoding = "rgb8"
                image_message.header.frame_id = "limelight"
                image_message.data = list(numpy.array(frame).flatten())

                limelight_back_image_publisher.publish(image_message)
        except:
            pass

        rate.sleep()


def ros_main(node_name):
    rospy.init_node(node_name)

    t1 = Thread(target=ros_func)
    t1.start()

    rospy.spin()

    t1.join(5)