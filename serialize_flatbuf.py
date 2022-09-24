#  Author: Aniruddha Gokhale
#  Created: Fall 2021
#  (based on code developed for Distributed Systems course in Fall 2019)
#  Modified: Fall 2022 (changed packet name to not confuse with pub/sub Messages)
#
#  Purpose: demonstrate serialization of user-defined packet structure
#  using flatbuffers
#
#  Here our packet or message format comprises a sequence number, a timestamp,
#  and a data buffer of several uint32 numbers (whose value is not relevant to us)

import os
import sys

# this is needed to tell python where to find the flatbuffers package
# make sure to change this path to where you have compiled and installed
# flatbuffers.  If the python package is installed in your system wide files
# or virtualenv, then this may not be needed
sys.path.append(os.path.join (os.path.dirname(__file__), '/home/marystirling/Apps/flatbuffers/python'))
import flatbuffers    # this is the flatbuffers package we import
import time   # we need this get current time
import numpy as np  # to use in our vector field

import zmq   # we need this for additional constraints provided by the zmq serialization

from applnlayer.ApplnMessageTypes import GroceryOrderMessage, HealthStatusMessage, ResponseMessage # our custom message in native format

import proto.grocery_proto.Grocery_Order as grocery_order   # this is the generated code by the flatc compiler
import proto.grocery_proto.Veggies as veggies
import proto.grocery_proto.Drinks as drinks
import proto.grocery_proto.Cans as cans
import proto.grocery_proto.Bottles as bottles
import proto.grocery_proto.Contents as contents
import proto.grocery_proto.Milk_Order as milk_order
import proto.grocery_proto.MilkType as milk_type
import proto.grocery_proto.Bread_Order as bread_order
import proto.grocery_proto.BreadType as bread_type
import proto.grocery_proto.Meat_Order as meat_order
import proto.grocery_proto.MeatType as meat_type
import proto.health_proto.Contents as hcontents
import proto.health_proto.Message as health_message
import proto.health_proto.Dispenser_Status as dispenser_status
import proto.health_proto.Status as status
import proto.response_proto.Response_Message as response_message
import proto.response_proto.Code_Type as code_type



message_key = 0

class key:
    #def __init__(self, x):
    #    self.__x = x
    def get_x(self):
        return self.__x
    def set_x(self, x):
        print("did we ever make it here")
        self.__x = x

# This is the method we will invoke from our driver program
# Note that if you have have multiple different message types, we could have
# separate such serialize/deserialize methods, or a single method can check what
# type of message it is and accordingly take actions.
def serialize_o (cm):
    # first obtain the builder object that is used to create an in-memory representation
    # of the serialized object from the custom message
    #global message_key
    
    #message_key = 1
    key_type = key()
    key_type.set_x(1)
    
    
    builder = flatbuffers.Builder (512);
    
    #grocery_order.Start(builder)
    
    
    
    contents.StartMilkVector(builder, len(cm.msg["contents"]["milk"]))
    for item in reversed(cm.msg["contents"]["milk"]):
        milk_order.CreateMilk_Order(builder, item[0], item[1])
    milkVec = builder.EndVector() 
    
    contents.StartBreadVector(builder, len(cm.msg["contents"]["bread"]))
    for item in reversed(cm.msg["contents"]["bread"]):
        bread_order.CreateBread_Order(builder, item[0], item[1])
    breadVec = builder.EndVector()
    
    contents.StartMeatVector(builder, len(cm.msg["contents"]["meat"]))
    for item in reversed(cm.msg["contents"]["meat"]):
        meat_order.CreateMeat_Order(builder, item[0], item[1])
    meatVec = builder.EndVector()
    
    cans.CreateCans(builder, cm.msg["contents"]["drinks"]["cans"]["coke"],
                             cm.msg["contents"]["drinks"]["cans"]["beer"],
                             cm.msg["contents"]["drinks"]["cans"]["rootbeer"])
    
    bottles.CreateBottles(builder, cm.msg["contents"]["drinks"]["bottles"]["sprite"],
                                   cm.msg["contents"]["drinks"]["bottles"]["gingerale"],
                                   cm.msg["contents"]["drinks"]["bottles"]["lemonade"])
    
    contents.Start(builder)
    contents.AddVeggies(builder, veggies.CreateVeggies(builder,
                                    cm.msg["contents"]["veggies"]["tomato"],
                                    cm.msg["contents"]["veggies"]["cucumber"],
                                    cm.msg["contents"]["veggies"]["carrot"],
                                    cm.msg["contents"]["veggies"]["corn"]))

    contents.AddDrinks (builder, drinks.CreateDrinks(builder,
                                    cm.msg["contents"]["drinks"]["cans"]["coke"],
                                    cm.msg["contents"]["drinks"]["cans"]["beer"],
                                    cm.msg["contents"]["drinks"]["cans"]["rootbeer"],
                                    cm.msg["contents"]["drinks"]["bottles"]["sprite"],
                                    cm.msg["contents"]["drinks"]["bottles"]["gingerale"],
                                    cm.msg["contents"]["drinks"]["bottles"]["lemonade"]))
    
    contents.AddMilk(builder, milkVec)
    contents.AddBread(builder, breadVec)
    contents.AddMeat(builder, meatVec)
    
    
    final_contents = contents.End(builder)
    #print(final_contents)

    grocery_order.Start(builder)
    
    grocery_order.AddType(builder, cm.msg["type"])
    grocery_order.AddContents(builder, final_contents)
    
    #grocery_order.End(builder)
    
    serialized_msg = grocery_order.End (builder)  # get the topic of all these fields

    # end the serialization process
    builder.Finish (serialized_msg)

    # get the serialized buffer
    buf = builder.Output ()

    # return this serialized buffer to the caller
    return buf

