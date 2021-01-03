from src.Game import Game
from src.Menu import Menu
from src.ApplicationState import ApplicationState


class Application:
    def run(self):
        """
        Run application.
        :return:
        """
        app_state = ApplicationState.application_state_menu
        # app_state = ApplicationState.APPLICATION_STATE_GAME

        # Run application until application state is not EXIT
        while app_state != ApplicationState.application_state_exit:
            if app_state == ApplicationState.application_state_menu:
                app_state = Menu().run()
            elif app_state == ApplicationState.application_state_game:
                app_state = Game().run()

        return 0
