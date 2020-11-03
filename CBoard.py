class CBoard:
    size = (0, 0)
    matrix = None

    def __init__(self, board_size=(15, 20)):
        self.board_size = board_size

        # Define game board size and create 2D array.
        # self.game_board = [[0] * cols] * rows
        self.game_board = [[0] * self.board_size[0]] * self.board_size[1]

    def cell_is_out_of_board(self, coords):
        """
        Is given cell out of this board?
        :param coords: Cell coords.
        :return: True - Cell is out of board.
        """

        if coords[0] < 0 or coords[0] >= self.size[0] or coords[1] < 0 or coords[1] >= self.size[1]:
            return True
        else:
            return False

    def cell_is_free(self, coords):
        """
        Is cell in given coord free?
        :param coords: Cell coords.
        :return: True - The cell is free.
        """

        # Given cell must be inside board matrix.
        if self.cell_is_out_of_board(coords):
            raise Exception("Sorry, invalid coords argument.")

        return self.matrix[coords[0], coords[1]]
