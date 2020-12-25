import pygame 
from pygame.sprite import Sprite

class Ship(Sprite):
	"""A class to manage the ship"""

	def __init__(self, ai_game):  #ai_game is the current instance of class Alien_invasion
		"""Initialize the ship and set its starting position"""

		super().__init__()
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()  #get_rect() gets the rect attribute of the screen(every element is considered as a rectangle) 
		self.settings = ai_game.settings

		#Load the ship image and get its rect.
		self.image = pygame.image.load('images/ship.bmp')  #to load the image 
		self.rect = self.image.get_rect()                  #to store the rect attribute of the image as the rect att. of the ship 

		#Start each new ship at the bottom center of the screen
		self.rect.midbottom = self.screen_rect.midbottom

		# Store a decimal value for the ship's horizontal position.
		self.x = float(self.rect.x)

		#Movement flags
		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""Update the ship's position based on movement flags."""
		# Update the ship's x value, not the rect.
		if self.moving_right and self.rect.right < self.screen_rect.right:  #the ship stops at the right edge 
			self.x += self.settings.ship_speed
		if self.moving_left  and self.rect.left > 0:           #again, so that the ship does not disaapear across the left edge
			self.x -= self.settings.ship_speed

		# Update rect object from self.x.
		self.rect.x = self.x

	def blitme(self):
		"""Draw the ship at its current location"""
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""Center the ship on the screen"""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)