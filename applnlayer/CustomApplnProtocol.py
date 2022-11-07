# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for our custom application protocol
#          used by our smart refrigerator to send grocery order and health status
#          messages. This is our Application Layer used in the Computer Networks
#          course Assignments
#

# import the needed packages
import os     # for OS functions
import sys    # for syspath and system exception
import time   # for sleep
from enum import Enum  # for enumerated types
import csv

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert (0, "../")

from transportlayer.CustomTransportProtocol import CustomTransportProtocol as XPortProtoObj
import serialize_flatbuf as sz_fb
import serialize_json as sz_json


############################################
#  Serialization Enumeration Type
############################################
class SerializationType (Enum):
  # One can extend this as needed. For now only these two
  UNKNOWN = -1
  JSON = 1
  FBUFS = 2
  
class RoutePath (Enum):
  UNKNOWN = -1
  R1 = 1
  R2 = 2


refrigerator_ip = ''
############################################
#  Bunch of Application Layer Exceptions
#
# @TODO@ Add more, if these are not enough
############################################
class BadSerializationType (Exception):
  '''Bad Serialization Type'''
  def __init__ (self, arg):
    msg = arg + " is not a known serialization type"
    super ().__init__ (msg)

class BadMessageType (Exception):
  '''Bad Message Type'''
  def __init__ (self):
    msg = "bad or unknown message type"
    super ().__init__ (msg)

############################################
#       Custom Application Protocol class
############################################
class CustomApplnProtocol ():
  '''Custom Application Protocol for the Smart Refrigerator'''

  ###############################
  # constructor
  ###############################
  def __init__ (self, role):
    self.role = role  # indicates if we are client or server, false => client
    self.ser_type = SerializationType.UNKNOWN
    self.route = RoutePath.UNKNOWN
    self.xport_obj = None # handle to our underlying transport layer object
    
  ###############################
  # configure/initialize
  ###############################
  def initialize (self, config, ip, port):
    ''' Initialize the object '''

    try:
      # Here we initialize any internal variables
      #print ("Custom Application Protocol Object: Initialize")
      print ("serialization type = {}".format (config["Application"]["Serialization"]))
    
      # initialize our variables
      if (config["Application"]["Serialization"] == "json"):
        self.ser_type = SerializationType.JSON
      elif (config["Application"]["Serialization"] == "fbufs"):
        self.ser_type = SerializationType.FBUFS
      else:  # Unknown; raise exception
        raise BadSerializationType (config["Application"]["Serialization"])
    
      
      if (config["Network"]["Route"] == "route1"):
          with open("route1.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                if(row[0]== 'H1' and row[1] == '10.0.0.6'):
                    pass
                else:
                    pass

      # Now obtain our transport object
      # @TODO
      print ("Custom Appln Protocol::initialize - obtain transport object")
      self.xport_obj = XPortProtoObj (self.role)

      # initialize it
      print ("Custom Appln Protocol::initialize - initialize transport object")
      self.xport_obj.initialize (config, ip, port)
      
    except Exception as e:
      raise e  # just propagate it
    
  ##################################
  #  send Grocery Order
  ##################################
  def send_grocery_order (self, flag_split, order, dest_ip, dest_port):
    try:

      if order.msg["type"] == 1:
          if self.ser_type == SerializationType.JSON:
              print ("serialize the message")

              buf = sz_json.serialize (order)
              
              order.__str__()
              
              
          elif self.ser_type == SerializationType.FBUFS:
              print ("serialize the message")

              buf = sz_fb.serialize (order)

              order.__str__()
      else:
          raise BadMessageType
      

      print ("CustomApplnProtocol::send_grocery_order")
      self.xport_obj.send_appln_msg (flag_split, dest_ip, dest_port, buf, len (buf))
    except Exception as e:
      raise e

  ##################################
  #  send Health Status
  ##################################
  def send_health_status (self, flag_split, status, dest_ip, dest_port):
    try:
      
      if status.msg["type"] == 2:
          print(self.ser_type)
          if self.ser_type == SerializationType.JSON:
              print ("serialize the message")

              buf = sz_json.serialize (status)

              status.__str__()
              
          elif self.ser_type == SerializationType.FBUFS:
              print ("serialize the message")

              buf = sz_fb.serialize (status)

              status.__str__()
              
      else:
          raise BadMessageType
        
        
      print ("CustomApplnProtocol::send_health_status")
      self.xport_obj.send_appln_msg (flag_split, dest_ip, dest_port, buf, len (buf))
    except Exception as e:
      raise e

  ##################################
  #  send response
  ##################################
  def send_response (self, flag_split, dest_ip, dest_port, response):
    try:
      # @TODO@ Implement this
      # Essentially, you will need to take the Health Status supplied in native host
      # format and invoke the serialization method (either json or flatbuf)

      # You must first check that the message type is response else raise the
      # BadMessageType exception
      #
      # Note, here we are sending some dummy field just for testing purposes
      # but remove it with the correct payload and length.
      
      if response.msg["type"] == 3:
          if self.ser_type == SerializationType.JSON:
              print ("serialize the message")

              buf = sz_json.serialize (response)

              response.__str__()
              
          elif self.ser_type == SerializationType.FBUFS:
              print ("serialize the message")

              buf = sz_fb.serialize (response)

             
              response.__str__()
              
      else:
          raise BadMessageType
      
      
      print ("CustomApplnProtocol::send_response")
      self.xport_obj.send_appln_msg (flag_split, dest_ip, dest_port, buf, len (buf))
    except Exception as e:
      raise e

  ##################################
  #  receive request
  ##################################
  def recv_request (self):
    try:
      # @TODO@ Implement this
      # receive the message and return it to caller
      #
      # To that end, we ask our transport object to retrieve
      # application level message
      #
      # Note, that in this assignment, we are not worrying about sending
      # transport segments etc and so what we receive from ZMQ is the complete
      # message.
      print ("CustomApplnProtocol::recv_appln_msg")

      request = self.xport_obj.recv_appln_msg ()
      print(request)

      return request
    except Exception as e:
      raise e

  ##################################
  #  receive response
  ##################################
  def recv_response (self):
    try:
      # @TODO@ Implement this
      # receive the message and return it to caller
      #
      # To that end, we ask our transport object to retrieve
      # application level message
      #
      # Note, that in this assignment, we are not worrying about sending
      # transport segments etc and so what we receive from ZMQ is the complete
      # message.
      

      print ("CustomApplnProtocol::recv_response")
      response = self.xport_obj.recv_appln_msg ()

      
      response = response.decode("Utf-8")
      response = response.split("!!!")
      response = response[-1]
      print(f"response now is: {response}")

      response = response.split("###")[0]
        
      flag_split, dest_ip, dest_port, payload = response.split("~")

      #flag_split, dest_ip, dest_port, payload = response.split("~")

      
      if self.ser_type == SerializationType.JSON:
              print ("deserialize the message")

              response_msg = sz_json.deserialize (payload)
 
              response.__str__()
              
      elif self.ser_type == SerializationType.FBUFS:
              
              print ("deserialize the message")
              response_msg = sz_fb.deserialize(response)
              
              response.__str__()
             


      return response_msg
    except Exception as e:
      raise e

