import os
import random
from random import randint
import pygame
from src.NamedTupples import Coord

from src.ApplicationState import ApplicationState
from src.Shape import Shape
from src.Board import Board
from src.Input import Input
from src.ScoreManager import ScoreManager


class Game:
    __font = 'assets/fonts/zorque.ttf'
    """
    Colors description.
    white|orange|red|green|blue|gold
    """
    __colors = [(255, 255, 255), (255, 128, 0), (178, 34, 34), (50, 205, 50), (0, 191, 255), (255, 215, 0)]
    __tile_textures = {}

    update_interval = 0.45  # Update interval is getting smaller value during playing. The game is getting harder then.
    speed_up = 1 / 10.0  # Speeding up quocient.
    actual_update_interval = update_interval  # Actual update interval which may be boosted by speed_up
    timer = 0  # Update timer.

    # Game leveling and speed constants
    MIN_UPDATE_INTERVAL = 0.10
    UPDATE_INTERVAL_STEP = 0.035  # cca 10 levels (10 speed levels)
    LEVEL_UP_QUOCIENT = 1.35  # cca 8042 is top highest level score
    SPEED_UP_QUOCIENT = 1.1

    # Pause and game over variables
    pause = False
    pause_text = None
    game_over = False
    game_over_title = None
    game_over_desc = None

    # Tile setup
    tile_size = 50
    tile_texture = None

    # Board and important shapes
    board = None
    active_shape = None
    next_shape = None

    # Important lcoations
    game_board_spawn_location = None
    next_shape_spawn_location = None

    # Window and input
    surface = None
    window_size = Coord(500, 650)
    input = None

    # Sound effects
    sound_effect_score = None
    sound_effect_game_over = None

    score = 0  # Actual score
    DEFAULT_LEVEL_UP_SCORE = 400  # New game level up score.
    level_up_score = DEFAULT_LEVEL_UP_SCORE  # Score needed to achieve to level up

    def prepare_game(self, window_width=600, window_height=650, tile_size=30):
        """
        Prepare game window.
        :param window_width: Window width in pixels.
        :param window_height: Window height in pixels.
        :param tile_size: Tile size.
        :return:
        """
        self.window_size = Coord(window_width, window_height)
        self.tile_size = tile_size

        # Create window and flip it
        self.surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.flip()

        pygame.display.set_caption("Tetris")

        # Prerender pause text
        font = pygame.font.Font(self.__font, 64)
        small_font = pygame.font.Font(self.__font, 32)
        self.pause_text = font.render("PAUSED", True, (255, 255, 255))
        self.game_over_title = font.render("GAME OVER", True, (255, 255, 255))
        self.game_over_desc = small_font.render("Press ESC to reset.", True, (255, 255, 255))

        # Init random seed
        random.seed(os.urandom(9999999))

        # Create input manager using default controls.
        self.input = Input()

        # Create new board.
        self.board = Board()
        self.game_board_spawn_location = Coord(self.board.size.x // 2, 0)
        self.next_shape_spawn_location = Coord((0.3 + self.board.size.x), 2)

        # Load tile image from resources.
        self.tile_texture = pygame.image.load('assets/img/tile.png')

        # Load sound effects
        self.sound_effect_score = pygame.mixer.Sound("assets/sound/score_achiveved.wav")
        self.sound_effect_score.set_volume(min(self.sound_effect_score.get_volume() * 0.25, 1.0))
        self.sound_effect_game_over = pygame.mixer.Sound("assets/sound/game_over.wav")
        self.sound_effect_game_over.set_volume(min(self.sound_effect_game_over.get_volume() * 0.5, 1.0))

        # Create sprite and scale it to self.cell_size size in pixels.
        self.tile_texture = pygame.transform.scale(self.tile_texture, (self.tile_size, self.tile_size))

        # Preload textures for every color.
        i = 0
        for color in self.__colors:
            tile_texture = self.tile_texture.copy()
            self.__tile_textures[i] = tile_texture
            tile_texture.fill(color, None, pygame.BLEND_MULT)

            i = i + 1

        # Define first 2 shapes.
        self.active_shape = Shape(self.__random_color(), self.game_board_spawn_location)
        self.next_shape = Shape(self.__random_color(), self.next_shape_spawn_location)

    def reset_game(self):
        """
        Reset game and prepare for new game.
        """
        self.save_top_score()

        # Load new random shapes.
        self.load_next_shape()
        self.load_next_shape()

        self.board = Board()
        self.input = Input()
        self.score = 0
        self.level_up_score = self.DEFAULT_LEVEL_UP_SCORE
        self.pause = False
        self.game_over = False

    def save_top_score(self):
        """
        Save top score using interface.
        """

        old_top_score = ScoreManager.get_score()
        if self.score > old_top_score:
            if ScoreManager.save_score(self.score):
                print("Written new top score: " + str(ScoreManager.get_score()))
            else:
                print("New score " + str(self.score) + " cannot be written! Top score is: " + str(
                    ScoreManager.get_score()))

    def run(self):
        """
        Run game stuff.
        :return:
        """

        # Some debug stuff
        # old_top_score = ScoreManager.get_score()
        # print("Current top score: " + str(old_top_score))

        pygame.init()
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

        self.save_top_score()

        return ApplicationState.APPLICATION_STATE_MENU

    def update(self, delta_time):
        """
        Update game state using delta_time and system events.
        :param delta_time: Delta time
        :return:
        """

        # Update input
        self.input.update(delta_time)

        # Reset game
        if self.game_over and self.input.is_pausing():
            self.reset_game()
            return

        # Pause
        if self.input.is_pausing():
            self.pause = not self.pause

        if self.pause or self.game_over:
            return

        # Inc timer
        self.timer += delta_time

        # Movement using timer.
        if self.timer > self.actual_update_interval:
            # Reset timer and make the movement.
            self.timer = 0
            movement = self.active_shape.move_down(self.board)

            # movement was not succesful
            if movement is False:
                self.load_next_shape()

        # Movement and rotation input handle.
        if self.input.is_moving_left():
            movement = self.active_shape.move_left(self.board)
        elif self.input.is_moving_right():
            movement = self.active_shape.move_right(self.board)
        elif self.input.is_rotating():
            movement = self.active_shape.rotate_shape(self.board)

        # Speeding up
        if self.input.is_speeding_up():
            self.actual_update_interval = self.update_interval * self.speed_up
        else:
            self.actual_update_interval = self.update_interval

        # Increse score.
        achieved_score = self.board.update(delta_time)
        self.score += achieved_score

        if achieved_score > 0:
            self.sound_effect_score.play()

            # Leveling up
            if self.score >= self.level_up_score:
                # Setup score for next level up
                self.level_up_score *= self.LEVEL_UP_QUOCIENT
                # Update speed up for current level
                self.speed_up *= self.SPEED_UP_QUOCIENT
                # Update interval. Update interval must be greater than self.MIN_UPDATE_INTERVAL
                self.update_interval = max(self.update_interval - self.UPDATE_INTERVAL_STEP, self.MIN_UPDATE_INTERVAL)

    def load_next_shape(self):
        """
        Save active shape and mark next_shape as active.
        Generated new random next_shape.
        :return:
        """

        # Store current shape into board.
        self.active_shape.store(self.board)

        # Make next shape active
        self.active_shape = self.next_shape
        # Set correct spawn location
        self.active_shape.location = self.game_board_spawn_location
        # generate new next shape
        self.next_shape = Shape(self.__random_color(), self.next_shape_spawn_location)

        # If game ends right now.
        if self.active_shape.check_collisions(self.board) != 0 and self.game_over is False:
            # Game ends now.
            self.game_over = True

            self.sound_effect_game_over.play()

    def draw(self):
        """
        Draw game in Pygame window.
        """
        self.surface.fill((0, 0, 0))
        self.draw_matrix()
        pygame.draw.rect(self.surface, (255, 140, 0),
                         (0, 0, self.board.size.x * self.tile_size, self.board.size.y * self.tile_size), 2)

        # Draw shapes and board.
        self.active_shape.draw(self.surface, self.__tile_textures[self.active_shape.color], self.tile_size)
        self.next_shape.draw(self.surface, self.__tile_textures[self.next_shape.color], self.tile_size)
        self.board.draw(self.surface, self.__tile_textures, self.tile_size)

        # Render score text
        font = pygame.font.Font(self.__font, 32)
        text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.surface.blit(text, (10, 5 + self.board.size.y * self.tile_size))

        # Render next text
        text = font.render("Next: ", True, (255, 255, 255))
        self.surface.blit(text, (10 + self.board.size.x * self.tile_size, 5))

        # Render pause-game layer
        if self.pause:
            self.render_text_in_center(self.surface, self.pause_text)

        # Render game-over layer
        elif self.game_over:
            self.render_text_in_center(self.surface, self.game_over_title)
            self.surface.blit(self.game_over_desc,
                              (((self.board.size.x / 2.0) * self.tile_size) - (self.game_over_desc.get_width() / 2.0),
                               ((self.board.size.y / 2.0) * self.tile_size) - (
                                       self.game_over_desc.get_height() / 2.0) + 80))

        pygame.display.update()

    def render_text_in_center(self, surface: pygame.Surface, text):
        surface.blit(text, (((self.board.size.x / 2.0) * self.tile_size) - (text.get_width() / 2.0)
                            , ((self.board.size.y / 2.0) * self.tile_size) - (text.get_height() / 2.0)))

    def draw_matrix(self):
        """
        Draw matrix.
        """
        color = (64, 64, 64)

        for i in range(self.board.size.x + 1):
            pygame.draw.line(self.surface, color, (i * self.tile_size, 0),
                             (i * self.tile_size, self.board.size.y * self.tile_size), 1)

        for i in range(self.board.size.y + 1):
            pygame.draw.line(self.surface, color, (0, i * self.tile_size),
                             (self.board.size.x * self.tile_size, i * self.tile_size), 1)

    @staticmethod
    def __random_color():
        """
        Return random color index in __colors.
        @:returns Random color.
        """

        # Generate random index in color list - We want new random color.
        random_index = randint(0, len(Game.__colors) - 1)

        return random_index
