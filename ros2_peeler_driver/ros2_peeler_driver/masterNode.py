#! /usr/bin/env python3

from typing import List
import rclpy                 # import Rospy
from rclpy.node import Node  # import Rospy Node
from std_msgs.msg import String
from .services.srv import peelerAction
from .services.srv import peelerDesc

class masterNode(Node):
    
    def __init__(self):

        super().__init__('Master_Node')


        timer_period = 0.5  # seconds

        self.i1 = 0         # Count 1 
        
        
        self.descriptionSer = self.create_service(List, 'description', self.descriptionCallback, 10)

        self.actionSer = self.create_service(String, 'action', self.actionCallback)

        self.stateSub = self.create_subscription(String, 'state', self.stateCallback, 10)

        self.stateSub  # prevent unused variable warning

        



    def actionCallback(self, request, response):
        
        request.action = self.manager_command

        response.success = True


    
    def descriptionCallback(self, request, response):
        
        commandIndex = 0    #user input

        self.manager_command = request.command[commandIndex]

        response.success = True







    def stateCallback(self,msg):

        self.get_logger().info('I am the state topic "%s"' % msg.data)

    

def main(args = None):

    rclpy.init(args=args)  # initialize Ros2 communication

    node = masterNode()

    rclpy.spin(node)     # keep Ros2 communication open for action node

    rclpy.shutdown()     # kill Ros2 communication


if __name__ == '__main__':

    main()
