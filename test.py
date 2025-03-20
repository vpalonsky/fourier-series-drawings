import cmath
import sympy as sy
from functions import read_svg_points

t = sy.Symbol("t")
ft = t*t

svg_points = read_svg_points("letter-a.svg")
ft = lambda t : svg_points[t]
# print(ft)


# cn = lambda n : sy.integrate(ft(t)*(cmath.exp(complex(0, -2*cmath.pi*n))**t), (t, 0, 1))

CANT_VECTORS = 10
STEPS = len(svg_points)
dt = 1/STEPS

def cn(n):
	res = 0

	for i in range(STEPS):
		t = dt*i
		res += ft(i)*cmath.exp(complex(0, -2*cmath.pi*n*t))*dt

	return res

def calc_vectors_cn(cant = CANT_VECTORS):
	vectors_cn = []

	for j in range(int(-cant/2), int(cant/2)):
		vectors_cn.append(cn(j))

	return vectors_cn

# *cmath.exp(complex(0, -2*cmath.pi*n*t))
print(calc_vectors_cn())