
import pygame, sys
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser
from button import Button
from gameover import Gameover
import random
#Initiation
pygame.init()

WIDTH = 1280
HEIGHT = 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

BG = pygame.transform.scale(pygame.image.load("assets/Background.png").convert_alpha(), (WIDTH,HEIGHT))
TV = pygame.transform.scale(pygame.image.load('tv.png').convert_alpha(), (WIDTH, HEIGHT))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def gameover():
  pygame.init()
  global main, run, score
  GM = pygame.transform.scale(pygame.image.load("assets/game_over.png").convert_alpha(), (WIDTH, HEIGHT))
  
  while True:  

    MENU_MOUSE_POS = pygame.mouse.get_pos()
    pygame.display.set_mode((1280, 720))
    SCREEN.blit(BG, (0, 0))
    SCREEN.blit(TV, (0, 0))
  
    MENU_MOUSE_POS = pygame.mouse.get_pos()
    #b68f40 line 43 end, if added remove 41 and 42
    MENU_TEXT = get_font(80).render("GAME OVER", True, "white")
    MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
    PREV_SCORE_TEXT = get_font(50).render(f"SCORE: {score}", True, (255, 255, 255))
    QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 400), 
                            text_input="QUIT", font=get_font(50), base_color="white", hovering_color="#999999")
  
    SCREEN.blit(MENU_TEXT, MENU_RECT)
    SCREEN.blit(PREV_SCORE_TEXT, (WIDTH - PREV_SCORE_TEXT.get_width() - 450, 550))
  
    for button in [QUIT_BUTTON]:
        button.changeColor(MENU_MOUSE_POS)
        button.update(SCREEN)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #if event.type == pygame.MOUSEBUTTONDOWN:
        if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
          pygame.quit()
          sys.exit()
  
    pygame.display.update()

main = True
run = False
score = 0

#Main menu system 
def menu(main, run):
  while main:
    SCREEN.blit(BG, (0, 0))
    SCREEN.blit(TV, (0, 0))
  
    MENU_MOUSE_POS = pygame.mouse.get_pos()
    #b68f40 line 43 end, if added remove 41 and 42
    MENU_TEXT = get_font(80).render("SPACE INVADERS", True, "white")
    MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
    PREV_SCORE_TEXT = get_font(50).render(f"SCORE: {score}", True, (255, 255, 255))
    PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(50), base_color="white", hovering_color="#999999")
    QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 400), 
                            text_input="QUIT", font=get_font(50), base_color="white", hovering_color="#999999")
  
    SCREEN.blit(MENU_TEXT, MENU_RECT)
    SCREEN.blit(PREV_SCORE_TEXT, (WIDTH - PREV_SCORE_TEXT.get_width() - 450, 550))
  
    for button in [PLAY_BUTTON, QUIT_BUTTON]:
        button.changeColor(MENU_MOUSE_POS)
        button.update(SCREEN)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
              run = True
              main = False
              return run, main 
            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()
  
    pygame.display.update()

