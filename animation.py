import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.animation as animation
from Physics2D import *
from Physics3D import *


def make_segments(x, y):
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments


def gradient_plot(x, y, colors, cmap=plt.get_cmap('gist_rainbow'), line_width=3, alpha=1.0):
    lines = make_segments(x, y)
    col = LineCollection(lines, array=colors, cmap=cmap, linewidth=line_width, alpha=alpha)
    return col


def update2d(i, time, x_first_ball, y_first_ball, x_second_ball, y_second_ball,
             trail, time_text, line1, line2, circle1, circle2):
    h = 0.01
    p = int(time / h) // 50
    if not i-p < 0:
        trail.set_segments(make_segments(x_second_ball[i - p:i], y_second_ball[i - p:i]))
    time_text.set_text(f'Time elapsed: {np.round(h * (i+1), 1)} seconds')
    line1.set_ydata([0, y_first_ball[i]])
    line1.set_xdata([0, x_first_ball[i]])
    line2.set_ydata([y_first_ball[i], y_second_ball[i]])
    line2.set_xdata([x_first_ball[i], x_second_ball[i]])

    circle1.center = x_first_ball[i], y_first_ball[i]
    circle2.center = x_second_ball[i], y_second_ball[i]
    return trail, time_text, line1, line2, circle1, circle2


def animate2d(initial_conditions, mass1, mass2, length1, length2, gravity, damping, time):

    h = 0.01
    steps = int(np.rint(time / h))
    time_grid = np.linspace(0, time, steps + 1)

    ans = odeint(system_dt_2d, y0=initial_conditions, t=time_grid,
                 args=(gravity, mass1, mass2, length1, length2, damping), atol=1.0e-9, rtol=1.0e-9)

    x_first_ball, y_first_ball, x_second_ball, y_second_ball = get_pos(ans[:, 0], ans[:, 1], length1, length2)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    plt.subplots_adjust(bottom=0.2, left=0.15)

    half = length1 + length2
    ax.axis([-half-1, half+1, -half-1, half+1])
    ax.set_title('Damped Double Pendulum')
    ax.set_xlabel('x(t)')
    ax.set_ylabel('y(t)')
    trail = gradient_plot(x_second_ball[:0], y_second_ball[:0], time_grid[:steps + 1],
                          plt.get_cmap('gist_rainbow'), line_width=1, alpha=0.5)
    ax.add_collection(trail)

    time_text = ax.text(-half, half, '', fontsize=12)
    time_text.set_text('Time elapsed: 0 seconds')

    line1 = ax.plot([0, x_first_ball[0]], [0, y_first_ball[0]], color='k', lw=3, zorder=20)[0]
    line2 = ax.plot([x_first_ball[0], x_second_ball[0]], [y_first_ball[0], y_second_ball[0]],
                    color='k', lw=3, zorder=20)[0]

    circle1 = plt.Circle((x_first_ball[0], y_first_ball[0]), 0.1, ec="k", lw=1.5, zorder=30)
    ax.add_patch(circle1)
    circle2 = plt.Circle((x_second_ball[0], y_second_ball[0]), 0.1, ec="k", lw=1.5, zorder=30)
    ax.add_patch(circle2)

    ani = animation.FuncAnimation(fig, update2d, frames=np.arange(steps),
                                  fargs=(time,
                                         x_first_ball, y_first_ball,
                                         x_second_ball, y_second_ball,
                                         trail, time_text, line1, line2, circle1, circle2),
                                  interval=h, blit=True, repeat=True, repeat_delay=5000)
    plt.show()

    return ani


def update3d(i, x_first_ball, y_first_ball, z_first_ball, x_second_ball, y_second_ball, z_second_ball,
             line1, line2, line_trace):
    line1.set_data([0, x_first_ball[i]], [0, y_first_ball[i]])
    line1.set_3d_properties([0, z_first_ball[i]])
    line2.set_data([x_first_ball[i], x_second_ball[i]], [y_first_ball[i], y_second_ball[i]])
    line2.set_3d_properties([z_first_ball[i], z_second_ball[i]])

    line_trace.set_data(x_second_ball[:i+1], y_second_ball[:i+1])
    line_trace.set_3d_properties(z_second_ball[:i+1])
    return line1, line2, line_trace


def animate3d(initial_conditions, mass1, mass2, length1, length2, gravity, damping, time):

    h = 0.01
    steps = int(np.rint(time / h))
    time_grid = np.linspace(0, time, steps + 1)

    ans = odeint(system_dt_3d, y0=initial_conditions, t=time_grid,
                 args=(gravity, mass1, mass2, length1, length2, damping), atol=1.0e-10, rtol=1.0e-10)

    (x_first_ball, y_first_ball, z_first_ball,
     x_second_ball, y_second_ball, z_second_ball) = get_pos_3d(ans[:, 0], ans[:, 1], ans[:, 2], ans[:, 3],
                                                               length1, length2)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    half = 4.5
    if half < length1 + length2:
        half = length1 + length2
    ax.axis([-half-1, half+1, -half-1, half+1, -half-1, half+1])
    ax.set_title('Damped Double Pendulum')
    ax.set_xlabel('x(t)')
    ax.set_ylabel('y(t)')
    ax.set_zlabel('z(t)')

    line1 = ax.plot3D([0, x_first_ball[0]], [0, y_first_ball[0]], [0, z_first_ball[0]],
                      'o-', color='blue', lw=4)[0]
    line2 = ax.plot3D([x_first_ball[0], x_second_ball[0]], [y_first_ball[0], y_second_ball[0]],
                      [z_first_ball[0], z_second_ball[0]], 'o-', color='blue', lw=4)[0]
    line_trace = ax.plot3D([], [], [], color='k', lw=1)[0]

    ani = animation.FuncAnimation(fig, update3d, frames=np.arange(steps),
                                  fargs=(x_first_ball, y_first_ball, z_first_ball,
                                         x_second_ball, y_second_ball, z_second_ball,
                                         line1, line2, line_trace),
                                  interval=h, blit=True, repeat=True, repeat_delay=1000)

    plt.show()

    return ani
