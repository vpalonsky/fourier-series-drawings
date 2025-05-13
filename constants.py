import pygame, os
pygame.init()

# Windows sizw and fps
W_WIDTH = 800
W_HEIGHT = 600
FRAMERATE = 30

# Colors
BACKGROUND_COLOR = "black"
DRAWING_COLOR = "white"
TEXT_COLOR = "white"

# Text position and size
TEXT_TOP_MARGIN = 10
TEXT_LEFT_MARGIN = 10
TEXT_SEPARATION = 10
FONT_SIZE = 24

# Simulation parameters
CANT_VECTORS = 81 # amount of vectors to use to draw every shape of the SVG (needs to be odd)
STEPS = 100 # in how much points do you divide each shape of the SVG
DRAW_JUMP = 20
EXPAND_FACTOR = 6
mid_i = int(CANT_VECTORS/2)

# SVGs constants
SVGS_PATH = "svg_imgs"
SVGS = os.listdir(SVGS_PATH) if len(os.listdir(SVGS_PATH))>0 else ['']
SVG_INDEX = 0

# Pygame objects
surface = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
clock = pygame.time.Clock()
my_font = pygame.font.Font(None, FONT_SIZE)

class Vector():
	def __init__(self, cn: complex, initial_pos: complex):
		self.cn = cn
		self.start = initial_pos
		self.end = initial_pos

	def draw(self):
		startx = self.start.real+(W_WIDTH/2)
		starty = self.start.imag+(W_HEIGHT/2)
		endx = startx+self.end.real
		endy = starty+self.end.imag
		pygame.draw.line(surface, "white", (startx, starty), (endx, endy))