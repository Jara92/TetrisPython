import copy
import numpy
import pyglet
from random import randint


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

    """
    Return random shape in __shapes.
    @:returns Random shape array.
    """

    @staticmethod
    def __random_shape():
        # Generate random index in shapes list - We want new random shape.
        random_index = randint(0, len(CShape.__shapes) - 1)

        return CShape.__shapes[random_index]

    """
    Return random color in __colors.
    @:returns Random color.
    """

    @staticmethod
    def __random_color():
        # Generate random index in color list - We want new random color.
        random_index = randint(0, len(CShape.__colors) - 1)

        return CShape.__colors[random_index]

    """
    Rotate shape by 90 degrees left.
    """

    def rotate_shape(self):
        self.shape_layout = numpy.rot90(numpy.array(self.shape_layout, bool), 1, (1, 0))
        return

    """
    Print shape layout.
    """

    def print_shape(self):
        N = len(self.shape_layout[0])
        for i in range(N):
            print(self.shape_layout[i])

    """
    Move shape down.
    """

    def move(self):
        self.location = (self.location[0], self.location[1] - 1)

    def draw(self, tile_size):
        for i in range(len(self.shape_layout)):
            for j in range(len(self.shape_layout)):
                if self.shape_layout[i][j]:
                    self.tile_sprite.position = (((self.location[0] - j) * tile_size,
                                                  (self.location[1] - i) * tile_size))
                    self.tile_sprite.draw()
