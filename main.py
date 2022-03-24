#from venv import create
import pygame
import random
from words import WORDS

pygame.init()

# Screen set up
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
gray = (128, 128, 128)
WIDTH = 500
HEIGHT = 800

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Wordle")
turn = 0
board = [[" ", " ", " "," ", " "],
        [" ", " ", " "," ", " "],
        [" ", " ", " "," ", " "],
        [" ", " ", " "," ", " "],
        [" ", " ", " "," ", " "],
        [" ", " ", " "," ", " "]]

fps = 60
timer = pygame.time.Clock()
title_font = pygame.font.SysFont('arial', 50)

secret_word = WORDS[random.randint(0, len(WORDS)-1)]
letter = 0
turn_active = True
game_over = False

def create_board():
    global turn
    global board
    for col in range(0, 5):
        for row in range(0, 6):
            pygame.draw.rect(screen, white, [col * 100 + 12, row * 100 + 12, 75, 75], 3, 0)
            piece_text = title_font.render(board[row][col], True, gray)
            screen.blit(piece_text, [col* 100 + 30, row * 100 + 25])


    # Adds a green box for the current turn
    #pygame.draw.rect(screen, green, [5, turn * 100 + 5, WIDTH - 10, 90], 3, 5)

def check_answer():
    global turn 
    global board
    global secret_word

    for col in range(0, 5):
        for row in range(0, 6):
            if secret_word[col] == board[row][col] and turn > row:
                pygame.draw.rect(screen, green, [col * 100 + 12, row * 100 + 12, 75, 75], 0, 0)
            elif board[row][col] in secret_word and turn > row:
                pygame.draw.rect(screen, yellow, [col * 100 + 12, row * 100 + 12, 75, 75], 0, 0)
    pass




running = True
while running:
    timer.tick(fps)
    screen.fill(black)
    check_answer()
    create_board()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and letter > 0:
                board[turn][letter - 1] = ' '
                letter -= 1

            if event.key == pygame.K_RETURN and not game_over and letter == 5:
                turn += 1
                letter = 0

            if event.key == pygame.K_RETURN and game_over:
                turn = 0
                letter = 0
                game_over = False
                secret_word = WORDS[random.randint(0, len(WORDS)-1)]
                board = [[" ", " ", " "," ", " "],
                        [" ", " ", " "," ", " "],
                        [" ", " ", " "," ", " "],
                        [" ", " ", " "," ", " "],
                        [" ", " ", " "," ", " "],
                        [" ", " ", " "," ", " "]]

        if event.type == pygame.TEXTINPUT and turn_active and not game_over:
            entry = event.__getattribute__('text')
            board[turn][letter] = entry
            letter += 1


    for row in range(0, 6):
        guess = board[row][0] + board[row][1] + board[row][2] + board[row][3] + board[row][4]
        if guess == secret_word and row < turn:
            game_over = True


    if letter == 5:
        turn_active = False
    if letter < 5:
        turn_active = True

    if turn == 6:
        game_over = True
        loser_text = title_font.render("The word is " + secret_word, True, white)
        screen.blit(loser_text, [40, 610])
    
    if game_over and turn < 6:
        winner_text = title_font.render("Winner", True, white)
        screen.blit(winner_text, [40, 610])
    

    pygame.display.flip()
pygame.quit()