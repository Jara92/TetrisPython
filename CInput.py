import pyglet
from pyglet.window import key
from EControls import EControls


class CInput:
    __window = None
    __controls = None
    __default_controls = {
        EControls.action_left: key.LEFT,
        EControls.action_right: key.RIGHT,
        EControls.action_add_speed: key.DOWN,
        EControls.action_rotate: key.UP,
        EControls.action_pause: key.ESCAPE
    }
    __state = {}

    def __init__(self, window: pyglet.window, controls: dict = None):
        # Set window reference. We are gonna need it to get keyboard status.
        self.__window = window
        if self.__window is None:
            raise Exception("Sorry, the window cannot be 'None'")

        # Set default layout.
        if controls is None:
            controls = CInput.__default_controls

        self.__controls = controls

    def change_controls(self, controls):
        self.__controls = controls

    def on_key_press(self, symbol, modifiers):
        return
        for action in EControls:
            if symbol == self.__controls[action]:
                self.__state[EControls.action_left] = True

    def update_input(self):
        return
        # TODO https://pyglet.readthedocs.io/en/latest/programming_guide/keyboard.html
        win = self.__window
        keyboard = key.KeyStateHandler()
        win.push_handlers(keyboard)

        old_state = self.__state
        # self.__state = {EControls.action_left: True}

        for action in EControls:
            if keyboard[self.__controls[action]]:
                pass
                self.__state[action] = True

        #return

        if keyboard[key.LEFT]:
            print("mackl")
            self.__state[EControls.action_left] = True

        for i in self.__state:
            print(i)

        # if keyboard[self.__controls[EControls.ACTION_MOVE_RIGHT]]:
        # self.__state[EControls.AC]

    def get_action(self, action: EControls):
        """
        Get action status.
        :param action:
        :return:
        """
        return self.__state.get(action)
