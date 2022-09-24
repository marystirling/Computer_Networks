# automatically generated by the FlatBuffers compiler, do not modify

# namespace: CustomAppProto2

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Veggies(object):
    __slots__ = ['_tab']

    @classmethod
    def SizeOf(cls):
        return 16

    # Veggies
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Veggies
    def Tomato(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # Veggies
    def Cucumber(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))
    # Veggies
    def Carrot(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(8))
    # Veggies
    def Corn(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(12))

def CreateVeggies(builder, tomato, cucumber, carrot, corn):
    builder.Prep(4, 16)
    builder.PrependFloat32(corn)
    builder.PrependFloat32(carrot)
    builder.PrependFloat32(cucumber)
    builder.PrependFloat32(tomato)
    return builder.Offset()