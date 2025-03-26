from functions import read_svg_points
import pygame
import cmath

SVG_PATH = "bolt.svg"
POINTS_PER_SEGMENT = 10
EXPAND_FACTOR = 3

pygame.init()
surface = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

def average(points):
	sum = 0
	for point in points:
		sum += point
		# sum += point
	return sum/len(points)*cmath.exp(complex(0, -2*cmath.pi*5))

def main():
	global EXPAND_FACTOR
	svg_points = read_svg_points(SVG_PATH, POINTS_PER_SEGMENT)

	running = True
	avg = average(svg_points)
	# print(avg)

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
				if event.key == pygame.K_SPACE:
					EXPAND_FACTOR += 1
				if event.key == pygame.K_BACKSPACE:
					EXPAND_FACTOR -= 1

		surface.fill("black")

		for point in svg_points:
			pygame.draw.circle(surface, "red", ((point.real*EXPAND_FACTOR)+400, (point.imag*EXPAND_FACTOR)+400), 2)
		pygame.draw.circle(surface, "blue", ((avg.real*EXPAND_FACTOR)+400, (avg.imag*EXPAND_FACTOR)+400), 2)

		pygame.display.flip()
		clock.tick(30)

	pygame.quit()

main()