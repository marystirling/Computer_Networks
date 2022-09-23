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

    except Exception as e:
      raise e

  ########################################
  #  A generator of the response message
  ########################################
  def gen_response_msg (self):
    '''Response message generator '''

    # @TODO@ Add code here.
    #
    # Basically, a response msg is very simple. Set the message type and message
    
    resp_msg = ResponseMessage ()
    
    

    # fill up the fields in whatever way you want
    #resp_msg.type = resp_msg.msg["type"] = 3

    return resp_msg
  
  ##################################
  # Driver program
  ##################################
  def driver (self):
    try:
      # The health status server will run forever
      while True:
        # receive a request. If we do not understand it, send a BadRequest response
        # else send a valid response
        # @TODO
        # For now we send a dummy response

        request = self.health_obj.recv_request ()
        print ("Received request: {}".format (request))
        
        #if (sz_json.get_message_type(request) == 2):
        #    print("worked")
        #else:
        #    print("did not work")
        
        
        resp = self.gen_response_msg()
        
        resp.type = resp.msg["type"] = 3
        #resp.code = resp.msg["code"] = 1
    
        if(sz_json.get_message_type(request) == 2):
            sz_json.deserialize_h(request)
            resp.code = resp.msg["code"] = 0
            resp.contents = resp.msg["contents"] = "You are Healthy"
        else:
            resp.code = resp.msg["code"] = 1
            resp.contents = resp.msg["contents"] = "Bad Request"
    

        #resp.type = resp.msg["type"] = 2
        #resp.code = resp.msg["code"] = 1
        #resp.contents = resp.msg["contents"] = "Bad Request"
    
        #print(sz_json.MESSAGE_TYPE)
        #resp = self.gen_response_
        #correct_type = sz_json.message_type()
        #print(correct_type)

        #print(sz_json.message_type(request))
        #if correct_type == 1:
        #    resp.code = resp.msg["code"] = 0
        #    resp.contents = resp.msg["contents"] = "You are Healthy"
            #resp =  sz_json.deserialize_h(request)
        #else:
        #    print("bad request!!!!")
        #    resp.code = resp.msg["code"] = 1
        #    resp.contents = resp.msg["contents"] = "Bad Request"
        #if sz_json.MESSAGE_TYPE == "GROCERY":
          #  print("worked")
        #if sz_json.MESSAGE_TYPE == "HEALTH":
        #    print("did i come in here")
        #    resp_ds = sz_json.deserialize_h(request)
        #else:

        
        self.health_obj.send_response (resp)
        
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
