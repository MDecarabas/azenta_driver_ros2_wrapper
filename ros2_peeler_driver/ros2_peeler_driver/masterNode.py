#! /usr/bin/env python3

from typing import List
import rclpy                 # import Rospy
from rclpy.node import Node  # import Rospy Node
from std_msgs.msg import String
# from .services.srv import peelerAction
# from .services.srv import peelerDesc
from .services.testDesc import command

class masterNode(Node):
    
    def __init__(self):

        super().__init__('masterNode')


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

        ###############################  
        '''
         sets variable of commands, client command list, client commands, 
         and parameters to the name of the commands, client command list, client commands, and parameters
        '''
        
        for response_command in response.command:
            # Command name
            # Format: <command name>
            globals()[f'{response_command[0]}'] = response_command[0]
            
            # Peeler commands
            #Format: <command name>_command_list
            globals()[f'{response_command[0]}_command_list'] = response_command[1]

            # Each Peeler Command
            # Format: <command name>_<peeler_command(without parentheses)>
            for peeler_command in response_command[1]:
                globals()[f'{response_command[0]}_{peeler_command}'] = peeler_command

            # Paramaters
            # Format: <command name>_<peeler_command(without parentheses)>_<parameter>
                for parameter_list in response_command[2]:
                    for parameter in parameter_list:
                        globals()[f'{response_command[0]}_{peeler_command}_{parameter}'] = parameter




        #################################

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
