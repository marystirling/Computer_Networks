#  Author: Aniruddha Gokhale
#  Created: Fall 2021
#  Modified: Fall 2022 (for Computer Networking course)
#
#  Purpose: demonstrate serialization of a user-defined data structure using
#  JSON combined with ZeroMQ's REQ-REP sample code. Note that here we
#  are more interested in how a serialized packet gets sent over the network
#  and retrieved. To that end, we really don't care even if the client and
#  server were both on the same machine or remote to each other. Thus,
#  to simplify coding, we have mixed both the client and server in the same
#  code so that they run on the same machine. Hence, we term this as a Peer
#  which can don both roles.  When writing code for distributed client and
#  server, just separate the two pieces.
#
#  Here our custom message format comprises a sequence number, a timestamp, a name,
#  and a data buffer of several uint32 numbers (whose value is not relevant to us) 

# The different packages we need in this Python driver code
import os
import sys
import time  # needed for timing measurements and sleep

import random  # random number generator
import argparse  # argument parser

import zmq   # for ZeroMQ

## the following are our files
from custom_msg import CustomMessage_Order, CustomMessage_Health, CustomMessage_Response  # our custom message in native format
import serialize as sz  # this is from the file serialize.py in the same directory
##################################
#  The Peer class
##################################

  
  
class Peer ():
  def __init__ (self):
    self.req = None  # represents the REQ socket
    self.rep = None  # represents the REP socket

  def configure (self, port):
    try:
      # every ZMQ session requires a context
      print ("Obtain the ZMQ context")
      context = zmq.Context ()   # returns a singleton object
    except zmq.ZMQError as err:
      print ("ZeroMQ Error obtaining context: {}".format (err))
      raise
    except:
      print ("Some exception occurred getting context {}".format (sys.exc_info()[0]))
      raise

    try:
      # The socket concept in ZMQ is far more advanced than the traditional socket in
      # networking. Each socket we obtain from the context object must be of a certain
      # type. For TCP, we will use REP for server side (many other pairs are supported
      # in ZMQ for tcp.
      print ("Obtain the REP type socket")
      self.rep = context.socket (zmq.REP)
    except zmq.ZMQError as err:
      print ("ZeroMQ Error obtaining REP socket: {}".format (err))
      raise
    except:
      print ("Some exception occurred getting REP socket {}".format (sys.exc_info()[0]))
      raise

    try:
      # as in a traditional socket, tell the system what port are we going to listen on
      # Moreover, tell it which protocol we are going to use, and which network
      # interface we are going to listen for incoming requests. This is TCP.
      bind_string = "tcp://*:" + str (port)
      print ("TCP server will be binding on {}".format (bind_string))
      self.rep.bind (bind_string)
    except zmq.ZMQError as err:
      print ("ZeroMQ Error binding REP socket: {}".format (err))
      self.rep.close ()
      raise
    except:
      print ("Some exception occurred binding REP socket {}".format (sys.exc_info()[0]))
      self.rep.close ()
      raise

    try:
      # The socket concept in ZMQ is far more advanced than the traditional socket in
      # networking. Each socket we obtain from the context object must be of a certain
      # type. For TCP, we will use REQ for client side (many other pairs are supported
      # in ZMQ for tcp.
      print ("Obtain the REQ type socket")
      self.req = context.socket (zmq.REQ)
    except zmq.ZMQError as err:
      print ("ZeroMQ Error obtaining REQ socket: {}".format (err))
      raise
    except:
      print ("Some exception occurred getting REQ socket {}".format (sys.exc_info()[0]))
      raise

    try:
      # as in a traditional socket, tell the system where we are going to connect
      # to.  In this code, we assume server is on localhost but port is configurable.
      connect_string = "tcp://localhost:" + str (port)
      print ("TCP client will be connecting to {}".format (connect_string))
      self.req.connect (connect_string)
    except zmq.ZMQError as err:
      print ("ZeroMQ Error connecting REQ socket: {}".format (err))
      self.rep.close ()
      raise
    except:
      print ("Some exception occurred connecting REQ socket {}".format (sys.exc_info()[0]))
      self.rep.close ()
      raise

  # clean up
  def cleanup (self):
    # cleanup the sockets
    self.req.close ()
    self.rep.close ()

  # Use the ZMQ's send_serialized method to send the custom message
  def send_request (self, cm):
    """ Send serialized request"""
    try:
      # Use ZMQ's send_json method to send the jsonified buffer
      print ("ZMQ sending custom message via ZMQ's send_json method")
      buf = sz.serialize_o (cm)
      self.req.send_json (buf)
    except zmq.ZMQError as err:
      print ("ZeroMQ Error serializing request: {}".format (err))
      raise
    except:
      print ("Some exception occurred with send_json {}".format (sys.exc_info()[0]))
      raise

        
  # Send the ACK from server to client
  def send_ack (self):
    """ Send ACK"""
    try:
      # just send the dummy ACK.  Note, this is sent by server to client
      print ("ZMQ sending dummy ACK message")
      self.rep.send (b"ACK")
    except zmq.ZMQError as err:
      print ("ZeroMQ Error sending ACK: {}".format (err))
      raise
    except:
      print ("Some exception occurred with send_ack {}".format (sys.exc_info()[0]))
      raise

  # Use the ZMQ's recv_serialized method to send the custom message
  def recv_request (self):
    """ receive serialized request"""
    try:
      # use ZMQ's recv_json method
      print ("ZMQ receiving serialized custom message as json and then deserialize")
      buf = self.rep.recv_json ()
      cm = sz.deserialize_o (buf)
      return cm
    except zmq.ZMQError as err:
      print ("ZeroMQ Error receiving serialized message: {}".format (err))
      raise
    except:
      print ("Some exception occurred with recv_serialized {}".format (sys.exc_info()[0]))
      raise

  # receive the dummy ACK on client side
  def recv_ack (self):
    """ receive dummy ACK"""
    try:
      # receive dummy ack on client side.
      print ("ZMQ receiving dummy ACK")
      buf = self.req.recv ()
    except zmq.ZMQError as err:
      print ("ZeroMQ Error receiving dummy ack: {}".format (err))
      raise
    except:
      print ("Some exception occurred with recv_ack {}".format (sys.exc_info()[0]))
      raise

        
        
