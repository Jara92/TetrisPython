import pyglet
from pyglet.window import key
from enum import Enum

class Controls(Enum):
    """
    Controls layout to be used.
    """
    ACTION_MOVE_LEFT = 0,
    ACTION_MOVE_RIGHT = 1,
    ACTION_ADD_SPEED = 2,
    ACTION_ROTATE = 3,
    ACTION_PAUSE = 4


class CInput:
    __controls = None
    __default_controls = {
        Controls.ACTION_MOVE_LEFT: key.LEFT,
        Controls.ACTION_MOVE_RIGHT: key.RIGHT,
        Controls.ACTION_ADD_SPEED: key.DOWN,
        Controls.ACTION_ROTATE: key.UP,
        Controls.ACTION_PAUSE: key.ESCAPE
    }
    __state = {}

    def __init__(self, controls=None):
        # Set default layout.
        if controls is None:
            controls = CInput.__default_controls

        self.__controls = controls

    def change_controls(self, controls):
        self.__controls = controls

    def update_input(self):
        # TODO https://pyglet.readthedocs.io/en/latest/programming_guide/keyboard.html
        keys = key.KeyStateHandler()


    def get_action(self, action:Controls):
        return self.__state.get(action, False)



