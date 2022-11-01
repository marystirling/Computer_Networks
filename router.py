# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Code taken from ZeroMQ's sample code for the HelloWorld
# program, but modified to use DEALER-ROUTER sockets to showcase
# TCP. Plus, added other decorations like comments, print statements,
# argument parsing, etc.
#
# This code is for the intermediate router.
#
# Note: my default indentation is now set to 2 (in other snippets, it
# used to be 4)

# import the needed packages
import sys    # for system exception
import time   # for sleep
import argparse # for argument parsing
import zmq    # this package must be imported for ZMQ to work
import socket
import csv
import configparser
from urllib.request import urlopen
import re
import subprocess
import time
import pandas as pd
import netifaces as ni

def GetHostIP (curr_address):
    if curr_address == "10.0.0.1" or curr_address == "127.0.0.1":
        return "H1"
    elif curr_address == "10.0.0.2" or curr_address == "127.0.0.2":
        return "H2"
    elif curr_address == "10.0.0.3" or curr_address == "127.0.0.3":
        return "H3"
    elif curr_address == "10.0.0.4" or curr_address == "127.0.0.4":
        return "H4"
    elif curr_address == "10.0.0.5" or curr_address == "127.0.0.5":
        return "H5"
    elif curr_address == "10.0.0.6" or curr_address == "127.0.0.6":
        return "H6"

def BackToIP (hostname):
    if hostname == "H1":
        #return "10.0.0.1"
        return "127.0.0.1"
    elif hostname == "H2":
        #return "10.0.0.2"
        return "127.0.0.2"
    elif hostname == "H3":
        #return "10.0.0.3"
        return "127.0.0.3"
    elif hostname == "H4":
        #return "10.0.0.4"
        return "127.0.0.4"
    elif hostname == "H5":
        #return "10.0.0.5"
        return "127.0.0.5"
    elif hostname == "H6":
        #return "10.0.0.6"
        return "127.0.0.6"
    
def hostname_to_ip (hostname):
    return "10.0.0." + str(hostname.split("H",1)[-1])

def ip_to_hostname (host_ip):
    return "H" + host_ip.split(".")[-1]


