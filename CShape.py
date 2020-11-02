import copy
import numpy
from random import randint


# Rotatable shape in game.
class CShape:
    __shapes = [[[False, False, False], [False, True, False], [True, True, True]],
                [[True, True], [True, True]]]
    shape_layout = None
    location = (0, 0)

    def __init__(self, spawn_location=(0, 0)):
        self.location = spawn_location
        # We need some random layout for this shape.
        # Deep copy needed because we will rotate the shape.
        self.shape_layout = copy.deepcopy(self.__random_shape())

    """
    Generate random index and return random array which represents the shape.
    @:returns Shape array
    """

    @staticmethod
    def __random_shape():
        # Generate random index in shapes list - We want new random shape.
        random_index = randint(0, len(CShape.__shapes) - 1)

        return CShape.__shapes[random_index]

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
