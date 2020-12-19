import pygame
from typing import Dict
from NamedTupples import Coord


class CBoard:
    """
    Game board.
    """
    size = Coord(0, 0)
    base_score = 50
    bonus_score = 250
    __matrix = []

    def __init__(self, board_size: Coord = Coord(15, 20)):
        self.size = board_size

        # Define game board size and create 2D array.
        # self.game_board = [[0] * cols] * rows
        # self.__matrix = [[0] * self.size[0]] * self.size[1]
        self.__matrix = [[-1 for x in range(self.size.y)] for y in range(self.size.x)]

        # Fill new matrix by None value.
        for i in range(self.size.x):
            for j in range(self.size.y):
                self.__matrix[i][j] = -1

    def cell_is_out_of_board(self, coords):
        """
        Is given cell out of this board?
        :param coords: Cell coords.
        :return: True - Cell is out of board.
        """

        if coords.x < 0 or coords.x >= self.size.x or coords.y < 0 or coords.y >= self.size.y:
            return True
        else:
            return False

    def cell_is_free(self, coords):
        """
        Is cell in given coord free?
        :param coords: Cell coords.
        :return: True - The cell is free.
        """

        # Given cell must be inside boards matrix.
        if self.cell_is_out_of_board(coords):
            return False
            # raise Exception("Sorry, invalid coords argument: " + str(coords))

        # print(str(coords))
        return self.__matrix[coords.x][coords.y] == -1

    def set_cell(self, coords: Coord, color: int):
        """
        Set given color in the cell.
        :param coords: Cell coords
        :param color: Color to be set.
        :return:
        """
        if self.cell_is_free(coords):
            self.__matrix[coords.x][coords.y] = color

    def update(self, delta_time: float):
        """
        Update game board.
        :param delta_time: Delta time.
        :return: Score to be achieved.
        """
        # Check rows while the row before was full
        score = 0
        y = self.size.y - 1
        running = True

        # While rows are full and y coord is ge 0
        while running and y >= 0:
            row_is_full = True
            # Check if row is full
            for i in range(self.size.x):
                # if there is one -1 item, the row is not full
                if self.__matrix[i][y] == -1:
                    row_is_full = False
                    break

            # We will increse score and shift board if row is full
            if row_is_full:
                score += self.shift_board(y)
            # In other cases will leave while cycle
            else:
                a = 5
                # running = False

            y = y - 1

        return score

    def shift_board(self, y: int):
        """
        Shift board and get score.
        :param y: Row num.
        :return: Score to be achieved.
        """
        single_color = True
        last_color = None
        # Check every row
        for y in range(y, 0, -1):
            # if there is another row over this row
            if y - 1 >= 0:
                # Move upper row down
                for x in range(self.size.x):
                    if last_color is not None and not last_color == self.__matrix[x][y]:
                        single_color = False

                    last_color = self.__matrix[x][y]

                    self.__matrix[x][y] = self.__matrix[x][y - 1]
            else:
                # Clear the last row
                for x in range(self.size.x):
                    self.__matrix[x][y] = -1

        # Return score based on row color
        # If the row has only one color then player gets bonus
        if single_color:
            return self.bonus_score
        else:
            return self.base_score

    def draw(self, surface: pygame.Surface, tile_textures: Dict, tile_size: int):
        """
        Draw the board using given pygame surface.
        :param surface: Pygame surface.
        :param tile_textures: Tile textures dict to be rendered.
        :param tile_size: One tile size
        :return:
        """
        for i in range(self.size.x):
            for j in range(self.size.y):
                if self.__matrix[i][j] != -1:
                    surface.blit(tile_textures[self.__matrix[i][j]], (i * tile_size, j * tile_size))
