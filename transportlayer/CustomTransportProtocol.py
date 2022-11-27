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
ack_list = []

def timer(self, choice, socket):
    response = None
    try:
      if choice == 3:
        time.sleep(1)
      else:
        response = 1
        response = socket.recv_packet()
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
  
  #################################
  # send application message RESPONSE
  ################################
  def send_appln_msg_response(self, flag_split, dest_ip, dest_port, payload, size):
    print("Custom Transport Protocol::send_appln_msg_response")
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
      
      print ("Custom Transport Protocol::send_appln_msg")
      segment = str(flag_split) + "~" + dest_ip + "~" + str(dest_port) + "~" + payload + "###"
      
      segment = bytes(segment,"utf-8")
      segment = GetPaddedSegment(segment)

      print(f"Segment in transport layer {sys.getsizeof(segment)}")


      print(segment)
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
            #choice = 1
            self.send_segment(choice, seq_num, dest_ip, dest_port, chunk, size)
            print(f"sending {chunk} with seq num {seq_num}")
            try:
              with ThreadPoolExecutor(max_workers = window_size) as executor:
                try:
                  future = executor.submit(timer, self, choice, self.nw_obj)
                  response = future.result(timeout = 2)
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
                    ack = future.result(timeout = 2)
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
          print("in selective repeat")
          window_size = 8
          base = 0
          seq_num = 0
          acks_recvd = []
          j = 0 # chunk index for list
          chunked_list = getChunks(segment, MTU)
          print(chunked_list)
          wrong_acks = 0
          flag_break = False
          buffer = []
          start_j = 0
          for i in range(window_size):
            buffer.append([i, -1, -1, False]) # (seq_num, j, chunk, ack received?)
          print(buffer)
          acks_recvd = []
          while True:

            if flag_break:
              break
            
            acks_recvd = []

            count_window = 0

            #seq_num = 0
            flag_stay = False
            for i in range(len(buffer)):
              print("do we enter this FOR LOOP")
              if buffer[i][3] == False:
                flag_stay = True
                print(f"flag_stay is {flag_stay} for {buffer[i][3]}")
            if not flag_stay:
              print("do we enter not flag stay")
              j = buffer[-1][1] + 1
              seq_num = j
              start_j += len(buffer)
              buffer = []
              for i in range(seq_num, seq_num + window_size):
                buffer.append([i, -1, -1, False]) # (seq_num, j, chunk, ack received?)
                print(buffer)
            else: 
              #j = j - window_size
              j = start_j
            m = 0
            seq_num = j 
            print(f"MY J IS {j} and m is {m} and seq_num is {seq_num}")
            #start_j = j
           
            if seq_num == 64:
              break
            
            for i in range(seq_num, seq_num + window_size):
              print(buffer)
              count_window = count_window + 1
              chunk = chunked_list[seq_num]
              print(f"the base is here {i}")
              print(f"the chunk in question is {chunk}")
              print(f"seq_num is {seq_num}")
              print(f"the seq_num in buffer here is already {buffer[m][0]}")
              buffer[m][0] = seq_num
              buffer[m][1] = j
              buffer[m][2] = chunk
              choice = random.randint(1,3)
              #choice = 1
              #if seq_num == 7 or j >= 55:
              #  choice = random.randint(1,2)
              #choice = 1
              if buffer[m][3] == False:
                print(f"chunk sending is {chunk} with seq num {seq_num}")
                self.send_segment(choice, seq_num, dest_ip, dest_port, chunk, size)
              
                with ThreadPoolExecutor(max_workers= window_size) as executor:
                  try:
                  
                      future = executor.submit(timer, self, choice, self.nw_obj)
                      print(f"future = {future}")
                      ack = future.result(timeout = 2)
                      if ack is not None:
                        acks_recvd.append(int(ack))
                  except Exception as e:
                    print("is this the exception")
                    print(f"Unknown exception: {e}")
              seq_num = seq_num + 1
              j = j + 1
              m += 1
              window_size = count_window
              print(f"count window is {count_window} and {window_size}")
              if seq_num == 64:
                #flag_break = True
                break
            
            print(f"window size is now {window_size}")
            #acks_recvd.sort()
            missing_acks = []
            #test_acks = acks_recvd
            acks_recvd = [*set(acks_recvd)]
            if -1 in acks_recvd:
              acks_recvd.remove(-1)
            print(f"acks_recvd is {acks_recvd}")
            acks_recvd.sort()
            print(f"acks in recv_acks is {acks_recvd}")
            for i in range(seq_num - window_size, seq_num):
              if i not in acks_recvd:
                missing_acks.append(i)
            print(f"missing acks is {missing_acks}")
            n = 0
            for i in range(seq_num - window_size, seq_num):
              if i in missing_acks:
                acks_recvd.insert(n, None)
              n += 1
            print(f"acks recvd is now {acks_recvd}")
            expected = list(range(seq_num - window_size, seq_num))
            print(f"expected is: {expected}")
            
            matching = []
            matching = list(itertools.zip_longest(expected, acks_recvd))
            print(f"matching: {matching}")
            end = window_size - 1
            print(f"end should be {end}")
            m = 0
            for exp, got in matching:
              if exp != got:
                #base = exp
                print(f"missed ack: {exp}")
                #seq_num = 0
                
                #break
              else:
                #base = exp
                print("DID WE GO IN HEREEEEEE")
                print(f"{buffer[m][3]}")
                buffer[m][3] = True
                #buffer.pop(seq_num)
                print(f"new base is {base}")
                #if exp == 0:
                #    base += 1
                if exp == end:
                  #seq_num = 0 
                  print(f"got full window, base = {base}")
                  print(f"the seq_num is now {seq_num}")
                  print(f"the j now is: {j}")
                  if j == 64:
                    flag_break = True
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
      print ("Custom Transport Protocol::send_segment")
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
    print("Custom Transport Protocol:: recv_appln_msg_response")
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
      print ("Custom Transport Protocol::recv_appln_msg")
      #appln_msg = self.recv_segment ()
      self.protocol = self.config["Transport"]["TransportProtocol"]

      chunk_sum = 0
      request = ''
      last = -1
      buffer = []
      window_size = 8
      m = 0
      for i in range(window_size):
        buffer.append([i, -1, False]) # (seq_num, chunk, ack received?)
        print(buffer)
      #i = 0
      #last = 0
      m = 0
      while True:
      #for i in range(64):
        chunk = self.recv_segment ()
        #chunk = chunk.decode("UTF-8")
        #seq_num = chunk.split("~")[-1]
        
        chunk = chunk.decode("UTF-8")
        print(f"chunk hereeee is now {chunk}")

        seq_num, dest_ip, dest_port, msg = chunk.split("!!!")

        print(f"seq_num {seq_num}, ip {dest_ip}, port {dest_port}")
        flag_break = False

        print(f"msg is {msg}")
        print(f"chunk sum is {chunk_sum}")

        if self.protocol == "AlternatingBit":
          seq_num = int(seq_num)
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
          seq_num = int(seq_num)
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
          seq_num = int(seq_num)

          #if m == 8:
            #m = 0
          for i in range(window_size):
            if seq_num == buffer[i][0]:
              m = i 
              print(f"THE M IS NOW: {m} with {seq_num}")
              
          #print(f"the last is {last} and the seq_num is {seq_num}")
          #buffer.append([seq_num, msg])
          print(f"THe M is currently {m}")
          buffer[m][0] = seq_num
          buffer[m][1] = msg
          buffer[m][2] = True
          print(f"buffer: {buffer}")
          #self.send_transport_ack(seq_num)
          #buffer.sort()
          buffer = sorted(buffer, key=itemgetter(0))
          print(f"sorted buffer: {buffer}")
          self.send_transport_ack(seq_num)
          
          
          for i in range(window_size):
            if buffer[i][2] == False:
              flag_break = True
          
          if not flag_break:
            for i in range(window_size):
              request = request + buffer[i][1]
              print(f"APPENDED MESSAGE is {request}")
            chunk_sum = chunk_sum + window_size
            print(f"chunk sum in this loop is {chunk_sum}")
            buffer = []
            for i in range(chunk_sum, chunk_sum + window_size):
              buffer.append([i, -1, False]) # (seq_num, chunk, ack received?)
              print(buffer)
          m += 1

          
            
          
          

        
        if chunk_sum == 64:
          print("received all chunks")
          break
      
      print(f"appended {request}")

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
      print ("Custom Transport Protocol::recv_segment")
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