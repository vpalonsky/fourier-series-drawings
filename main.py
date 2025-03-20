import pygame
from functions import read_svg_points, calc_vectors_cn
import cmath

SVG_PATH = "bolt.svg"
W_WIDTH = 800
W_HEIGHT = 800
FRAMERATE = 2
CANT_VECTORS = 71
POINTS_PER_SEGMENT = 1

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
		# if i>0:
		# 	vector = vectors[i]
		# 	vector.end = vector.cn*cmath.exp(complex(0, i*2*cmath.pi*t))

		# 	if i>1:
		# 		vector.start = vectors[i-1].end
		if i!=mid_i:
			n = i-(CANT_VECTORS/2)
			new_vectors[i].end = new_vectors[i].cn*cmath.exp(complex(0, n*2*cmath.pi*t))

			# if i!=(mid_i+1):
			new_vectors[i].start = new_vectors[i-1].start + new_vectors[i-1].end

	return new_vectors

def main():
	svg_points = read_svg_points(SVG_PATH, POINTS_PER_SEGMENT)
	ft = lambda t : svg_points[t]
	steps = len(svg_points)
	print(steps)

	vectors_cn = calc_vectors_cn(CANT_VECTORS, steps, ft)
	vectors = [Vector(vectors_cn[i], complex(0, 0)) for i in range(CANT_VECTORS)]
	vectors[mid_i].end = vectors[mid_i].cn
	vectors[mid_i+1].start = vectors[mid_i].cn

	running = True
	simulation = False
	step = 0

	draw_points = []

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
				if event.key == pygame.K_s:
					simulation = not simulation

		surface.fill("black")

		if True:
			vectors = update_vectors(vectors, (step/steps)%1)

			for point in draw_points:
				pygame.draw.circle(surface, "red", (point[0], point[1]), 1)

		next_point = [W_WIDTH/2, W_HEIGHT/2]
		for v in vectors:
			next_point[0] += v.end.real
			next_point[1] += v.end.imag
			v.draw()
		if next_point not in draw_points: draw_points.append(next_point)


		pygame.display.flip()
		step+=1
		clock.tick(FRAMERATE)

	pygame.quit()

if __name__ == '__main__':
	main()