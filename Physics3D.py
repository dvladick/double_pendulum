import sympy as smp

t, g = smp.symbols('t g')
m1, m2 = smp.symbols('m1 m2')
L1, L2 = smp.symbols('L1, L2')
b = smp.symbols('b')

alpha1, alpha2, phi1, phi2 = smp.symbols(r'\alpha_1, \alpha_2, \phi_1, \phi_2', cls=smp.Function)

alpha1 = alpha1(t)
alpha2 = alpha2(t)
phi1 = phi1(t)
phi2 = phi2(t)

alpha1_diff = smp.diff(alpha1, t)
alpha2_diff = smp.diff(alpha2, t)
alpha1_ddiff = smp.diff(alpha1_diff, t)
alpha2_ddiff = smp.diff(alpha2_diff, t)
phi1_diff = smp.diff(phi1, t)
phi2_diff = smp.diff(phi2, t)
phi1_ddiff = smp.diff(phi1_diff, t)
phi2_ddiff = smp.diff(phi2_diff, t)


rx1 = L1 * smp.sin(alpha1) * smp.cos(phi1)
ry1 = -L1 * smp.sin(alpha1) * smp.sin(phi1)
rz1 = -L1 * smp.cos(alpha1)
rx2 = rx1 + L2 * smp.sin(alpha2) * smp.cos(phi2)
ry2 = ry1 - L2 * smp.sin(alpha2) * smp.sin(phi2)
rz2 = rz1 - L2 * smp.cos(alpha2)

rx1_func = smp.lambdify((alpha1, alpha2, phi1, phi2, L1, L2), rx1)
ry1_func = smp.lambdify((alpha1, alpha2, phi1, phi2, L1, L2), ry1)
rz1_func = smp.lambdify((alpha1, alpha2, phi1, phi2, L1, L2), rz1)
rx2_func = smp.lambdify((alpha1, alpha2, phi1, phi2, L1, L2), rx2)
ry2_func = smp.lambdify((alpha1, alpha2, phi1, phi2, L1, L2), ry2)
rz2_func = smp.lambdify((alpha1, alpha2, phi1, phi2, L1, L2), rz2)


vel1 = (smp.diff(rx1, t) ** 2 + smp.diff(ry1, t) ** 2 + smp.diff(rz1, t) ** 2)
vel2 = (smp.diff(rx2, t) ** 2 + smp.diff(ry2, t) ** 2 + smp.diff(rz2, t) ** 2)
T1_3D = smp.Rational(1, 2) * m1 * vel1
T2_3D = smp.Rational(1, 2) * m2 * vel2
T_3D = T1_3D + T2_3D

V1_3D = m1 * g * rz1
V2_3D = m2 * g * rz2
V_3D = V1_3D + V2_3D

L_3D = T_3D - V_3D
F_3D = smp.Rational(1, 2) * b * (vel1 + vel2)

LE1_3D = (-smp.diff(L_3D, alpha1) + smp.diff(smp.diff(L_3D, alpha1_diff), t).simplify()
          + smp.diff(F_3D, alpha1_diff).simplify())
LE2_3D = (-smp.diff(L_3D, alpha2) + smp.diff(smp.diff(L_3D, alpha2_diff), t).simplify()
          + smp.diff(F_3D, alpha2_diff).simplify())
LE3_3D = (-smp.diff(L_3D, phi1) + smp.diff(smp.diff(L_3D, phi1_diff), t).simplify()
          + smp.diff(F_3D, phi1_diff).simplify())
LE4_3D = (-smp.diff(L_3D, phi2) + smp.diff(smp.diff(L_3D, phi2_diff), t).simplify()
          + smp.diff(F_3D, phi2_diff).simplify())
sols_3D = smp.solve([LE1_3D, LE2_3D, LE3_3D, LE4_3D], (alpha1_ddiff, alpha2_ddiff, phi1_ddiff, phi2_ddiff),
                    simplify=False, rational=False)

omega1dt_func = smp.lambdify((t, g, m1, m2, L1, L2, b, alpha1, alpha2,
                             alpha1_diff, alpha2_diff, phi1, phi2, phi1_diff, phi2_diff), sols_3D[alpha1_ddiff])
omega2dt_func = smp.lambdify((t, g, m1, m2, L1, L2, b, alpha1, alpha2,
                             alpha1_diff, alpha2_diff, phi1, phi2, phi1_diff, phi2_diff), sols_3D[alpha2_ddiff])
alpha1dt_func = smp.lambdify(alpha1_diff, alpha1_diff)
alpha2dt_func = smp.lambdify(alpha2_diff, alpha2_diff)

dw1dt_func = smp.lambdify((t, g, m1, m2, L1, L2, b, alpha1, alpha2,
                           alpha1_diff, alpha2_diff, phi1, phi2, phi1_diff, phi2_diff), sols_3D[phi1_ddiff])
dw2dt_func = smp.lambdify((t, g, m1, m2, L1, L2, b, alpha1, alpha2,
                           alpha1_diff, alpha2_diff, phi1, phi2, phi1_diff, phi2_diff), sols_3D[phi2_ddiff])
phi1dt_func = smp.lambdify(phi1_diff, phi1_diff)
phi2dt_func = smp.lambdify(phi2_diff, phi2_diff)


def system_dt_3d(variables, time, gravity, mass1, mass2, length1, length2, damping):
    alpha1, alpha2, phi1, phi2, omega1, omega2, w1, w2 = variables
    return [
        alpha1dt_func(omega1),
        alpha2dt_func(omega2),
        phi1dt_func(w1),
        phi2dt_func(w2),
        omega1dt_func(time, gravity, mass1, mass2, length1, length2, damping,
                      alpha1, alpha2, omega1, omega2, phi1, phi2, w1, w2),
        omega2dt_func(time, gravity, mass1, mass2, length1, length2, damping,
                      alpha1, alpha2, omega1, omega2, phi1, phi2, w1, w2),
        dw1dt_func(time, gravity, mass1, mass2, length1, length2, damping,
                   alpha1, alpha2, omega1, omega2, phi1, phi2, w1, w2),
        dw2dt_func(time, gravity, mass1, mass2, length1, length2, damping,
                   alpha1, alpha2, omega1, omega2, phi1, phi2, w1, w2),
    ]


def get_pos_3d(alpha1, alpha2, phi1, phi2, length1, length2):
    return (rx1_func(alpha1, alpha2, phi1, phi2, length1, length2),
            ry1_func(alpha1, alpha2, phi1, phi2, length1, length2),
            rz1_func(alpha1, alpha2, phi1, phi2, length1, length2),
            rx2_func(alpha1, alpha2, phi1, phi2, length1, length2),
            ry2_func(alpha1, alpha2, phi1, phi2, length1, length2),
            rz2_func(alpha1, alpha2, phi1, phi2, length1, length2))
