import pygame

EMPTY = 0  # no stone
BLACK = 1  # black stone
WHITE = 2  # white stone
COLOR_BLACK = [0, 0, 0]  # define color for black stone
COLOR_WHITE = [255, 255, 255]  # define color for white stone


class Gomoku:

    def __init__(self):
        # size of the board: 15*15=225
        self._board = [[]] * 15
        self.reset()
        self.id = id

    def reset(self):
        for row in range(len(self.board)):
            self.board[row] = [EMPTY] * 15

    def draw_board(self, screen):
        # fill background color
        screen.fill([218, 165, 105])

        # draw board
        for i in range(1, 16):
            # draw lines
            pygame.draw.line(screen, COLOR_BLACK, [40, i * 40], [600, i * 40], 1)
            pygame.draw.line(screen, COLOR_BLACK, [i * 40, 40], [i * 40, 600], 1)
            # draw a rectangle to present a think line to make the board pretty
            pygame.draw.rect(screen, COLOR_BLACK, [36, 36, 568, 568], 4)
            # mark center and four special intersections on board
            pygame.draw.circle(screen, COLOR_BLACK, [320, 320], 3, 0)
            pygame.draw.circle(screen, COLOR_BLACK, [480, 160], 3, 0)
            pygame.draw.circle(screen, COLOR_BLACK, [160, 480], 3, 0)
            pygame.draw.circle(screen, COLOR_BLACK, [480, 480], 3, 0)
            pygame.draw.circle(screen, COLOR_BLACK, [160, 160], 3, 0)

        # get coordinates
        for row in range(len(self._board)):
            for column in range(len(self._board[row])):
                # draw the stone on board
                if self._board[row][column] != EMPTY:
                    c_color = COLOR_BLACK if self._board[row][column] == BLACK else COLOR_WHITE
                    pos = [40 * (column + 1), 40 * (row + 1)]
                    pygame.draw.circle(screen, c_color, pos, 20, 0)

    @property
    def board(self):
        return self._board

    def move(self, row, column, is_black):
        if 0 <= row <= 14 and 0 <= column <= 14:
            if self._board[row][column] == EMPTY:
                if is_black:
                    self._board[row][column] = BLACK
                else:
                    self._board[row][column] = WHITE
                return True
        return False

    # clear board
    def clear(self, screen):
        self._board = [[0] * 15 for _ in range(15)]

    def winner(self, row, column):
        list1 = [
            [[0, -1], [0, 1]],
            [[-1, 0], [1, 0]],
            [[-1, -1], [1, 1]],
            [[-1, 1], [1, -1]]
        ]
        for i in range(4):
            count = 1
            for j in range(2):
                temp1 = row
                temp2 = column
                while True:
                    temp1 += list1[i][j][0]
                    temp2 += list1[i][j][1]
                    if 0 <= temp1 <= 14 and 0 <= temp2 <= 14:
                        if self._board[row][column] == self._board[temp1][temp2]:
                            count += 1  # if stones are next to each other and have the same color
                        else:
                            break  # end while loop if one or more is not the same color
                            # then check same the line but the opposite direction
                    else:
                        break
            if count >= 5:
                return True
        return False
