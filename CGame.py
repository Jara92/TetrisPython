# import pyglet
# from pyglet import window, shapes
from pyglet.window import key
from random import randint
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
    """
    Colors description.
    white|orange|red|green|blue|gold
    """
    __colors = [(255, 255, 255), (255, 128, 0), (178, 34, 34), (50, 205, 50), (0, 191, 255), (255, 215, 0)]

    __tile_textures = {}
    """
    Update interval is getting smaller value during playing. The game is getting harder then.
    """
    update_interval = 0.45
    MINIMAL_UPDATE_INTERVAL = 0.2
    SPEED_UP_QUOCIENT = 1 / 10.0
    actual_update_interval = 0.5
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

        # Create window and flip it
        self.surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.flip()

        pygame.display.set_caption("Tetris")

        # Create input manager using default controls.
        self.input = CInput()

        # Create new board.
        self.board = CBoard()

        # Load tile image from resources.
        self.image_source = pygame.image.load('assets/img/tile.png')

        # Create sprite and scale it to self.cell_size size in pixels.
        self.image_source = pygame.transform.scale(self.image_source, (self.tile_size, self.tile_size))

        i = 0
        for color in self.__colors:
            tile_texture = self.image_source.copy()
            self.__tile_textures[i] = tile_texture
            tile_texture.fill(color, None, pygame.BLEND_MULT)

            i = i + 1

        # Define first shape
        self.active_shape = CShape(self.__random_color(), (self.board.size[0] // 2, 1))

    def run(self):
        self.prepare_game()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.input.on_key_down(event.key)
                elif event.type == pygame.KEYUP:
                    self.input.on_key_up(event.key)

            # Calculate delta time and convert to to seconds.
            delta_time = pygame.time.Clock().tick(60) / 1000
            self.update(delta_time)
            self.draw()

        pygame.display.quit()
        pygame.quit()

        return ApplicationState.APPLICATION_STATE_MENU

    # Update game state.
    def update(self, delta_time):
        self.timer += delta_time

        if self.timer > self.actual_update_interval:
            self.timer = 0
            movement = self.active_shape.move_down(self.board)

            # movement was not succesful
            if movement is False:
                self.load_next_shape()

        if self.input.get_action(EControls.action_left):
            movement = self.active_shape.move_left(self.board)
        elif self.input.get_action(EControls.action_right):
            movement = self.active_shape.move_right(self.board)
        elif self.input.is_rotating():
            movement = self.active_shape.rotate_shape(self.board)

        # Speeding up
        if self.input.is_speeding_up():
            self.actual_update_interval = self.update_interval * self.SPEED_UP_QUOCIENT
        else:
            self.actual_update_interval = self.update_interval

    def load_next_shape(self):
        # Store current shape into board.
        self.active_shape.store(self.board)

        # load new shape
        self.active_shape = CShape(self.__random_color(), (self.board.size[0] // 2, 1))

        # Check collisison

    def draw(self):
        self.surface.fill((0, 0, 0))
        self.draw_debug()

        self.board.draw(self.surface, self.tile_size)
        # self.active_shape.draw(self.surface, self.tile_size)

        # Print all tiles in active shape using its color
        for tile in self.active_shape.get_tiles():
            self.surface.blit(self.__tile_textures[self.active_shape.tile_color], (
                tile.x * self.tile_size, tile.y * self.tile_size))

        pygame.display.update()

    def draw_debug(self):
        """
        Draw debug matrix and other debugging objects.
        """

        # batch = pyglet.graphics.Batch()

        for i in range(self.board.size[0] + 1):
            pygame.draw.line(self.surface, (255, 0, 0), (i * self.tile_size, 0),
                             (i * self.tile_size, self.board.size[1] * self.tile_size))
            # line1 = shapes.Line(i * self.tile_size, 0,i * self.tile_size, self.board.size[1] * self.tile_size, 2,color=(255, 0, 0),batch=batch)
            # batch.draw()

        for i in range(self.board.size[1] + 1):
            pygame.draw.line(self.surface, (255, 0, 0), (0, i * self.tile_size),
                             (self.board.size[0] * self.tile_size, i * self.tile_size))
            # line1 = shapes.Line(0, i * self.tile_size,self.board.size[0] * self.tile_size, i * self.tile_size, 2,color=(255, 0, 0),batch=batch)
            # batch.draw()

    @staticmethod
    def __random_color():
        """
        Return random color in __colors.
        @:returns Random color.
        """

        # Generate random index in color list - We want new random color.
        random_index = randint(0, len(CGame.__colors) - 1)

        return random_index
        #return CGame.__colors[random_index]