def serialize_h (cm_h):
    
    global message_key
    message_key = 2
    # first obtain the builder object that is used to create an in-memory representation
    # of the serialized object from the custom message
    builder = flatbuffers.Builder (0);

   
    health_message.Start (builder)  # serialization starts with the "Start" method
    
    if cm_h.msg["contents"]["dispenser"] == 0:
        dispenser = dispenser_status.Dispenser_Status().OPTIMAL
    elif cm_h.msg["contents"]["dispenser"] == 1:
        dispenser = dispenser_status.Dispenser_Status().PARTIAL
    else:
        dispenser = dispenser_status.Dispenser_Status().BLOCKAGE
    
    icemaker = cm_h.msg["contents"]["icemaker"]
    
    if cm_h.msg["contents"]["lightbulb"] == 0:
        lightbulb = status.Status().GOOD
    else:
        lightbulb = status.Status().BAD
    
    fridge_temp = cm_h.msg["contents"]["fridge_temp"]
    freezer_temp = cm_h.msg["contents"]["freezer_temp"]
    
    if cm_h.msg["contents"]["sensor_status"] == 0:
        sensor = status.Status().GOOD
    else:
        sensor = status.Status().BAD
    
    capacity_full = cm_h.msg["contents"]["capacity_full"]
    
    
    final_hcontents = hcontents.CreateContents(builder, dispenser, icemaker, lightbulb, fridge_temp, freezer_temp, sensor, capacity_full)
    
    health_message.AddContents(builder, final_hcontents)
    health_message.AddType(builder, cm_h.msg["type"])
    
    serialized_msg = health_message.End (builder)  # get the topic of all these fields

    # end the serialization process
    builder.Finish (serialized_msg)

    # get the serialized buffer
    buf = builder.Output ()

    # return this serialized buffer to the caller
    return buf

def serialize_r (cm_r):
    
    global message_key
    message_key = 3
    
    # first obtain the builder object that is used to create an in-memory representation
    # of the serialized object from the custom message
    builder = flatbuffers.Builder (0);

   
    
    content_field = builder.CreateString(cm_r.msg["contents"])
    
    response_message.Start (builder)  # serialization starts with the "Start" method
    
    
    if cm_r.msg["code"] == 0:
        code = code_type.Code_Type().OK
    else:
        code = code_type.Code_Type().BAD_REQUEST
    
    
    response_message.AddCode(builder, code)
    #response_message.AddCode(builder, cm_r.msg["code"])
    response_message.AddType(builder, cm_r.msg["type"])
    response_message.AddContents(builder, content_field)
    #response_message.AddContents(builder, cm_r.msg["contents"])
    
    
    serialized_msg = response_message.End (builder)  # get the topic of all these fields

    # end the serialization process
    builder.Finish (serialized_msg)


    # get the serialized buffer
    buf = builder.Output ()
    print("did i finish here")
    # return this serialized buffer to the caller
    return buf

