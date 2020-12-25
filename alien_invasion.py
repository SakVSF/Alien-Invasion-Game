import sys #For sys.exit() 
from time import sleep       #pause the game for a moment when the ship is hit. 
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullets import Bullet
from alien import Alien
import pygame  #Essential for making a game

class AlienInvasion:
	"""Overall class to manage game assets and behavior."""

	def __init__(self):
		"""Initialize the game, and create game resources."""

		pygame.init()  #Initializing the background settings

		self.settings = Settings()   # Creating an instance of Class Settings

		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))   #The entire game window will be redrawn on each pass

		pygame.display.set_caption("Alien Invasion")

		#Create an instance to store game statistics
		self.stats = GameStats(self)

		#Create a coreboard
		self.sb = Scoreboard(self)
		
		#To give Ship access to game resources like screen
		self.ship = Ship(self)   #call to Ship() required an instance- 'self'

		self.bullets = pygame.sprite.Group() #a list to store all the live bullets so we can manage the bullets that have already been fired - to access bullets.py
	
		self.aliens = pygame.sprite.Group()  # to access aliens.py

		self._create_fleet()

		#make the Play button
		self.play_button = Button(self, "Play")
	


	def run_game(self):

		"""Start the main loop for the game"""
		while True:
			self._check_events()  #checks for player input

			if self.stats.game_active :
				self.ship.update()    #updates position of the ship 
			
				self._update_bullets()  #updates any bullets that have been fired

				self._update_aliens()

			self._update_screen()    #use updated position to drawnew screen


	def _check_events(self):  #helper method - starts with '_'

		#Watch for Keyboard and mouse actions by user
			for event in pygame.event.get():  #This fn returns list of detected events
				if event.type == pygame.QUIT:  #If the user decides to quit
					sys.exit()

				elif event.type == pygame.KEYDOWN:
					self._check_keydown_events(event)


				elif event.type == pygame.KEYUP:
 					self._check_keyup_events(event)

				elif event.type == pygame.MOUSEBUTTONDOWN:  # only mouseclicks for play button
 					mouse_pos = pygame.mouse.get_pos()
 					self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		"""Start a new game when a player clicks Play"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos) #whether the point of the mouse click overlaps the region defined by the Play button’s rect 
		if button_clicked and not self.stats.game_active : 
		  # button clicked while NOT playing the game 			
 			#Reset the game statistics
 			self.settings.initialize_dynamic_settings() 
 			self.stats.game_active = True
 			self.sb.prep_score() #score starts with 0 again
 			self.sb.prep_level() #level 1 again
 			self.sb.prep_ships() #restore 3 lives for ship

 			#Get rid of any remaining aliens and bullets
 			self.aliens.empty()
 			self.bullets.empty()

 			#Create a new fleet and center the ship
 			self._create_fleet()
 			self.ship.center_ship()
 			#hide the mouse cursor
 			pygame.mouse.set_visible(False)



	def _check_keydown_events(self, event):

 		"""Responds to keypresses."""
 		if event.key == pygame.K_RIGHT:
 			self.ship.moving_right = True
 		elif event.key == pygame.K_LEFT:
 			self.ship.moving_left = True
 		elif event.key == pygame.K_q:    #Quit by pressing Q
 			sys.exit()
 		elif event.key == pygame.K_SPACE: #fires bullet on pressing spacebar
 			self._fire_bullet()

	def _check_keyup_events(self, event):

		"""Responds to key releases"""
		if event.key == pygame.K_RIGHT:
 			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _fire_bullet(self):

		"""Create a new bullet and add it to the bullets group"""
		if len(self.bullets) < self.settings.bullets_allowed: 
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)


	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets"""
		#Update bullet positions

		self.bullets.update() # group automatically calls update() for each sprite(bullet) in the group.

		#Get rid of the bullets that have disappeared
		for bullet in self.bullets.copy():   #copy for the list
			if bullet.rect.bottom <= 0 :
				self.bullets.remove(bullet)   # as you are removing elements in the list while in the for loop, you have to use a copy for the loop


		self._check_bullet_alien_collisions()


	def _check_bullet_alien_collisions(self):
		"""Respond to bullet-alien collisions"""
		#Remove any bullets and aliens that may have collided
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
		"""compares the positions of all the bullets in
		self.bullets and all the aliens in self.aliens, and identifies any that overlap. If so,  groupcollide() adds a keyvalue pair to the dictionary it returns.
		The two True arguments tell Pygame to delete the bullets and aliens that have collided. The first argument is to make bullet disaooera(True) and 
		second argument is to make alien disappear."""
		if collisions:
			for aliens in collisions.values():
				self.stats.score +=self.settings.alien_points
				self.sb.prep_score()
				self.sb.check_high_score()

		if not self.aliens:
		#Destroy existing bullets and create new fleet.
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			#Increase level if a fleet is destroyed
			self.stats.level += 1
			self.sb.prep_level()


	def _update_aliens(self):
		"""Check if the fleet is at an edge, then update the positions of all aliens in the fleet."""
		self._check_fleet_edges()
		"""Update the positions of all alens in the fleet"""
		self.aliens.update()

		#Look for alien_ship collisions
		if pygame.sprite.spritecollideany(self.ship, self.aliens):    #Here, it loops through the group aliens and returns the first alien it finds that has collided with ship.
			self._ship_hit()

		#Look for aliens hitting bottom of the screen
		self._check_aliens_bottom()


	def _check_aliens_bottom(self):
		"""Check if any aliens have reached the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom :
				#Treat this same as if the ship got hit
				self._ship_hit()
				break

	def _ship_hit(self):
		"""Respond to the ship being hit by an alien"""
		if self.stats.ship_left > 0 :
			self.stats.ship_left -= 1   #Decrement ships_left
			self.sb.prep_ships()        #Update scoreboard

			#Get rid of any remaining aliens and bullets.
			self.aliens.empty()
			self.bullets.empty()

			#Create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#pause
			sleep(0.5)

		else : 
			self.stats.game_active = False
			pygame.mouse.set_visible(True)



	def _create_fleet(self):

		"""Create the fleet of aliens"""
		#Make an alien.
		alien = Alien(self)
		# Create an alien and find the number of aliens in a row.
		# Spacing between each alien is equal to one alien width.
		alien_width, alien_height = alien.rect.size 
		available_space_x = self.settings.screen_width - (2 * alien_width)   #empty margin on both sided
		number_aliens_x = available_space_x // (2 * alien_width)


		#Determine the number of rows of aliens that fit on the screen
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (3*alien_height) - ship_height) #2 aliens from bottom to give ship time to shoot, and 1 alien from the top 
		number_rows = available_space_y // (2*alien_height)

		# Create full fleet of aliens.
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)


	def _create_alien(self, alien_number, row_number):

			# Create an alien and place it in the row.
			alien=Alien(self)
			alien_width, alien_height = alien.rect.size
			
			#we multiply the alien width by 2 to account for the space each alien takes up
			#including the #empty space to its right, and we multiply this amount by the alien’s position
			##in the row. We use the alien’s x attribute to set the position of its rect.
			alien.x = alien_width + 2 * alien_width * alien_number 
			alien.rect.x = alien.x

			# Each row starts two alien heights below the previous row, so we multiply the alien height by two and then by the row
			# number. The first row number is 0, so the vertical placement of the first row
			# is unchanged. All subsequent rows are placed farther down the screen.
			alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
			self.aliens.add(alien)
			

	

	def _check_fleet_edges(self):
		"""Respond appropriately if fleet has reached an edge."""
		for alien in self.aliens.sprites():
			if alien.check_edges():          #returns true if alien has hit edge
				self._change_fleet_direction()
				break


	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleet's direction"""
		for alien in self.aliens.sprites():
			alien.rect.y +=self.settings.fleet_drop_speed   #drops the fleet by 10 pixels
		self.settings.fleet_direction *= -1                #changes the direction 


	def _update_screen(self): #helper method- update image on screen and flip to new screen

		# Redraw the screen during each pass through the loop.
			self.screen.fill(self.settings.bg_color) #we fill the screen with the background color using the fill() method, which acts on a surface
	        
			self.ship.blitme() #after filling the bckgd, so that the ship appears on top of it 

			for bullet in self.bullets.sprites():  #to draw all the bullets in the list
				bullet.draw_bullet()

			self.aliens.draw(self.screen)  #to draw aliens on the screen at the position acc. to rect attribute

			#Draw the score information
			self.sb.show_score()

			#Draw the play button if the game is inactive
			if not self.stats.game_active : 
				self.play_button.draw_button()

	         #Make the most recently drawn screen visible
			pygame.display.flip() # Continually updates the display for smooth illustration


	


if __name__ == '__main__': # Only if this file is called directly from main program
    ai = AlienInvasion() # Make a game instance
    ai.run_game()

