# CS4283/5283: Computer Networks
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
#
# Purpose: Define a native representation of a custom message format
#          that will then undergo serialization/deserialization
#

from typing import List
from dataclasses import dataclass
from enum import IntEnum

class Milk_Type(IntEnum):
  one_percent = 1
  two_percent = 2
  fat_free = 3
  whole = 4
  almond = 5
  cashew = 6
  oat = 7

class Bread_Type(IntEnum):
  whole_wheat = 1
  white = 2
  pumpernickel = 3
  rye = 4
  sourdough = 5
  
class Meat_Type(IntEnum):
  ground_beef = 1
  turkey = 2
  ham = 3
  chicken = 4
  steak = 5

class Dispenser_Status(IntEnum):
  OPTIMAL = 1
  PARTIAL = 2
  BLOCKAGE = 3

class Status(IntEnum):
  GOOD = 1
  BAD = 2

class Code_Type(IntEnum):
  OK = 1
  BAD_REQUEST = 2
  

@dataclass
class CustomMessage_Order:
  """ Our message in native representation"""
  

  def __init__ (self):
    self.msg = {
        #"type": Order,
        "contents": {
            "veggies": {
                "tomato": float,
                "cucumber": float,
                "carrot": int,
                "corn": int
            },
            "drinks":{
                "cans":{
                    "coke": int,
                    "beer": int,
                    "rootbeer":int,
                },
                "bottles":{
                    "sprite": int,
                    "gingerale":int,
                    "lemonade":int
                }
            },
            "milk": [],
            "bread": [],
            "meat": []
        }
        
    }
  
  def dump (self):
    pass
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
      print(f"   {Milk_Type(self.milk[i][0]).name}: {self.milk[i][1]}")
    print (" bread:")
    for i in range(3):
      print(f"   {Bread_Type(self.bread[i][0]).name}: {self.bread[i][1]}") 
    print (" meat:")
    for i in range(3):
      print(f"   {Meat_Type(self.meat[i][0]).name}: {self.meat[i][1]}") 
 
@dataclass
class CustomMessage_Health:
  """ Our message in native representation"""
  
  
  def __init__ (self):
    self.msg = {
        #"type": health,
        "contents": {
            "dispenser": str,
            "icemaker": int,
            "lightbulb": str,
            "fridge_temp": int,
            "freezer_temp": int,
            "sensor_status": str,
            "capacity_full": int
        }
    }
    
  
  def dump (self):
    print ("Dumping contents of HEALTH")
    print (" dispenser: {}".format(Dispenser_Status(self.dispenser).name))
    print (" icemaker: {}".format(self.icemaker))
    print (" lightbulb: {}".format(Status(self.lightbulb).name))
    print (" fridge_temp: {}".format(self.fridge_temp))
    print (" freezer_temp: {}".format(self.freezer_temp))
    print (" sensor_status: {}".format(Status(self.sensor_status).name))
    print (" capacity_full: {}".format(self.capacity_full))

@dataclass
class CustomMessage_Response:
  """ Our message in native representation"""

  
  
  def __init__ (self):
      self.msg = {
        #"type": response,
        "code": int,
        "contents": str
        }
  
  def dump (self):
    print ("Dumping contents of RESPONSE")
    print(" code: {}".format(Code_Type(self.code).name))

        
    #print (" order_response: {}".format(self.order_response))
    #print (" health_response: {}".format(self.health_response))
    #print (" bad_response: {}".format(self.bad_response))
