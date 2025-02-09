from enum import Enum
import pygame.key
from src.Controls import Controls


class InputState(Enum):
    state_pressed = 0
    state_released = 1
    state_idling = 2


class Input:
    """
    Class which handles user input.
    """
    INPUT_HOLD_DELAY = -0.06
    __controls = None
    # Default controls dict to be used.
    __default_controls = {
        Controls.action_left: pygame.K_LEFT,
        Controls.action_right: pygame.K_RIGHT,
        Controls.action_speed_up: pygame.K_DOWN,
        Controls.action_rotate: pygame.K_UP,
        Controls.action_pause: pygame.K_ESCAPE
    }
    __state = {}
    __movement_idle = 0.045
    __movement_counter = 0

    def __init__(self, controls: dict = None):
        # Set default layout.
        if controls is None:
            controls = Input.__default_controls

        self.__controls = controls

    def update(self, delta_time):
        """
        Update input state.
        :param delta_time: Delta time
        """
        # if movement is on
        movements = [Controls.action_left, Controls.action_right]

        # Movement timer
        for movement in movements:
            if self.__state.get(movement, InputState.state_released) == InputState.state_idling:
                self.__movement_counter += delta_time

                # Reset movement timer
                if self.__movement_counter >= self.__movement_idle:
                    self.__movement_counter = 0

    def change_controls(self, controls: dict):
        """
        Change game controls.
        :param controls: New game controls dict.
        :return:
        """
        self.__controls = controls

    def on_key_down(self, symbol):
        """
        Key down event.
        :param symbol: Pressed symbol.
        """

        # Rotation action
        if symbol == self.__controls[Controls.action_rotate] \
                and self.__state.get(Controls.action_rotate, InputState.state_released) != InputState.state_idling:
            self.__state[Controls.action_rotate] = InputState.state_pressed

        # Other actions
        elif symbol != self.__controls[Controls.action_rotate]:
            for action in Controls:
                if symbol == self.__controls[action]:
                    self.__state[action] = InputState.state_pressed

    def on_key_up(self, symbol):
        """
        Key up event.
        :param symbol: Released symbol.
        """
        for action in Controls:
            if symbol == self.__controls[action]:
                # The key is released now.
                self.__state[action] = InputState.state_released

    def is_rotating(self):
        """
        Is rotation rotation input on?
        :return: True - Is rotating; False - Is not rotating
        """
        out = self.__get_action(Controls.action_rotate)

        # We dont want to rotate the shape few times.
        if out:
            # We will wait until rotate key is released.
            self.__state[Controls.action_rotate] = InputState.state_idling

        return out

    def is_speeding_up(self):
        """
        Is speeding up input on?
        :return: True - Is speeding up; False - Is not speeding up
        """
        return self.__get_action(Controls.action_speed_up)

    def __is_moving(self, action):
        # Get Action state
        action_state = self.__state.get(action, InputState.state_released)

        # If key is being hold and movement timer is 0
        if action_state == InputState.state_idling and self.__movement_counter is 0:
            return True

        # key was pressed now
        elif action_state == InputState.state_pressed:
            # Mark key as being hold
            self.__state[action] = InputState.state_idling

            # Next movement will be little bit delayed
            self.__movement_counter = Input.INPUT_HOLD_DELAY

            return True

        return False

    def is_moving_left(self):
        """
        Is moving left input on?
        :return: True - Is moving left; False - Is not moving left
        """
        return self.__is_moving(Controls.action_left)

    def is_moving_right(self):
        """
        Is moving right input on?
        :return: True - Is moving right; False - Is not moving right
        """
        return self.__is_moving(Controls.action_right)

    def is_pausing(self):
        """
        Is pausing action on?
        :return: True - Is pausing action on; False - Is not pausing action on
        """
        if self.__state.get(Controls.action_pause, InputState.state_released) == InputState.state_pressed:
            self.__state[Controls.action_pause] = InputState.state_idling
            return True

        return False

    def __get_action(self, action: Controls):
        """
        Get action status.
        :param action:
        :return:
        """

        return self.__state.get(action, InputState.state_released) == InputState.state_pressed
