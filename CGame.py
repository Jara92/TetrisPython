# import pyglet
# from pyglet import window, shapes
from pyglet.window import key

import pygame
from pygame import display

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

    surface = None
    window_size = (500, 650)
    input = None
    image_source = None

    # Prepare new game.
    def prepare_game(self, window_width=500, window_height=650, tile_size=30):
        self.window_size = (window_width, window_height)
        self.tile_size = tile_size

        # self.window = pyglet.window.Window(width=window_width, height=window_height, resizable=True)
        self.surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.flip()

        pygame.display.set_caption("Tetris")

        # @self.window.event
        # def on_key_press(symbol, modifiers):
        #    self.input.on_key_press(symbol, modifiers)

        # @self.window.event
        # def on_key_release(symbol, modifiers):
        #    self.input.on_key_release(symbol, modifiers)

        # @self.window.event
        # def on_draw():
        #    self.window.clear()

        #   self.draw_debug()

        #   self.active_shape.draw(self.tile_size)

        # Create input manager using default controls.
        self.input = CInput(self.surface)

        # Create new board.
        self.board = CBoard()

        # Load tile image from resources.
        self.image_source = pygame.image.load('assets/img/tile.png')

        # Create sprite and scale it to self.cell_size size in pixels.
        # self.tile_sprite = pyglet.sprite.Sprite(image_source, x=self.tile_size, y=self.tile_size)
        # self.tile_sprite.scale = self.tile_size / self.tile_sprite.width

        # TODO I will have to change this dynamically because the game is getting faster.
        # pyglet.clock.schedule_interval(self.update, 1 / 120.0)

        # Define first shape # TODO exception when the shape is on starting location
        # self.active_shape = CShape(self.tile_sprite, (self.board.size[0] // 2 + 1, self.board.size[1] + 1))
        # self.active_shape = CShape(self.tile_sprite, (self.board.size[0] // 2 + 1, self.board.size[1] -1))
        # self.active_shape = CShape(self.tile_sprite, (self.board.size[0] // 2 + 1, self.board.size[1] - 7))

    # Run a new game.
    def run(self):
        self.prepare_game()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update(0)  # TODO delta time
        # pyglet.app.run()
        pygame.display.quit()
        pygame.quit()

        return ApplicationState.APPLICATION_STATE_MENU

    # Update game state.
    def update(self, delta_time):
        self.timer += delta_time

        self.draw()
        return

        if self.timer > self.update_interval:
            self.timer = 0
            movement = self.active_shape.move_down(self.board)

        if self.input.get_action(EControls.action_left):
            movement = self.active_shape.move_left(self.board)
        elif self.input.get_action(EControls.action_right):
            movement = self.active_shape.move_right(self.board)
        elif self.input.get_action(EControls.action_rotate):
            movement = self.active_shape.rotate_shape(self.board)

        # print("Update game. DeltaTime: " + str(delta_time))

    def changColor(self, image, color):
        colouredImage = pygame.Surface(image.get_size())
        colouredImage.fill(color)

        finalImage = image.copy()
        finalImage.blit(colouredImage, (0, 0), special_flags=pygame.BLEND_MULT)
        return finalImage

    def draw(self):

        # print("draw")
        self.surface.fill((0, 0, 0))

        self.image_source = self.changColor(self.image_source, (255,128,0))

        #self.image_source.blit(colorImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # self.image_source.fill((0, 255, 255, 100), special_flags=pygame.BLENDMODE_ADD)
        #self.image_source.blit(self.image_source, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        self.surface.blit(self.image_source, (0, 0))

        pygame.display.update()

    def draw_debug(self):
        """
        Draw debug matrix and other debugging objects.
        """

        # batch = pyglet.graphics.Batch()

        for i in range(self.board.size[0] + 1):
            i = i
            # line1 = shapes.Line(i * self.tile_size, 0,i * self.tile_size, self.board.size[1] * self.tile_size, 2,color=(255, 0, 0),batch=batch)
            # batch.draw()

        for i in range(self.board.size[1] + 1):
            i = i
            # line1 = shapes.Line(0, i * self.tile_size,self.board.size[0] * self.tile_size, i * self.tile_size, 2,color=(255, 0, 0),batch=batch)
            # batch.draw()