##################################
# Driver program
##################################
def driver (args):
    
  start_time = time.time()
    
  config = configparser.ConfigParser ()
  config.read (args.config)
  
  intfs = ni.interfaces()
      
  for intf in intfs:
    print("IP addresses associated with interface {} are {}".format (intf, ni.ifaddresses (intf)))
  host_ip = ni.ifaddresses(intfs[1])[ni.AF_INET][0]['addr']
  print(type(host_ip))
  print(host_ip)
  
  try:
    # every ZMQ session requires a context
    print ("Obtain the ZMQ context")
    context = zmq.Context ()   # returns a singleton object
  except zmq.ZMQError as err:
    print ("ZeroMQ Error obtaining context: {}".format (err))
    return
  except:
    print ("Some exception occurred getting context {}".format (sys.exc_info()[0]))
    return

  try:
    # Get a poller object
    print ("Obtain the Poller")
    poller = zmq.Poller ()
  except zmq.ZMQError as err:
    print ("ZeroMQ Error obtaining poller: {}".format (err))
    return
  except:
    print ("Some exception occurred getting poller {}".format (sys.exc_info()[0]))
    return


  try:
    # The socket concept in ZMQ is far more advanced than the traditional socket in
    # networking. Each socket we obtain from the context object must be of a certain
    # type. For TCP, we will use ROUTER for server side (many other pairs are supported
    # in ZMQ for tcp.
    print ("Obtain the ROUTER type socket")
    bind_sock = context.socket (zmq.ROUTER)
  except zmq.ZMQError as err:
    print ("ZeroMQ Error obtaining ROUTER socket: {}".format (err))
    return
  except:
    print ("Some exception occurred getting ROUTER socket {}".format (sys.exc_info()[0]))
    return
  
  try:
    # as in a traditional socket, tell the system what port are we going to listen on
    # Moreover, tell it which protocol we are going to use, and which network
    # interface we are going to listen for incoming requests. This is TCP.
    print ("Bind the ROUTER socket")
    bind_string = "tcp://" + args.myaddr + ":" + str (args.myport)
    #print(args.myaddr)
    print ("TCP router will be binding on {}".format (bind_string))
    bind_sock.bind (bind_string)
  except zmq.ZMQError as err:
    print ("ZeroMQ Error binding ROUTER socket: {}".format (err))
    bind_sock.close ()
    return
  except:
    print ("Some exception occurred binding ROUTER socket {}".format (sys.exc_info()[0]))
    bind_sock.close ()
    return

  try:
    # The socket concept in ZMQ is far more advanced than the traditional socket in
    # networking. Each socket we obtain from the context object must be of a certain
    # type. For TCP, we will use the DEALER socket type (many other pairs are supported)
    # and this is to be used on the client side.
    print ("Router acquiring connection socket")
    conn_sock = context.socket (zmq.DEALER)
  except zmq.ZMQError as err:
    print ("ZeroMQ Error obtaining context: {}".format (err))
    return
  except:
    print ("Some exception occurred getting DEALER socket {}".format (sys.exc_info()[0]))
    return
  
  try:
    # set our identity
    print ("router setting its identity: {}".format (args.demux_token))
    conn_sock.setsockopt (zmq.IDENTITY, bytes (args.demux_token, "utf-8"))
  except zmq.ZMQError as err:
    print ("ZeroMQ Error setting sockopt: {}".format (err))
    return
  except:
    print ("Some exception occurred setting sockopt on REQ socket {}".format (sys.exc_info()[0]))
    return
 

  try:
    # as in a traditional socket, tell the system what IP addr and port are we
    # going to connect to. Here, we are using TCP sockets.

    print ("Router connecting to next hop")
 
    #ip_addr = socket.gethostbyname(hostname)
    #print(f"IP ADDRESS: {ip_addr}")
    #print(os.system('ifconfig'))

    
    if (config["Network"]["Route"] == "route1"):
      with open("route1.csv") as f:
        print("are we in here")
        reader = csv.reader(f)
        for row in reader:
          host_ip = "H5"
         # if(row[0] == host_ip and row[1] == args.final_dest_ip):
          if(row[0]== host_ip and row[1] == '10.0.0.6'):
          #if (row[0] == "H1" and row[1] == '10.0.0.6'):
            #nexthopaddr = row[2]
            #nexthopip = BackToIP(nexthopaddr)
            #nextport = 5555
            #print(nexthopaddr)
            #print(nexthopip)
            print("did i even go in here")


    elif (config["Network"]["Route"] == "route2"):
      self.final_dest_ip = '10.0.0.27'
    #connect_string = "tcp://" + nexthopip + ":" + str(nextport)
    #connect_string = "tcp://" + nexthopip + ":" + str(args.nexthopport)
    connect_string = "tcp://" + args.nexthopaddr + ":" + str (args.nexthopport)
    #connect_string = "tcp://" + next_hop + ":" + str(args.nexthopport)
    print ("TCP client will be connecting to {}".format (connect_string))
    conn_sock.connect (connect_string)
  except zmq.ZMQError as err:
    print ("ZeroMQ Error connecting DEALER socket: {}".format (err))
    conn_sock.close ()
    return
  except:
    print ("Some exception occurred connecting DEALER socket {}".format (sys.exc_info()[0]))
    conn_sock.close ()
    return

  try:
    # register sockets
    print ("Register sockets for incoming events")
    poller.register (bind_sock, zmq.POLLIN)
    poller.register (conn_sock, zmq.POLLIN)
  except zmq.ZMQError as err:
    print ("ZeroMQ Error registering with poller: {}".format (err))
    return
  except:
    print ("Some exception occurred getting poller {}".format (sys.exc_info()[0]))
    return
  
  # since we are a server, we service incoming clients forever
  print ("Router now starting its forwarding loop")
  while True:
    try:
      # collect all the sockets that are enabled in this iteration
      print ("Poller polling")
      socks = dict (poller.poll ())
    except zmq.ZMQError as err:
      print ("ZeroMQ Error polling: {}".format (err))
      return
    except:
      print ("Some exception occurred in polling {}".format (sys.exc_info()[0]))
      return

    # Now handle the event for each enabled socket
    if bind_sock in socks:
      # we are here implies that the bind_sock had some info show up.
      try:
        #  Wait for next request from previous hop. When using DEALER/ROUTER, it is suggested to use
        # multipart send/receive. What we receive will comprise the sender's info which we must preserve, an empty
        # byte, and then the actual payload
        print ("Receive from prev hop")
        request = bind_sock.recv_multipart ()
        
        print("Router received request from prev hop via ROUTER: %s" % request)
        
    
      except zmq.ZMQError as err:
        print ("ZeroMQ Error receiving: {}".format (err))
        bind_sock.close ()
        return
      except:
        print ("Some exception occurred receiving/sending {}".format (sys.exc_info()[0]))
        bind_sock.close ()
        return
      
      
      try:
        #  forward request to server
        print ("Forward the same request to next hop over the DEALER")
        conn_sock.send_multipart (request)
      except zmq.ZMQError as err:
        print ("ZeroMQ Error forwarding: {}".format (err))
        conn_sock.close ()
        return
      except:
        print ("Some exception occurred forwarding {}".format (sys.exc_info()[0]))
        conn_sock.close ()
        return
    

    if conn_sock in socks:
      try:
        #  Wait for response from next hop
        print ("Receive from next hop")
        response = conn_sock.recv_multipart ()
        print("Router received response from next hop via DEALER: %s" % response)
      except zmq.ZMQError as err:
        print ("ZeroMQ Error receiving response: {}".format (err))
        conn_sock.close ()
        return
      except:
        print ("Some exception occurred receiving response {}".format (sys.exc_info()[0]))
        conn_sock.close ()
        return

      try:
        #  Send reply back to previous hop. request[0] is the original client identity preserved at every hop
        # response[1] has actual payload
        print ("Send reply to prev hop via ROUTER")
        bind_sock.send_multipart (response)
      except zmq.ZMQError as err:
        print ("ZeroMQ Error sending: {}".format (err))
        bind_sock.close ()
        return
      except:
        print ("Some exception occurred receiving/sending {}".format (sys.exc_info()[0]))
        bind_sock.close ()
        return
      end_time = time.time()
      print(f"overall time is {end_time - start_time}")

