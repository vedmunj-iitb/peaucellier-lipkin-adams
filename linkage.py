"""Peaucellier-Lipkin linkage: position analysis in plain Python.

Written in 2026 for this repo, after the course. It is not part of the ADAMS
model, but it uses the link lengths of the ME 7001 course model.

O = fixed pivot at the origin, Q = crank pivot at (r, 0)
fixed    O-Q        length r   (as long as the crank)
crank    Q-C        length r   (C moves on a circle through O)
long     O-A, O-B   length L
rhombus  A-C, B-C, A-P, B-P   length s
"""
import numpy as np
import matplotlib.pyplot as plt

r, L, s = 3.0, 9.0, 4.0  # cm

O = np.array([0.0, 0.0])
Q = np.array([r, 0.0])


def circle_intersection(p0, r0, p1, r1):
    """The two points at distance r0 from p0 and r1 from p1."""
    d = np.linalg.norm(p1 - p0)
    a = (r0**2 - r1**2 + d**2) / (2 * d)
    h = np.sqrt(r0**2 - a**2)
    mid = p0 + a * (p1 - p0) / d
    perp = np.array([-(p1 - p0)[1], (p1 - p0)[0]]) / d
    return mid + h * perp, mid - h * perp


def solve(theta):
    """Joint positions C, A, B, P for crank angle theta (rad)."""
    C = Q + r * np.array([np.cos(theta), np.sin(theta)])
    A, B = circle_intersection(O, L, C, s)
    P = A + B - C  # fourth corner of the rhombus
    return C, A, B, P


# The rhombus folds flat when O-C shrinks to L - s, at a crank angle of
# 2 acos((L - s) / 2r), about 67 degrees, so the sweep stops at 66.
path = np.array([solve(t)[3] for t in np.radians(np.arange(-66, 67, 2))])

line_x = (L**2 - s**2) / (2 * r)
print(f'expected line: x = {line_x:.3f} cm')
print(f'largest deviation of P from it: {np.abs(path[:, 0] - line_x).max():.1e} cm')
print(f'P moves from y = {path[:, 1].min():.1f} to {path[:, 1].max():.1f} cm')

# the linkage at one crank angle, the crank circle and the path of P
C, A, B, P = solve(np.radians(40))
for p0, p1 in [(Q, C), (O, A), (O, B), (A, C), (B, C), (A, P), (B, P)]:
    plt.plot([p0[0], p1[0]], [p0[1], p1[1]], 'k-', lw=2)
a = np.radians(np.arange(0, 361, 5))
plt.plot(Q[0] + r * np.cos(a), Q[1] + r * np.sin(a), ':', color='grey')
plt.plot(path[:, 0], path[:, 1], 'o', ms=3, label='path of P')
plt.axvline(line_x, color='grey', ls='--', label='x = (L² - s²) / 2r')

plt.axis('equal')
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')
plt.legend()
plt.title('Peaucellier-Lipkin linkage, crank at 40 degrees')
plt.savefig('path.png', dpi=110)
