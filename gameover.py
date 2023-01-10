import pygame, sys
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser
from button import Button
import random



class Gameover():
    def game_over():
        width = 1280
        HEIGHT = 720
        SCREEN = pygame.display.set_mode((width, HEIGHT))
        pygame.display.set_caption("Game Over")

        def get_font(size): # Returns Press-Start-2P in the desired size
            return pygame.font.Font("assets/font.ttf", size)


        MENU_MOUSE_POS = pygame.mouse.get_pos()
        GAME_OVER_BUTTON = Button(image=pygame.image.load("assets/game_over.png"), pos=(640, 250), 
                                text_input="GAME OVER", font=get_font(50), base_color="white", hovering_color="#999999")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 400), 
                                text_input="QUIT", font=get_font(50), base_color="white", hovering_color="#999999")
        for button in [GAME_OVER_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()