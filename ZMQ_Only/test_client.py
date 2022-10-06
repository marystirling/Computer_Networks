# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Code taken from ZeroMQ's sample code for the HelloWorld
# program, but modified to use REQ-REP sockets to showcase
# TCP. Plus, added other decorations like comments, print statements,
# argument parsing, etc.
#
# ZMQ is also offering a new CLIENT-SERVER pair of ZMQ sockets but
# these are still in draft form and are not properly supported. If you
# want to try, just replace REQ by CLIENT here (and correspondingly, in
# the tcp_server.py, replace REP by SERVER)
#
# Note: my default indentation is now set to 2 (in other snippets, it
# used to be 4)

# import the needed packages
import sys    # for system exception
import time   # for sleep
import argparse # for argument parsing
import zmq    # this package must be imported for ZMQ to work

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import statistics
import seaborn as sns


latencies = []

##################################
# Driver program
##################################
def driver (args):
  try:
    # every ZMQ session requires a context
    print ("Obtain the ZMQ context")
    context = zmq.Context ()   # returns a singleton object
  except zmq.ZMQError as err:
    print ("ZeroMQ Error: {}".format (err))
    return
  except:
    print ("Some exception occurred getting context {}".format (sys.exc_info()[0]))
    return

  try:
    # The socket concept in ZMQ is far more advanced than the traditional socket in
    # networking. Each socket we obtain from the context object must be of a certain
    # type. For TCP, we will use the REQ socket type (many other pairs are supported)
    # and this is to be used on the client side.
    socket = context.socket (zmq.REQ)
  except zmq.ZMQError as err:
    print ("ZeroMQ Error obtaining context: {}".format (err))
    return
  except:
    print ("Some exception occurred getting REQ socket {}".format (sys.exc_info()[0]))
    return

  try:
    # set our identity
    print ("client setting its identity: {}".format (args.demux_token))
    socket.setsockopt (zmq.IDENTITY, bytes (args.demux_token, "utf-8"))
  except zmq.ZMQError as err:
    print ("ZeroMQ Error setting sockopt: {}".format (err))
    return
  except:
    print ("Some exception occurred setting sockopt on REQ socket {}".format (sys.exc_info()[0]))
    return

  try:
    # as in a traditional socket, tell the system what IP addr and port are we
    # going to connect to. Here, we are using TCP sockets.
    connect_string = "tcp://" + args.addr + ":" + str (args.port)
    print ("TCP client will be connecting to {}".format (connect_string))
    socket.connect (connect_string)
  except zmq.ZMQError as err:
    print ("ZeroMQ Error connecting REQ socket: {}".format (err))
    socket.close ()
    return
  except:
    print ("Some exception occurred connecting REQ socket {}".format (sys.exc_info()[0]))
    socket.close ()
    return

  # since we are a client, we actively send something to the server
  print ("client sending Hello messages for specified num of iterations")
  for i in range (args.iters):
    try:
      #  Wait for next request from client
      print ("Send message {}".format (args.message))
      start_time = time.time ()
      socket.send (bytes (args.message, "utf-8"))
    except zmq.ZMQError as err:
      print ("ZeroMQ Error sending: {}".format (err))
      socket.close ()
      return
    except:
      print ("Some exception occurred receiving/sending {}".format (sys.exc_info()[0]))
      socket.close ()
      return

    try:
      # receive a reply
      print ("Waiting to receive")
      message = socket.recv ()
      end_time = time.time ()
      latency_time = end_time - start_time
      latencies.append(latency_time)
      print ("Received reply in iteration {} is {} with latency {}".format (i, message, end_time-start_time))
    except zmq.ZMQError as err:
      print ("ZeroMQ Error receiving: {}".format (err))
      socket.close ()
      return
    except:
      print ("Some exception occurred receiving/sending {}".format (sys.exc_info()[0]))
      socket.close ()
      return

##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ()

  # add optional arguments
  parser.add_argument ("-a", "--addr", default="127.0.0.1", help="IP Address of next hop router to connect to (default: localhost i.e., 127.0.0.1)")
  parser.add_argument ("-p", "--port", type=int, default=4444, help="Port that next hop router is listening on (default: 4444)")
  parser.add_argument ("-i", "--iters", type=int, default=1000, help="Number of iterations (default: 1000")
  parser.add_argument ("-m", "--message", default="HelloWorld", help="Message to send: default HelloWorld")
  parser.add_argument ("-t", "--demux_token", default="client", help="Our identity used as a demultiplexing token (default: client)")
  args = parser.parse_args ()

  return args
    
#------------------------------------------
# main function
def main ():
  """ Main program """

  print("Demo program for TCP Client with ZeroMQ Using Intermediate routers")

  # first parse the command line args
  parsed_args = parseCmdLineArgs ()
    
  # start the driver code
  driver (parsed_args)
	
  print(latencies)
  
  ax = sns.distplot(a=latencies, bins=40, color='blue', hist_kws={"edgecolor": 'black'})
  ax.set(ylabel = "latency time")
  ax.set(title = "Scenario 1: 7 hosts, 1 switch, no loss, 1 client")
  plt.show()
 
  
  
#----------------------------------------------
if __name__ == '__main__':
  # here we just print the version numbers
  print("Current libzmq version is %s" % zmq.zmq_version())
  print("Current pyzmq version is %s" % zmq.pyzmq_version())

  main ()
