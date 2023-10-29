import sympy as smp

t, g = smp.symbols('t g')
m1, m2 = smp.symbols('m1 m2')
L1, L2 = smp.symbols('L1, L2')
b = smp.symbols('b')

theta1, theta2 = smp.symbols(r'\theta_1, \theta_2', cls=smp.Function)

theta1 = theta1(t)
theta2 = theta2(t)

theta1_diff = smp.diff(theta1, t)
theta2_diff = smp.diff(theta2, t)
theta1_ddiff = smp.diff(theta1_diff, t)
theta2_ddiff = smp.diff(theta2_diff, t)

x1 = L1 * smp.sin(theta1)
y1 = -L1 * smp.cos(theta1)
x2 = x1 + L2 * smp.sin(theta2)
y2 = y1 - L2 * smp.cos(theta2)

x1_func = smp.lambdify((theta1, theta2, L1, L2), x1)
y1_func = smp.lambdify((theta1, theta2, L1, L2), y1)
x2_func = smp.lambdify((theta1, theta2, L1, L2), x2)
y2_func = smp.lambdify((theta1, theta2, L1, L2), y2)


T1 = smp.Rational(1, 2) * m1 * (smp.diff(x1, t) ** 2 + smp.diff(y1, t) ** 2)
T2 = smp.Rational(1, 2) * m2 * (smp.diff(x2, t) ** 2 + smp.diff(y2, t) ** 2)
T = T1 + T2

V1 = m1 * g * y1
V2 = m2 * g * y2
V = V1 + V2

L = T-V
F = smp.Rational(1, 2) * b * (smp.diff(x1, t) ** 2 + smp.diff(y1, t) ** 2
                              + smp.diff(x2, t) ** 2 + smp.diff(y2, t) ** 2)

LE1 = -smp.diff(L, theta1) + smp.diff(smp.diff(L, theta1_diff), t).simplify() + smp.diff(F, theta1_diff).simplify()
LE2 = -smp.diff(L, theta2) + smp.diff(smp.diff(L, theta2_diff), t).simplify() + smp.diff(F, theta2_diff).simplify()
sols = smp.solve([LE1, LE2], (theta1_ddiff, theta2_ddiff))

omega1dt_func = smp.lambdify((t, g, m1, m2, L1, L2, b, theta1, theta2, theta1_diff, theta2_diff), sols[theta1_ddiff])
omega2dt_func = smp.lambdify((t, g, m1, m2, L1, L2, b, theta1, theta2, theta1_diff, theta2_diff), sols[theta2_ddiff])
theta1dt_func = smp.lambdify(theta1_diff, theta1_diff)
theta2dt_func = smp.lambdify(theta2_diff, theta2_diff)


def system_dt_2d(variables, time, gravity, mass1, mass2, length1, length2, damping):
    theta1, theta2, omega1, omega2 = variables
    return [
        theta1dt_func(omega1),
        theta2dt_func(omega2),
        omega1dt_func(time, gravity, mass1, mass2, length1, length2, damping, theta1, theta2, omega1, omega2),
        omega2dt_func(time, gravity, mass1, mass2, length1, length2, damping, theta1, theta2, omega1, omega2),
    ]


def get_pos(theta1, theta2, length1, length2):
    return (x1_func(theta1, theta2, length1, length2),
            y1_func(theta1, theta2, length1, length2),
            x2_func(theta1, theta2, length1, length2),
            y2_func(theta1, theta2, length1, length2))
