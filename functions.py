from svg.path import parse_path, Path
from svg.path.path import Close
from xml.dom import minidom
import cmath

def read_svg_paths(path_to_svg):
	# read the SVG file
	doc = minidom.parse(path_to_svg)
	path_commands = [path.getAttribute('d') for path
									in doc.getElementsByTagName('path')]
	doc.unlink()

	new_paths = []
	for path_string in path_commands:
		path = parse_path(path_string)

		new_path = Path()
		for e in path:
			new_path.insert(-1, e)
			if isinstance(e, Close):
				new_paths.append(new_path)
				new_path = Path()

	return new_paths

def cn(n, steps, ft):
	res = 0
	dt = 1/steps

	for i in range(steps):
		t = dt*i
		res += ft(t)*cmath.exp(complex(0, -2*cmath.pi*n*t))*dt

	return res

def calc_vectors_cn(cant, steps, ft):
	vectors_cn = []

	for j in range(int(-cant/2), int(cant/2)+1):
	# for j in range(cant):
		vectors_cn.append(cn(j, steps, ft))

	return vectors_cn