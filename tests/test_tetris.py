import copy
import numpy
import sys, os
from shutil import rmtree

# This stuff finds src module
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path + '/../')

from src.Shape import Shape
from src.Board import Board
from src.NamedTupples import Coord
from src.ScoreManager import ScoreManager


def test_shape_rotation1():
    shape = Shape()
    shape_layout = copy.deepcopy(shape.layout)

    board = Board(Coord(20, 30))

    # Rotate n*4 time - the shape should be the same
    n = 16
    for i in range(n):
        shape.rotate_shape(board)
        shape.rotate_shape(board)
        shape.rotate_shape(board)
        shape.rotate_shape(board)

    compare = numpy.array(shape_layout) == numpy.array(shape.layout)
    assert (compare.all())


def test_shape_rotation2():
    """
    Shape rotation algoritm test.
    :return:
    """
    shape = Shape()
    shape.layout = [[False, False, True], [False, True, True], [False, False, True]]

    ref_rotation = [[True, True, True], [False, True, False], [False, False, False]]

    board = Board(Coord(20, 30))

    # Rotate shape
    shape.rotate_shape(board)

    compare = numpy.array(shape.layout) == numpy.array(ref_rotation)
    assert (compare.all())


def test_shape_rotation3():
    """
    Shape rotation collision test.
    :return:
    """
    shape = Shape(0, Coord(5, 1))
    shape.layout = [[False, False, True], [False, True, True], [False, False, True]]
    shape.print_shape()

    # Rotation should not be changed.
    ref_rotation = shape.layout.copy()

    board = Board(Coord(20, 30))

    board.set_cell(Coord(6, 2), 1)

    # Rotate shape
    shape.rotate_shape(board)
    shape.print_shape()

    compare = numpy.array(shape.layout) == numpy.array(ref_rotation)
    assert (compare.all())


def test_shape_movement1():
    """
    Shape basic movement.
    :return:
    """
    shape = Shape(0, Coord(0, 0))
    board = Board(Coord(20, 30))

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
    """
    Shape moves correctly when there are no filled cells.
    :return:
    """
    shape = Shape(0, Coord(0, 0))
    shape.layout = [[True, True], [True, True]]
    board = Board(Coord(20, 30))

    # 29 is last valid y position but shape has "height" tiles 2
    ref_location = (Coord(0, 28))

    # Trying to move out of board.
    for i in range(30):
        shape.move_down(board)

    assert (shape.location == ref_location)


def test_shape_movement3():
    """
    Shape cannot move to filled cells.
    :return:
    """
    shape = Shape(0, Coord(0, 0))
    shape.layout = [[True, True], [True, True]]
    board = Board(Coord(20, 30))

    # Set filled cells.
    board.set_cell(Coord(0, 29), 0)
    board.set_cell(Coord(1, 29), 0)
    board.set_cell(Coord(2, 29), 0)
    board.set_cell(Coord(3, 29), 0)

    ref_location = Coord(0, 27)

    # Trying to move out of board.
    for i in range(30):
        shape.move_down(board)

    assert (shape.location == ref_location)


def test_shape_bad_spawn():
    """
    Spawn location is filled so new shape cannot move or rotate.
    :return:
    """
    shape = Shape(0, Coord(5, 0))
    shape.layout = [[False, False, False, False], [False, False, False, False], [True, True, True, True],
                    [False, False, False, False]]
    board = Board(Coord(20, 30))

    # Set filled cells.
    for i in range(3):
        board.set_cell(Coord(2, i), 0)
        board.set_cell(Coord(3, i), 0)
        board.set_cell(Coord(4, i), 0)
        board.set_cell(Coord(5, i), 0)
        board.set_cell(Coord(6, i), 0)
        board.set_cell(Coord(7, i), 0)

    ref_location = Coord(5, 0)

    # Trying to move out of board.
    for i in range(30):
        shape.move_down(board)
        shape.rotate_shape(board)

    assert (shape.location == ref_location)
    assert (shape.layout == [[False, False, False, False], [False, False, False, False], [True, True, True, True],
                             [False, False, False, False]])


def test_score_manager_load():
    """
    Load data form file.
    :return:
    """
    test_data_directory = "test_data"
    assert (ScoreManager.init_manager(test_data_directory))
    value = ScoreManager.get_score()

    assert (value >= 0)

    # Clear testing mess
    rmtree(test_data_directory)


def test_score_manager_save():
    """
    Save new data to file.
    :return:
    """
    test_data_directory = "test_data"
    assert (ScoreManager.init_manager(test_data_directory))

    new_value = 954
    ScoreManager.save_score(new_value)

    assert (ScoreManager.get_score() == new_value)

    # Clear testing mess
    rmtree(test_data_directory)
