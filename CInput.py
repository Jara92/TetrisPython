import pygame
from enum import Enum
import pygame.key
from EControls import EControls


class EInputState(Enum):
    state_pressed = 0
    state_released = 1
    state_idling = 2


class CInput:
    INPUT_HOLD_DELAY = -0.06
    __controls = None
    __default_controls = {
        EControls.action_left: pygame.K_LEFT,
        EControls.action_right: pygame.K_RIGHT,
        EControls.action_speed_up: pygame.K_DOWN,
        EControls.action_rotate: pygame.K_UP,
        EControls.action_pause: pygame.K_ESCAPE
    }
    __state = {}
    __movement_idle = 0.045
    __movement_counter = 0

    def __init__(self, controls: dict = None):
        # Set default layout.
        if controls is None:
            controls = CInput.__default_controls

        self.__controls = controls

    def update(self, delta_time):
        # if movement is on
        movements = [EControls.action_left, EControls.action_right]

        for movement in movements:
            if self.__state.get(movement, EInputState.state_released) == EInputState.state_idling:
                self.__movement_counter += delta_time

                if self.__movement_counter >= self.__movement_idle:
                    self.__movement_counter = 0

    def change_controls(self, controls):
        self.__controls = controls

    def on_key_down(self, symbol):
        if symbol == self.__controls[EControls.action_rotate] and not self.get_action(EControls.action_rotate):
            self.__state[EControls.action_rotate] = EInputState.state_pressed

        else:
            for action in EControls:
                if symbol == self.__controls[action]:
                    self.__state[action] = EInputState.state_pressed

    def on_key_up(self, symbol):
        for action in EControls:
            if symbol == self.__controls[action]:
                self.__state[action] = EInputState.state_released

    def is_rotating(self):
        out = self.get_action(EControls.action_rotate)

        self.__state[EControls.action_rotate] = EInputState.state_idling
        return out

    def is_speeding_up(self):
        return self.get_action(EControls.action_speed_up)

    def __is_moving(self, action):
        # Get Action state
        action_state = self.__state.get(action, EInputState.state_released)

        # If key is being hold and movement timer is 0
        if action_state == EInputState.state_idling and self.__movement_counter is 0:
            return True

        # key was pressed now
        elif action_state == EInputState.state_pressed:
            # Mark key as being hold
            self.__state[action] = EInputState.state_idling

            # Next movement will be little bit delayed
            self.__movement_counter = CInput.INPUT_HOLD_DELAY

            return True

        return False

    def is_moving_left(self):
        return self.__is_moving(EControls.action_left)

    def is_moving_right(self):
        return self.__is_moving(EControls.action_right)

    def get_action(self, action: EControls):
        """
        Get action status.
        :param action:
        :return:
        """

        return self.__state.get(action, EInputState.state_released) == EInputState.state_pressed
