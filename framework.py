import pygame
import sys
import os
from menu import *


class Player(object):
	s = pygame.Surface((50,50)) # create 50px by 50px surface
	s.fill((33,66,99)) # surface color blue
	r = s.get_rect() # rectangle bounds for the surface

	speed = [0, 0] # initial speed is 0

	def left(self):
		self.speed[0] -= 4

	def right(self):
		self.speed[0] += 4

	def up(self):
		self.speed[1] -= 4

	def down(self):
		self.speed[1] += 4

	def move(self):
		self.r = self.r.move(self.speed) # move the square


class Enemy(pygame.sprite.Sprite):
	# constructor for this class
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) # call the parent class constructor
		self.image = pygame.image.load(os.path.join('images', 'ball.png')) # load the PNG
		self.rect = self.image.get_rect() # get the rect of this sprite
		# self.rect.topleft = 0, 0


def event_loop():
	screen = pygame.display.get_surface() # get the pygame screen
	clock = pygame.time.Clock() # make a clock
	
	player = Player()
	enemy = Enemy()

	while 1: # game loop
	    for event in pygame.event.get():
	        if event.type == pygame.QUIT:
	            sys.exit()

	        elif event.type == pygame.KEYDOWN:
	        	if event.key == pygame.K_LEFT:
	        		player.left()
	        	elif event.key == pygame.K_RIGHT:
	        		player.right()
	        	elif event.key == pygame.K_UP:
	        		player.up()
	        	elif event.key == pygame.K_DOWN:
	        		player.down()

	        elif event.type == pygame.KEYUP:
	        	if event.key == pygame.K_LEFT:
	        		player.right()
	        	elif event.key == pygame.K_RIGHT:
	        		player.left()
	        	elif event.key == pygame.K_UP:
	        		player.down()
	        	elif event.key == pygame.K_DOWN:
	        		player.up()
	    
	    player.move() # move the player
	    
	    screen.fill((0,0,0)) # black background
	    screen.blit(player.s, player.r) # render the surface onto the rectangle
	    pygame.display.flip() # update the screen

	    clock.tick(30) # limit to 30 FPS

def main():
	pygame.init() # initialize pygame

	size = width, height = 480, 480 # size of window
	screen = pygame.display.set_mode(size) # create the window

	pygame.display.set_caption("Example Framework") # set the window title

	# create the menu
	menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                 [('Start Game',   1, None),
                  ('Other Option', 2, None),
                  ('Exit',         3, None)])
	menu.set_center(True, True) # center the menu
	menu.set_alignment('center', 'center') # center the menu

	# state variables for the finite state machine menu
	state = 0
	prev_state = 1

	pygame.event.set_blocked(pygame.MOUSEMOTION) # ignore mouse for efficiency
	rect_list = [] # only update certain rects for efficiency

	while 1:
		# check if the state has changed, if it has, then post a user event to
		# the queue to force the menu to be shown at least once
		if prev_state != state:
			pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
			prev_state = state

		# get the next event
		e = pygame.event.wait()

		# update the menu
		if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
			if state == 0:
				# "default" state
				rect_list, state = menu.update(e, state)
			elif state == 1:
				# start the game
				event_loop()
			elif state == 2:
				# just to demonstrate how to make other options
				pygame.display.set_caption("y u touch this") # change the window title
				state = 0 # reset the state
			else:
				# exit the game and program
				pygame.quit()
				sys.exit()

			# quit if the user closes the window
			if e.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			# update the screen
			pygame.display.update(rect_list)

if __name__ == '__main__':
	main()