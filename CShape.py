import copy
import numpy
import pyglet
from random import randint
from CBoard import CBoard


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

    def __init__(self, tile_sprite: pyglet.sprite, spawn_location=(5, 0)):
        self.tile_sprite = tile_sprite
        self.tile_sprite.color = CShape.__random_color()
        self.location = spawn_location

        # We need some random layout for this shape.
        # Deep copy needed because we will rotate the shape.
        self.shape_layout = copy.deepcopy(CShape.__random_shape())

        #self.print_shape()
        self.rotate_shape()
        #self.print_shape()

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

    def rotate_shape(self, board=None):
        """
        Rotate shape by 90 degrees left. We need to verify that we are not colliding in @board.
        @param board Game board.
        """

        self.shape_layout = numpy.rot90(numpy.array(self.shape_layout, bool), 1, (1, 0))
        return

    def print_shape(self):
        """
        Print shape layout.
        """

        N = len(self.shape_layout[0])
        for i in range(N):
            print(self.shape_layout[i])

    def move(self, board: CBoard):
        """
        Move shape down. We need to verify that we are not colliding in @board.
        @param board Game board.
        """

        # Save old location before making the move.
        old_location = self.location

        # Make the move.
        self.location = (self.location[0], self.location[1] - 1)

        # Check collisions.
        for i in range(len(self.shape_layout)):
            for j in range(len(self.shape_layout[0])):
                # Get tile global coords.
                tile_coords = (self.location[0] + j, self.location[1] - i)

                # If tile is active in current layout and cell is not free in board
                if self.shape_layout[i][j] and not board.cell_is_free(tile_coords):
                    # Reset location and return False, because the movement was not successful.
                    self.location = old_location
                    return False

        # Every tile is in free cell so the movement is successful.
        return True

    def draw(self, tile_size):
        """
        Draw shape using Pyglet library.
        @param tile_size Size of one cell in gameboard in pixels.
        """

        for i in range(len(self.shape_layout)):
            for j in range(len(self.shape_layout[0])):
                if self.shape_layout[i][j]:
                    self.tile_sprite.position = (((self.location[0] + j) * tile_size,
                                                  (self.location[1] - i) * tile_size))
                    self.tile_sprite.draw()
