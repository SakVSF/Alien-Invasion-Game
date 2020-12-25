class Settings:
	"""A class to store all settings for Alien Invasion"""

	def __init__(self):
		"""Initialize the game's  static settings"""
		#Screen Settings
		self.screen_width = 1200
		self.screen_height = 650
		self.bg_color = (230, 230, 230)

		#Ship settings
		self.ship_limit = 3
		
		# Bullet settings
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)  #dark gray
		self.bullets_allowed = 3 #limiting the number of bullets at a time

		#Alien Settings
		self.fleet_drop_speed = 10 #controls how quickly the fleet drops down the screen each time an alien reaches either edge
		
		#How quickly the game speeds up
		self.speedup_scale = 2

		#How quickly the alien point values increase
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize the settings that change throughout the game"""
		self.ship_speed = 1.5
		self.bullet_speed = 3.0
		self.alien_speed = 1.0

		#fleet_direction of 1 represents right; -1 represents left
		self.fleet_direction = 1

		#Scoring
		self.alien_points = 50 #default value when alien is shot down

	def increase_speed(self):
		"""Increase the speed settings and alien point values"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)

