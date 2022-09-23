#  Author: Aniruddha Gokhale
#  Created: Fall 2021
#  Modified: Fall 2022 (for Computer Networking course)
#
#  Purpose: demonstrate serialization of a user-defined data structure using
#  JSON
#
#  Here our custom message format comprises a sequence number, a timestamp, a name,
#  and a data buffer of several uint32 numbers (whose value is not relevant to us) 

# The different packages we need in this Python driver code
import os
import sys
import time  # needed for timing measurements and sleep

import random  # random number generator
import argparse  # argument parser

## the following are our files
from custom_msg import CustomMessage_Order, CustomMessage_Health, CustomMessage_Response  # our custom message in native format
import serialize as sz  # this is from the file serialize.py in the same directory



 


##################################
#        Driver program
##################################

def driver (name, iters, vec_len):

  print ("Driver program: Name = {}, Num Iters = {}, Vector len = {}".format (name, iters, vec_len))
    
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
        
  # here we are calling our serialize method passing it
  # the iteration number, the topic identifier, and length.
  # The underlying method creates some dummy data, fills
  # up the data structure and serializes it into the buffer
  print ("serialize the message")
  start_time = time.time ()
  buf = sz.serialize_o (cm)
  end_time = time.time ()
  print ("Serialization took {} secs".format (end_time-start_time))

  # now deserialize and see if it is printing the right thing
  print ("deserialize the message")
  start_time = time.time ()
  cm = sz.deserialize_o (buf)
  end_time = time.time ()
  print ("Deserialization took {} secs".format (end_time-start_time))

  print ("------ contents of message after deserializing ----------")
  cm.dump ()

  # sleep a while before we send the next serialization so it is not
  # extremely fast
  time.sleep (0.050)  # 50 msec
  
  
  cm_h.dump ()
        
  # here we are calling our serialize method passing it
  # the iteration number, the topic identifier, and length.
  # The underlying method creates some dummy data, fills
  # up the data structure and serializes it into the buffer
  print ("serialize the message")
  start_time = time.time ()
  buf_h = sz.serialize_h (cm_h)
  end_time = time.time ()
  print ("Serialization took {} secs".format (end_time-start_time))

  # now deserialize and see if it is printing the right thing
  print ("deserialize the message")
  start_time = time.time ()
  cm_h = sz.deserialize_h (buf_h)
  end_time = time.time ()
  print ("Deserialization took {} secs".format (end_time-start_time))

  print ("------ contents of message after deserializing ----------")
  cm_h.dump ()

  # sleep a while before we send the next serialization so it is not
  # extremely fast
  time.sleep (0.050)  # 50 msec
  
  
  cm_r.dump ()
        
  # here we are calling our serialize method passing it
  # the iteration number, the topic identifier, and length.
  # The underlying method creates some dummy data, fills
  # up the data structure and serializes it into the buffer
  print ("serialize the message")
  start_time = time.time ()
  buf_r = sz.serialize_r (cm_r)
  end_time = time.time ()
  print ("Serialization took {} secs".format (end_time-start_time))

  # now deserialize and see if it is printing the right thing
  print ("deserialize the message")
  start_time = time.time ()
  cm_r = sz.deserialize_r (buf_r)
  end_time = time.time ()
  print ("Deserialization took {} secs".format (end_time-start_time))

  print ("------ contents of message after deserializing ----------")
  cm_r.dump ()

  # sleep a while before we send the next serialization so it is not
  # extremely fast
  time.sleep (0.050)  # 50 msec


##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()

    # add optional arguments
    parser.add_argument ("-i", "--iters", type=int, default=10, help="Number of iterations to run (default: 10)")
    parser.add_argument ("-l", "--veclen", type=int, default=20, help="Length of the vector field (default: 20; contents are irrelevant)")
    parser.add_argument ("-n", "--name", default="FlatBuffer Local Demo", help="Name to include in each message")
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
    driver (parsed_args.name, parsed_args.iters, parsed_args.veclen)

#----------------------------------------------
if __name__ == '__main__':
    main ()
