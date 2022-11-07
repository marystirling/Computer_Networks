# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for the Smart Refrigerator server
#          needed for the Computer Networks course Assignments. This one handles
#          grocery order requests
#
#          Since we are hoping to develop a very crude networking stack
#          in this course, we will see that our server uses an Application
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
import json
# add to the python system path so that the following packages can be found
# relative to this directory
sys.path.insert (0, os.getcwd ())

# this is our application level protocol and its message types
from applnlayer.CustomApplnProtocol import CustomApplnProtocol as ApplnProtoObj
from applnlayer.ApplnMessageTypes import GroceryOrderMessage
from applnlayer.ApplnMessageTypes import HealthStatusMessage
from applnlayer.ApplnMessageTypes import ResponseMessage

import serialize_flatbuf as sz_fb
import serialize_json as sz_json

##################################
#   Health Status Server class
##################################
class GroceryOrder ():
  '''GroceryOrder Server'''
  
  ########################################
  # constructor
  ########################################
  def __init__ (self):
    self.grocery_obj = None

  ########################################
  # configure/initialize
  ########################################
  def initialize (self, args):
    ''' Initialize the object '''

    try:
      # Here we initialize any internal variables
      print ("GroceryOrder Object: Initialize")
    
      # Now, get the configuration object
      config = configparser.ConfigParser ()
      config.read (args.config)
    
      # Next, obtain the custom application protocol object
      self.grocery_obj = ApplnProtoObj (True)  # the True flag indicates this is a server side


      # initialize the custom application objects
      self.grocery_obj.initialize (config, args.addr, args.port)
      
      self.ser_type = config["Application"]["Serialization"]

    except Exception as e:
      raise e

  ########################################
  #  A generator of the response message
  ########################################
  def gen_response_msg (self):
    '''Response message generator '''

    resp_msg = ResponseMessage ()

    return resp_msg
  
  ##################################
  # Driver program
  ##################################
  def driver (self):
    try:
      # The health status server will run forever
      while True:
        
        #request = self.health_obj.recv_request ()
        #print ("Received request: {}".format (request))

        print("did we make it in the groc server")
        chunk_sum = 0
        request = ''
        #while True:
        for i in range(64):
          print("are we trying to receive")
          chunk = self.grocery_obj.recv_request ()
          #chunk = chunk.decode("UTF-8")
          #seq_num = chunk.split("~")[-1]
         
          chunk = chunk.decode("UTF-8")
          chunk = chunk.split('!!!')
          seq_num = chunk[0]
          msg = chunk[-1]
          print(f"sending ack {seq_num}")
          self.grocery_obj.send_ack (seq_num)
          
          chunk_sum += 1
         
         
          request = request + msg
          if chunk_sum == 64:
            print("received all chunks")
            break
        
        print(f"full request: {request}")




        request = request.split("###")[0]
        
        flag_split, dest_ip, dest_port, payload = request.split("~")

        print ("Received request: {}".format (request))
        #request = bytes(request, "utf-8")
        resp = self.gen_response_msg()
        #request = payload
        resp.type = resp.msg["type"] = 3

        if (self.ser_type == "json"):
            print ("deserialize the message")
            msg_d = sz_json.deserialize (payload)
            #msg_d.__str__()
            flag_split = 0
            if (msg_d.type == 1):
                resp.code = resp.msg["code"] = 0
                resp.contents = resp.msg["contents"] = "Order Placed"
            else:
                resp.code = resp.msg["code"] = 1
                resp.contents = resp.msg["contents"] = "Bad Request"
        elif (self.ser_type == "fbufs"):
            print ("deserialize the message")
            msg_d = sz_fb.deserialize (request)
            msg_d.__str__()
            if (msg_d.type == 1):
                resp.code = resp.msg["code"] = 0
                resp.contents = resp.msg["contents"] = "Order Placed"
            else:
                resp.code = resp.msg["code"] = 1
                resp.contents = resp.msg["contents"] = "Bad Request"
        
        self.grocery_obj.send_response (flag_split, dest_ip, dest_port, resp)
        
    except Exception as e:
      raise e

##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ("Argument parser for the health status server")

  # add optional arguments
  parser.add_argument ("-c", "--config", default="config.ini", help="configuration file (default: config.ini")
  parser.add_argument ("-a", "--addr", default="*", help="Interface we are accepting connections on (default: all)")
  parser.add_argument ("-p", "--port", type=int, default=5555, help="Port the health status server is listening on (default: 5555)")
 #parser.add_argument ("-fp", "--finalport", type=int, default=5555, help="Final destination port (default: 5555)")
  #parser.add_argument ("-fip", "--finalip", default ="*", help = "Final destination ip (default: all)")
  
  args = parser.parse_args ()

  return args
    
#------------------------------------------
# main function
def main ():
  """ Main program """

  try:
    print("Skeleton Code for the GroceryOrder Server")

    # first parse the command line args
    print ("GroceryOrder main: parsing command line")
    parsed_args = parseCmdLineArgs ()
    
    # Obtain a health status server object
    print ("GroceryOrder main: obtain the object")
    hs = GroceryOrder ()

    # initialize our refrigerator object
    print ("GroceryOrder main: initialize the object")
    hs.initialize (parsed_args)

    # Now drive the rest of the assignment
    print ("GroceryOrder main: invoke driver")
    hs.driver ()

    # we are done. collect results and do the plotting etc.
    #
    # @TODO@ Add code here.
  except Exception as e:
    print ("Exception caught in main - {}".format (e))
    return

#----------------------------------------------
if __name__ == '__main__':
  # here we just print the version numbers
  print("Current libzmq version is %s" % zmq.zmq_version())
  print("Current pyzmq version is %s" % zmq.pyzmq_version())

  main ()