##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ()

  # add optional arguments
  parser.add_argument ("-c", "--config", default="config.ini", help="configuration file (default: config.ini")
  parser.add_argument ("-a", "--myaddr", default="*", help="Interface to bind to (default: *)")
  parser.add_argument ("-p", "--myport", type=int, default=4444, help="Port to bind to (default: 4444)")
  parser.add_argument ("-A", "--nexthopaddr", default="127.0.0.1", help="IP Address of next router or end server to connect to (default: localhost i.e., 127.0.0.1)")
  parser.add_argument ("-P", "--nexthopport", type=int, default=4444, help="Port that appln or next router is listening on (default: 4444)")
  parser.add_argument ("-t", "--demux_token", default="router", help="Our identity used as a demultiplexing token (default: router)")
  args = parser.parse_args ()

  return args
    
#------------------------------------------
# main function
def main ():
  """ Main program """

  print("Demo program for TCP Router with ZeroMQ")

  # first parse the command line args
  parsed_args = parseCmdLineArgs ()
    
  # start the driver code
  driver (parsed_args)

#----------------------------------------------
if __name__ == '__main__':
  # here we just print the version numbers
  print("Current libzmq version is %s" % zmq.zmq_version())
  print("Current pyzmq version is %s" % zmq.pyzmq_version())

  main ()