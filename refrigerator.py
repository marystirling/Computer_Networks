# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for the Smart Refrigerator client
#          needed for the Computer Networks course Assignments
#
#          Since we are hoping to develop a very crude networking stack
#          in this course, we will see that our client uses an Application
#          layer object instead of directly using the ZeroMQ socket API, which
#          is used under the hood at some layer.  That in turn uses a Transport
#          object and so on.
#

# import the needed packages
import os     # for OS functions
import sys    # for syspath and system exception
import time   # for sleep
import argparse # for argument parsing
import configparser # for configuration parsing
import zmq # actually not needed here but we are printing zmq version and hence needed
import random 
import time
import netifaces as ni



# add to the python system path so that the following packages can be found
# relative to this directory
sys.path.insert (0, os.getcwd ())

# this is our application level protocol and its message types
from applnlayer.CustomApplnProtocol import CustomApplnProtocol as ApplnProtoObj
from applnlayer.ApplnMessageTypes import GroceryOrderMessage
from applnlayer.ApplnMessageTypes import HealthStatusMessage
from applnlayer.ApplnMessageTypes import ResponseMessage

time_list = []
groc_server_ip = ''
health_server_ip = ''
dest_port = 5555
##################################
#       Refrigerator class
##################################
class Refrigerator ():

  ########################################
  # constructor
  ########################################
  def __init__ (self):
    self.iters = None
    self.req_ratio = None
    self.groc_obj = None
    self.health_obj = None

  ########################################
  # configure/initialize
  ########################################
  def initialize (self, args):
    ''' Initialize the object '''

    try:
      # Here we initialize any internal variables
      print ("Refrigerator Object: Initialize")
    
      # initialize our variables
      self.iters = args.iters
      self.req_ratio = args.req_ratio

      # Now, get the configuration object
      config = configparser.ConfigParser ()
      config.read (args.config)
      
      if (config["Network"]["Route"] == "route1"):
          groc_server_ip = "10.0.0.5"
          health_server_ip = "10.0.0.6"
      elif (config["Network"]["Route"] == "route2"):
          groc_server_ip = "10.0.0.1"
          health_server_ip = "10.0.0.27"
      print(f"GROCERY SERVER IP is {groc_server_ip}")
    
      # Next, obtain the custom application protocol objects
      self.groc_obj = ApplnProtoObj (False)  # the false flag indicates this is a client side
      self.health_obj = ApplnProtoObj (False)  # the false flag indicates this is a client side

      # initialize the custom application objects
      self.groc_obj.initialize (config, args.groc_ip, args.groc_port)
      self.health_obj.initialize (config, args.status_ip, args.status_port)

    except Exception as e:
      raise e

  ########################################
  #  A generator of the grocery message
  ########################################
  def gen_grocery_order_msg (self):
    '''Grocery order message generator '''

    groc_msg = GroceryOrderMessage ()
    
    # fill up the fields in whatever way you want
    
    #groc_msg.type = groc_msg.msg["type"] = MessageType
    groc_msg.type = groc_msg.msg["type"] = 1
    # veggies
    groc_msg.tomato = groc_msg.msg["contents"]["veggies"]["tomato"] = random.uniform(1,10)
    groc_msg.cucumber = groc_msg.msg["contents"]["veggies"]["cucumber"] = random.uniform(1,10)
    groc_msg.carrot = groc_msg.msg["contents"]["veggies"]["carrot"] = random.uniform(1,10)
    groc_msg.corn = groc_msg.msg["contents"]["veggies"]["corn"] = random.uniform(1,10)
    
    # drinks (cans)
    groc_msg.coke = groc_msg.msg["contents"]["drinks"]["cans"]["coke"] = random.randint(1,10)
    groc_msg.beer = groc_msg.msg["contents"]["drinks"]["cans"]["beer"] = random.randint(1,10)
    groc_msg.rootbeer = groc_msg.msg["contents"]["drinks"]["cans"]["rootbeer"] = random.randint(1,10)

    # drinks (bottles)
    groc_msg.sprite = groc_msg.msg["contents"]["drinks"]["bottles"]["sprite"] = random.randint(1,10)
    groc_msg.gingerale = groc_msg.msg["contents"]["drinks"]["bottles"]["gingerale"] = random.randint(1,10)
    groc_msg.lemonade = groc_msg.msg["contents"]["drinks"]["bottles"]["lemonade"] = random.randint(1,10)

    # milk
    groc_msg.milk = groc_msg.msg["contents"]["milk"] = [(random.randint(0,6), random.uniform(1,10)) for j in range(3)]

    # bread
    groc_msg.bread = groc_msg.msg["contents"]["bread"] = [(random.randint(0,4), random.uniform(1,10)) for j in range(3)]
    
    # meat
    groc_msg.meat = groc_msg.msg["contents"]["meat"] = [(random.randint(0,4), random.uniform(1,10)) for j in range(3)]

    return groc_msg
  
  ########################################
  #  A generator of the health status message
  ########################################
  def gen_health_status_msg (self):
    '''Status message generator '''
    
    status_msg = HealthStatusMessage ()
    # fill up the fields in whatever way you want
     
    status_msg.type = status_msg.msg["type"] = 2
    status_msg.dispenser = status_msg.msg["contents"]["dispenser"] = random.randint(0,2)
    status_msg.icemaker = status_msg.msg["contents"]["icemaker"] = random.randint(1,100)
    status_msg.lightbulb = status_msg.msg["contents"]["lightbulb"] = random.randint(0,1)
    status_msg.fridge_temp = status_msg.msg["contents"]["fridge_temp"] = random.randint(0,100)
    status_msg.freezer_temp = status_msg.msg["contents"]["freezer_temp"] = random.randint(-50,100)
    status_msg.sensor_status = status_msg.msg["contents"]["sensor_status"] = random.randint(0,1)
    status_msg.capacity_full = status_msg.msg["contents"]["capacity_full"] = random.randint(1,100)
    
    return status_msg
  
  ##################################
  # Driver program
  ##################################
  time_list = []
  def driver (self, args):
    try:

      # To ensure that bad requests are handled correctly, initially let us first
      # try sending wrong message to wrong server.

      # Test 1:
      # create a grocery order
      config = configparser.ConfigParser ()
      config.read (args.config)
      
      intfs = ni.interfaces()
      #intf, ni.ifaddresses (intf)[ni.AF_INET][0]['addr']
      
      for intf in intfs:
          print("IP addresses associated with interface {} are {}".format (intf, ni.ifaddresses (intf)))
      host_ip = ni.ifaddresses(intfs[1])[ni.AF_INET][0]['addr']
      print(type(host_ip))
      print(host_ip)
      hostname = "H" + host_ip.split(".")[-1]
      print (f"this is hostname: {hostname}")
      host_ip = "10.0.0." + str(hostname.split("H",1)[-1])
      print(f"this is host_ip: {host_ip}")
      
      
      flag_split = 1
      
      #print("IPv4 address associated with interface {} are {}".format (intfs[1], dictionary[ni.AF_INET][0]['addr']))
    
      
      if (config["Network"]["Route"] == "route1"):
          groc_server_ip = "10.0.0.5"
          health_server_ip = "10.0.0.6"
      elif (config["Network"]["Route"] == "route2"):
          groc_server_ip = "10.0.0.1"
          health_server_ip = "10.0.0.27"
          
      msg = self.gen_grocery_order_msg ()

      print ("Sending grocery msg to health server {}".format (msg))
      start_time = time.time()

      # send it to health server and see if we get a bad request reply
      self.health_obj.send_grocery_order (flag_split, msg, health_server_ip, dest_port)
      
      # now receive a response
      reply = self.health_obj.recv_response ()
      end_time = time.time()
      latency_time = end_time - start_time
      time_list.append(latency_time)
      print("latency time {}".format(latency_time))
      print ("Received reply {}".format (reply))
      flag_split = 1
      # Test 2:
      # create a health status
      msg = self.gen_health_status_msg ()
      print ("Sending health msg to grocery server {}".format (msg))
      start_time = time.time()
      # send it to grocery server and see if we get a bad request reply
      self.groc_obj.send_health_status (flag_split, msg, groc_server_ip, dest_port)
      # now receive a response

      reply = self.groc_obj.recv_response ()
      end_time = time.time()
      latency_time = end_time - start_time
      time_list.append(latency_time)
      print("latency time {}".format(latency_time))

      print ("Received reply {}".format (reply))
      
      
      # Test 3: 
      # Here in each iteration and depending on the ratio, we decide whether to
      # send Grocery Message or Health Status Message. These are sent correctly. 
      #
      # @TODO - 
      # Sending messages as per the ratio is not such a big deal for this assignment.
      # Just alternating between the two is fine. What we really care is that both
      # kinds of message types can be sent, and that if they received by the right
      # server, we get a success response. Time the result.
      for i in range(2):
      #for i in range (self.iters):
        if (i % 2) == 0:
          # create a grocery order
          msg = self.gen_grocery_order_msg ()
          print ("Sending grocery msg to grocery server {}".format (msg))
          start_time = time.time()
          # send it to health server and see if we get a bad request reply
          self.groc_obj.send_grocery_order (flag_split, msg, groc_server_ip, dest_port)
          # now receive a response
          print ("Waiting for response")
          response = self.groc_obj.recv_response ()
          end_time = time.time()
          latency_time = end_time - start_time
          time_list.append(latency_time)
          print ("latency time {}".format(latency_time))
          print ("Received reply {}".format (response))
        else:
          # create a health status
          msg = self.gen_health_status_msg ()
          print ("Sending health msg to health server {}".format (msg))
          start_time = time.time()
          # send it to grocery server and see if we get a bad request reply
          self.health_obj.send_health_status (flag_split, msg, health_server_ip, dest_port)
          # now receive a response
          print ("Waiting for response")
          response = self.health_obj.recv_response ()
          end_time = time.time()
          latency_time = end_time - start_time
          time_list.append(latency_time)
          print ("latency time {}".format(latency_time))
          print ("Received reply {}".format (response))
        #print(time_list)
        # some delay between requests
        time.sleep (1)
      
    except Exception as e:
      raise e

