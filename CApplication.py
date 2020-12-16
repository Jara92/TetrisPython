from CGame import CGame
from CMenu import CMenu
from EApplicationState import ApplicationState


class CApplication:
    game_instance = None
    menu_instance = None
    app_window = None

    def __init__(self):
        self.menu_instance = CMenu()
        self.game_instance = CGame()

    def run(self):
        app_state = ApplicationState.APPLICATION_STATE_MENU
        #app_state = ApplicationState.APPLICATION_STATE_GAME

        while app_state != ApplicationState.APPLICATION_STATE_EXIT:
            if app_state == ApplicationState.APPLICATION_STATE_MENU:
                # app_state = self.menu_instance.run();
                app_state = self.menu_instance.run()
            elif app_state == ApplicationState.APPLICATION_STATE_GAME:
                app_state = self.game_instance.run()

        return 0




