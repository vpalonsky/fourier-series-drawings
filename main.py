import pygame
from functions import read_svg_paths, calc_vectors_cn
import cmath
import os

W_WIDTH = 800
W_HEIGHT = 600
FRAMERATE = 30
CANT_VECTORS = 81 # cantidad a utilizar para cada segmento cerrado del path (obligatoriamente impar)
STEPS = 100 # cantidad a utilizar para cada segmento cerrado del path
EXPAND_FACTOR = 6
DRAWING_COLOR = "blue"
BACKGROUND_COLOR = "black"
TEXT_TOP_MARGIN = 10
TEXT_LEFT_MARGIN = 10
TEXT_SEPARATION = 10
FONT_SIZE = 24
SVGS_PATH = "svg_imgs"
SVGS = os.listdir(SVGS_PATH) if len(os.listdir(SVGS_PATH))>0 else ['']
SVG_INDEX = 0
DRAW_JUMP = 20

pygame.init()
surface = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
clock = pygame.time.Clock()
my_font = pygame.font.Font(None, FONT_SIZE)
mid_i = int(CANT_VECTORS/2)
sign_texts = [
	"Actual svg: " + SVGS[SVG_INDEX],
	"Arrows: " + str(CANT_VECTORS),
	"Points per shape: " + str(STEPS),
	"Draw jump: " + str(DRAW_JUMP)
]

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

def generate_containers(svg_index):
	generate_new_text()

	actual_svg_path = os.path.join(SVGS_PATH, SVGS[svg_index%len(SVGS)])
	paths = read_svg_paths(actual_svg_path)

	initial_vectors_cn = []
	draw_points_container = [[] for _ in paths]
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

	return (vectors_container, draw_points_container)

def generate_new_text():
	global sign_texts

	sign_texts = [
		"Actual svg: " + SVGS[SVG_INDEX],
		"Arrows: " + str(CANT_VECTORS),
		"Points per shape: " + str(STEPS),
		"Draw jump: " + str(DRAW_JUMP)
	]

def main():
	global surface
	global EXPAND_FACTOR, STEPS, CANT_VECTORS, SVG_INDEX, DRAW_JUMP, mid_i

	vectors_container, draw_points_container = generate_containers(SVG_INDEX)
	running = True
	simulation = True
	draw_vectors = True
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
				if event.key == pygame.K_d:
					draw_vectors = not draw_vectors
				if event.key == pygame.K_SPACE:
					EXPAND_FACTOR += 1
				if event.key == pygame.K_BACKSPACE  and EXPAND_FACTOR>1:
					EXPAND_FACTOR -= 1
				if event.key == pygame.K_UP:
					SVG_INDEX+=1
					vectors_container, draw_points_container = generate_containers(SVG_INDEX)
				if event.key == pygame.K_DOWN:
					SVG_INDEX-=1
					vectors_container, draw_points_container = generate_containers(SVG_INDEX)
				if event.key == pygame.K_RIGHT:
					STEPS += 20
					vectors_container, draw_points_container = generate_containers(SVG_INDEX)
				if event.key == pygame.K_LEFT and STEPS>20:
					STEPS -= 20
					vectors_container, draw_points_container = generate_containers(SVG_INDEX)
				if event.key == pygame.K_RETURN:
					CANT_VECTORS += 20
					mid_i = int(CANT_VECTORS/2)
					vectors_container, draw_points_container = generate_containers(SVG_INDEX)
				if event.key == pygame.K_TAB and CANT_VECTORS>21:
					CANT_VECTORS -= 20
					mid_i = int(CANT_VECTORS/2)
					vectors_container, draw_points_container = generate_containers(SVG_INDEX)
				if event.key == pygame.K_n and DRAW_JUMP<STEPS:
					DRAW_JUMP += 10
					for i in range(len(draw_points_container)):
						draw_points_container[i] = draw_points_container[i][10:]
					generate_new_text()
				if event.key == pygame.K_m and DRAW_JUMP>0:
					DRAW_JUMP -= 10
					generate_new_text()


		surface.fill(BACKGROUND_COLOR)

		if simulation:
			for i in range(len(vectors_container)):
				vectors_container[i] = update_vectors(vectors_container[i], (step/STEPS))

			for draw_points in draw_points_container:
				for i in range(1, len(draw_points)):
					pygame.draw.line(surface, DRAWING_COLOR, (draw_points[i-1][0], draw_points[i-1][1]), (draw_points[i][0], draw_points[i][1]), 1)

			for i in range(len(vectors_container)):
				next_point = [W_WIDTH/2, W_HEIGHT/2]
				for v in vectors_container[i]:
					next_point[0] += v.end.real
					next_point[1] += v.end.imag
					if draw_vectors: v.draw()
				draw_points_container[i].append(next_point)
				if len(draw_points_container[i])>(STEPS-DRAW_JUMP): draw_points_container[i].pop(0)

			for i in range(len(sign_texts)):
				text = sign_texts[i]
				text_surface = my_font.render(text, False, "white")
				surface.blit(text_surface, (TEXT_LEFT_MARGIN, (i+1)*TEXT_TOP_MARGIN+TEXT_SEPARATION*i))

			pygame.display.flip()
			step+=1
		clock.tick(FRAMERATE)

	pygame.quit()

if __name__ == "__main__":
	main()