# automatically generated by the FlatBuffers compiler, do not modify

# namespace: grocery_proto

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Grocery_Order(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Grocery_Order()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsGrocery_Order(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Grocery_Order
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Grocery_Order
    def Contents(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from proto.grocery_proto.Contents import Contents
            obj = Contents()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def Grocery_OrderStart(builder): builder.StartObject(1)
def Start(builder):
    return Grocery_OrderStart(builder)
def Grocery_OrderAddContents(builder, contents): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(contents), 0)
def AddContents(builder, contents):
    return Grocery_OrderAddContents(builder, contents)
def Grocery_OrderEnd(builder): return builder.EndObject()
def End(builder):
    return Grocery_OrderEnd(builder)