#! /usr/bin/env python3

from tkinter import Image
import rclpy                 # import Rospy
from rclpy.node import Node  # import Rospy Node
from std_msgs.msg import String
from .services.srv import peelerAction
# from .services.srv import peelerDesc



from .drivers.peeler_client import BROOKS_PEELER_CLIENT # import peeler driver

peeler = BROOKS_PEELER_CLIENT("/dev/ttyUSB0")           # port name for peeler

class peelerNode(Node):
    '''
    The peelerNode inputs data from the 'action' topic, providing a set of commands for the driver to execute. It then receives feedback, 
    based on the executed command and publishes the state of the peeler and a description of the peeler to the respective topics.
    '''
    def __init__(self):


        '''
        The init function is neccesary for the peelerNode class to initialize all variables, parameters, and other functions.
        Inside the function the parameters exist, and calls to other functions and services are made so they can be executed in main.
        '''

        super().__init__('Peeler_Node')

        self.state = "READY"

        # [
        # [command, [peeler command 1, peeler command 2], [[paramater 1( peeler command 1), paramater 2( peeler command 1)], [],[]]
        # repeat
        # ]
        self.peelerDescription = [
            ["prepare_peeler",["reset", "check_version", "check_status"], [[""],[""],[""]]],
            ["standard_peel", ["seal_check", "peel"], [[""],["loc", "time"]]],
            ["check_threshold", ["sensor_threshold"], [[""]]]
        ]

        timer_period = 0.5  # seconds

        self.i1 = 0         # Count 1 

        self.i2 = 0         # Count 2

        self.i3 = 0         # Count 3
        

        self.actionSub = self.create_subscription(String, 'action', self.actionCallback, 10)

        self.actionSub  # prevent unused variable warning


        self.statePub = self.create_publisher(String, 'state', 10)

        self.stateTimer = self.create_timer(timer_period, self.stateCallback)

        
            
        self.descriptionPub = self.create_publisher(String, 'description', 10)

        self.descriptionTimer = self.create_timer(timer_period, self.descriptionCallback)


        self.actionSer = self.create_service(String, "actionCall", self.actionSerCallback)
        

        self.cameraSub = self.create_subscription(Image, "camera", self.cameraCallback)
        
        
    #     self.descriptionSer = self.create_service(String, "description", self.descriptionSerCallback)

    
    def actionSerCallback(self, request, response):

        self.manager_command = request.action # Run commands if manager sends corresponding command

        self.state = "BUSY"

        match self.manager_command:
            
            case "prepare peeler":
                peeler.reset()
                peeler.check_version()
                peeler.check_status()

                response.success = True
            
            case "standard peel":
                peeler.seal_check()
                peeler.peel(1,2.5)

                response.success = True

            case "check threshold":
                peeler.sensor_threshold()

                response.success = True
                
            case other:
                response.success = False
        
        self.state = "COMPLETED"

        
        if "Error:" in peeler.peeler_output:
            self.state = peeler.error_msg
        
        peeler.error_msg = ""

        return response

    def actionCallback(self, msg):

        '''
        Stores the data received from the 'action' topic.
        '''

        self.get_logger().info('I am the action topic "%s"' % msg.data)

 
    def cameraCallback(self, msg):

        self.get_logger().info('I am the camera topic "%s"' % msg.data)
        


    def stateCallback(self):

        '''
        Publishes the peeler state to the 'state' topic. 
        '''

        msg = String()

        msg.data = 'State: %s' % self.state

        self.statePub.publish(msg)

        self.get_logger().info('Publishing: "%s"' % msg.data)

        self.i += 1


    def descriptionCallback(self):
        '''
        Publishes the peeler description to the 'description' topic.
        '''

        msg2 = String()
        msg2.data = 'This is the description topic %d' % self.i2
        self.descriptionPub.publish(msg2)
        self.get_logger().info('Publishing: "%s"' % msg2.data)
        self.i2 += 1

        
    def driverCommunication(self):

        '''
        Matches action received from action subscriber to peeler actions,
        and makes driver execute the command required to complete the action.
        '''

        self.manager_command = "test_command"  # Run commands if manager sends corresponding command


        match self.manager_command:
            
            case "test_command":
                peeler.check_status()
                peeler.check_version()
                peeler.reset()
    
        # self.statePub.publish(peeler.peeler_output)
        # self.get_logger().info('Publishing: "%s"' % peeler.peeler_output)      Publishing peeler output


def main(args = None):

    rclpy.init(args=args)  # initialize Ros2 communication

    #node = peelerNode()

    #rclpy.spin(node)     # keep Ros2 communication open for action node

    rclpy.shutdown()     # kill Ros2 communication


if __name__ == '__main__':

    main()
