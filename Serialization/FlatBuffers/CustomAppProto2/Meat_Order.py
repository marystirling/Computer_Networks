# automatically generated by the FlatBuffers compiler, do not modify

# namespace: CustomAppProto2

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Meat_Order(object):
    __slots__ = ['_tab']

    @classmethod
    def SizeOf(cls):
        return 8

    # Meat_Order
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Meat_Order
    def Type(self): return self._tab.Get(flatbuffers.number_types.Int32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # Meat_Order
    def Quantity(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))

def CreateMeat_Order(builder, type, quantity):
    builder.Prep(4, 8)
    builder.PrependFloat32(quantity)
    builder.PrependInt32(type)
    return builder.Offset()