import pyglet
from pyglet import window
from EApplicationState import ApplicationState
from CShape import CShape
from pyglet import image

"""
Change window origin to top-left corner.
@source https://stackoverflow.com/questions/10167329/change-the-position-of-the-origin-in-pygame-coordinate-system
"""


def to_pygame(coords, height):
    return coords[0], height - coords[1]


class CGame:
    update_interval = 10

    board_size = (10, 35)
    tile_size = 50

    active_shape = None
    next_shape = None
    game_board = []
    tile_sprite = None

    window = None
    window_size = (500, 650)

    # Prepare new game.
    def prepare_game(self, window_width=500, window_height=650, tile_size=25):
        self.window_size = (window_width, window_height)
        self.tile_size = tile_size

        self.window = pyglet.window.Window(width=window_width, height=window_height)

        if not self.window:
            return False

        self.window.set_caption("Tetris")
        """
        label = pyglet.text.Label('Tetris',
                                  font_name='Arial',
                                  font_size=36,
                                  x=self.window.width // 2, y=self.window.height // 2,
                                  anchor_x='center', anchor_y='center')
        """

        @self.window.event
        def on_draw():
            self.window.clear()
            # label.draw()

            for i in range(len(self.active_shape.shape_layout)):
                for j in range(len(self.active_shape.shape_layout)):
                    if self.active_shape.shape_layout[i][j]:
                        self.tile_sprite.position = to_pygame(((self.active_shape.location[0] + j) * self.tile_size,
                                                               (self.active_shape.location[1] + i) * self.tile_size),
                                                              self.window_size[1])
                        self.tile_sprite.draw()

        # Load tile image from resources.
        image_source = pyglet.image.load('assets/img/tile.png')

        # Create sprite and scale it to self.cell_size size in pixels.
        self.tile_sprite = pyglet.sprite.Sprite(image_source, x=self.tile_size, y=self.tile_size)
        self.tile_sprite.scale = self.tile_size / self.tile_sprite.width

        # Define game board size and create 2D array.
        # self.game_board = [[0] * cols] * rows
        self.game_board = [[0] * self.board_size[0]] * self.board_size[1]

        # TODO I will have to change this dynamically because the game is getting faster.
        pyglet.clock.schedule_interval(self.update, 1 / self.update_interval)

        # Define first shape
        self.active_shape = CShape((self.board_size[0] // 2 + 1, 0))

    # Run a new game.
    def run(self):
        self.prepare_game()

        pyglet.app.run()

        return ApplicationState.APPLICATION_STATE_MENU

    # Update game state.
    def update(self, delta_time):
        self.active_shape.move()
        debu = ""
        # self.active_shape.print_shape()
        # print("=========")
        # self.active_shape.rotate_shape()

    # print("Update game. DeltaTime: " + str(delta_time))
