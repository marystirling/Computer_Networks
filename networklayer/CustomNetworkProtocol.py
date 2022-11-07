# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for our custom network protocol
#          For assignment 1, this will be very simple and will include
#          all the ZeroMQ logic
#

# import the needed packages
import os     # for OS functions
import sys    # for syspath and system exception

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert (0, "../")

# import the zeromq capabilities
import zmq
timeout = 500

############################################
#  Bunch of Network Layer Exceptions
#
# @TODO@ Add whatever make sense here.
############################################

############################################
#       Custom Network Protocol class
############################################
class CustomNetworkProtocol ():
  '''Custom Network Protocol'''

  ###############################
  # constructor
  ###############################
  def __init__ (self):
    self.role = None  # indicates if we are client or server, false => client
    self.config = None # network configuration
    self.ctx = None # ZMQ context
    self.socket = None  # At this stage we do not know if more than one socket needs to be maintained
    
  ###############################
  # configure/initialize
  ###############################

  def initialize (self, config, role, ip, port, router=True):
    ''' Initialize the object '''

    try:
      # Here we initialize any internal variables
      print ("Custom Network Protocol Object: Initialize")
      self.config = config
      self.role = role
      self.ip = ip
      self.port = port
    
      # initialize our variables
      print ("Custom Network Protocol Object: Initialize - get ZeroMQ context")
      self.ctx = zmq.Context ()

      # initialize the config object
      
      # initialize our ZMQ socket
      #
      # @TODO@
      # Note that in a subsequent assignment, we will need to move on to a
      # different ZMQ socket pair, which supports asynchronous transport. In those
      # assignments we may be using the DEALER-ROUTER pair instead of REQ-REP

      if (self.role):

        print ("Custom Network Protocol Object: Initialize - get REQ socket")

        # we are the server side
        try:
          self.socket = self.ctx.socket (zmq.DEALER)
        except zmq.ZMQError as err:
          print ("ZeroMQ Error obtaining context: {}".format (err))
          return
        except:
          print ("Some exception occurred getting DEALER socket {}".format (sys.exc_info()[0]))
          return
          

  
        try:
          # as in a traditional self.socket, tell the system what IP addr and port are we
          # going to connect to. Here, we are using TCP self.sockets.
          bind_string = "tcp://" + self.ip + ":" + str (self.port)
          print ("Custom Network Protocol Object: Initialize - connect self.socket to {}".format (bind_string))
          self.socket.bind (bind_string)
        except zmq.ZMQError as err:
          print ("ZeroMQ Error connecting REQ self.socket: {}".format (err))
          self.socket.close ()
          return
        except:
          print ("Some exception occurred connecting REQ self.socket {}".format (sys.exc_info()[0]))
          self.socket.close ()
          return


      


      else:
        # we are the client side
        print ("Custom Network Protocol Object: Initialize - get REQ socket")

        # since we are client, we connect
        try:
          self.socket = self.ctx.socket (zmq.DEALER)
        except zmq.ZMQError as err:
          print ("ZeroMQ Error obtaining context: {}".format (err))
          return
        except:
          print ("Some exception occurred getting DEALER socket {}".format (sys.exc_info()[0]))
          return

        try:
          # set our identity
          addr = self.ip + ":" + str(self.port)
          print ("client setting its identity: {}".format (addr))
          self.socket.setsockopt (zmq.IDENTITY, bytes (addr, "utf-8"))
        except zmq.ZMQError as err:
          print ("ZeroMQ Error setting sockopt: {}".format (err))
          return
        except:
          print ("Some exception occurred setting sockopt on REQ self.socket {}".format (sys.exc_info()[0]))
          return
        
        try:
          # as in a traditional self.socket, tell the system what IP addr and port are we
          # going to connect to. Here, we are using TCP self.sockets.
          connect_string = "tcp://" + self.ip + ":" + str (self.port)
          print ("Custom Network Protocol Object: Initialize - connect self.socket to {}".format (connect_string))
          self.socket.connect (connect_string)
        except zmq.ZMQError as err:
          print ("ZeroMQ Error connecting REQ self.socket: {}".format (err))
          self.socket.close ()
          return
        except:
          print ("Some exception occurred connecting REQ self.socket {}".format (sys.exc_info()[0]))
          self.socket.close ()
          return

    except Exception as e:
      raise e  # just propagate it
  
  
  ######################################
  #  send packet
  ######################################
  def send_packet (self, seq_num, packet, size):
    try:

      # Here, we simply delegate to our ZMQ socket to send the info
      print ("Custom Network Protocol::send_packet")
      
      #dest_ip = packet[0]
      #dest_port = packet[1]
      #payload = packet[2]
      #print(f"seq_num is {seq_num} and packet is {packet}")
      
      #print(f"the size of my packet in network layer is: {sys.getsizeof(packet)}")
      #print(packet)
      packet = packet.decode()
      #print(packet)
      #print(f"The size of my packet in network layer is: {sys.getsizeof(packet)}")
      str_packet = str(seq_num) + "!!!" + str(packet)
      #print(f"chunk in nw layer is {str_packet}")

      if self.config["Application"]["Serialization"] == "json":
        #self.socket.send (bytes(packet, "utf-8"))
        self.socket.send_multipart([b'', bytes(str_packet,"utf-8")])
      elif self.config["Application"]["Serialization"] == "fbufs":
        self.socket.send (packet)


    except Exception as e:
      raise e
    
 

  ######################################
  #  receive packet 
  ######################################
  def recv_packet (self, len=0):
    try:
      # @TODO@ Note that this method always receives bytes. So if you want to
      # convert to json, some mods will be needed here. Use the config.ini file.
      print ("CustomNetworkProtocol::recv_packet")

      
      packet = self.socket.recv_multipart()[-1]
     # print(packet)
      packet.decode("utf-8")
      #print(f"packet after recv_packet is {packet}")
      #packet = self.socket.recv ()
      
      return packet
    except Exception as e:
      raise e

 

  def send_nw_ack (self, seq_num, packet, len=0):
    try:
      # @TODO@ Note that this method always receives bytes. So if you want to
      # convert to json, some mods will be needed here. Use the config.ini file.
      print ("CustomNetworkProtocol::send_nw_ack")
      seq_num = bytes(seq_num)
      #self.socket.send_multipart ([b'',str(seq_num) + "~" + packet])
      self.socket.send(seq_num, len)
      #print("made it past this packet thing")
      
    except Exception as e:
      raise e



  def recv_nw_ack (self, seq_num, len=0):
    try:
      # @TODO@ Note that this method always receives bytes. So if you want to
      # convert to json, some mods will be needed here. Use the config.ini file.
      print ("CustomNetworkProtocol::recv_nw_ack")
      ack = self.socket.recv_multipart()
      
      return ack
      
      
      return packet
    except Exception as e:
      raise e

