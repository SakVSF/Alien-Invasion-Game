import pygame.font  #writes text to screen
from pygame.sprite import Group
from ship import Ship              #for making a group of ships

class Scoreboard:
	"""A class to report scoring information"""
	def __init__(self, ai_game):
		"""Initialize scorekeeping attributes"""
		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats

		#Font setiings for scoring information
		self.text_color = (30,30,30)
		self.font = pygame.font.SysFont(None, 48)

		#Prepare the initial score image
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()


	def prep_score(self):
		"""Turn the score into a rendered image"""
		rounded_score = round(self.stats.score, -1)  #rounded to nearest 10
		score_str = "{:,}".format(rounded_score)    # output 1,000,000 instead of 1000000
		score_str = str(self.stats.score)
		score_str1 = "Score: " + score_str
		self.score_image = self.font.render(score_str1, True, self.text_color, self.settings.bg_color)


		#Display the score at the top rigjt of the screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20  #score displayed on  top right
		self.score_rect.top = 20

	def prep_high_score(self):
		"""Turn the high score into a rendered image"""
		high_score = round(self.stats.high_score, -1)   #round high score to the nearest 10
		high_score_str = "{:,}".format(high_score)
		high_score_str = str(high_score_str)
		high_score_str1 = "High Score: " + high_score_str
		self.high_score_image = self.font.render(high_score_str1, True,self.text_color, self.settings.bg_color)
		# Center the high score at the top of the screen.
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx   # high score on top center
		self.high_score_rect.top = self.score_rect.top

	def prep_ships(self):
		"""Show how many ships are left"""
		self.ships = Group()
		for ship_number in range(self.stats.ship_left):
			ship = Ship(self.ai_game)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)



	def show_score(self):
		"""Draw score and levels and ships to screen"""
		self.screen.blit(self.score_image, self.score_rect)
		#This method draws the score image onscreen at the location score_rect specifies
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)

	def check_high_score(self):
		"""Check to see if there's a new high score"""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()

	def prep_level(self):
		"""Turn the level into a rendered image"""
		level_str = str(self.stats.level)
		level_str1 = "Level: " + level_str
		self.level_image = self.font.render(level_str1, True,self.text_color, self.settings.bg_color)
		
    
		# Position the level below the score.
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10
