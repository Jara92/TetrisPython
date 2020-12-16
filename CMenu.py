import pygame
from EApplicationState import ApplicationState
from NamedTupples import *
import pygame_gui
import thorpy


class CMenu:
    window_size = None
    surface = None
    ui_manager = None
    button = None

    def prepare_menu(self, window_width=450, window_height=500):
        self.window_size = Coord(window_width, window_height)

        # Create window and flip it
        self.surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.flip()

        pygame.display.set_caption("Tetris")

        self.ui_manager = pygame_gui.UIManager((window_width, window_height), "assets/ui/menu.json")

        return
        # Define play button
        button_size = Coord(250, 125)
        button_location = Coord(window_width / 2 - (button_size.x / 2), 75)
        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(button_location, button_size),
                                                   text='Play',
                                                   manager=self.ui_manager)

    def run(self):
        """
        Run game stuff.
        :return:
        """

        pygame.init()

        self.prepare_menu()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.button:
                            print('Play')

                self.ui_manager.process_events(event)

            # Calculate delta time and convert to to seconds.
            delta_time = pygame.time.Clock().tick(60) / 1000

            self.ui_manager.update(delta_time)
            self.surface.blit(self.surface, (0, 0))
            self.ui_manager.draw_ui(self.surface)

            pygame.display.update()
            # self.update(delta_time)
            # self.draw()

        pygame.display.quit()
        pygame.quit()

        return ApplicationState.APPLICATION_STATE_EXIT
