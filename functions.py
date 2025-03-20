from svg.path import parse_path
from svg.path.path import Line, Move,CubicBezier, Close
from xml.dom import minidom
import cmath
# import sympy as sy

def read_svg_points(path_to_svg, points_per_segment):
	# read the SVG file
	doc = minidom.parse(path_to_svg)
	path_strings = [path.getAttribute('d') for path
									in doc.getElementsByTagName('path')]
	doc.unlink()

	points = []
	for path_string in path_strings:
		path = parse_path(path_string)
		for e in path:
			if isinstance(e, Line):
				# diffx = e.end.real-e.start.real
				# diffy = e.end.imag-e.start.imag

				# if diffx==0:
				# 	for i in range(points_per_segment):
				# 		x = e.start.real
				# 		y = e.start.imag+(diffy/points_per_segment)*i

				# 		points.append(complex(x, y))
				# else:
				# 	m = diffy/diffx
				# 	b = e.start.imag-m*e.start.real

				# 	for i in range(points_per_segment):
				# 		x = e.start.real+(diffx/points_per_segment)*i
				# 		y = m*x + b

				# 		points.append(complex(x, y))

				diffx = e.end.real-e.start.real
				diffy = e.end.imag-e.start.imag

				for i in range(points_per_segment+1):
					x = e.start.real+(diffx/points_per_segment)*i
					y = e.start.imag+(diffy/points_per_segment)*i
					points.append(complex(x, y))

				# points.append(e.start)
				# points.append(e.end)

	return points

def cn(n, steps, ft):
	res = 0
	dt = 1/steps

	for i in range(steps):
		t = dt*i
		res += ft(i)*cmath.exp(complex(0, -2*cmath.pi*n*t))*dt

	return res

def calc_vectors_cn(cant, steps, ft):
	vectors_cn = []

	for j in range(int(-cant/2), int(cant/2)+1):
	# for j in range(cant):
		vectors_cn.append(cn(j, steps, ft))

	return vectors_cn

# def cubic_bezier(t, P0, P1, P2, P3):
#     """Compute a point on a cubic Bézier curve for a given t (0 to 1)."""
#     x = (1-t)**3 * P0[0] + 3 * (1-t)**2 * t * P1[0] + 3 * (1-t) * t**2 * P2[0] + t**3 * P3[0]
#     y = (1-t)**3 * P0[1] + 3 * (1-t)**2 * t * P1[1] + 3 * (1-t) * t**2 * P2[1] + t**3 * P3[1]
#     return x, y

# def draw_bezier_curve(P0, P1, P2, P3, steps=50):
# 	"""Draw a cubic Bézier curve using Turtle."""
# 	goto(P0)  # Move to start point
# 	pendown()

# 	for i in range(steps + 1):
# 			t = i / steps
# 			x, y = cubic_bezier(t, P0, P1, P2, P3)
# 			goto(x, y)