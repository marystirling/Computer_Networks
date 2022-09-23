# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the definition of supported messages
#

# import the needed packages
import sys
from enum import IntEnum  # for enumerated types
from typing import List
# @TODO import whatever more packages are needed

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert (0, "../")


class Milk_Type(IntEnum):
  one_percent = 0
  two_percent = 1
  fat_free = 2
  whole = 3
  almond = 4
  cashew = 5
  oat = 6

class Bread_Type(IntEnum):
  whole_wheat = 0
  white = 1
  pumpernickel = 2
  rye = 3
  sourdough = 4
  
class Meat_Type(IntEnum):
  ground_beef = 0
  turkey = 1
  ham = 2
  chicken = 3
  steak = 4

class Dispenser_Status(IntEnum):
  OPTIMAL = 0
  PARTIAL = 1
  BLOCKAGE = 2

class Status(IntEnum):
  GOOD = 0
  BAD = 1

class Code_Type(IntEnum):
  OK = 0
  BAD_REQUEST = 1
  
############################################
#  Enumeration for Message Types
############################################
class MessageTypes (IntEnum):
  # One can extend this as needed. For now only these two
  UNKNOWN = -1
  GROCERY = 1
  HEALTH = 2
  RESPONSE = 3

############################################
#  Grocery Order Message
############################################
class GroceryOrderMessage:
  '''Grocery Order Message'''
  def __init__ (self):
    self.msg = {
        #"type": MessageTypes.GROCERY.name,
        "type": int,
        "contents": {
            "veggies": {
                "tomato": float,
                "cucumber": float,
                "carrot": float,
                "corn": float
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


  def __str__ (self):
      print ("Dumping contents of ORDER")
      print (" type: {}".format(MessageTypes(self.type).name))
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
      return "grocery order"

    
############################################
#  Health Status Message
############################################
class HealthStatusMessage:
  '''Health Status Message'''
  def __init__ (self):
      self.msg = {
          "type": int,
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


  def __str__ (self):
      print ("Dumping contents of HEALTH")
      print (" type: {}".format(MessageTypes(self.type).name))
      print (" dispenser: {}".format(Dispenser_Status(self.dispenser).name))
      print (" icemaker: {}".format(self.icemaker))
      print (" lightbulb: {}".format(Status(self.lightbulb).name))
      print (" fridge_temp: {}".format(self.fridge_temp))
      print (" freezer_temp: {}".format(self.freezer_temp))
      print (" sensor_status: {}".format(Status(self.sensor_status).name))
      print (" capacity_full: {}".format(self.capacity_full))
      return "health status"


    
############################################
#  Response Message
############################################
class ResponseMessage:
  '''Response Message'''
  def __init__ (self):
      self.msg = {
          "type": int,
          "code": int,
          "contents": str
        }


  def __str__ (self):
      print ("Dumping contents of RESPONSE")
      #print(" type: {}".format(MessageTypes(self.type).name))
      #print(" code: {}".format(Code_Type(self.code).name))
      print(" contents: {}".format(self.contents))
      return "response message"
    