# serialize the custom message to iterable frame objects needed by zmq
def serialize_to_frames (cm):
  """ serialize into an interable format """
  # We had to do it this way because the send_serialized method of zmq under the hood
  # relies on send_multipart, which needs a list or sequence of frames. The easiest way
  # to get an iterable out of the serialized buffer is to enclose it inside []
  print ("serialize custom message to iterable list")
  return [serialize (cm)]
  
  
# deserialize the incoming serialized structure into native data type
def deserialize_o (buf):
    cm = GroceryOrderMessage ()
    
    packet = grocery_order.Grocery_Order.GetRootAs (buf, 0)
    
    cm.type = packet.Type()
    cm.tomato = packet.Contents().Veggies().Tomato()
    cm.cucumber = packet.Contents().Veggies().Cucumber()
    cm.carrot = packet.Contents().Veggies().Carrot()
    cm.corn = packet.Contents().Veggies().Corn()
    
    can = cans.Cans()
    bottle = bottles.Bottles()
    
    cm.coke = packet.Contents().Drinks().Cans(can).Coke()
    cm.beer = packet.Contents().Drinks().Cans(can).Beer()
    cm.rootbeer = packet.Contents().Drinks().Cans(can).Rootbeer()
    cm.sprite = packet.Contents().Drinks().Bottles(bottle).Sprite()
    cm.gingerale = packet.Contents().Drinks().Bottles(bottle).Gingerale()
    cm.lemonade = packet.Contents().Drinks().Bottles(bottle).Lemonade()
    
    cm.milk = [(packet.Contents().Milk(j).Type(), packet.Contents().Milk(j).Quantity()) for j in range (packet.Contents().MilkLength ())]
    cm.bread = [(packet.Contents().Bread(j).Type(), packet.Contents().Bread(j).Quantity()) for j in range (packet.Contents().BreadLength ())]
    cm.meat = [(packet.Contents().Meat(j).Type(), packet.Contents().Meat(j).Quantity()) for j in range (packet.Contents().MeatLength ())]


    return cm

def deserialize_h (buf):
    cm_h = HealthStatusMessage ()
    
    packet = health_message.Message.GetRootAs (buf, 0)

  
    cm_h.type = packet.Type()
    cm_h.dispenser = packet.Contents().Dispenser()
    cm_h.icemaker = packet.Contents().Icemaker()
    cm_h.lightbulb = packet.Contents().Lightbulb()
    cm_h.fridge_temp = packet.Contents().FridgeTemp()
    cm_h.freezer_temp = packet.Contents().FreezerTemp()
    cm_h.sensor_status = packet.Contents().SensorStatus()
    cm_h.capacity_full = packet.Contents().CapacityFull()
    
    return cm_h
    
def deserialize_r (buf):
    cm_r = ResponseMessage ()
    
    packet = response_message.Response_Message.GetRootAs (buf, 0)

    cm_r.type = packet.Type()
    cm_r.code = packet.Code()
    cm_r.contents = packet.Contents()
    
    return cm_r
    
    
# deserialize from frames
def deserialize_from_frames (recvd_seq):
  """ This is invoked on list of frames by zmq """

  # For this sample code, since we send only one frame, hopefully what
  # comes out is also a single frame. If not some additional complexity will
  # need to be added.
  assert (len (recvd_seq) == 1)
  #print ("type of each elem of received seq is {}".format (type (recvd_seq[i])))
  print ("received data over the wire = {}".format (recvd_seq[0]))
  cm = deserialize (recvd_seq[0])  # hand it to our deserialize method

  # assuming only one frame in the received sequence, we just send this deserialized
  # custom message
  return cm


