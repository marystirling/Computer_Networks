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
from operator import itemgetter
import os     # for OS functions
import sys    # for syspath and system exception
import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import concurrent.futures
from threading import Event
import heapq
import itertools

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert (0, "../")

from networklayer.CustomNetworkProtocol import CustomNetworkProtocol as NWProtoObj


FULL_PACKET_SIZE = 1024 # application request packet size of 1024 bytes
MTU = 16 # maximum transfer unit of 16 bytes
#ack_list = []

def timer(self, choice, socket):
    response = None
    try:
      if choice == 3:
        time.sleep(0.2)
      else:
        response = 1
        response = socket.recv_packet()
        #response = socket.recv_packet_ack()
    except Exception as e:
      print(e)
    finally:
      return response

def GetPaddedSegment(segment):
    segment_size = sys.getsizeof(segment)
    added_bits = FULL_PACKET_SIZE - segment_size
    need_to_add = bytes(added_bits)
    segment = segment + need_to_add
 
    return segment

def getChunks(segment, MTU):
  chunked_list = []
  for i in range(0, sys.getsizeof(segment), MTU):
    #chunk = segment[i:i+MTU]
    chunked_list.append(segment[i:i+MTU])
  return chunked_list



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
      #print ("Custom Transport Protocol Object: Initialize")
    
      # initialize our variables
      self.ip = ip
      self.port = port
      self.config = config


      # in a subsequent assignment, we will use the max segment size for our
      # transport protocol. This will be passed in the config.ini file.
      # Right now we do not care.
      
      # Now obtain our network layer object
      #print ("Custom Transport Protocol::initialize - obtain network object")
      self.nw_obj = NWProtoObj ()
      
      # initialize it
      # 
      # In this assignment, we let network layer (which holds all the ZMQ logic) to
      # directly talk to the remote peer. In future assignments, this will be the
      # next hop router to whom we talk to.
      #print ("Custom Transport Protocol::initialize - initialize network object")
      self.nw_obj.initialize (config, self.role, self.ip, self.port)
      
    except Exception as e:
      raise e  # just propagate it
  
  #################################
  # send application message RESPONSE
  ################################
  def send_appln_msg_response(self, flag_split, dest_ip, dest_port, payload, size):
    #print("Custom Transport Protocol::send_appln_msg_response")
    payload = bytes(payload, "utf-8")
    self.send_segment(1, 0, dest_ip, dest_port, payload, size)




  ##################################
  #  send application message
  ##################################
  def send_appln_msg (self, flag_split, dest_ip, dest_port, payload, size):

    protocol = self.config["Transport"]["TransportProtocol"]
      
    
    try:
      # @TODO@ Implement this
      # What we should get here is a serialized message from the application
      # layer along with the payload size. Now, depending on what is the
      # maximum segment size allowed by our transport, we will need to break the
      # total message into chunks of segment size and send segment by segment.
      # But we will do all this when we are implementing our custom transport
      # protocol. For Assignment #1, we send the entire message as is in a single
      # segment
      
      #print ("Custom Transport Protocol::send_appln_msg")
      segment = str(flag_split) + "~" + dest_ip + "~" + str(dest_port) + "~" + payload + "###"
      
      segment = bytes(segment,"utf-8")
      segment = GetPaddedSegment(segment)

      
      if (flag_split):
        if protocol == "AlternatingBit":
          window_size = 1
          seq_num = 0
          j = 0
          chunked_list = getChunks(segment, MTU)
          print(chunked_list)
          flag_break = False
          while True:
            if flag_break:
              break
            chunk = chunked_list[j]
            choice = random.randint(1,3)
            self.send_segment(choice, seq_num, dest_ip, dest_port, chunk, size)
            #time.sleep(1)
            print(f"sending {chunk} with seq num {seq_num}")
            try:
              with ThreadPoolExecutor(max_workers = window_size) as executor:
                try:
                  future = executor.submit(timer, self, choice, self.nw_obj)
                  response = future.result(timeout = 0.3)
                  if response is not None:
                    response = int(response)
                  if response == seq_num:
                    print(f"correct ack: {response}")
                    seq_num = int(not(seq_num))
                    j += 1
                    if j == 64:
                      flag_break = True
                  else:
                    print(f"wrong ack: {response}")
                except Exception as e:
                  print(f"Unknown exception: {e}")
                
            except Exception as e:
              print(f"Unknown exception {e}")

    
        elif protocol == "GoBackN":
          window_size = 8
          seq_num = 0
          chunked_list = getChunks(segment, MTU)
          wrong_acks = 0

          while True:
            seq_num = seq_num - wrong_acks
            wrong_acks = 0
            acks_recvd = []
            count_window = 0
            if seq_num == 64:
              break
            for i in range(seq_num, seq_num + window_size):
              count_window = count_window + 1
              chunk = chunked_list[seq_num]
              choice = random.randint(1,3)
              print(f"sending {chunk} with seq num {seq_num}")
              self.send_segment(choice, seq_num, dest_ip, dest_port, chunk, size)
              with ThreadPoolExecutor(max_workers= window_size) as executor:
                try:
                    future = executor.submit(timer, self, choice, self.nw_obj)
                    ack = future.result(timeout = 0.3)
                    if ack is not None:
                      acks_recvd.append(int(ack))
                except Exception as e:
                  print(f"Unknown exception: {e}")
              seq_num = seq_num + 1
              window_size = count_window
              if seq_num == 64:
                break
            expected = list(range(seq_num - window_size, seq_num))
            matching = []
            matching = list(itertools.zip_longest(expected, acks_recvd))
            print(f"(expected, received): {matching}")
            for exp, got in matching:
              if exp == got:
                print(f"correck ack: {exp}")
              if exp != got:
                print(f"missed ack: {exp}")
                wrong_acks += 1

        elif protocol == "SelectiveRepeat":
          window_size = 8
          seq_num = 0
          chunked_list = getChunks(segment, MTU)
          wrong_acks = 0
          buffer = []
          start = 0
          for i in range(window_size):
            buffer.append([i, -1, False]) # (seq_num, chunk, ack received?)
         

          while True:
            acks_recvd = []
            count_window = 0
            flag_stay = False

            for i in range(len(buffer)):
              if buffer[i][2] == False:
                flag_stay = True
                
            if not flag_stay:
              seq_num = buffer[-1][0] + 1
              start += len(buffer)
              buffer = []
              for i in range(seq_num, seq_num + window_size):
                buffer.append([i, -1, False]) # (seq_num, chunk, ack received?)
            else: 
              seq_num = start
            m = 0
          
            if seq_num == 64:
              break
            
            for i in range(seq_num, seq_num + window_size):
              count_window = count_window + 1
              chunk = chunked_list[seq_num]
              buffer[m][0] = seq_num
              buffer[m][1] = chunk
              choice = random.randint(1,3)

              if buffer[m][2] == False:
                print(f"chunk sending {chunk} with seq num {seq_num}")
                self.send_segment(choice, seq_num, dest_ip, dest_port, chunk, size)
              
                with ThreadPoolExecutor(max_workers= window_size) as executor:
                  try:
                      future = executor.submit(timer, self, choice, self.nw_obj)
                      ack = future.result(timeout = 0.3)
                      if ack is not None:
                        acks_recvd.append(int(ack))
                  except Exception as e:
                    print(f"Unknown exception: {e}")
              seq_num = seq_num + 1
              m += 1
              window_size = count_window
              if seq_num == 64:
                break
            
            
            missing_acks = []
            acks_recvd.sort()
            for i in range(seq_num - window_size, seq_num):
              if i not in acks_recvd:
                missing_acks.append(i)
            n = 0
            for i in range(seq_num - window_size, seq_num):
              if i in missing_acks:
                acks_recvd.insert(n, None)
              n += 1
            expected = list(range(seq_num - window_size, seq_num))
            
            matching = []
            matching = list(itertools.zip_longest(expected, acks_recvd))
            print(f"(expected, got): {matching}")

            m = 0
            for exp, got in matching:
              if exp != got and buffer[m][2] == False:
                print(f"missed ack: {exp}")
              else:
                buffer[m][2] = True
                print(f"correct ack: {buffer[m][0]}")
              m += 1
            
      else:
        choice = 1
        seq_num = 0
        self.send_segment(choice, seq_num, segment, size)

        
    
      

    except Exception as e:
      raise e

  ##################################
  #  send transport layer segment
  ##################################
  def send_segment (self, choice, seq_num, dest_ip, dest_port, chunk, len=0):
    protocol = self.config["Transport"]["TransportProtocol"]
    #print(chunk)
    try:
      # For this assignment, we ask our dummy network layer to
      # send it to peer. We ignore the length in this assignment
      #print ("Custom Transport Protocol::send_segment")
      if choice == 1:
        print("Choice 1: Send the chunk to the next hop")
        self.nw_obj.send_packet(seq_num, dest_ip, dest_port, chunk, len)
      elif choice == 2:
          print("Choice 2: Delay sending chunk to the next hop")
          time.sleep(0.2) 
          self.nw_obj.send_packet (seq_num, dest_ip, dest_port, chunk, len)
      elif choice == 3:
          print("Choice 3: Drop chunk")
          #self.nw_obj.send_packet(seq_num, chunk, len)

      #self.nw_obj.send_packet (segment, len)
      
    except Exception as e:
      raise e


  ######################################
  #  receive application-level message
  ######################################
  def recv_appln_msg_response (self, len=0):
    #print("Custom Transport Protocol:: recv_appln_msg_response")
    segment = self.nw_obj.recv_packet(len)
    return segment

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
      #print ("Custom Transport Protocol::recv_appln_msg")

      self.protocol = self.config["Transport"]["TransportProtocol"]
      chunk_sum = 0
      request = ''
      last = -1
      buffer = []
      window_size = 8
      m = 0

      for i in range(window_size):
        buffer.append([i, -1, False]) 
      m = 0

      while True:
        chunk = self.recv_segment ()
        chunk = chunk.decode("UTF-8")
        seq_num, dest_ip, dest_port, msg = chunk.split("!!!")
        seq_num = int(seq_num)
        flag_break = False

        if self.protocol == "AlternatingBit":
          if seq_num != last:
            self.send_transport_ack (seq_num)
            print(f"sent ack for sequence number {seq_num}")
            request = request + msg
            chunk_sum += 1
            last = seq_num
          else:
            self.send_transport_ack(last)
            print(f"sending wrong ack of {last} for sequence number {seq_num}")

        
        elif self.protocol == "GoBackN":
          if seq_num == last + 1:
            self.send_transport_ack(seq_num)
            print(f"sent ack for sequence number {seq_num}")
            request = request + msg
            chunk_sum = chunk_sum + 1
            last = seq_num
          else:
            self.send_transport_ack(last)
            print(f"sending wrong ack of {last} for sequence number {seq_num}")
      
   

        elif self.protocol == "SelectiveRepeat":
          for i in range(window_size):
            if seq_num == buffer[i][0]:
              m = i 

          buffer[m][0] = seq_num
          buffer[m][1] = msg
          buffer[m][2] = True
          buffer = sorted(buffer, key=itemgetter(0))
          
          self.send_transport_ack(seq_num)
          print(f"sending ack for sequence number {seq_num}")
          
          
          for i in range(window_size):
            if buffer[i][2] == False:
              flag_break = True
          
          if not flag_break:
            for i in range(window_size):
              request = request + buffer[i][1]
            chunk_sum = chunk_sum + window_size
            buffer = []
            for i in range(chunk_sum, chunk_sum + window_size):
              buffer.append([i, -1, False]) # (seq_num, chunk, ack received?)
          m += 1
        
        if chunk_sum == 64:
          print("received all chunks")
          break
      
      print(f"appended request: {request}")

      appln_msg = request.split("###")[0]

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
      #print ("Custom Transport Protocol::recv_segment")
      segment = self.nw_obj.recv_packet (len)

      return segment
    
    except Exception as e:
      raise e


 
    

  ######################################
  #  send transport layer ack
  ######################################
  def send_transport_ack (self, seq_num):
    
    try:
      print ("Custom Transport Protocol::send_transport_ack")
      self.nw_obj.send_packet_ack(seq_num)
      
    except Exception as e:
      raise e