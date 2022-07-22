#! /usr/bin/env python3

from tkinter import Image
import rclpy                 # import Rospy
from rclpy.node import Node  # import Rospy Node
from std_msgs.msg import String

# from .services.srv import peelerDesc


class cameraNode(Node):
    
    def __init__(self):
        
        self.i1 = 0

        super().__init__('Camera_Node')

        self.imagePub = self.create_publisher(Image, 'camera', self.imageCallback, 10)

        self.imagePub  # prevent unused variable warning


    def imageCallback(self):

        msg1 = Image()
        msg1.data = 'This is the camera topic %d' % self.i1
        self.imagePub.publish(msg1)
        self.get_logger().info('Publishing: "%s"' % msg1.data)


def main(args = None):

    rclpy.init(args=args)  # initialize Ros2 communication

    #node = cameraNode()

    #rclpy.spin(node)     # keep Ros2 communication open for action node

    rclpy.shutdown()     # kill Ros2 communication


if __name__ == '__main__':

    main()
