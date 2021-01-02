from src.Game import Game
from src.Menu import Menu
from src.ApplicationState import ApplicationState


class Application:
    def run(self):
        """
        Run application.
        :return:
        """
        app_state = ApplicationState.APPLICATION_STATE_MENU
        # app_state = ApplicationState.APPLICATION_STATE_GAME

        # Run application until application state is not EXIT
        while app_state != ApplicationState.APPLICATION_STATE_EXIT:
            if app_state == ApplicationState.APPLICATION_STATE_MENU:
                app_state = Menu().run()
            elif app_state == ApplicationState.APPLICATION_STATE_GAME:
                app_state = Game().run()

        return 0
