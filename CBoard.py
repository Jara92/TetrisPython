class CBoard:
    size = (0, 0)
    __matrix = []

    def __init__(self, board_size=(15, 20)):
        self.size = board_size

        # Define game board size and create 2D array.
        # self.game_board = [[0] * cols] * rows
        # self.__matrix = [[0] * self.size[0]] * self.size[1]
        self.__matrix = [[None for x in range(self.size[1])] for y in range(self.size[0])]

        # Fill new matrix by None value.
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.__matrix[i][j] = None

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

        # Given cell must be inside boards matrix.
        if self.cell_is_out_of_board(coords):
            return False
            #raise Exception("Sorry, invalid coords argument: " + str(coords))

        #print(str(coords))
        return self.__matrix[coords[0]][coords[1]] is None
