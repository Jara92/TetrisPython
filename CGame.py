import pyglet
from EApplicationState import ApplicationState
from CShape import CShape
from pyglet import image


class CGame:
    update_interval = 30

    board_size = (10, 35)
    cell_size = 50

    active_shape = None
    next_shape = None
    game_board = []
    tile_texture = None

    window = None

    # Prepare new game.
    def prepare_game(self, window_width=500, window_height=650, tile_size=25):
        self.window = pyglet.window.Window(width=window_width, height=window_height)

        if not self.window:
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

            self.tile_texture.draw()

        image_source = pyglet.image.load('assets/img/tile.png')
        self.tile_texture = pyglet.sprite.Sprite(image_source, x=self.cell_size, y=self.cell_size)

        # Define game board size and create 2D array.
        # self.game_board = [[0] * cols] * rows
        self.game_board = [[0] * self.board_size[0]] * self.board_size[1]

        # TODO I will have to change this dynamically because the game is getting faster.
        pyglet.clock.schedule_interval(self.update, 1 / self.update_interval)

        # Define first shape
        self.active_shape = CShape((0, 0))

    # Run a new game.
    def run(self):
        self.prepare_game()

        pyglet.app.run()

        return ApplicationState.APPLICATION_STATE_MENU

    # Update game state.
    def update(self, delta_time):

        self.active_shape.print_shape()
        print("=========")
        self.active_shape.rotate_shape()


       # print("Update game. DeltaTime: " + str(delta_time))
