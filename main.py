#imports all necessary modules
import pygame, sys
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser
from button import Button
import random
#Initiatizes pygame
pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menu")

BG = pygame.transform.scale(pygame.image.load("assets/Background.png").convert_alpha(), (width,height))
TV = pygame.transform.scale(pygame.image.load('tv.png').convert_alpha(), (width, height))
main = True
run = False
score = 0

#acquires font file from assets subfolder
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def gameover(menu, main, run, score):
  #sets caption to 'game over' 
  pygame.display.set_caption('Game Over')
  GM = pygame.transform.scale(pygame.image.load("assets/game_over.png").convert_alpha(), (width, height))
  pygame.display.set_mode((1280, 720))
  
  while True:
    #retracts cursor position using .get_pos()
    menuMousePos = pygame.mouse.get_pos()
    #game over menu title set to 'try again'
    menuText = get_font(80).render("TRY AGAIN", True, "white")
    #declares rect value and draws a rectangle starting from center position(640, 100)
    menuRect = menuText.get_rect(center=(640, 100))
    #shows score from previous game (stored in "score")
    prevScoreText = get_font(50).render(f"SCORE: {score}", True, (255, 255, 255))
    #restart button function, using play rect from previous game, still in development***
    restartButton = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 225), 
                            textInput="BACK TO MAIN MENU", font=get_font(50), baseColor="white", hoveringColor="#999999")
    playButton = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            textInput="PLAY", font=get_font(50), baseColor="white", hoveringColor="#999999")
    #quit button image loads, sets text display to 'quit' and the base colour to white
    quitButton = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 450), 
                            textInput="QUIT", font=get_font(50), baseColor="white", hoveringColor="#999999")

    screen.blit(menuText, menuRect)
    screen.blit(prevScoreText, (width - prevScoreText.get_width() - 450, 550))
    score = score

    #when the button is hovered over and is clicked, screen is updated and redraws from pos 0, 0
    for button in [quitButton]:
        button.changeColor(menuMousePos)
        button.update(screen)
    for button in [restartButton]:
        button.changeColor(menuMousePos)
        button.update(screen)
    for event in pygame.event.get():
        #if the event type is quit, pygame stops and game exits
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #when mouse cursor is moved checks for input in restart and quit, restart = runs game again, quit = pygame stops and sys exit
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restartButton.checkForInput(menuMousePos): 
              menu(run, main)
              if playButton.checkForInput(menuMousePos):
                run = True
                main = False
                return run, main
            if quitButton.checkForInput(menuMousePos):
              pygame.quit()
              sys.exit()

    #updates display
    pygame.display.update()
    
#default variables


#Main menu system 
def menu(main, run):
  while main:
    screen.blit(BG, (0, 0))
    screen.blit(TV, (0, 0))
  
    #almost all of this stuff is explained before, use gameover function for ref
    menuMousePos = pygame.mouse.get_pos()
    #b68f40 line 43 end, if added remove 41 and 42
    menuText = get_font(80).render("ALIEN SHOOTOUT", True, "white")
    menuRect = menuText.get_rect(center=(640, 100))
    prevScoreText = get_font(50).render(f"SCORE: {score}", True, (255, 255, 255))
    playButton = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            textInput="PLAY", font=get_font(50), baseColor="white", hoveringColor="#999999")
    quitButton = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 400), 
                            textInput="QUIT", font=get_font(50), baseColor="white", hoveringColor="#999999")
  
    screen.blit(menuText, menuRect)
    screen.blit(prevScoreText, (width - prevScoreText.get_width() - 450, 550))
  
    for button in [playButton, quitButton]:
        button.changeColor(menuMousePos)
        button.update(screen)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if playButton.checkForInput(menuMousePos):
              run = True
              main = False
              return run, main 
            if quitButton.checkForInput(menuMousePos):
                pygame.quit()
                sys.exit()
  
    pygame.display.update()
