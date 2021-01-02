import pygame
import pygame_menu
from src.ApplicationState import ApplicationState
from src.NamedTupples import *
from src.ScoreManager import ScoreManager


class Menu:
    """
    Menu window.
    """
    window_size = None
    surface = None
    menu = None

    return_state = ApplicationState.APPLICATION_STATE_EXIT

    def prepare_menu(self, window_size=400):
        """
        Prepare menu window.
        :param window_size Window size in pixels.
        :return:
        """
        self.window_size = Coord(window_size, window_size)

        # Create window and flip it
        self.surface = pygame.display.set_mode((window_size, window_size))
        pygame.display.flip()

        pygame.display.set_caption("Tetris")

        # Create custom theme
        custom_theme = pygame_menu.themes.THEME_ORANGE.copy()
        custom_theme.menubar_close_button = False

        # Fonts
        custom_theme.title_font = pygame_menu.font.FONT_FRANCHISE
        custom_theme.widget_font = pygame_menu.font.FONT_FRANCHISE
        custom_theme.title_font_size = 64
        custom_theme.widget_font_size = 56

        # Define menu
        self.menu = pygame_menu.Menu(window_size, window_size, 'Tetris', theme=custom_theme)

        # Define Play button
        start_game_button = self.menu.add_button('Play', self.start_game)
        start_game_button.set_selected(True)
        start_game_button.set_shadow(enabled=False)

        # Define quit button
        quit_game_button = self.menu.add_button('Quit', self.exit_game)
        quit_game_button.set_selected(False)
        quit_game_button.set_shadow(enabled=False)

        # Define top score label
        top_score = ScoreManager.get_score()
        score_label = self.menu.add_label("Top score: " + str(top_score))
        score_label.set_font(pygame_menu.font.FONT_FRANCHISE, 36, (255, 255, 255), (255, 255, 255), (0, 0, 0, 0))

    def run(self):
        """
        Run game menu stuff.
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

    def start_game(self):
        """
        Start game action.
        """
        self.return_state = ApplicationState.APPLICATION_STATE_GAME
        self.menu.disable()

    def exit_game(self):
        """
        Exit game action.
        """
        self.return_state = ApplicationState.APPLICATION_STATE_EXIT
        self.menu.disable()
