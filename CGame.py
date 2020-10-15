import pyglet
from EApplicationState import ApplicationState
from pyglet import image


class CGame:
    window = None


    def __init__(self):
        a = 1

    # Prepare new game.
    def prepare_game(self, window_width=500, window_height=650):

        self.window = pyglet.window.Window(width=window_width, height=window_height)
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

            sprite = pyglet.sprite.Sprite(pyglet.image.load("assets/img/tile.png"))
            sprite.x = 0
            sprite.y = 0
            sprite.draw()



        pyglet.clock.schedule_interval(self.update, 1 / 120.0)

    # Run a new game.
    def run(self):
        self.prepare_game()

        pyglet.app.run()

        return ApplicationState.APPLICATION_STATE_MENU

    # Update game state.
    def update(self, delta_time):
        print("Update game. DeltaTime: " + str(delta_time))