##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ("Argument parser for the refrigerator client")

  # add optional arguments
  parser.add_argument ("-c", "--config", default="config.ini", help="configuration file (default: config.ini")
  parser.add_argument ("-i", "--iters", type=int, default=10, help="Number of iterations (default: 10")
  parser.add_argument ("-g", "--groc_ip", default="127.0.0.1", help="IP Address of Grocery server to connect to (default: localhost i.e., 127.0.0.1)")
  parser.add_argument ("-p", "--groc_port", type=int, default=5555, help="Port that grocery server is listening on (default: 5555)")
  parser.add_argument ("-s", "--status_ip", default="127.0.0.1", help="IP Address of Health Status server to connect to (default: localhost i.e., 127.0.0.1)")
  parser.add_argument ("-q", "--status_port", type=int, default=7777, help="Port that Healt Status server is listening on (default: 7777)")
  parser.add_argument ("-r", "--req_ratio", default="1:1", help="Ratio of grocery orders sent to health status (default: 1:1 implying equal number)")
  
  
  parser.add_argument ("-a", "--addr", default="127.0.0.1", help="IP Address of next hop router to connect to (default: localhost i.e., 127.0.0.1)")
  parser.add_argument ("-n", "--port", type=int, default=4444, help="Port that next hop router is listening on (default: 4444)")
  #parser.add_argument ("-i", "--iters", type=int, default=1000, help="Number of iterations (default: 1000")
  parser.add_argument ("-m", "--message", default="HelloWorld", help="Message to send: default HelloWorld")
  parser.add_argument ("-t", "--demux_token", default="client", help="Our identity used as a demultiplexing token (default: client)")
  #parser.add_argument ("-fp", "--finalport", type=int, default=5555, help="Final destination port (default: 5555)")
  #parser.add_argument ("-fip", "--finalip", default ="*", help = "Final destination ip (default: all)")
  
  args = parser.parse_args ()

  return args
    
