import time
import serial
import logging
import re

#Log Configuration
# file_path = os.path.join(os.path.split(os.path.dirname(__file__))[0]  + '/sealer_logs/sealer_logs.log')
# logging.basicConfig(filename = file_path, level=logging.DEBUG, format = '[%(levelname)s] [%(asctime)s] [%(name)s] %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')


class BROOKS_PEELER_CLIENT():
    """
    Description: 
                 - Python interface that allows remote commands to be executed using simple string messages to XPeel. 
    Serial Communication Messages from the Robot:
                 - Responses from XPeel are displayed in the terminal.
    """
    def __init__(self, host_path, baud_rate=9600):

        self.host_path = host_path
        self.baud_rate = baud_rate
        self.status_var = ""
        # self.version = self.check_version()
        self.tape_remaining_var = 0
        self.sensor_threshold_var = 0


    def connect_peeler(self):
        #Connect to serial port / If wrong port entered inform user 
        try:
            ser = serial.Serial(self.host_path, self.baud_rate)
        except:
            print("Wrong port entered")
            pass
        return ser


    def response_fun(self, time_wait):                         
        ser = self.connect_peeler()
        response_timer = time.time()
        while time.time() - response_timer < time_wait: 
            if ser.in_waiting != 0:           
                response = ser.read_until(expected=b'\r')
                response_string = response.decode('utf-8')
                break
            else:
                response_string = ""
        return response_string
    

    def send_command(self, command, success_msg, err_msg, timeout=1):

        print('COMMAND: ' + command)
        #check if connected / if not (error? / reconnect?)
        ser = self.connect_peeler()        
        ser.write(command.encode('utf-8'))        

        #Declares success/error messsage if none are given
        ready_timer = time.time()
        response_buffer = ""

        while "ready" not in response_buffer:
            new_string = self.response_fun(timeout)

            if new_string != "":
                print(new_string)

            response_buffer = response_buffer + new_string
            if "ack" in new_string:
                print('ACK TRUE')

            if time.time() - ready_timer > 20:
                break

        self.error(response_buffer)

        return response_buffer

    def error(self, response_buffer):        
        error_dict = {
            "00" : "",
            "01" : "Error: Conveyor motor stalled",
            "02" : "Error: Elevator motor stalled",
            "03" : "Error: Take up spool staled",
            "04" : "Error: Seal not removed",
            "05" : "Error: Illegal Command",
            "06" : "Error: No plate found", 
            "07" : "Error: Out of tape, or tape broke",
            "08" : "Error: Parameters not saved",
            "09" : "Error: Stop button pressed while running",
            "10" : "Error: Seal Sensor unplugged or broke",
            "20" : "Error: Less than 30 seals left on the supply roll",
            "21" : "Error: Room for less than 30 seals on take up spool",
            "51" : "Error: Emergency Stop: Power relay is not settable- i.e. cover open, or hardware problem",
            "52" : "Error: Circuitry Fault Detected: Remove Power"
            }

        response_string = re.search(r"\*ready:(\d+,\d+,\d+)", response_buffer)
        error_code = response_string[1]

        first_error = error_code[0:2]
        second_error = error_code[3:5]
        third_error = error_code [6:8]
        if first_error == "00" and second_error == "00" and third_error == "00":
            error_code_msg = "No Errors"
        else:
            error_code_msg = error_dict[first_error]+ "\n" + error_dict[second_error] + "\n" + error_dict[third_error]

        print(error_code_msg)


    def check_status(self):
        cmd_string = '*stat\r\n'
        success_msg = "Displaying status:"
        err_msg = "Displaying status:"
        self.send_command(cmd_string, success_msg, err_msg)


    
    def check_version(self):
        cmd_string = '*version\r\n'
        success_msg = "XPeel Firmware Version:"
        err_msg = "Failed to display XPeel firmware version"
        response = self.send_command(cmd_string, success_msg, err_msg)   

        global matches_ver

        matches_ver = re.search(r"\*(\d+.\d+)",response)

        version = matches_ver[1]

        print('Version = ' + version)
        return version


    def reset(self):
        cmd_string = '*reset\r\n'
        success_msg = "Successful reset"
        err_msg = "Failed to reset"
        self.send_command(cmd_string, success_msg, err_msg)


    def restart(self):
        cmd_string = '*restart\r\n'
        success_msg = "Successful restart"
        err_msg = "Failed to restart"
        self.send_command(cmd_string, success_msg, err_msg)        


    def peel(self, param_set_num, param_time):
        peel_dict = {
            1: ["default -2 mm", "fast"],
            2: ["default -2 mm", "slow"],
            3: ["default", "fast"],
            4: ["default", "slow"],
            5: ["default +2 mm", "fast"],
            6: ["default +2 mm", "slow"],
            7: ["default +4 mm", "fast"],
            8: ["default +4 mm", "slow"],
            9: ["custom", "custom"]
        }
        cmd_string = '*xpeel:%s%s\r\n'%(param_set_num, int(param_time/2.5))
        success_msg = "Successfully adjusted peel location to %s and speed to %s" %(peel_dict[param_set_num][0], peel_dict[param_set_num][1])
        err_msg = "Failed to adjust peel location to %s and speed to %s"%(peel_dict[param_set_num][0], peel_dict[param_set_num][1])
        self.send_command(cmd_string, success_msg, err_msg)      


    def seal_check(self):
        cmd_string = '*sealcheck\r\n'
        success_msg = "Successful seal check"
        err_msg = "Failed to conduct seal check"
        self.send_command(cmd_string, success_msg, err_msg)        
    

    def tape_remaining(self):
        cmd_string = '*tapeleft\r\n'
        success_msg = " deseals remaining on supply spool \n deseals remaining on take-up spool"
        err_msg = "Failed to find amount of tape remaining"
        response = self.send_command(cmd_string, success_msg, err_msg)   

        matches = re.search(r"\*tape:(\d+),(\d+)",response)

        deseals_supply = int(matches[1])*10
        deseals_take = int(matches[2]) *10
        print("Deseals on supply spool: " + str(deseals_supply))
        print("Deseals on take-up spool: "+ str(deseals_take))
        return deseals_supply, deseals_take


    def plate_check(self, pc_yn = ""):
        #pc_yn = y for yes n for no
        pc_yn = input("Set platecheck to yes (y) or no (n): ")
        cmd_string = '*platecheck:%s\r\n'%(pc_yn)
        if pc_yn == "y":
            pc_yn_string =  "yes"
        if pc_yn == "n":
            pc_yn_string = "no"
        success_msg = "Platecheck set to %s"%(pc_yn_string)
        err_msg = "Failed to set plate check to %s"%(pc_yn_string)
        self.send_command(cmd_string, success_msg, err_msg)   


    def sensor_threshold(self, threshold_value = "Not Found"):
        cmd_string = '*sealstat\r\n'
        success_msg = "Threshold value of %s for the seal detected sensor" %(threshold_value)
        err_msg = "Failed to get threshold value"
        response = self.send_command(cmd_string, success_msg, err_msg)   
    
        matches = re.search(r"\*seal:(\d+)",response)

        threshold_value = matches[1]
        
        print("Threshold Value: " + threshold_value)
        return threshold_value


    def sensor_threshold_higher(self, seal_higher_input = "", threshold_value_high = "Not Found"):
        seal_higher_input = input("3 digit threshold value: ")
        cmd_string = '*sealhigher:%s\r\n'%(seal_higher_input)
        success_msg = "Threshold value of %s for the seal detected sensor" %(threshold_value_high)
        err_msg = "Failed to get threshold value"
        response = self.send_command(cmd_string, success_msg, err_msg)  

        matches = re.search(r"\*seal:(\d+)",response)

        threshold_value_high = matches[1]

        print("Threshold Value: " + threshold_value_high)


    def sensor_threshold_lower(self, seal_lower_input = "", threshold_value_low = "Not Found"):
        seal_lower_input = input("3 digit threshold value: ")
        cmd_string = '*seallower:%s\r\n' %(seal_lower_input)
        success_msg = "Threshold value of %s for the seal detected sensor" %(threshold_value_low)
        err_msg = "Failed to get threshold value"
        response = self.send_command(cmd_string, success_msg, err_msg)

        matches = re.search(r"\*seal:(\d+)",response)

        threshold_value_low = matches[1]

        print("Threshold Value: " + threshold_value_low)

    def conveyor_out(self):
        cmd_string = '*moveout\r\n'
        success_msg = "Successfully moved conveyor out"
        err_msg = "Failed to move conveyor out"
        self.send_command(cmd_string, success_msg, err_msg) 
#^^^ doesn't move
    def conveyor_in(self):
        cmd_string = '*movein\r\n'
        success_msg = "Successfully moved conveyor in"
        err_msg = "Failed to move conveyor in"
        self.send_command(cmd_string, success_msg, err_msg) 

    def elevator_down(self):
        cmd_string = '*movedown\r\n'
        success_msg = "Successfully moved elevator down"
        err_msg = "Failed to move elevator down"
        self.send_command(cmd_string, success_msg, err_msg) 

    def elevator_up(self):
        cmd_string = '*moveup\r\n'
        success_msg = "Successfully moved elevator up"
        err_msg = "Failed to move elevator up"
        self.send_command(cmd_string, success_msg, err_msg) 
#^^^ doesn't move
    def move_spool(self):
        cmd_string = '*movespool\r\n'
        success_msg = "Successfully moved spool 10 mm"
        err_msg = "Failed to move spool 10 mm"
        self.send_command(cmd_string, success_msg, err_msg) 
     



if __name__ == "__main__":

    peeler_client = BROOKS_PEELER_CLIENT("/dev/ttyUSB0")
    peeler_client.move_spool()
