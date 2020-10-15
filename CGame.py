import pyglet
from EApplicationState import ApplicationState


class CGame:
    game_window = None

    def __init__(self):
        self.prepare_game()

    # Prepare new game.
    def prepare_game(self):
        window_width = 400
        window_height = 750

        self.game_window = pyglet.window.Window(width=window_width, height=window_height)

        self.game_window.set_caption("Tetris")

        label = pyglet.text.Label('Tetris',
                                  font_name='Arial',
                                  font_size=36,
                                  x=self.game_window.width // 2, y=self.game_window.height // 2,
                                  anchor_x='center', anchor_y='center')

        @self.game_window.event
        def on_draw():
            self.game_window.clear()
            label.draw()

        pyglet.clock.schedule_interval(self.update, 1 / 120.0)

    # Run a new game.
    def run(self):
        self.prepare_game()

        pyglet.app.run()

        return ApplicationState.APPLICATION_STATE_MENU

    # Update game state.
    def update(self, delta_time):
        print("Update game. DeltaTime: " + str(delta_time))
