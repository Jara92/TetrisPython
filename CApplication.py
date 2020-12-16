from CGame import CGame
from CMenu import CMenu
from EApplicationState import ApplicationState


class CApplication:
    def run(self):
        app_state = ApplicationState.APPLICATION_STATE_MENU
        #app_state = ApplicationState.APPLICATION_STATE_GAME

        while app_state != ApplicationState.APPLICATION_STATE_EXIT:
            if app_state == ApplicationState.APPLICATION_STATE_MENU:
                app_state = CMenu().run()
            elif app_state == ApplicationState.APPLICATION_STATE_GAME:
                app_state = CGame().run()

        return 0




