import copy
import numpy
import pygame
# import pyglet
from random import randint

from typing import Tuple

from CBoard import CBoard

from NamedTupples import Coord


# Rotatable shape in game.
class CShape:
    __shapes = [[[False, False, False], [False, True, False], [True, True, True]],
                [[True, True], [True, True]]]
    """
    Colors description.
    white|orange|red|green|blue|gold
    """
    __colors = [(255, 255, 255), (255, 128, 0), (178, 34, 34), (50, 205, 50), (0, 191, 255), (255, 215, 0)]
    shape_layout = None
    location = (5, 0)
    tile_sprite = None
    tile_color = None

    def __init__(self, tile_sprite: pygame.image, spawn_location=(5, 0)):
        # TODO add tile_sprite type
        self.tile_sprite = tile_sprite.copy()
        # self.tile_sprite.color =
        self.tile_sprite.fill(CShape.__random_color(), None, pygame.BLEND_MULT)
        self.location = spawn_location

        # We need some random layout for this shape.
        # Deep copy needed because we will rotate the shape.
        self.shape_layout = copy.deepcopy(CShape.__random_shape())

        # self.print_shape()

    #        self.rotate_shape()
    # self.print_shape()

    @staticmethod
    def __random_shape():
        """
        Return random shape in __shapes.
        @:returns Random shape array.
        """

        # Generate random index in shapes list - We want new random shape.
        random_index = randint(0, len(CShape.__shapes) - 1)

        return CShape.__shapes[random_index]

    @staticmethod
    def __random_color():
        """
        Return random color in __colors.
        @:returns Random color.
        """

        # Generate random index in color list - We want new random color.
        random_index = randint(0, len(CShape.__colors) - 1)

        return CShape.__colors[random_index]

    def rotate_shape(self, board):
        """
        Rotate shape by 90 degrees left. We need to verify that we are not colliding in @board.
        @param board Game board.
        """

        old_rotation = copy.deepcopy(self.shape_layout)
        self.shape_layout = numpy.rot90(numpy.array(self.shape_layout, bool), 1, (0, 1))

        # Check new location collisions.
        if self.check_collisions(board) is False:
            # Reset location and return False, because the movement was not successful.
            self.shape_layout = old_rotation
            return False

        return True

    def print_shape(self):
        """
        Print shape layout.
        """

        N = len(self.shape_layout[0])
        for i in range(N):
            print(self.shape_layout[i])

    def move_down(self, board: CBoard):
        """
        Move shape down.
        @param board Game board.
        :return: True - success; False - we are colliding with something.
        """

        movement_direction = (0, 1)

        return self.move(board, movement_direction)

    def move_left(self, board: CBoard):
        """
        Move shape left.
        @param board Game board.
        :return: True - success; False - we are colliding with something.
        """

        movement_direction = (-1, 0)

        return self.move(board, movement_direction)

    def move_right(self, board: CBoard):
        """
        Move shape right.
        @param board Game board.
        :return: True - success; False - we are colliding with something.
        """

        movement_direction = (1, 0)

        return self.move(board, movement_direction)

    def move(self, board: CBoard, direction: Tuple[int, int]):
        """
        Move the shape. We need to verify that we are not colliding in @board.
        :param board: Board Game board.
        :param direction: Direction to be Moved.
        :return: True - success; False - we are colliding with something.
        """

        # Save old location before making the move.
        old_location = self.location

        # Make the move.
        self.location = (self.location[0] + direction[0], self.location[1] + direction[1])

        # Check new location collisions.
        if self.check_collisions(board) is False:
            # Reset location and return False, because the movement was not successful.
            self.location = old_location
            return False

        return True

    def check_collisions(self, board: CBoard):
        # Check collisions.
        for i in range(len(self.shape_layout)):
            for j in range(len(self.shape_layout[0])):
                # Get tile global coords.
                tile_coords = (self.location[0] + i, self.location[1] - j)

                # If tile is active in current layout and cell is not free in board
                if self.shape_layout[j][i] and not board.cell_is_free(tile_coords):
                    return False

        # Every tile is in free cell so the movement is successful.
        return True

    def draw(self, surface: pygame.Surface, tile_size: int):
        """
        Draw shape using Pyglet library.
        :param tile_size Size of one cell in gameboard in pixels.
        :param surface: Surface to be used for drawing.
        """

        for i in range(len(self.shape_layout)):
            for j in range(len(self.shape_layout)):
                if self.shape_layout[j][i]:
                    surface.blit(self.tile_sprite, (
                    (self.location[0] + i) * tile_size, (self.location[1] - j) * tile_size))
