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
import time
import time
import concurrent.futures
#from threading import Event
import random

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
  

  def prob_drop ():
    return random.randint(1, 100)
  


  def sock_recv(socket):
    response = None
    prob_drop = 0
    try:
      #if prob_drop():
      if prob_drop():
        time.sleep(10)

      response = socket.recv()
    except Exception as e:
      print(e)
    finally:
      return response


  def c_alternating_bit(self, socket):
    print("sending with alternating bit protocol")
    flag = True
    sock_recv = 0
    for i in range(self.iters):
      try:
        message = f"m={i}f={1 if flag else 0}"
        socket.send(bytes(message), "utf-8")
      except Exception as e:
        print("error when sending message in c_alternating_bit")
      try:
        with concurrent.futures.ThreadPoolExecutor (max_workers=1) as executor:
          future = executor.submit(sock_recv, socket)
          print("future: {future}")
          response = future.result(timeout=self.timeout)
          print(f"response: {response}")
          ack = True if response == b'1' else False
          if flag == ack:
            print("response ack our message")
            flag = not flag
      except Exception as e:
        print("mesage timed out")
    return None

  def s_alternating_bit(socket):
    print("using alternating bit protocol")
    last = False
    while True:
      try:
        message = str(socket.recv(), "utf-8")
        print(f"received: {message}")
      except Exception as e:
        print(e)
        socket.close()
      try:
        def is_good(m):
          return (int(m[-1] == 0) or (int(m[-1] == 1)))
        if is_good(message):
          message_flag = True if int(message[-1]) == 1 else False
          if message_flag != last:
            resp = bytes(str(1 if not last else 0), "utf-8")
            print(f"sending good ack: {resp}")
          else:
            resp = bytes(str(1 if last else 0), "utf-8")
            print(f"sending bad ack: {resp}")
        else:
          print("message was bad")
          resp = bytes(str(1 if last else 0), "utf-8")
        print(f"responding: {resp}")
        socket.send(resp)
      except Exception as e:
        print(e)
        socket.close()
        return




  ##################################
  #  send application message
  ##################################
  def send_appln_msg (self, dest_ip, dest_port, payload, size):

    protocol = self.config["Transport"]["TransportProtocol"]
      
    print(f"Role is: {self.role}")
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
      
      segment = bytes(segment,"utf-8")
      segment = GetPaddedSegment(segment)

      print(f"Segment in transport layer {sys.getsizeof(segment)}")


      
      
      if protocol == "AlternatingBit":
        window_size = 1
        seq_num = 0
        
        for i in range(0, sys.getsizeof(segment), MTU):
          chunk = segment[i:i+MTU-1]
          #choice = random.randint(1,3)
          choice = 1
          print(f"chunk is {chunk}")
          print(f"chunks size is {sys.getsizeof(chunk)}")
          seq_num = int(not(seq_num))

          #self.send_segment(choice, seq_num, chunk, size)
          
          # sending one segment at a time
          #self.send_segment(choice, seq_num, chunk, size)
          # wait until timeout or receives an ack
          # if timeout then resend chunk
          # else if ack has been received then move onto next chunk
   
      elif protocol == "GoBackN":
        window_size = 8
        seq_num = 0
        sum = 0
        buffer = []
        for i in range(0, sys.getsizeof(segment), MTU):
          chunk = segment[i:i+MTU-1]
          choice = random.randint(1,3)
          choice = 1
          if seq_num < window_size:
            #self.send_segment(choice, seq_num, chunk, size)
            buffer.append(chunk)
          
          # have a way to tell which seq_num have an ack
          # resend those with timeout 
          # once all have an ack then move window size to next 8 chunks

       
      elif protocol == "SelectiveRepeat":
        window_size = 8
    
      #self.send_segment(choice, seq_num, segment, size)


      
  
      choice = 1
      print(f"The size of my packet in transport layer is: {sys.getsizeof(segment)}")
      print(f" final choice is: {choice}")
      #print(segment)
      self.send_segment(choice, seq_num, segment, size)

    except Exception as e:
      raise e

  ##################################
  #  send transport layer segment
  ##################################
  def send_segment (self, choice, seq_num, chunk, len=0):
    print("here")
    protocol = self.config["Transport"]["TransportProtocol"]
    #print(chunk)
    try:
      # For this assignment, we ask our dummy network layer to
      # send it to peer. We ignore the length in this assignment
      print ("Custom Transport Protocol::send_segment")
      
      if protocol == "AlternatingBit":
          print("do alternating bit")
          if choice == 1:
              print("Send the chunk to the next hop")
              #print(f"what i am sending to network layer is {sys.getsizeof(chunk)}")
              #print(chunk)
              self.nw_obj.send_packet (seq_num, chunk, len)
          elif choice == 2:
              print("Delay sending chunk to the next hop")
              time.sleep(random.randint(1,10)) # delay for random integer from 1 to 10 
              self.nw_obj.send_packet (seq_num, chunk, len)
          elif choice == 3:
              print("Drop chunk")

      #self.nw_obj.send_packet (segment, len)
      
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
      #print(f"now we have {appln_msg}")
      full_msg = []
      #appln_msg = []
      buffer = []
      if self.config["Transport"]["TransportProtocol"] == "AlternatingBit":
          print("alternating bit protocol")
          
          
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


  ######################################
  #  send transport layer ack
  ######################################
  def send_transport_ack (self, seq_num, len):
    try:
      # receive a segment. In future assignments, we may be asking for
      # a pipeline of segments.
      #
      # For this assignment, we do not care about all these things.
      print ("Custom Transport Protocol::send_transport_ack")
      self.nw_obj.send_nw_ack (seq_num, len)
      #return segment
    
    except Exception as e:
      raise e
    

  ######################################
  #  receive transport layer ack
  ######################################
  def recv_transport_ack (self, seq_num, len):
    try:
      # receive a segment. In future assignments, we may be asking for
      # a pipeline of segments.
      #
      # For this assignment, we do not care about all these things.
      print ("Custom Transport Protocol::recv_transport_ack")
      self.nw_obj.send_nw_ack (seq_num, len)
      #return segment
    
    except Exception as e:
      raise e
    

