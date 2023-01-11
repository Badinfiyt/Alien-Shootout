import pygame, sys
from button import Button
import random
pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        menuMousePos = pygame.mouse.get_pos()

        menuText = get_font(100).render("MAIN MENU", True, "#b68f40")
        menuRect = menuText.get_rect(center=(640, 100))
        """color = ["red", "blue"]
        color = random.choice(color)"""
        playButton = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            textInput="PLAY", font=get_font(75), baseColor="#d7fcd4", hoveringColor = "White")
        quitButton = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            textInput="QUIT", font=get_font(75), baseColor="#d7fcd4", hoveringColor="White")

        screen.blit(menuText, menuRect)

        for button in [playButton, quitButton]:
            button.changeColor(menuMousePos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.checkForInput(menuMousePos):
                    play()
                if quitButton.checkForInput(menuMousePos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()