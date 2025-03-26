import pygame
from functions import read_svg_points, calc_vectors_cn
import cmath

W_WIDTH = 800
W_HEIGHT = 600
FRAMERATE = 30
SVG_PATH = "letter-a.svg"
# POINTS_PER_SEGMENT = 10
CANT_VECTORS = 81 # cantidad a utilizar para cada segmento cerrado del path (obligatoriamente impar)

STEPS = 300 # cantidad a utilizar para cada segmento cerrado del path
EXPAND_FACTOR = 6

pygame.init()
surface = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
clock = pygame.time.Clock()
mid_i = int(CANT_VECTORS/2)

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

def main():
	global EXPAND_FACTOR
	paths = read_svg_points(SVG_PATH)

	initial_vectors_cn = []

	for path in paths:
		ft = lambda t : path.point(t)
		vectors_cn = calc_vectors_cn(CANT_VECTORS, STEPS, ft)
		initial_vectors_cn.append(vectors_cn)

	vectors_container: list[list[Vector]] = []
	for j in range(len(paths)):
		path_vectors = []
		for i in range(CANT_VECTORS):
			path_vectors.append(Vector(initial_vectors_cn[j][i], complex(0, 0)))
		vectors_container.append(path_vectors)

	for vectors in vectors_container:
		vectors[mid_i].end = complex(0, 0)
		vectors[mid_i+1].start = vectors[mid_i].cn

	running = True
	simulation = False
	step = 0

	draw_points_container = []
	for _ in paths: draw_points_container.append([])

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
				if event.key == pygame.K_BACKSPACE:
					EXPAND_FACTOR -= 1

		surface.fill("black")

		if True:
			for i in range(len(paths)):
				vectors_container[i] = update_vectors(vectors_container[i], (step/STEPS)%1)

			for draw_points in draw_points_container:
				for i in range(1, len(draw_points)):
					pygame.draw.line(surface, "red", (draw_points[i-1][0], draw_points[i-1][1]), (draw_points[i][0], draw_points[i][1]), 1)
				# for point in draw_points:
				# 	pygame.draw.circle(surface, "red", (point[0], point[1]), 1)

		for i in range(len(paths)):
			next_point = [W_WIDTH/2, W_HEIGHT/2]
			for v in vectors_container[i]:
				next_point[0] += v.end.real
				next_point[1] += v.end.imag
				v.draw()
			if next_point not in draw_points_container[i]: draw_points_container[i].append(next_point)
			if len(draw_points_container[i])>STEPS: draw_points_container[i].pop(0)

		pygame.display.flip()
		step+=1
		clock.tick(FRAMERATE)

	pygame.quit()

if __name__ == '__main__':
	main()