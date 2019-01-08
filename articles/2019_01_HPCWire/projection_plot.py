import numpy as np
from matplotlib import pyplot as plt

# make the plots beautiful
import seaborn as sb
sb.set()

def riemann_projection(x):
    """
    Maps a point on the infinitely long real line onto a finite
    semicircle of radius 1 centered at (0, 1), which touches the real
    line at the origin. 
    If we drew a line from the center of the semicircle to the point on
    the real line that we're mapping *from*, the line touches the
    semicircle at the point that we're mapping *to*.   
    """
    
    # Handle edge cases

    # Projection diverges at x = 0
    if np.abs(x) < 10**-100:
        return(0., 0.)
    
    # math doesn't work with big numbers
    if np.abs(x) > 10**100:
        if x > 0:
            return (1., 1.)
        elif x < 0: 
            return (-1., 1.)

    denominator = np.sqrt(np.float64(x**2 + 1))
    
    return (x / denominator, 1. -1. / denominator)

max_bits = 10

# Let's make the plots look nice:
hue_lst = np.linspace(255, 0, max_bits + 1)
hex_col = lambda rgb: "#{0:02x}{1:02x}{2:02x}".format(*rgb)
rgb_colours = [(int(r), 0, int(255 - r)) for r in hue_lst]
point_colour = list(map(hex_col, rgb_colours))

# Semi-circle for comparison
thetas = np.linspace(0, np.pi, 100)
plt.plot(np.cos(thetas), 1 - np.sin(thetas), 'k')
plt.axis('scaled')
plt.xlim(-1.05, 1.05)
plt.ylim(-0.05, 1.05)

for n_bits, colour in zip(range(max_bits), point_colour):

    # Let's write out the set of points
    current_set = []
    
    for significand in range(2**n_bits):
        for exponent in range(2**n_bits):
            numbers = [
                        significand * 10 ** exponent,
                        -significand * 10 ** exponent,
                        significand * 10 ** -exponent,
                        -significand * 10 ** -exponent
                    ]
            current_set.extend(numbers)

    xs, ys = zip(*map(riemann_projection, current_set))
    plt.plot(xs, ys, color = colour, marker = 'o', linestyle='None')
    plt.savefig(f'riemann_frame_{n_bits}.png')
    # print(xs)
    # print(ys)

plt.close()