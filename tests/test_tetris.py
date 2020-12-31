import copy
import numpy

from src.CShape import CShape
from src.CBoard import CBoard
from src.NamedTupples import Coord


def test_shape_rotation1():
    shape = CShape()
    shape_layout = copy.deepcopy(shape.layout)

    # Rotate n*4 time - the shape should be the same
    n = 16
    for i in range(n):
        shape.rotate_shape()
        shape.rotate_shape()
        shape.rotate_shape()
        shape.rotate_shape()

    compare = numpy.array(shape_layout) == numpy.array(shape.layout)
    assert (compare.all())


def test_shape_rotation2():
    shape = CShape()
    shape.layout = [[False, False, True], [False, True, True], [False, False, True]]

    ref_rotation = [[True, True, True], [False, True, False], [False, False, False]]

    # Rotate shape
    shape.rotate_shape()

    compare = numpy.array(shape.layout) == numpy.array(ref_rotation)
    assert (compare.all())


def test_shape_movement1():
    shape = CShape(0, Coord(0, 0))
    board = CBoard(Coord(20, 30))

    ref_location = (2, 3)

    # move right 2 times
    shape.move_right(board)
    shape.move_right(board)

    # move down 3 times
    shape.move_down(board)
    shape.move_down(board)
    shape.move_down(board)

    assert (shape.location == ref_location)


def test_shape_movement2():
    shape = CShape(0, Coord(0, 0))
    shape.layout = [[True, True], [True, True]]
    board = CBoard(Coord(20, 30))

    # 29 is last valid y position but shape has "height" tiles 2
    ref_location = (Coord(0, 28))

    # Trying to move out of board.
    for i in range(30):
        shape.move_down(board)

    assert (shape.location == ref_location)


def test_shape_movement3():
    # TODO ovrit
    shape = CShape(0, Coord(0, 0))
    shape.layout = [[True, True], [True, True]]
    board = CBoard(Coord(20, 30))

    board.set_cell(Coord(19, 29), 0)
    board.set_cell(Coord(10, 29), 0)
    board.set_cell(Coord(11, 29), 0)
    board.set_cell(Coord(12, 29), 0)

    ref_location = Coord(19, 27)

    # Trying to move out of board.
    for i in range(30):
        shape.move_down(board)

    assert (shape.location == ref_location)
