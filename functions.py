from svg.path import parse_path, Path, PathSegment
from svg.path.path import Line, CubicBezier, Close
from xml.dom import minidom
import cmath
# import sympy as sy

def read_svg_points(path_to_svg):
	# read the SVG file
	doc = minidom.parse(path_to_svg)
	path_strings = [path.getAttribute('d') for path
									in doc.getElementsByTagName('path')]
	doc.unlink()

	new_paths = []
	for path_string in path_strings:
		path = parse_path(path_string)

		new_path = Path()
		for e in path:
			if isinstance(e, Close):
				new_path.insert(-1, e)
				new_paths.append(new_path)
				new_path = Path()
			else: new_path.insert(-1, e)

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

def cubic_bezier(t, P0, P1, P2, P3):
	"""Compute a point on a cubic Bézier curve for a given t (0 to 1)."""
	x = (1-t)**3 * P0[0] + 3 * (1-t)**2 * t * P1[0] + 3 * (1-t) * t**2 * P2[0] + t**3 * P3[0]
	y = (1-t)**3 * P0[1] + 3 * (1-t)**2 * t * P1[1] + 3 * (1-t) * t**2 * P2[1] + t**3 * P3[1]
	return x, y

# def draw_bezier_curve(P0, P1, P2, P3, steps=50):
# 	"""Draw a cubic Bézier curve using Turtle."""
# 	goto(P0)  # Move to start point
# 	pendown()

# 	for i in range(steps + 1):
# 		t = i / steps
# 		x, y = cubic_bezier(t, P0, P1, P2, P3)
# 		goto(x, y)

def divide_cubic_bezier(controllers: CubicBezier, points_per_curve):
	P0 = (controllers.start.real, controllers.start.imag)
	P1 = (controllers.control1.real, controllers.control1.imag)
	P2 = (controllers.control2.real, controllers.control2.imag)
	P3 = (controllers.end.real, controllers.end.imag)

	points = []

	for i in range(points_per_curve+1):
		t = i/points_per_curve
		x, y = cubic_bezier(t, P0, P1, P2, P3)
		points.append(complex(x, y))

	return points