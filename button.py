import pygame.font  #lets Pygame render text to the screen

class Button: 

	def __init__(self, ai_game, msg):   #msg contains button's text
		"""Initialize button attributes."""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
        
        # Set the dimensions and properties of the button.
		self.width, self.height = 200, 50
		self.button_color = (0, 255, 0)      #green
		self.text_color = (255, 255, 255)    #white
		self.font = pygame.font.SysFont(None, 48)
        
		# Build the button's rect object and center it.
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center
        
        # The button message needs to be prepped only once.
		self._prep_msg(msg)
		


	def _prep_msg(self, msg):
		"""Turn msg into a rendered image and center text on the button."""
		self.msg_image = self.font.render(msg, True, self.text_color,self.button_color)
		"""The call to font.render() turns the text stored in msg into an image.
		set antialiasing to True- (antialiasing makes the edges of the text smoother)"""
		self.msg_image_rect = self.msg_image.get_rect()   #centralize the text on the button
		self.msg_image_rect.center = self.rect.center


	def draw_button(self): 
		# Draw blank button and then draw message.
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)


