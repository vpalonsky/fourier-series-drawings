from xml.dom import minidom
import svg.path, cmath, os
from constants import surface, my_font
from constants import Vector, SVGS_PATH, SVGS, TEXT_COLOR, TEXT_LEFT_MARGIN, TEXT_TOP_MARGIN, TEXT_SEPARATION
import constants

# Read the SVG file and separate SVG paths commands in lists
def read_svg_paths(path_to_svg):
	doc = minidom.parse(path_to_svg)
	path_commands = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
	doc.unlink()

	new_paths = []
	for path_string in path_commands:
		path = svg.path.parse_path(path_string)

		new_path = svg.path.Path()
		for e in path:
			new_path.insert(-1, e)
			if isinstance(e, svg.path.Close):
				new_paths.append(new_path)
				new_path = svg.path.Path()

	return new_paths

# Calculate vectors lists constants
def calculate_vectors_lists_constants(svg_index):
	actual_svg_path = os.path.join(SVGS_PATH, SVGS[svg_index%len(SVGS)])
	paths = read_svg_paths(actual_svg_path)

	vectors_constants_list = []
	shapes_points_list = [[] for _ in paths]
	shapes_vectors_list: list[list[Vector]] = []

	for path in paths:
		ft = lambda t : path.point(t)
		vectors_constants = calculate_vectors_constants(constants.CANT_VECTORS, constants.STEPS, ft)
		vectors_constants_list.append(vectors_constants)

	for j in range(len(paths)):
		path_vectors = []
		for i in range(constants.CANT_VECTORS):
			path_vectors.append(Vector(vectors_constants_list[j][i], complex(0, 0)))
		shapes_vectors_list.append(path_vectors)

	for vectors in shapes_vectors_list:
		vectors[constants.mid_i].end = complex(0, 0)
		vectors[constants.mid_i+1].start = vectors[constants.mid_i].cn

	return (shapes_vectors_list, shapes_points_list)

# Calculate vectors list constants
def calculate_vectors_constants(cant, steps, ft):
	vectors_constants = []

	for j in range(int(-cant/2), int(cant/2)+1):
		vectors_constants.append(calculate_vector_constant(j, steps, ft))

	return vectors_constants

# Calculate one vector constant
def calculate_vector_constant(n, steps, ft):
	res = 0
	dt = 1/steps

	for i in range(steps):
		t = dt*i
		res += ft(t)*cmath.exp(complex(0, -2*cmath.pi*n*t))*dt

	return res

# Update vectors rotation based on t step, and apply expand factor
def update_vectors_rotation(vectors: list[Vector], t):
	new_vectors = vectors
	for i in range(constants.CANT_VECTORS):
		if i!=constants.mid_i:
			n = i-constants.mid_i
			new_vectors[i].end = new_vectors[i].cn*cmath.exp(complex(0, n*2*cmath.pi*t))*constants.EXPAND_FACTOR

	for i in range(1, constants.mid_i+1):
		i_fst = constants.mid_i+i
		i_snd = constants.mid_i-i

		new_vectors[i_fst].start = new_vectors[i_fst - (2*i-1)].start + new_vectors[i_fst - (2*i-1)].end
		new_vectors[i_snd].start = new_vectors[i_snd + (2*i)].start + new_vectors[i_snd + (2*i)].end

	return new_vectors

# Generate and embed to surface informative text
def generate_text():
	global surface, my_font

	sign_texts = [
		"Actual svg: " + SVGS[constants.SVG_INDEX%len(SVGS)],
		"Arrows: " + str(constants.CANT_VECTORS),
		"Points per shape: " + str(constants.STEPS),
		"Draw jump: " + str(constants.DRAW_JUMP)
	]

	for i in range(len(sign_texts)):
		text = sign_texts[i]
		text_surface = my_font.render(text, False, TEXT_COLOR)
		surface.blit(text_surface, (TEXT_LEFT_MARGIN, (i+1)*TEXT_TOP_MARGIN+TEXT_SEPARATION*i))