run = menu(main, run)[0]
main = menu(main, run)[1]
#Game run
if run:
  pygame.display.set_caption('Space Invaders')
  class Game:

    def __init__(self):
      global main, run
      # Player setup
      player_sprite = Player((screen_width / 2,screen_height),screen_width, 5)
      self.player = pygame.sprite.GroupSingle(player_sprite)
  
  		# health and score setup
      self.lives = 3
      self.live_surf = pygame.image.load('player.png').convert_alpha()
      self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
      self.score = 0
      self.font = pygame.font.Font('Pixeled.ttf',20)
    
      # Obstacle setup
      self.shape = obstacle.shape
      self.block_size = 6
      self.blocks = pygame.sprite.Group()
      self.obstacle_amount = 4
      self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
      self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 15, y_start = 480)
    
      # Alien setup
      self.aliens = pygame.sprite.Group()
      self.alien_lasers = pygame.sprite.Group()
      self.alien_setup(rows = 6, cols = 8)
      self.alien_direction = 1
    
      # Extra setup
      self.extra = pygame.sprite.GroupSingle()
      self.extra_spawn_time = randint(40,80)
  
    def create_obstacle(self, x_start, y_start,offset_x):
      for row_index, row in enumerate(self.shape):
        for col_index,col in enumerate(row):
          if col == 'x':
            x = x_start + col_index * self.block_size + offset_x
            y = y_start + row_index * self.block_size
            block = obstacle.Block(self.block_size,(241,79,80),x,y)
            self.blocks.add(block)
  
    def create_multiple_obstacles(self,*offset,x_start,y_start):
      for offset_x in offset:
        self.create_obstacle(x_start,y_start,offset_x)
  
    def alien_setup(self,rows,cols,x_distance = 60,y_distance = 48,x_offset = 70, y_offset = 100):
      for row_index, row in enumerate(range(rows)):
        for col_index, col in enumerate(range(cols)):
          x = col_index * x_distance + x_offset
          y = row_index * y_distance + y_offset
          
          if row_index == 0: alien_sprite = Alien('yellow',x,y)
          elif 1 <= row_index <= 2: alien_sprite = Alien('green',x,y)
          else: alien_sprite = Alien('red',x,y)
          self.aliens.add(alien_sprite)
  
    def alien_position_checker(self):
      all_aliens = self.aliens.sprites()
      for alien in all_aliens:
        if alien.rect.right >= screen_width:
          self.alien_direction = -1
          self.alien_move_down(2)
        elif alien.rect.left <= 0:
          self.alien_direction = 1
          self.alien_move_down(2)
  
    def alien_move_down(self,distance):
      if self.aliens:
        for alien in self.aliens.sprites():
          alien.rect.y += distance
  
    def alien_shoot(self):
      if self.aliens.sprites():
        random_alien = choice(self.aliens.sprites())
        laser_sprite = Laser(random_alien.rect.center,6,screen_height)
        self.alien_lasers.add(laser_sprite)
        
    def extra_alien_timer(self):
      self.extra_spawn_time -= 1
      if self.extra_spawn_time <= 0:
        self.extra.add(Extra(choice(['right','left']),screen_width))
        self.extra_spawn_time = randint(400,800)
  
    def collision_checks(self):
      global score
      # player lasers 
      if self.player.sprite.lasers:
        for laser in self.player.sprite.lasers:
          # obstacle collisions
          if pygame.sprite.spritecollide(laser,self.blocks,True):
            laser.kill()
            
  
          # alien collisions
          aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
          if aliens_hit:
            for alien in aliens_hit:
              score += alien.value
            laser.kill()
  
          # extra collision
          if pygame.sprite.spritecollide(laser,self.extra,True):
            score += 500
            laser.kill()
  
      # alien lasers 
      if self.alien_lasers:
        for laser in self.alien_lasers:
          # obstacle collisions
          if pygame.sprite.spritecollide(laser,self.blocks,True):
            laser.kill()
  
          if pygame.sprite.spritecollide(laser,self.player,False):
            laser.kill()
            self.lives -= 1
            if self.lives <= 0:
              gameover()
              #pygame.quit()
              #sys.exit()
              
  
      # aliens
      if self.aliens:
        for alien in self.aliens:
          pygame.sprite.spritecollide(alien,self.blocks,True)
  
          if pygame.sprite.spritecollide(alien,self.player,False):
            gameover() 
            #pygame.quit()
            #sys.exit()

    def display_lives(self):
      for live in range(self.lives - 1):
        x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
        screen.blit(self.live_surf,(x,8))
  
    def display_score(self):
      global score
      score_surf = self.font.render(f'score: {score}',False,'white')
      score_rect = score_surf.get_rect(topleft = (10,-10))
      screen.blit(score_surf,score_rect)
  
    def victory_message(self):
      if not self.aliens.sprites():
        victory_surf = self.font.render('You won',False,'white')
        victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
        screen.blit(victory_surf,victory_rect)
        menu(main, run)
  
    def run(self):
      self.player.update()
      self.alien_lasers.update()
      self.extra.update()
      
      self.aliens.update(self.alien_direction)
      self.alien_position_checker()
      self.extra_alien_timer()
      self.collision_checks()
      
      self.player.sprite.lasers.draw(screen)
      self.player.draw(screen)
      self.blocks.draw(screen)
      self.aliens.draw(screen)
      self.alien_lasers.draw(screen)
      self.extra.draw(screen)
      self.display_lives()
      self.display_score()
      self.victory_message()
  
  class CRT:
    def __init__(self):
      self.tv = pygame.image.load('tv.png').convert_alpha()
      self.tv = pygame.transform.scale(self.tv,(screen_width,screen_height))
  
    def create_crt_lines(self):
      line_height = 3
      line_amount = int(screen_height / line_height)
      for line in range(line_amount):
        y_pos = line * line_height
        pygame.draw.line(self.tv,'black',(0,y_pos),(screen_width,y_pos),1)
  
    def draw(self):
      self.tv.set_alpha(randint(75,90))
      self.create_crt_lines()
      screen.blit(self.tv,(0,0))
  
  if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()
  
    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER,800)
  
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == ALIENLASER:
          game.alien_shoot()
        
        if event.type == pygame.KEYDOWN:
          if event.type == pygame.K_r:
            menu()

      screen.fill((30,30,30))  
      game.run()
      crt.draw() 
      pygame.display.flip()
      clock.tick(60)