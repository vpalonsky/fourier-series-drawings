import pygame
from functions import calculate_vectors_lists_constants, update_vectors_rotation, generate_text
from constants import surface, clock
from constants import W_WIDTH, W_HEIGHT, FRAMERATE, BACKGROUND_COLOR, DRAWING_COLOR
import constants

def main():
	# Simulation state
	shapes_vectors_list, shapes_points_list = calculate_vectors_lists_constants(constants.SVG_INDEX)
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
					constants.EXPAND_FACTOR += 1
				if event.key == pygame.K_BACKSPACE  and constants.EXPAND_FACTOR>1:
					constants.EXPAND_FACTOR -= 1
				if event.key == pygame.K_UP:
					constants.SVG_INDEX+=1
					shapes_vectors_list, shapes_points_list = calculate_vectors_lists_constants(constants.SVG_INDEX)
				if event.key == pygame.K_DOWN:
					constants.SVG_INDEX-=1
					shapes_vectors_list, shapes_points_list = calculate_vectors_lists_constants(constants.SVG_INDEX)
				if event.key == pygame.K_RIGHT:
					constants.STEPS += 20
					shapes_vectors_list, shapes_points_list = calculate_vectors_lists_constants(constants.SVG_INDEX)
				if event.key == pygame.K_LEFT and constants.STEPS>20:
					constants.STEPS -= 20
					shapes_vectors_list, shapes_points_list = calculate_vectors_lists_constants(constants.SVG_INDEX)
				if event.key == pygame.K_RETURN:
					constants.CANT_VECTORS += 20
					constants.mid_i = int(constants.CANT_VECTORS/2)
					shapes_vectors_list, shapes_points_list = calculate_vectors_lists_constants(constants.SVG_INDEX)
				if event.key == pygame.K_TAB and constants.CANT_VECTORS>21:
					constants.CANT_VECTORS -= 20
					constants.mid_i = int(constants.CANT_VECTORS/2)
					shapes_vectors_list, shapes_points_list = calculate_vectors_lists_constants(constants.SVG_INDEX)
				if event.key == pygame.K_n and constants.DRAW_JUMP<constants.STEPS:
					constants.DRAW_JUMP += 10
					for i in range(len(shapes_points_list)):
						shapes_points_list[i] = shapes_points_list[i][10:]
				if event.key == pygame.K_m and constants.DRAW_JUMP>0:
					constants.DRAW_JUMP -= 10

		surface.fill(BACKGROUND_COLOR)
		generate_text()

		if simulation:
			for i in range(len(shapes_vectors_list)):
				shapes_vectors_list[i] = update_vectors_rotation(shapes_vectors_list[i], (step/constants.STEPS))

			for draw_points in shapes_points_list:
				for i in range(1, len(draw_points)):
					pygame.draw.line(surface, DRAWING_COLOR, (draw_points[i-1][0], draw_points[i-1][1]), (draw_points[i][0], draw_points[i][1]), 1)

			for i in range(len(shapes_vectors_list)):
				next_point = [W_WIDTH/2, W_HEIGHT/2]
				for v in shapes_vectors_list[i]:
					next_point[0] += v.end.real
					next_point[1] += v.end.imag
					if draw_vectors: v.draw()
				shapes_points_list[i].append(next_point)
				if len(shapes_points_list[i])>(constants.STEPS-constants.DRAW_JUMP): shapes_points_list[i].pop(0)

			pygame.display.flip()
			step+=1

		clock.tick(FRAMERATE)

	pygame.quit()

if __name__ == "__main__":
	main()