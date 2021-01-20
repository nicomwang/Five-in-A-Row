import socket
import pygame
from threading import Thread
import sys
import os
from game import Gomoku

pygame.init()  # initialize pygame and pygame.font
startBackground = pygame.image.load(os.path.join("img", "background.jpg"))


def main():
    status = 0  # status, continue to play when status = 0, stop when status = 1
    pygame.display.set_caption('Network Programming Project: Gomoku')
    window_width = 640
    window_height = 640
    screen = pygame.display.set_mode([window_width, window_height])  # Initialize a window for display
    screen.fill([218, 165, 105])  # fill background color
    play_gomoku = Gomoku()
    play_gomoku.draw_board(screen)
    pygame.display.flip()  # refresh board

    def start_game(row, column):
        nonlocal status, is_black, is_recv
        # print(row, column)
        if status == 0:
            if play_gomoku.move(row, column, is_black):
                # refresh the game
                play_gomoku.draw_board(screen)
                pygame.display.flip()
                if play_gomoku.winner(row, column):
                    my_font = pygame.font.SysFont('comicsansms', 60)
                    # determine the winner
                    if is_black:
                        text = my_font.render('b l a c k   w i n s !', True, (255, 0, 0))
                    else:
                        text = my_font.render('w h i t e   w i n s !', True, (255, 0, 0))
                    screen.blit(text, (80, 280))
                    pygame.display.flip()
                    # is_black = True
                    # is_recv = False
                    status = 1
                is_black = not is_black

    class ClientRecv(Thread):
        def __init__(self, client):
            super().__init__()
            self.client = client

        def run(self):
            nonlocal is_recv
            while True:
                try:
                    data = self.client.recv(1024)
                    if not data:
                        break
                    is_recv = True
                    text = data.decode('utf-8')
                    row, column = eval(text)  # convert (x,y)
                    start_game(row, column)
                except Exception:
                    break

    is_black = True  # check if received a black stone
    is_recv = False  # check if received data
    index = 0  # when index is 0, it is the first time placing a stone, so there is no receive
    running = True

    host = '127.0.0.1'
    port = 5000
    client_socket = socket.socket()
    client_socket.connect((host, port))

    ClientRecv(client_socket).start()

    while running:
        for event in pygame.event.get():
            # if play click on 'x' to close window
            if event.type == pygame.QUIT:
                client_socket.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                i, j = event.pos[0], event.pos[1]
                if event.button == 1:
                    x, y = event.pos  # get current position of mouse
                    row = round((y - 40) / 40)  # convert mouse coordinates to board coordinates
                    column = round((x - 40) / 40)
                    if (is_recv or index == 0) and play_gomoku.board[row][column] == 0:
                        start_game(row, column)
                        index = 1
                        client_socket.send(('(%d, %d)' % (row, column)).encode('utf-8'))  # send data
                        is_recv = False

'''
Menu screen idea came from this youTube pygame tutorial. 
We modified it and added a background image 
https://www.youtube.com/watch?v=VV31Z-H075M&t=396s
'''
def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        window_width = 640
        window_height = 640
        screen = pygame.display.set_mode([window_width, window_height])
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (0, 0, 0))  # display text in black
        screen.blit(startBackground, (0, 0))  # display image
        screen.blit(text, (300, 500))  # position of text
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()
