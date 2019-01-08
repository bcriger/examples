import numpy as np
import qutip as qt

# H and T are commonly-used single-letter variable names in this field
# (sorry).
h = np.matrix([[1, 1], [1, -1]], np.complex_) / np.sqrt(2.)
t = np.matrix(np.diag([1., np.sqrt(1j)]), np.complex_)

# X, Y, and Z coordinates on the Bloch sphere are given by 
# 'sandwich' products with the following matrices
x_mat = np.matrix([[0,  1],  [1,  0]], np.complex_)
y_mat = np.matrix([[0, -1j], [1j, 0]], np.complex_)
z_mat = np.matrix([[1,  0],  [0, -1]], np.complex_)

crds = lambda _: [(_.H * mat * _)[0, 0].real
                    for mat in (x_mat, y_mat, z_mat)]

def int_pad(num, dgts):
    return str(num).zfill(dgts)


def not_close_to_any_in(thing, lst):
    return not(any([np.allclose(thing, _) for _ in lst]))

# Which states can we reach, starting with |0>?
explored_states = [np.matrix([[1.],[0.]], np.complex_)]

# how many gates do we put in a given sequence, at most?
max_levels = 21

sphere = qt.Bloch()

# Let's make the sphere look nice:
hue_lst = np.linspace(255, 0, max_levels + 1)
hex_col = lambda rgb: "#{0:02x}{1:02x}{2:02x}".format(*rgb)
rgb_colours = [(int(r), 0, int(255 - r)) for r in hue_lst]
sphere.point_color = list(map(hex_col, rgb_colours))
sphere.point_marker = ['o']

for recursion_level in range(max_levels):
    # Let's plot the states we've seen so far:
    coord_list = list(map(crds, explored_states))

    # sphere.clear()
    sphere.add_points(list(map(list, zip(*coord_list))))
    sphere.save(f'frame_{int_pad(recursion_level, 2)}.png')

    # For every sequence, we can generate a new one by prepending an
    # H or a T, our choice.
    new_states = []
    for state in explored_states:

        h_state, t_state = h @ state, t @ state
        # For ease of plotting, I'll avoid plotting points that are
        # too close together, or to what we just saw:
        check_states = explored_states + new_states
        if not_close_to_any_in(h_state, check_states):
            new_states.append(h_state)
        if not_close_to_any_in(t_state, check_states):
            new_states.append(t_state)

    explored_states = new_states

# Last round of plots
coord_list = list(map(crds, explored_states))
sphere.add_points(list(map(list, zip(*coord_list))))
sphere.save(f'frame_{int_pad(max_levels, 2)}.png')
