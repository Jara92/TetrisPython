import pyglet
from pyglet import window, shapes
from pyglet.window import key
from EApplicationState import ApplicationState
from CShape import CShape
from CBoard import CBoard
from CInput import CInput
from EControls import EControls
from pyglet import image

"""
Change window origin to top-left corner.
@source https://stackoverflow.com/questions/10167329/change-the-position-of-the-origin-in-pygame-coordinate-system
"""


def to_pygame(coords, height):
    # return coords[0], height - coords[1]
    return coords


class CGame:
    update_interval = 0.5
    timer = 0

    tile_size = 50

    board = None
    active_shape = None
    next_shape = None
    tile_sprite = None

    window = None
    window_size = (500, 650)
    input = None

    # Prepare new game.
    def prepare_game(self, window_width=500, window_height=650, tile_size=30):
        self.window_size = (window_width, window_height)
        self.tile_size = tile_size

        self.window = pyglet.window.Window(width=window_width, height=window_height, resizable=True)

        if not self.window:
            return False

        self.window.set_caption("Tetris")

        @self.window.event
        def on_key_press(symbol, modifiers):
            self.input.on_key_press(symbol, modifiers)

        @self.window.event
        def on_key_release(symbol, modifiers):
            self.input.on_key_release(symbol, modifiers)

        @self.window.event
        def on_draw():
            self.window.clear()

            self.draw_debug()

            self.active_shape.draw(self.tile_size)

        # Create input manager using default controls.
        self.input = CInput(self.window)

        # Create new board.
        self.board = CBoard()

        # Load tile image from resources.
        image_source = pyglet.image.load('assets/img/tile.png')

        # Create sprite and scale it to self.cell_size size in pixels.
        self.tile_sprite = pyglet.sprite.Sprite(image_source, x=self.tile_size, y=self.tile_size)
        self.tile_sprite.scale = self.tile_size / self.tile_sprite.width

        # TODO I will have to change this dynamically because the game is getting faster.
        pyglet.clock.schedule_interval(self.update, 1 / 120.0)

        # Define first shape # TODO exception when the shape is on starting location
        #self.active_shape = CShape(self.tile_sprite, (self.board.size[0] // 2 + 1, self.board.size[1] + 1))
        #self.active_shape = CShape(self.tile_sprite, (self.board.size[0] // 2 + 1, self.board.size[1] -1))
        self.active_shape = CShape(self.tile_sprite, (self.board.size[0] // 2 + 1, self.board.size[1] - 7))

    # Run a new game.
    def run(self):
        self.prepare_game()

        pyglet.app.run()

        return ApplicationState.APPLICATION_STATE_MENU

    # Update game state.
    def update(self, delta_time):
        self.timer += delta_time

        if self.timer > self.update_interval:
            self.timer = 0
            movement = self.active_shape.move_down(self.board)

        if self.input.get_action(EControls.action_left):
            movement = self.active_shape.move_left(self.board)
        elif self.input.get_action(EControls.action_right):
            movement = self.active_shape.move_right(self.board)

        # print("Update game. DeltaTime: " + str(delta_time))

    def draw_debug(self):
        """
        Draw debug matrix and other debugging objects.
        """

        batch = pyglet.graphics.Batch()

        for i in range(self.board.size[0] + 1):
            line1 = shapes.Line(i * self.tile_size, 0,
                                i * self.tile_size, self.board.size[1] * self.tile_size, 2,
                                color=(255, 0, 0),
                                batch=batch)
            batch.draw()

        for i in range(self.board.size[1] + 1):
            line1 = shapes.Line(0, i * self.tile_size,
                                self.board.size[0] * self.tile_size, i * self.tile_size, 2,
                                color=(255, 0, 0),
                                batch=batch)
            batch.draw()
