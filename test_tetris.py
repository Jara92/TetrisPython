import copy
import numpy
from shutil import rmtree
from src.Shape import Shape
from src.Board import Board
from src.NamedTupples import Coord
from src.ScoreManager import ScoreManager


def test_board_set_cell():
    board = Board(Coord(10, 20))

    # Check every cell
    for i in range(10):
        for j in range(20):
            # If x and y coord is equal set color to 1 - make cell filled.
            if i == j:
                board.set_cell(Coord(i, j), 1)
                assert (board.cell_is_free(Coord(i, j)) is False)

            # In other cases cell should be free.
            else:
                assert (board.cell_is_free(Coord(i, j)) is True)


def test_shape_store():
    shape = Shape(Coord(0, 0))

    for layout in Shape.SHAPES:
        board = Board(Coord(15, 20))
        shape.layout = layout

        # Save shape in the board.
        shape.store(board)

        # Check the board
        for i in range(layout.count(0)):
            for j in range(layout.count(1)):
                # If given tile at (i, j) is active.
                if layout[i][j] is True:
                    # Tile at shape.location + (i, j) must not be free.
                    assert (board.cell_is_free(Coord(shape.location.x + i, shape.location.y + j)) is False)
                else:
                    # Other tiles has to be free.
                    assert (board.cell_is_free(Coord(shape.location.x + i, shape.location.y + j)) is True)


def test_shape_collision1():
    """
    Shape collision - no collission.
    :return:
    """
    shape = Shape(Coord(5, 2))
    board = Board(Coord(15, 20))

    # Check every possible layout.
    for layout in shape.SHAPES:
        shape.layout = layout
        assert (shape.check_collisions(board) == 0)


def test_shape_collision2():
    """
    Shape collision - out of board.
    :return:
    """

    shape_a = Shape(0, Coord(-4, 2))
    shape_b = Shape(1, Coord(21, 5))
    board = Board(Coord(15, 20))

    # Check every possible layout.
    for layout in shape_a.SHAPES:
        shape_a.layout = layout
        shape_b.layout = layout

        assert (shape_a.check_collisions(board) == 1)
        assert (shape_b.check_collisions(board) == 1)


def test_shape_collision3():
    """
    Shape collision with filled cells in the board.
    :return:
    """
    shape = Shape(0, Coord(5, 1))
    board = Board(Coord(15, 20))

    # Check every possible layout.
    for layout in shape.SHAPES:
        shape.layout = layout

        # No collision now
        assert (shape.check_collisions(board) == 0)

        # Set one single cell in board as filled and check if shape is in collision.
        for tile in shape.get_global_tiles():
            board.set_cell(tile, 1)

            # The shape should be colliding with the tile.
            assert (shape.check_collisions(board) == 2)

            board.set_cell(tile, -1)


def test_shape_rotation1():
    shape = Shape()
    shape.layout = [[False, False, True], [False, True, True], [False, False, True]]

    shape_layout = copy.deepcopy(shape.layout)

    board = Board(Coord(20, 30))

    # Rotate n*4 time - the shape should be the same
    for i in range(17):
        assert (shape.rotate_shape(board) is True)
        assert (shape.rotate_shape(board) is True)
        assert (shape.rotate_shape(board) is True)
        assert (shape.rotate_shape(board) is True)

    compare = numpy.array(shape_layout) == numpy.array(shape.layout)
    assert (compare.all())


def test_shape_rotation2():
    shape = Shape(0, Coord(1, 5))
    shape.layout = [[False, False, True], [False, True, True], [False, False, True]]

    # All possible rotations
    shape_rotations = [[[True, True, True], [False, True, False], [False, False, False]],
                       [[True, False, False], [True, True, False], [True, False, False]],
                       [[False, False, False], [False, True, False], [True, True, True]],
                       [[False, False, True], [False, True, True], [False, False, True]]
                       ]

    board = Board(Coord(20, 30))

    # Test all possible roations.
    for rot in shape_rotations:
        assert (shape.rotate_shape(board) is True)

        compare = numpy.array(rot) == numpy.array(shape.layout)
        assert (compare.all())


def test_shape_rotation3():
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


def test_shape_rotation4():
    """
    Shape rotation collision test.
    :return:
    """
    shape = Shape(0, Coord(5, 1))
    shape.layout = [[False, False, True], [False, True, True], [False, False, True]]

    # Rotation should not be changed.
    ref_rotation = shape.layout.copy()

    board = Board(Coord(20, 30))
    board.set_cell(Coord(6, 2), 1)

    # Rotate shape
    assert (shape.rotate_shape(board) is False)

    compare = numpy.array(shape.layout) == numpy.array(ref_rotation)
    assert (compare.all())


def test_shape_rotation5():
    """
    Test every shape rotation.
    :return:
    """
    shape = Shape()
    board = Board(Coord(20, 30))
    n = 17

    for layout in Shape.SHAPES:
        shape.layout = layout

        shape_layout = copy.deepcopy(shape.layout)

        # Rotate n*4 time - the shape should be the same
        for i in range(n):
            assert (shape.rotate_shape(board) is True)
            assert (shape.rotate_shape(board) is True)
            assert (shape.rotate_shape(board) is True)
            assert (shape.rotate_shape(board) is True)

        compare = numpy.array(shape_layout) == numpy.array(shape.layout)
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
    assert (shape.move_right(board) is True)
    assert (shape.move_right(board) is True)
    assert (shape.move_right(board) is True)

    # move left 1 time
    assert (shape.move_left(board) is True)

    # move down 3 times
    assert (shape.move_down(board) is True)
    assert (shape.move_down(board) is True)
    assert (shape.move_down(board) is True)

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
