import pyglet
from EApplicationState import ApplicationState
from pyglet import image


class CGame:
    window = None
    board = None

    # Prepare new game.
    def prepare_game(self, window_width=500, window_height=650, tile_size=25):
        self.window = pyglet.window.Window(width=window_width, height=window_height)

        if self.window == False:
            return False

        self.window.set_caption("Tetris")

        label = pyglet.text.Label('Tetris',
                                  font_name='Arial',
                                  font_size=36,
                                  x=self.window.width // 2, y=self.window.height // 2,
                                  anchor_x='center', anchor_y='center')

        @self.window.event
        def on_draw():
            self.window.clear()
            label.draw()

         #   self.sprite.draw()

        # Define game board size and create 2D array.
        cols = rows = 18
        self.board = [[0] * cols] * rows

        # TODO I will have to change this dynamically because the game is getting faster.
        pyglet.clock.schedule_interval(self.update, 1 / 120.0)

    # Run a new game.
    def run(self):
        self.prepare_game()

        pyglet.app.run()

        return ApplicationState.APPLICATION_STATE_MENU

    # Update game state.
    def update(self, delta_time):
        print("Update game. DeltaTime: " + str(delta_time))
