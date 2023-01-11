import pygame 
from laser import Laser

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,constraint,speed):
		super().__init__()
		self.image = pygame.image.load('player.png').convert_alpha()
		self.rect = self.image.get_rect(midbottom = pos)
		self.speed = speed
		self.maxXConstraint = constraint
		self.ready = True
		self.laserTime = 0
		self.laserCooldown = 600

		self.lasers = pygame.sprite.Group()

		self.laserSound = pygame.mixer.Sound('laser.wav')
		self.laserSound.set_volume(0.5)

	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.rect.x += self.speed
		elif keys[pygame.K_LEFT]:
			self.rect.x -= self.speed

		if keys[pygame.K_SPACE] and self.ready:
			self.shoot_laser()
			self.ready = False
			self.laserTime = pygame.time.get_ticks()
			self.laserSound.play()

	def recharge(self):
		if not self.ready:
			currentTime = pygame.time.get_ticks()
			if currentTime - self.laserTime >= self.laserCooldown:
				self.ready = True

	def constraint(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		if self.rect.right >= self.maxXConstraint:
			self.rect.right = self.maxXConstraint

	def shoot_laser(self):
		self.lasers.add(Laser(self.rect.center,-8,self.rect.bottom))

	def update(self):
		self.get_input()
		self.constraint()
		self.recharge()
		self.lasers.update()