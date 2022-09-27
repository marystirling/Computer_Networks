#  Author: Aniruddha Gokhale
#  Created: Fall 2022
#  (based on code developed for Distributed Systems course in Fall 2019)
#
#  Purpose: demonstrate serialization of user-defined packet structure
#  using JSON
#
#  Here our packet or message format comprises a sequence number, a timestamp,
#  and a data buffer of several uint32 numbers (whose value is not relevant to us)

import os
import sys

import json # JSON package

from applnlayer.ApplnMessageTypes import GroceryOrderMessage, HealthStatusMessage, ResponseMessage # our custom message in native format
import random

# This is the method we will invoke from our driver program to convert a data structure
# in native format to JSON
def serialize(cm):
        msg_type = cm.type
        if (msg_type == 1):
            json_buf = {
                "type": cm.type,
                "carrot": cm.carrot,
                "tomato": cm.tomato,
                "cucumber": cm.cucumber,
                "corn" : cm.corn,
                "coke": cm.coke,
                "beer": cm.beer,
                "rootbeer": cm.rootbeer,
                "sprite": cm.sprite,
                "gingerale": cm.gingerale,
                "lemonade": cm.lemonade,
                "milk": cm.milk,
                "bread": cm.bread,
                "meat": cm.meat
                }
        elif (msg_type == 2):
            json_buf = {
                "type": cm.type,
                "dispenser": cm.dispenser,
                "icemaker": cm.icemaker,
                "lightbulb": cm.lightbulb,
                "fridge_temp": cm.fridge_temp,
                "freezer_temp": cm.freezer_temp,
                "sensor_status": cm.sensor_status,
                "capacity_full": cm.capacity_full
               }
        elif (msg_type == 3):
            json_buf = {
                "type": cm.type,
                "code": cm.code,
                "contents": cm.contents
               }
        return json.dumps (json_buf)
        
        
def deserialize(buf):
  json_buf = json.loads (buf)
  
  if json_buf["type"] == 1:
      cm = GroceryOrderMessage ()
      cm.type = json_buf["type"]
      cm.tomato = json_buf["tomato"]
      cm.carrot = json_buf["carrot"]
      cm.cucumber = json_buf["cucumber"]
      cm.corn = json_buf["corn"]
      cm.coke = json_buf["coke"]
      cm.beer = json_buf["beer"]
      cm.rootbeer = json_buf["rootbeer"]
      cm.sprite = json_buf["sprite"]
      cm.gingerale = json_buf["gingerale"]
      cm.lemonade = json_buf["lemonade"]
      cm.milk = json_buf["milk"]
      cm.bread = json_buf["bread"]
      cm.meat = json_buf["meat"]

  elif json_buf["type"] == 2:
      cm = HealthStatusMessage
      cm.type = json_buf["type"]
      cm.dispenser = json_buf["dispenser"]
      cm.icemaker = json_buf["icemaker"]
      cm.lightbulb = json_buf["lightbulb"]
      cm.fridge_temp = json_buf["fridge_temp"]
      cm.freezer_temp = json_buf["freezer_temp"]
      cm.sensor_status = json_buf["sensor_status"]
      cm.capacity_full = json_buf["capacity_full"]

  elif json_buf["type"] == 3:
      cm = ResponseMessage()
      cm.type = json_buf["type"]
      cm.code = json_buf["code"]
      cm.contents = json_buf["contents"]

  return cm

