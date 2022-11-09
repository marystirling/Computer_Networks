# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for the Smart Refrigerator server
#          needed for the Computer Networks course Assignments. This one handles
#          health status messages
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
import json
# add to the python system path so that the following packages can be found
# relative to this directory
sys.path.insert (0, os.getcwd ())

# this is our application level protocol and its message types
from applnlayer.CustomApplnProtocol import CustomApplnProtocol as ApplnProtoObj
from applnlayer.ApplnMessageTypes import GroceryOrderMessage
from applnlayer.ApplnMessageTypes import HealthStatusMessage
from applnlayer.ApplnMessageTypes import ResponseMessage

from enum import Enum


import serialize_flatbuf as sz_fb
import serialize_json as sz_json
#from serialize_json import *


class SerializationType (Enum):
  # One can extend this as needed. For now only these two
  UNKNOWN = -1
  JSON = 1
  FBUFS = 2

##################################
#   Health Status Server class
##################################
class HealthStatus ():

  ########################################
  # constructor
  ########################################
  def __init__ (self):
    self.health_obj = None

  ########################################
  # configure/initialize
  ########################################
  def initialize (self, args):
    ''' Initialize the object '''

    try:
      # Here we initialize any internal variables
      print ("HealthStatus Object: Initialize")
    
      # Now, get the configuration object
      config = configparser.ConfigParser ()
      config.read (args.config)
    
      # Next, obtain the custom application protocol object
      self.health_obj = ApplnProtoObj (True)  # the True flag indicates this is a server side

      # initialize the custom application objects
      self.health_obj.initialize (config, args.addr, args.port)
      
      self.ser_type = config["Application"]["Serialization"]
      self.protocol = config["Transport"]["TransportProtocol"]

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
    print("in health_server driver")
    try:
      # The health status server will run forever
      while True:
        
        #request = self.health_obj.recv_request ()
        #print ("Received request: {}".format (request))


        chunk_sum = 0
        request = ''
        last = -1
        #i = 0
        #last = 0
        while True:
        #for i in range(64):
          chunk = self.health_obj.recv_request ()
          #chunk = chunk.decode("UTF-8")
          #seq_num = chunk.split("~")[-1]
         
          chunk = chunk.decode("UTF-8")
          chunk = chunk.split('!!!')
          seq_num = chunk[0]
          msg = chunk[-1]
          print(f"chunk sum is {chunk_sum}")
          #start_i = i
          
          print(f"sending ack {seq_num}")
          if self.protocol == "AlternatingBit":
            if seq_num != last:
              self.health_obj.send_ack (seq_num)
              print("got correct ack")
              request = request + msg
              chunk_sum += 1
              last = seq_num
              #i = i + 1
            else:
              self.health_obj.send_ack(last)
              print("got wrong ack")
            #request = request + msg
          
          elif self.protocol == "GoBackN":
            seq_num = int(seq_num)
            print(f"received packet with seq_num  {seq_num}")
            #print(f" i iteration right now is {i}")
            #time.sleep(4)
            #if seq_num == 1:
              #  print("do we go in here")
              #seq_num = 0
              #time.sleep(5)
            if seq_num == last + 1:
              
              self.health_obj.send_ack(seq_num)
              print("got correct ack")
              request = request + msg
              chunk_sum = chunk_sum + 1
              last = seq_num
              print(f"last here is {last}")
              if last != 7:
                print(f"do we ever go in here")
                last = seq_num
              elif last == 7:
                print(f"we reached the end so the new last is: {last}")
                last = -1
            else:
              self.health_obj.send_ack(last)
              #i = start_i - 1
              #print(f"start_i is {start_i} and new i is {i}")
              #time.sleep(5)
              print("got wrong ack")
              print(f"chunk_sum = {chunk_sum}")

          elif self.protocol == "SelectiveRepeat":
            self.health_obj.send_ack(seq_num)
            request = request + msg
            chunk_sum += 1

          
          if chunk_sum == 64:
            print("received all chunks")
            break
        
        print(f"appended {request}")



        request = request.split("###")[0]
        
        flag_split, dest_ip, dest_port, payload = request.split("~")

        print ("Received request: {}".format (request))
        #request = bytes(request, "utf-8")
        resp = self.gen_response_msg()
        #request = payload
        resp.type = resp.msg["type"] = 3
        
        if (self.ser_type == "json"):
            print ("deserialize the message")
            flag_split = 0
            print(payload)
            msg_d = sz_json.deserialize (payload)
            
            #msg_d.__str__()
            if (msg_d.type == 2):
                resp.code = resp.msg["code"] = 0
                resp.contents = resp.msg["contents"] = "You are Healthy"
            else:
                resp.code = resp.msg["code"] = 1
                resp.contents = resp.msg["contents"] = "Bad Request"
        elif (self.ser_type == "fbufs"):
            print ("deserialize the message")
            msg_d = sz_fb.deserialize (request)
            msg_d.__str__()
            if (msg_d.type == 2):
                resp.code = resp.msg["code"] = 0
                resp.contents = resp.msg["contents"] = "You are Healthy"
            else:
                resp.code = resp.msg["code"] = 1
                resp.contents = resp.msg["contents"] = "Bad Request"

        
        self.health_obj.send_response (flag_split, dest_ip, dest_port, resp)
        
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
  parser.add_argument ("-p", "--port", type=int, default=7777, help="Port the health status server is listening on (default: 7777)")
 
  
  args = parser.parse_args ()

  return args
    
#------------------------------------------
# main function
def main ():
  """ Main program """

  try:
    print("Skeleton Code for the HealthStatus Server")

    # first parse the command line args
    print ("HealthStatus main: parsing command line")
    parsed_args = parseCmdLineArgs ()
    
    # Obtain a health status server object
    print ("HealthStatus main: obtain the object")
    hs = HealthStatus ()

    # initialize our refrigerator object
    print ("HealthStatus main: initialize the object")
    hs.initialize (parsed_args)

    # Now drive the rest of the assignment
    print ("HealthStatus main: invoke driver")
    hs.driver ()


  except Exception as e:
    print ("Exception caught in main - {}".format (e))
    return

#----------------------------------------------
if __name__ == '__main__':
  # here we just print the version numbers
  print("Current libzmq version is %s" % zmq.zmq_version())
  print("Current pyzmq version is %s" % zmq.pyzmq_version())

  main ()