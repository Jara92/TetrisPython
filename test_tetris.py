import copy
import numpy

from CShape import CShape
from CBoard import CBoard


def test_shape_rotation1():
    shape = CShape()
    shape_layout = copy.deepcopy(shape.layout)

    # Rotate 4 time - the shape should be the same
    shape.rotate_shape()
    shape.rotate_shape()
    shape.rotate_shape()
    shape.rotate_shape()

    compare = numpy.array(shape_layout) == numpy.array(shape.layout)
    assert(compare.all())
