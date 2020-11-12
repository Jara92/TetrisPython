#import pyglet
#from pyglet.window import key
import pygame
import pygame.key
from EControls import EControls


class CInput:
    __controls = None
    __default_controls = {
        EControls.action_left: pygame.K_LEFT,
        EControls.action_right: pygame.K_RIGHT,
        EControls.action_add_speed: pygame.K_DOWN,
        EControls.action_rotate: pygame.K_UP,
        EControls.action_pause: pygame.K_ESCAPE
    }
    __state = {}

    def __init__(self, controls: dict = None):
        # Set default layout.
        if controls is None:
            controls = CInput.__default_controls

        self.__controls = controls

    def change_controls(self, controls):
        self.__controls = controls

    def on_key_down(self, symbol):
        for action in EControls:
            if symbol == self.__controls[action]:
                self.__state[action] = True

    def on_key_up(self, symbol):
        for action in EControls:
            if symbol == self.__controls[action]:
                self.__state[action] = False

    def get_action(self, action: EControls):
        """
        Get action status.
        :param action:
        :return:
        """
        return self.__state.get(action)