returnValues = menu(main, run)
run = returnValues[0]
main = returnValues[1]
#Game run
if run:
  pygame.display.set_caption('Alien Shootout')
  #OOP, AJ should explain this part as I am not too familiar with this topic
  class Game:

    def __init__(self, main, run):
      # Player setup
      playerSprite = Player((screenWidth / 2,screenHeight),screenWidth, 5)
      self.player = pygame.sprite.GroupSingle(playerSprite)
  
  		# health and score setup, change when submitting
      self.lives = 1
      self.liveSurf = pygame.image.load('player.png').convert_alpha()
      self.liveXStartPos = screenWidth - (self.liveSurf.get_size()[0] * 2 + 20)
      self.score = 0
      self.font = pygame.font.Font('Pixeled.ttf',20)
    
      # Obstacle setup
      self.shape = obstacle.shape
      self.blockSize = 6
      self.blocks = pygame.sprite.Group()
      self.obstacleAmount = 4
      self.obstacleXPositions = [num * (screenWidth / self.obstacleAmount) for num in range(self.obstacleAmount)]
      self.create_multiple_obstacles(*self.obstacleXPositions, xStart = screenWidth / 15, yStart = 480)
    
      # Alien setup
      self.aliens = pygame.sprite.Group()
      self.alienLasers = pygame.sprite.Group()
      self.alien_setup(rows = 6, cols = 8)
      self.alienDirection = 1
    
      # Extra setup
      self.extra = pygame.sprite.GroupSingle()
      self.extraSpawnTime = randint(40,80)
  
    #defines create obstacle with given parameters, checks for row_index and row, then iterates through to col_index and col
    #if col = x, sets x var to x_start + col index * block size + offset, likewise for y, just with row and without offset
    #block variable set to class obstacle.Block with args block_size, position, and x,y
    #adds block
    def create_obstacle(self, xStart, yStart,offsetX):
      for rowIndex, row in enumerate(self.shape):
        for colIndex,col in enumerate(row):
          if col == 'x':
            x = xStart + colIndex * self.blockSize + offsetX
            y = yStart + rowIndex * self.blockSize
            block = obstacle.Block(self.blockSize,(241,79,80),x,y)
            self.blocks.add(block)
  
    #creates multiple obstacles using create obstacle for every x offset in offset
    def create_multiple_obstacles(self,*offset,xStart,yStart):
      for offsetX in offset:
        self.create_obstacle(xStart,yStart,offsetX)
  
    #creates aliens using x and y column and row indexes within the range of rows and columns
    #makes sure to not create aliens outside the given area
    def alien_setup(self,rows,cols,xDistance = 60,yDistance = 48,xOffset = 70, yOffset = 100):
      for rowIndex, row in enumerate(range(rows)):
        for colIndex, col in enumerate(range(cols)):
          x = colIndex * xDistance + xOffset
          y = rowIndex * yDistance + yOffset
          
          #if row_index = 0, creates alien with the Alien class and yellow image, 1st row from top
          if rowIndex == 0: alienSprite = Alien('yellow',x,y)
          #sets alien image to green on second row from top
          elif 1 <= rowIndex <= 2: alienSprite = Alien('green',x,y)
          #anything else is coloured with red alien image
          else: alienSprite = Alien('red',x,y)
          #adds aliens
          self.aliens.add(alienSprite)
  
    #if alien position hits the end of the screen, moves down aliens one row
    def alien_position_checker(self):
      allAliens = self.aliens.sprites()
      for alien in allAliens:
        if alien.rect.right >= screenWidth:
          self.alienDirection = -1
          self.alien_move_down(2)
        elif alien.rect.left <= 0:
          self.alienDirection = 1
          self.alien_move_down(2)
  
    #moves down aliens by adding distance to alien.rect.y
    def alien_move_down(self,distance):
      if self.aliens:
        for alien in self.aliens.sprites():
          alien.rect.y += distance
  
    #alien shoots laser using Laser class and adds lasers to alien artillery
    def alien_shoot(self):
      if self.aliens.sprites():
        randomAlien = choice(self.aliens.sprites())
        laserSprite = Laser(randomAlien.rect.center,6,screenHeight)
        self.alienLasers.add(laserSprite)
        
    #not sure entirely what this function is for
    def extra_alien_timer(self):
      self.extraSpawnTime -= 1
      if self.extraSpawnTime <= 0:
        self.extra.add(Extra(choice(['right','left']),screenWidth))
        self.extraSpawnTime = randint(400,800)
  
    #checks if user collides with laser, if so, removes laser from visuals
    def collision_checks(self, score):
      # player lasers 
      if self.player.sprite.lasers:
        for laser in self.player.sprite.lasers:
          # obstacle collisions
          if pygame.sprite.spritecollide(laser,self.blocks,True):
            laser.kill()
            
  
          # alien collisions
          #if player laser hits alien, removes laser and adds score of alien value to score var
          aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
          if aliens_hit:
            for alien in aliens_hit:
              score += alien.value
            laser.kill()
  
          # extra collision
          #if laser hits ufo at top, adds 500 to score
          if pygame.sprite.spritecollide(laser,self.extra,True):
            score += 500
            laser.kill()
  
      # alien lasers 
      #if alien lasers collide with obstacles, removes laser and 1 pixel of the obstacle
      #if laser collides with player, -1 from lives, if lives hits 0, gameover function runs
      if self.alienLasers:
        for laser in self.alienLasers:
          # obstacle collisions
          if pygame.sprite.spritecollide(laser,self.blocks,True):
            laser.kill()
  
          if pygame.sprite.spritecollide(laser,self.player,False):
            laser.kill()
            self.lives -= 1
            if self.lives <= 0:
              gameover(menu, main, run, score)
              #pygame.quit()
              #sys.exit()
              
  
      # aliens
      #if alien collides with player, gamemover()
      #if alien collides with block, removes 1 layer of the obstacle
      if self.aliens:
        for alien in self.aliens:
          pygame.sprite.spritecollide(alien,self.blocks,True)
  
          if pygame.sprite.spritecollide(alien,self.player,False):
            gameover() 
            #pygame.quit()
            #sys.exit()

    #displays amount of lives left, shown bottom right of screen
    def display_lives(self):
      for live in range(self.lives - 1):
        x = self.liveXStartPos + (live * (self.liveSurf.get_size()[0] + 10))
        screen.blit(self.liveSurf,(x,8))
  
    #displays score top left of screen
    def display_score(self, score):
      scoreSurf = self.font.render(f'score: {score}',False,'white')
      scoreRect = scoreSurf.get_rect(topleft = (10,-10))
      screen.blit(scoreSurf,scoreRect)
  
    #if no more aliens are on screen, runs victory message and screen (bit buggy, doesn't run 100% of the time)
    def victory_message(self):
      if not self.aliens.sprites():
        victorySurf = self.font.render('You won',False,'white')
        victoryRect = victorySurf.get_rect(center = (screenWidth / 2, screenHeight / 2))
        screen.blit(victorySurf,victoryRect)
        menu(main, run)
  
    #runs main program, updates all functions and includes all necessary variables and functions to run
    def run(self):
      self.player.update()
      self.alienLasers.update()
      self.extra.update()
      
      self.aliens.update(self.alienDirection)
      self.alien_position_checker()
      self.extra_alien_timer()
      self.collision_checks(score)
      
      self.player.sprite.lasers.draw(screen)
      self.player.draw(screen)
      self.blocks.draw(screen)
      self.aliens.draw(screen)
      self.alienLasers.draw(screen)
      self.extra.draw(screen)
      self.display_lives()
      self.display_score(score)
      self.victory_message()
  
  #runtime class
  class CRT:
    #initiation, load tv border image and scale tv background with desired width and height amount
    def __init__(self):
      self.tv = pygame.image.load('tv.png').convert_alpha()
      self.tv = pygame.transform.scale(self.tv,(screenWidth,screenHeight))
  
    #creates lines for crt and draws line on display in black
    def create_crt_lines(self):
      lineHeight = 3
      lineAmount = int(screenHeight / lineHeight)
      for line in range(lineAmount):
        yPos = line * lineHeight
        pygame.draw.line(self.tv,'black',(0,yPos),(screenWidth,yPos),1)
  
    #makes tv background slightly transparent, giving retro feel
    def draw(self):
      self.tv.set_alpha(randint(75,90))
      self.create_crt_lines()
      screen.blit(self.tv,(0,0))
  
  if __name__ == '__main__':
    pygame.init()
    screenWidth = 600
    screenHeight = 600
    screen = pygame.display.set_mode((screenWidth,screenHeight))
    clock = pygame.time.Clock()
    game = Game(main, run)
    crt = CRT()
  
    alienLaser = pygame.USEREVENT + 1
    pygame.time.set_timer(alienLaser,800)
  
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == alienLaser:
          game.alien_shoot()
        
        if event.type == pygame.KEYDOWN:
          if event.type == pygame.K_r:
            menu()

      screen.fill((30,30,30))  
      game.run()
      crt.draw() 
      pygame.display.flip()
      clock.tick(60)