#! /usr/bin/env python3

import rclpy                 # import Rospy
from rclpy.node import Node  # import Rospy Node
from std_msgs.msg import String
from .services.srv import sealerAction

from .drivers.sealer_client import A4S_SEALER_CLIENT # import sealer driver

sealer = A4S_SEALER_CLIENT("/dev/ttyUSB0")           # port name for sealer

class sealerNode(Node):

    '''
        The init function is neccesary for the sealerNode class to initialize all variables, parameters, and other functions.
        Inside the function the parameters exist, and calls to other functions and services are made so they can be executed in main.
    '''

    def __init__(self):
        
        super().__init__('Sealer_Node')

        timer_period = 0.5  # seconds

        self.i1 = 0         # Count 1 

        self.i2 = 0         # Count 2
        

        self.actionSub = self.create_subscription(String, 'action', self.actionCallback, 10)

        self.actionSub  # prevent unused variable warning


        self.statePub = self.create_publisher(String, 'state', 10)

        self.stateTimer = self.create_timer(timer_period, self.stateCallback)

        
        # self.stateOutput = self.create_timer(timer_period, self.driverCommunication)      Publishing sealer output

        
        self.descriptionPub = self.create_publisher(String, 'description', 10)

        self.descriptionTimer = self.create_timer(timer_period, self.descriptionCallback)

      
        self.actionService = self.create_service(String, 'actionCall', self.actionService)


    def actionService(self, request, response):

        self.manager_command = "test_command" #request.action # Run commands if manager sends corresponding command

        match self.manager_command:

            case "test_command":
                sealer.reset()

                response.success = True

            case other:
                response.success = False



    def actionCallback(self, msg):

        '''
        Stores the data received from the 'action' topic.
        '''

        self.get_logger().info('I am the action topic "%s"' % msg.data)


    def stateCallback(self):
        '''
        Publishes the sealer state to the 'state' topic.
        '''
        msg1 = String()
        msg1.data = 'This is the state topic: %d' % self.i1
        self.statePub.publish(msg1)
        self.get_logger().info('Publishing: "%s"' % msg1.data)
        self.i1 += 1

    def descriptionCallback(self):
        '''
        Publishes the sealer description to the 'description' topic.
        '''

        msg2 = String()
        msg2.data = 'This is the description topic %d' % self.i2
        self.descriptionPub.publish(msg2)
        self.get_logger().info('Publishing: "%s"' % msg2.data)
        self.i2 += 1

        
    def driverCommunication(self):

        '''
        Matches action received from action subscriber to sealer actions,
        and makes driver execute the command required to complete the action.
        '''

        self.manager_command = "test_command"  # Run commands if manager sends corresponding command


        match self.manager_command:
            
            case "test_command":
                sealer.reset()
    



def main(args = None):

    rclpy.init(args=args)  # initialize Ros2 communication

    node = sealerNode()

    rclpy.spin(node)     # keep Ros2 communication open for action node

    rclpy.shutdown()     # kill Ros2 communication


if __name__ == '__main__':

    main()
