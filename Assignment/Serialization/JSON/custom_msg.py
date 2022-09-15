# CS4283/5283: Computer Networks
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
#
# Purpose: Define a native representation of a custom message format
#          that will then undergo serialization/deserialization
#

from typing import List
from dataclasses import dataclass

@dataclass
class CustomMessage_Order:
  """ Our message in native representation"""
  #veggies: {"tomato": float, "carrot": float}
  veggies: dict
  tomato: float
  cucumber: float
  carrot: float
  corn: float
  coke: int
  beer: int
  rootbeer: int
  sprite: int
  gingerale: int
  lemonade: int
  milk: List[tuple]
  bread: List[tuple]
  meat: List[tuple]
  
  
  seq_num: int  # a sequence number
  ts: float    # timestamp
  name: str    # some name
  vec: List[int] # some vector of unsigned ints
  quantity_i: int
  quantity_f: float

  def __init__ (self):
    pass
  
  def dump (self):
    print ("Dumping contents of ORDER")
    print (" veggies: ")
    print ("   tomato: {}".format (self.tomato))
    print ("   cucumber: {}".format (self.cucumber))
    print ("   carrot: {}".format (self.carrot))
    print ("   corn: {}".format (self.corn))
    print (" drinks:")
    print ("   cans:")
    print ("     coke: {}".format(self.coke))
    print ("     beer: {}".format(self.beer))
    print ("     rootbear: {}".format(self.rootbeer))
    print ("   bottles:")
    print ("     sprite: {}".format(self.sprite))
    print ("     gingerale: {}".format(self.gingerale))
    print ("     lemonade: {}".format(self.lemonade))
    print (" milk:")
    for i in range(3):
    	print(f"     {self.milk[i][0]}: {self.milk[i][1]}") 
    print (" bread:")
    for i in range(3):
    	print(f"     {self.bread[i][0]}: {self.bread[i][1]}") 
    print (" meat:")
    for i in range(3):
    	print(f"     {self.meat[i][0]}: {self.meat[i][1]}") 
 
@dataclass
class CustomMessage_Health:
  """ Our message in native representation"""
  dispenser: int
  icemaker: int
  lightbulb: int
  fridge_temp: int
  freezer_temp: int
  sensor_status: int
  capacity_full: int
  
  
  def __init__ (self):
    pass
  
  def dump (self):
    print ("Dumping contents of HEALTH")
    print (" dispenser: {}".format(self.dispenser))
    print (" icemaker: {}".format(self.icemaker))
    print (" lightbulb: {}".format(self.lightbulb))
    print (" fridge_temp: {}".format(self.fridge_temp))
    print (" freezer_temp: {}".format(self.freezer_temp))
    print (" sensor_status: {}".format(self.sensor_status))
    print (" capacity_full: {}".format(self.capacity_full))

@dataclass
class CustomMessage_Response:
  """ Our message in native representation"""
  order_response: int
  health_response: int
  bad_response: int
  
  
  def __init__ (self):
    pass
  
  def dump (self):
    print ("Dumping contents of RESPONSE")
    if (self.order_response == "OK"):
    	print("Order Placed")
    elif(self.order_response == "BAD_REQUEST"):
    	print("Bad Request")
    if (self.health_response == "OK"):
    	print("You are Healthy")
    elif(self.health_response == "BAD_REQUEST"):
    	print("Bad Request")
    if (self.bad_response == "BAD_REQUEST"):
    	print("Bad Request")
    
    #print (" order_response: {}".format(self.order_response))
    #print (" health_response: {}".format(self.health_response))
    #print (" bad_response: {}".format(self.bad_response))