#------------------------------------------
# main function
def main ():
  """ Main program """

  try:
    print("Skeleton Code for the Refrigerator Client")

    # first parse the command line args
    print ("Refrigerator main: parsing command line")
    parsed_args = parseCmdLineArgs ()
    
    # Obtain a refrigerator object
    print ("Refrigerator main: obtain the object")
    fridge = Refrigerator ()

    # initialize our refrigerator object
    print ("Refrigerator main: initialize the object")
    fridge.initialize (parsed_args)

    # Now drive the rest of the assignment
    print ("Refrigerator main: invoke driver")
    fridge.driver (parsed_args)
    print(time_list)

    # we are done. collect results and do the plotting etc.
    #
    # @TODO@ Add code here.
  except Exception as e:
      print ("Exception caught in main - {}".format (e))
      exception_type, exception_object, exception_traceback = sys.exc_info()
      filename = exception_traceback.tb_frame.f_code.co_filename
      line_number = exception_traceback.tb_lineno

      print("Exception type: ", exception_type)
      print("File name: ", filename)
      print("Line number: ", line_number)
      return

#----------------------------------------------
if __name__ == '__main__':
  # here we just print the version numbers
  print("Current libzmq version is %s" % zmq.zmq_version())
  print("Current pyzmq version is %s" % zmq.pyzmq_version())

  main ()
