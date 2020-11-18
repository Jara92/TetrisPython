from enum import Enum
import copy
import numpy
import pygame
from random import randint
from typing import Tuple
from CBoard import CBoard

from NamedTupples import Coord


class EShapeState(Enum):
    state_idling = 0  # Waiting in queue to be spawned
    state_spawning = 1  # Shape is spawning in the board - we are ignoring out of range movement error
    state_moving = 2  # main state. Shape is moving down in the board.
    state_collision = 3  # shape is colliding in the board


# Rotatable shape in game.
class CShape:
    """
    Shape layout defined by columsn.
    """
    __shapes = [[[False, False, True], [False, True, True], [False, False, True]],
                [[True, True], [True, True]],
                [[False, False, False, False], [False, False, False, False], [True, True, True, True],
                 [False, False, False, False]],
                [[True, True, True], [False, False, True], [False, False, False]],
                [[False, False, False], [False, False, True], [True, True, True]]
                ]
    __shape_state = None
    layout = None
    location = Coord(5, 0)
    color = None

    def __init__(self, color: int = 0, spawn_location: Coord = Coord(5, 0)):
        self.color = color
        self.location = spawn_location

        # We need some random layout for this shape.
        # Deep copy needed because we will rotate the shape.
        self.layout = copy.deepcopy(CShape.__random_shape())

    def store(self, board: CBoard):
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

    def rotate_shape(self, board):
        """
        Rotate shape by 90 degrees left. We need to verify that we are not colliding in @board.
        @param board Game board.
        """

        # Rotate 90° right
        old_rotation = copy.deepcopy(self.layout)
        self.layout = numpy.rot90(numpy.array(self.layout, bool), 1, (0, 1))

        # Check new location collisions.
        if self.check_collisions(board) is False:
            # Reset location and return False, because the movement was not successful.
            self.layout = old_rotation
            return False

        return True

    def print_shape(self):
        """
        Print shape layout.
        """

        N = len(self.layout[0])
        for i in range(N):
            print(self.layout[i])

    def move_down(self, board: CBoard):
        """
        Move shape down.
        @param board Game board.
        :return: True - success; False - we are colliding with something.
        """

        movement_direction = Coord(0, 1)

        return self.__move(board, movement_direction)

    def move_left(self, board: CBoard):
        """
        Move shape left.
        @param board Game board.
        :return: True - success; False - we are colliding with something.
        """

        movement_direction = Coord(-1, 0)

        return self.__move(board, movement_direction)

    def move_right(self, board: CBoard):
        """
        Move shape right.
        @param board Game board.
        :return: True - success; False - we are colliding with something.
        """

        movement_direction = Coord(1, 0)

        return self.__move(board, movement_direction)

    def __move(self, board: CBoard, direction: Coord):
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
        if self.check_collisions(board) is False:
            # Reset location and return False, because the movement was not successful.
            self.location = old_location
            return False

        return True

    def check_collisions(self, board: CBoard):
        """
        Check shape collisions.
        :param board: Board to be used.
        :return: True - Shape is colliding with board
        """
        for tile in self.__get_tiles():
            # Get tile global coords.
            tile_coords = Coord(self.location.x + tile.x, self.location.y + tile.y)

            # If tile is active in current layout and cell is not free in board
            if self.layout[tile.x][tile.y] and not board.cell_is_free(tile_coords):
                return False

        # Every tile is in free cell so the movement is successful.
        return True

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
        random_index = randint(0, len(CShape.__shapes) - 1)

        return CShape.__shapes[random_index]
