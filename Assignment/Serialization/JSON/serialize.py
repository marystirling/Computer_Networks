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

from custom_msg import CustomMessage_Order, CustomMessage_Health, CustomMessage_Response # our custom message in native format

# This is the method we will invoke from our driver program to convert a data structure
# in native format to JSON
def serialize_o (cm):

  # create a JSON representation from the original data structure
  json_buf1 = {
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
    
  # return the underlying jsonified buffer
  return json.dumps (json_buf1)

# This is the method we will invoke from our driver program to convert a data structure
# in native format to JSON
def serialize_h (cm_h):

  # create a JSON representation from the original data structure

    
  json_buf2 = {
    "dispenser": cm_h.dispenser,
    "icemaker": cm_h.icemaker,
    "lightbulb": cm_h.lightbulb,
    "fridge_temp": cm_h.fridge_temp,
    "freezer_temp": cm_h.freezer_temp,
    "sensor_status": cm_h.sensor_status,
    "capacity_full": cm_h.capacity_full
   }
  
  # return the underlying jsonified buffer
  return json.dumps (json_buf2)

def serialize_r (cm_r):

  # create a JSON representation from the original data structure

    
  json_buf3 = {
    "order_response": cm_r.order_response,
    "health_response": cm_r.health_response,
    "bad_response": cm_r.bad_response
   }
  
  # return the underlying jsonified buffer
  return json.dumps (json_buf3)

# deserialize the incoming serialized structure into native data type
def deserialize_o (buf):

  # get the json representation from the incoming buffer
  json_buf = json.loads (buf)

  # now retrieve the native data structure out of it.
  cm = CustomMessage_Order ()
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

  return cm
    
# deserialize the incoming serialized structure into native data type
def deserialize_h (buf):

  # get the json representation from the incoming buffer
  json_buff = json.loads (buf)

  # now retrieve the native data structure out of it.
  cm_h = CustomMessage_Health ()
  cm_h.dispenser = json_buff["dispenser"]
  cm_h.icemaker = json_buff["icemaker"]
  cm_h.lightbulb = json_buff["lightbulb"]
  cm_h.fridge_temp = json_buff["fridge_temp"]
  cm_h.freezer_temp = json_buff["freezer_temp"]
  cm_h.sensor_status = json_buff["sensor_status"]
  cm_h.capacity_full = json_buff["capacity_full"]

  return cm_h

# deserialize the incoming serialized structure into native data type
def deserialize_r (buf):

  # get the json representation from the incoming buffer
  json_buff = json.loads (buf)

  # now retrieve the native data structure out of it.
  cm_r = CustomMessage_Response()
  cm_r.order_response = json_buff["order_response"]
  cm_r.health_response = json_buff["order_response"]
  cm_r.bad_response = json_buff["bad_response"]

  return cm_r
