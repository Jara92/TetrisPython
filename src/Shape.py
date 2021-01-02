from enum import Enum
import copy
import numpy
import pygame
from random import randint
from src.Board import Board

from src.NamedTupples import Coord


# Rotatable shape in game.
class Shape:
    """
    Shape layout defined by columns.
    """
    SHAPES = [[[False, False, True], [False, True, True], [False, False, True]],
              [[True, True], [True, True]],
              [[False, False, False, False], [False, False, False, False], [True, True, True, True],
               [False, False, False, False]],
              [[False, False, False], [True, True, True], [False, False, True]],
              [[False, False, True], [True, True, True], [False, False, False]],
              [[False, False, True], [False, True, True], [False, True, False]],
              [[False, True, False], [False, True, True], [False, False, True]]
              ]
    layout = None
    location = Coord(5, 0)
    color = None

    def __init__(self, color: int = 0, spawn_location: Coord = Coord(5, 0)):
        self.color = color
        self.location = spawn_location

        # We need some random layout for this shape.
        # Deep copy needed because we will rotate the shape.
        self.layout = copy.deepcopy(Shape.__random_shape())

    def store(self, board: Board):
        """
        Store this shape in given board.
        :param board: Board to be used
        :return:
        """
        for tile in self.__get_tiles():
            # Get tile global coords.
            tile_coords = Coord(self.location.x + tile.x, self.location.y + tile.y)

            # If tile is active in current layout and cell is not free in board
            board.set_cell(tile_coords, self.color)

    def rotate_shape(self, board: Board = None):
        """
        Rotate shape by 90 degrees left. We need to verify that we are not colliding in @board.
        @param board Game board.
        """

        # Rotate 90° right
        old_rotation = copy.deepcopy(self.layout)
        old_location = self.location
        self.layout = numpy.rot90(numpy.array(self.layout, bool), 1, (0, 1))

        # All possible paddings
        padding = [Coord(0, 0), Coord(1, 0), Coord(-1, 0), Coord(2, 0), Coord(-2, 0)]

        # Try every padding until there is some valid.
        for padd in padding:
            # Check new location collisions.
            self.location = Coord(old_location.x + padd.x, old_location.y + padd.y)

            # Get collision state
            collision = self.check_collisions(board)

            # No collision - rotation success
            if collision == 0:
                return True

            # Shape is out of board - continue in cycle
            if collision == 1:
                continue

            # Collision with filled cell - no way to rotate
            if collision == 2:
                break

        # There si collision for every padding so we will restore the shape.
        self.location = old_location
        self.layout = old_rotation

        return False

    def print_shape(self):
        """
        Print shape layout.
        """

        for i in range(len(self.layout)):
            for j in range(len(self.layout)):
                print(str(self.layout[j][i]), end=" ")
            print("")

    def move_down(self, board: Board):
        """
        Move shape down.
        @param board Game board.
        :return: True - success; False - we are colliding with something.
        """

        movement_direction = Coord(0, 1)

        return self.__move(board, movement_direction)

    def move_left(self, board: Board):
        """
        Move shape left.
        @param board Game board.
        :return: True - success; False - we are colliding with something.
        """

        movement_direction = Coord(-1, 0)

        return self.__move(board, movement_direction)

    def move_right(self, board: Board):
        """
        Move shape right.
        @param board Game board.
        :return: True - success; False - we are colliding with something.
        """

        movement_direction = Coord(1, 0)

        return self.__move(board, movement_direction)

    def __move(self, board: Board, direction: Coord):
        """
        Move the shape. We need to verify that we are not colliding in @board.
        :param board: Board Game board.
        :param direction: Direction to be Moved.
        :return: True - success; False - we are colliding with something.
        """

        # Save old location before making the move.
        old_location = self.location

        # Make the move.
        self.location = Coord(self.location.x + direction.x, self.location.y + direction.y)

        # Check new location collisions.
        if self.check_collisions(board) != 0:
            # Reset location and return False, because the movement was not successful.
            self.location = old_location
            return False

        return True

    def check_collisions(self, board: Board):
        """
        Check shape collisions.
        :param board: Board to be used.
        :return: 0 - No collisions; 1 - Shape is out of board; 2 - Shape is in collision.
        """

        for tile in self.__get_tiles():
            # Get tile global coords.
            tile_coords = Coord(self.location.x + tile.x, self.location.y + tile.y)

            if self.layout[tile.x][tile.y] and board.cell_is_out_of_board(tile_coords):
                return 1

            # If tile is active in current layout and cell is not free in board
            if self.layout[tile.x][tile.y] and not board.cell_is_free(tile_coords):
                return 2

        # Every tile is in free cell so the movement is successful.
        return 0

    def __get_tiles(self):
        """
        Return all active tiles in this shape (returns local coordinates).
        :return: All active tiles.
        """
        for i in range(len(self.layout)):
            for j in range(len(self.layout)):
                if self.layout[i][j]:
                    yield Coord(i, j)

    def get_global_tiles(self):
        """
        Return all active tiles in this shape (returns global coordinates).
        :return: All active tiles.
        """
        for tile in self.__get_tiles():
            yield Coord(tile.x + self.location.x, tile.y + self.location.y)

    def draw(self, surface: pygame.Surface, tile_texture: pygame.image, tile_size: int):
        """
        Draw shape in given surface.
        :param surface: Surface to be used.
        :param tile_texture: Single tile texture to be used.
        :param tile_size: Single tile texture size.
        :return:
        """
        for tile in self.__get_tiles():
            surface.blit(tile_texture, (
                (self.location.x + tile.x) * tile_size, (self.location.y + tile.y) * tile_size))

    @staticmethod
    def __random_shape():
        """
        Return random shape in __shapes.
        @:returns Random shape array.
        """

        # Generate random index in shapes list - We want new random shape.
        random_index = randint(0, len(Shape.SHAPES) - 1)

        return Shape.SHAPES[random_index]