##################################
#        Driver program
##################################

def driver (name, iters, vec_len, port):

  print ("Driver program: Name = {}, Num Iters = {}, Vector len = {}, Peer port = {}".format (name, iters, vec_len, port))

  # first obtain a peer and initialize it
  print ("Driver program: create and configure a peer object")
  peer = Peer ()
  try:
    peer.configure (port)
  except:
    print ("Some exception occurred")
    return
  
  # now publish our information for the number of desired iterations
  cm = CustomMessage_Order ()   # create this once and reuse it for send/receive
  cm_h = CustomMessage_Health()
  cm_r = CustomMessage_Response()
  
  # veggies
  cm.tomato = cm.msg["contents"]["veggies"]["tomato"] = round(random.uniform(1,10),2)
  cm.carrot = cm.msg["contents"]["veggies"]["carrot"] = round(random.uniform(1,10),2)
  cm.cucumber = cm.msg["contents"]["veggies"]["cucumber"] = round(random.uniform(1,10),2)
  cm.corn = cm.msg["contents"]["veggies"]["corn"] = round(random.uniform(1,10),2)
  
  # drinks (cans)
  cm.coke = cm.msg["contents"]["drinks"]["coke"] = random.randint(1,10)
  cm.beer = cm.msg["contents"]["drinks"]["beer"] = random.randint(1,10)
  cm.rootbeer = cm.msg["contents"]["drinks"]["rootbeer"] = random.randint(1,10)
    
  # drinks (bottles)
  cm.sprite = cm.msg["contents"]["drinks"]["sprite"] = random.randint(1,10)
  cm.gingerale = cm.msg["contents"]["drinks"]["gingerale"] = random.randint(1,10)
  cm.lemonade = cm.msg["contents"]["drinks"]["lemonade"] = random.randint(1,10)
    
  # milk
  cm.milk = cm.msg["contents"]["milk"] = [(random.randint(1,7), round(random.uniform(1,10),2)) for j in range(3)]
        
  # bread
  cm.bread = cm.msg["contents"]["bread"] = [(random.randint(1,5), round(random.uniform(1,10),2)) for j in range(3)]
        
  # meat
  cm.meat = cm.msg["contents"]["meat"] = [(random.randint(1,5), round(random.uniform(1,10),2)) for j in range(5)]
  
  cm_h.dispenser = cm_h.msg["contents"]["dispenser"] = random.randint(1,3)
  cm_h.icemaker = cm_h.msg["contents"]["icemaker"] = random.randint(1,100)
  cm_h.lightbulb = cm_h.msg["contents"]["lightbulb"] = random.randint(1,2)
  cm_h.fridge_temp = cm_h.msg["contents"]["fridge_temp"] = random.randint(0,100)
  cm_h.freezer_temp = cm_h.msg["contents"]["freezer_temp"] = random.randint(-50,100)
  cm_h.sensor_status = cm_h.msg["contents"]["sensor_status"] = random.randint(1,2)
  cm_h.capacity_full = cm_h.msg["contents"]["capacity_full"] = random.randint(1,100)
  
  cm_r.code = cm_r.msg["code"] = random.randint(0,1)
  #cm_r.health_response = cm_r.msg["contents"]["health_response"] = 1
  #cm_r.bad_response = cm_r.msg["contents"]["bad_response"] = 2
    
  
  cm.dump ()

    # Recall that we are a peer running on the same machine, and because
    # we are using the REQ-REP pattern, there has to be a response
    # from server to client side. Here we send a dummy ACK which does not
    # need any serialization.
  try:
      # now let the peer send the message to its server part
      print("got here")
      print ("Peer client sending the serialized message")
      start_time = time.time ()
      peer.send_request (cm)
      end_time = time.time ()
      print ("Serialization took {} secs".format (end_time-start_time))
  except:
      return

  try:
      # now let the peer receive the message at the server end
      print ("Peer client sending the serialized message")
      start_time = time.time ()
      cm = peer.recv_request ()
      end_time = time.time ()
      print ("Deserialization took {} secs".format (end_time-start_time))
      print ("------ contents of message after deserializing ----------")
      cm.dump ()
  except:
      return

  try:
      # now let the peer send the ACK
      print ("Peer server sending ACK")
      peer.send_ack ()
  except:
      return

  try:
      # now let the peer receive the ack
      print ("Peer client receiving the ACK")
      peer.recv_ack ()
  except:
      return

    # sleep a while before we send the next serialization so it is not
    # extremely fast
  time.sleep (0.050)  # 50 msec



  # we are done. Just cleanup the peer before exiting
  peer.cleanup ()
  
##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()

    # add optional arguments
    parser.add_argument ("-i", "--iters", type=int, default=10, help="Number of iterations to run (default: 10)")
    parser.add_argument ("-l", "--veclen", type=int, default=20, help="Length of the vector field (default: 20; contents are irrelevant)")
    parser.add_argument ("-n", "--name", default="FlatBuffer ZMQ Demo", help="Name to include in each message")
    parser.add_argument ("-p", "--port", type=int, default=5555, help="Port where the server part of the peer listens and client side connects to (default: 5555)")
    # parse the args
    args = parser.parse_args ()

    return args
    
#------------------------------------------
# main function
def main ():
  """ Main program """

  print("Demo program for Flatbuffer serialization/deserialization")

  # first parse the command line args
  parsed_args = parseCmdLineArgs ()
    
  # start the driver code
  driver (parsed_args.name, parsed_args.iters, parsed_args.veclen, parsed_args.port)

#----------------------------------------------
if __name__ == '__main__':
    main ()
