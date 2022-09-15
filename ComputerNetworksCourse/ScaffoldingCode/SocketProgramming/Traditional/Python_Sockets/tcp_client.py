# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Demonstrate a TCP-based server using traditional
# sockets
#
# See https://docs.python.org/3/library/socket.html

# import the needed packages
import sys    # for system exception
import time   # for sleep
import argparse # for argument parsing
import socket # this is the underlying socket package

##################################
# Driver program
##################################
def driver (args):
  try:
    # The first step is to obtain a socket. Here we create one in BLOCKING mode
    print ("Create a socket")
    s = socket.socket (socket.AF_INET, # this indicates we need an IPv4 style socket
                       socket.SOCK_STREAM) # this indicates we need a reliable stream style socket
  except OSError as err:
    print ("Exception creating a socket {}".format (err))
    return
  except:
    print ("Other exception obtaining a socket {}".format (sys.exc_info()[0]))
    return

  try:
    # The next step is to connect the socket to the IP addr and port on which
    # the server is listening
    print ("Connect to addr: {} and port {}".format (args.addr, args.port))
    addr = (args.addr, args.port)
    s.connect (addr)
  except OSError as err:
    print ("Exception connecting {}".format (err))
    return
  except:
    print ("Some exception occurred connecting {}".format (sys.exc_info()[0]))
    return

  # since we are a client, we actively send something to the server
  print ("client sending Hello messages for specified num of iterations")
  for i in range (args.iters):
    try:
      #  Wait for next request from client
      print ("Send a Hello")
      s.send (b"HelloWorld")
    except OSError as err:
      print ("Exception sending {}".format (err))
      break
    except:
      print ("Some exception occurred sending {}".format (sys.exc_info()[0]))
      break
    
    try:
      # receive a reply
      print ("Waiting to receive from server")
      message = s.recv (1024)
      print ("Received reply in iteration {} is {}".format (i, message))
    except OSError as err:
      print ("Exception receiving {}".format (err))
      break
    except:
      print ("Some exception occurred receiving {}".format (sys.exc_info()[0]))
      break

  # since we are out of this loop due to client closing the connection,
  # we close the client's socket here too
  print ("Closing connection to the server")
  s.close ()

##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ()

  # add optional arguments
  parser.add_argument ("-a", "--addr", default="127.0.0.1", help="IP Address to connect to (default: localhost i.e., 127.0.0.1)")
  parser.add_argument ("-i", "--iters", type=int, default=10, help="Number of iterations (default: 10")
  parser.add_argument ("-p", "--port", type=int, default=5555, help="Port that server is listening on (default: 5555)")
  args = parser.parse_args ()

  return args
    
#------------------------------------------
# main function
def main ():
  """ Main program """

  print("Demo program for TCP Client Using Traditional Sockets")

  # first parse the command line args
  parsed_args = parseCmdLineArgs ()
    
  # start the driver code
  driver (parsed_args)

#----------------------------------------------
if __name__ == '__main__':

  main ()
