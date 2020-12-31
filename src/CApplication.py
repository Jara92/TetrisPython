from src.CGame import CGame
from src.CMenu import CMenu
from src.EApplicationState import ApplicationState


class CApplication:
    def run(self):
        """
        Run application.
        :return:
        """
        app_state = ApplicationState.APPLICATION_STATE_MENU
        #app_state = ApplicationState.APPLICATION_STATE_GAME

        while app_state != ApplicationState.APPLICATION_STATE_EXIT:
            if app_state == ApplicationState.APPLICATION_STATE_MENU:
                app_state = CMenu().run()
            elif app_state == ApplicationState.APPLICATION_STATE_GAME:
                app_state = CGame().run()

        return 0




