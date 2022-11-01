# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for our custom transport protocol
#          For assignment 1, this will be a No-Op. But we keep the layered
#          architecture in all the assignments
#

# import the needed packages
import os     # for OS functions
import sys    # for syspath and system exception
import csv

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert (0, "../")

from networklayer.CustomNetworkProtocol import CustomNetworkProtocol as NWProtoObj


FULL_PACKET_SIZE = 1024 # application request packet size of 1024 bytes
MTU = 16 # maximum transfer unit of 16 bytes


def GetPaddedSegment(segment):
    segment_size = sys.getsizeof(segment)
    added_bits = FULL_PACKET_SIZE - segment_size
    need_to_add = bytes(added_bits)
    segment = segment + need_to_add
    #segment_size = sys.getsizeof(segment)
    #print(f"segment size: {segment_size}")
    return segment

############################################
#  Bunch of Transport Layer Exceptions
#
# @TODO@ Add more, if these are not enough
############################################

############################################
#       Custom Transport Protocol class
############################################
class CustomTransportProtocol ():
  '''Custom Transport Protocol'''

  ###############################
  # constructor
  ###############################
  def __init__ (self, role):
    self.role = role  # indicates if we are client or server, false => client
    self.ip = None
    self.port = None
    self.nw_obj = None # handle to our underlying network layer object

    self.config = None
    
  ###############################
  # configure/initialize
  ###############################
  def initialize (self, config, ip, port):
    ''' Initialize the object '''

    try:
      # Here we initialize any internal variables
      print ("Custom Transport Protocol Object: Initialize")
    
      # initialize our variables
      self.ip = ip
      self.port = port
      self.config = config
      
      
      
      
      


      # in a subsequent assignment, we will use the max segment size for our
      # transport protocol. This will be passed in the config.ini file.
      # Right now we do not care.
      
      # Now obtain our network layer object
      print ("Custom Transport Protocol::initialize - obtain network object")
      self.nw_obj = NWProtoObj ()
      
      # initialize it
      # 
      # In this assignment, we let network layer (which holds all the ZMQ logic) to
      # directly talk to the remote peer. In future assignments, this will be the
      # next hop router to whom we talk to.
      print ("Custom Transport Protocol::initialize - initialize network object")
      self.nw_obj.initialize (config, self.role, self.ip, self.port)
      
    except Exception as e:
      raise e  # just propagate it
    
  ##################################
  #  send application message
  ##################################
  def send_appln_msg (self, dest_ip, dest_port, payload, size):
    try:
      # @TODO@ Implement this
      # What we should get here is a serialized message from the application
      # layer along with the payload size. Now, depending on what is the
      # maximum segment size allowed by our transport, we will need to break the
      # total message into chunks of segment size and send segment by segment.
      # But we will do all this when we are implementing our custom transport
      # protocol. For Assignment #1, we send the entire message as is in a single
      # segment
      
      print ("Custom Transport Protocol::send_appln_msg")
      segment = dest_ip + "~" + str(dest_port) + "~" + payload + "~~"
      
      if self.config["Transport"]["TransportProtocol"] == "AlternatingBit":
        window_size = 1
        print(f"window size is {window_size}")
      elif self.config["Transport"]["TransportProtocol"] == "GoBackN" or self.config["Transport"]["TransportProtocol"] == "SelectiveRepeat":
        window_size = 8
        print(f"window size is {window_size}")

      segment = bytes(segment,"utf-8")
      segment = GetPaddedSegment(segment)
      
      seq_num = 0
      sum = 0
      for i in range(0, sys.getsizeof(segment), MTU):
          chunk = segment[i:i+MTU-1]
          sum = sum + 1
          print(f"sequence number is {seq_num}")
          print(f"amount of bytes so far is {sum*16}")
          #self.send_segment(seq_num, segment, size)
          seq_num = int(not(seq_num))
          
          #self.send_segment(chunk, size)
          #print(f"chunk is {chunk} with size {sys.getsizeof(chunk)}")
      #chunks = [segment[i:i+2] for i in range(0, sys.getsizeof(segment), MTU)]
      #print(chunks)
      
      
      print(f"The size of my packet in transport layer is: {sys.getsizeof(segment)} and the packet is {segment} and the length is {len(segment)}")
      
      self.send_segment(segment, size)

    except Exception as e:
      raise e

  ##################################
  #  send transport layer segment
  ##################################
  def send_segment (self, segment, len=0):
    try:
      # For this assignment, we ask our dummy network layer to
      # send it to peer. We ignore the length in this assignment
      print ("Custom Transport Protocol::send_segment")
      
      if self.config["Transport"]["TransportProtocol"] == "AlternatingBit":
          print("do alternating bit")

      self.nw_obj.send_packet (segment, len)
      
    except Exception as e:
      raise e

  ######################################
  #  receive application-level message
  ######################################
  def recv_appln_msg (self, len=0):
    try:
      # The transport protocol (at least TCP) is byte stream, which means it does not
      # know the boundaries of the message. So it must be told how much to receive
      # to make up a meaningful message. In reality, a transport layer will receive
      # all the segments that make up a meaningful message, assemble it in the correct
      # order and only then pass it up to the caller.
      #
      # For this assignment, we do not care about all these things.
      print ("Custom Transport Protocol::recv_appln_msg")
      appln_msg = self.recv_segment ()
      return appln_msg
    
    except Exception as e:
      raise e

  ######################################
  #  receive transport segment
  ######################################
  def recv_segment (self, len=0):
    try:
      # receive a segment. In future assignments, we may be asking for
      # a pipeline of segments.
      #
      # For this assignment, we do not care about all these things.
      print ("Custom Transport Protocol::recv_segment")
      segment = self.nw_obj.recv_packet (len)
      return segment
    
    except Exception as e:
      raise e

