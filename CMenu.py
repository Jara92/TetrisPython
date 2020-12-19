import pygame
import pygame_menu
from EApplicationState import ApplicationState
from NamedTupples import *
from CScoreManager import CScoreManager


class CMenu:
    """
    Menu window.
    """
    window_size = None
    surface = None
    menu = None

    return_state = ApplicationState.APPLICATION_STATE_EXIT

    def prepare_menu(self, window_width=400, window_height=400):
        """
        Prepare menu window.
        :param window_width: Window width in pixels.
        :param window_height: Window height in pixels.
        :return:
        """
        self.window_size = Coord(window_width, window_height)

        # Create window and flip it
        self.surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.flip()

        pygame.display.set_caption("Tetris")

        # Create custom theme
        custom_theme = pygame_menu.themes.THEME_ORANGE.copy()
        custom_theme.menubar_close_button = False

        custom_theme.title_font = pygame_menu.font.FONT_FRANCHISE
        custom_theme.widget_font = pygame_menu.font.FONT_FRANCHISE
        custom_theme.title_font_size = 64
        custom_theme.widget_font_size = 56

        # Define menu
        self.menu = pygame_menu.Menu(window_width, window_height, 'Tetris',
                                     theme=custom_theme)

        # Define Play button
        start_game_button = self.menu.add_button('Play', self.start_game)
        start_game_button.set_selected(True)
        start_game_button.set_shadow(enabled=False)

        # Define quit button
        quit_game_button = self.menu.add_button('Quit', self.exit_game)
        quit_game_button.set_selected(False)
        quit_game_button.set_shadow(enabled=False)

        # Define top score label
        top_score = CScoreManager.get_score()
        score_label = self.menu.add_label("Top score: " + str(top_score))
        score_label.set_font(pygame_menu.font.FONT_FRANCHISE, 36, (255, 255, 255), (255, 255, 255), (0, 0, 0, 0))

        # Define author label
        #label = self.menu.add_label("Jaroslav Fikar 2020")
        #label.set_font(pygame_menu.font.FONT_FRANCHISE, 18, (255, 255, 255), (255, 255, 255), (0, 0, 0, 0))
        #label.set_alignment(pygame_menu.locals.ALIGN_RIGHT)

    def start_game(self):
        """
        Start game action.
        :return:
        """
        self.return_state = ApplicationState.APPLICATION_STATE_GAME
        self.menu.disable()

    def exit_game(self):
        """
        Exit game action.
        :return:
        """
        self.return_state = ApplicationState.APPLICATION_STATE_EXIT
        self.menu.disable()

    def run(self):
        """
        Run game stuff.
        :return: New application state.
        """

        pygame.init()

        # Prepare menu
        self.prepare_menu()

        # Menu loop
        self.menu.mainloop(self.surface)

        pygame.display.quit()
        pygame.quit()

        return self.return_state
