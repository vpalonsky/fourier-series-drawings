import pygame
from functions import read_svg_points, calc_vectors_cn
import cmath
import os

W_WIDTH = 800
W_HEIGHT = 600
FRAMERATE = 30
CANT_VECTORS = 81 # cantidad a utilizar para cada segmento cerrado del path (obligatoriamente impar)
STEPS = 100 # cantidad a utilizar para cada segmento cerrado del path
EXPAND_FACTOR = 6
SVGS_PATH = "svg_imgs"
DRAWING_COLOR = "blue"
BACKGROUND_COLOR = "black"
TEXT_TOP_MARGIN = 10
TEXT_LEFT_MARGIN = 10
TEXT_SEPARATION = 5
FONT_SIZE = 24
CONTROLS = [
	"Next/previous svg: Up/down arrow",
	"+20/-20 segment points: Right/left arrow",
	"+20/-20 vectors: Enter/tab",
	"Extend/contract svg: Space/backspace"
]

pygame.init()
surface = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
clock = pygame.time.Clock()
my_font = pygame.font.Font(None, FONT_SIZE)
mid_i = int(CANT_VECTORS/2)
svgs = os.listdir(SVGS_PATH)

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

def update_vectors(vectors: list[Vector], t):
	new_vectors = vectors
	for i in range(CANT_VECTORS):
		if i!=mid_i:
			n = i-mid_i
			new_vectors[i].end = new_vectors[i].cn*cmath.exp(complex(0, n*2*cmath.pi*t))*EXPAND_FACTOR

	for i in range(1, mid_i+1):
		i_fst = mid_i+i
		i_snd = mid_i-i

		new_vectors[i_fst].start = new_vectors[i_fst - (2*i-1)].start + new_vectors[i_fst - (2*i-1)].end
		new_vectors[i_snd].start = new_vectors[i_snd + (2*i)].start + new_vectors[i_snd + (2*i)].end

	return new_vectors

def abc(svg_index):
	actual_svg_path = os.path.join(SVGS_PATH, svgs[svg_index%len(svgs)])
	paths = read_svg_points(actual_svg_path)

	initial_vectors_cn = []
	draw_points_container = []
	vectors_container: list[list[Vector]] = []

	for path in paths:
		ft = lambda t : path.point(t)
		vectors_cn = calc_vectors_cn(CANT_VECTORS, STEPS, ft)
		initial_vectors_cn.append(vectors_cn)

	for j in range(len(paths)):
		path_vectors = []
		for i in range(CANT_VECTORS):
			path_vectors.append(Vector(initial_vectors_cn[j][i], complex(0, 0)))
		vectors_container.append(path_vectors)

	for vectors in vectors_container:
		vectors[mid_i].end = complex(0, 0)
		vectors[mid_i+1].start = vectors[mid_i].cn

	for _ in paths: draw_points_container.append([])

	return (vectors_container, draw_points_container)

def main():
	global surface
	global EXPAND_FACTOR, STEPS, CANT_VECTORS, mid_i

	svg_index = 0
	vectors_container, draw_points_container = abc(svg_index)
	running = True
	simulation = False
	step = 0

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
				if event.key == pygame.K_s:
					simulation = not simulation
				if event.key == pygame.K_SPACE:
					EXPAND_FACTOR += 1
				if event.key == pygame.K_BACKSPACE and EXPAND_FACTOR>1:
					EXPAND_FACTOR -= 1
				if event.key == pygame.K_UP:
					svg_index+=1
					vectors_container, draw_points_container = abc(svg_index)
				if event.key == pygame.K_DOWN:
					svg_index-=1
					vectors_container, draw_points_container = abc(svg_index)
				if event.key == pygame.K_RIGHT:
					STEPS += 20
					vectors_container, draw_points_container = abc(svg_index)
				if event.key == pygame.K_LEFT and STEPS>20:
					STEPS -= 20
					vectors_container, draw_points_container = abc(svg_index)
				if event.key == pygame.K_RETURN:
					CANT_VECTORS += 20
					mid_i = int(CANT_VECTORS/2)
					vectors_container, draw_points_container = abc(svg_index)
				if event.key == pygame.K_TAB and CANT_VECTORS>21:
					CANT_VECTORS -= 20
					mid_i = int(CANT_VECTORS/2)
					vectors_container, draw_points_container = abc(svg_index)

		surface.fill(BACKGROUND_COLOR)

		if True:
			for i in range(len(vectors_container)):
				vectors_container[i] = update_vectors(vectors_container[i], (step/STEPS)%1)

			for draw_points in draw_points_container:
				for i in range(1, len(draw_points)):
					pygame.draw.line(surface, DRAWING_COLOR, (draw_points[i-1][0], draw_points[i-1][1]), (draw_points[i][0], draw_points[i][1]), 1)

		for i in range(len(vectors_container)):
			next_point = [W_WIDTH/2, W_HEIGHT/2]
			for v in vectors_container[i]:
				next_point[0] += v.end.real
				next_point[1] += v.end.imag
				v.draw()
			if next_point not in draw_points_container[i]: draw_points_container[i].append(next_point)
			if len(draw_points_container[i])>STEPS: draw_points_container[i].pop(0)

		segment_points_text_surface = my_font.render("Segment points: %d" % STEPS, False, "white")
		vectors_text_surface = my_font.render("Vectors: %d" % CANT_VECTORS, False, "white")
		surface.blit(segment_points_text_surface, (TEXT_LEFT_MARGIN, TEXT_TOP_MARGIN))
		surface.blit(vectors_text_surface, (TEXT_LEFT_MARGIN, TEXT_TOP_MARGIN+segment_points_text_surface.get_height()+TEXT_SEPARATION))

		for i in range(len(CONTROLS)):
			control = CONTROLS[i]
			control_text_surface = my_font.render(control, False, "white")
			surface.blit(control_text_surface, (TEXT_LEFT_MARGIN,(vectors_text_surface.get_height()+segment_points_text_surface.get_height()+TEXT_SEPARATION*(i+4)+segment_points_text_surface.get_height()*i)))

		pygame.display.flip()
		step+=1
		clock.tick(FRAMERATE)

	pygame.quit()

if __name__ == "__main__":
	main()