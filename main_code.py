import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

eph_names = ['earth', 'mars', 'jupiter', 'saturn', 'uranus', 'voyager2']

def get_ephemeris(filename):
    """Get the ephemeris data from filename."""

    def parse_line(line):
        """Parse a single line of the data file, returning position, (x,y,z)."""
        sx, sy, sz = line[4:26], line[30:52], line[56:78]
        return float(sx), float(sy), float(sz)

    dates, xyz = [], []
    print(filename)
    with open(filename) as fi:
        while not fi.readline().strip() == '$$SOE':
            pass
        while True:
            line = fi.readline().rstrip()
            if line == '$$EOE':
                break
            if 'A.D.' in line:
                date = line[25:36]
                if date.startswith('1988-Jul'):
                    # Stop reading data at this date.
                    break
                dates.append(date)
            elif line.startswith(' X ='):
                xyz.append(parse_line(line))
            # Otherwise, this line doesn't interest us: move on.

    return dates, np.array(xyz).T


class Ephemeris:
    """A simple class representing the trajectory of an astronomical object."""

    def __init__(self, r, c, trajectory):
        """
        Initilize the Ephemeris object with a radius, r of the circle to plot,
        colour, c, and trajectory parsed from its HORIZON file, traj.

        """

        self.r = r
        self.c = c
        self.date_series, self.traj = trajectory

    def get_xy(self, i=None):
        """
        Get the x, y position of the object. If i is None, return the entire
        trajectory in an array, otherwise return the position at index i.

        """

        if i is None:
            return self.traj[:2]
        return self.traj[0][i], self.traj[1][i]


# Initialize the Ephemeris objects for each of the objects.
ephemerides = {
        'earth': Ephemeris(0.3, 'tab:blue', get_ephemeris("C:/Users/Jossy/Documents/School/CSC/CSC Project/earth.txt")),
        'mars': Ephemeris(0.3, 'tab:red', get_ephemeris("C:/Users/Jossy/Documents/School/CSC/CSC Project/mars.txt")),
        'jupiter': Ephemeris(0.6, 'tab:orange', get_ephemeris("C:/Users/Jossy/Documents/School/CSC/CSC Project/jupiter.txt")),
        'saturn': Ephemeris(0.5, 'brown', get_ephemeris("C:/Users/Jossy/Documents/School/CSC/CSC Project/saturn.txt")),
        'uranus': Ephemeris(0.4, 'tab:green', get_ephemeris("C:/Users/Jossy/Documents/School/CSC/CSC Project/uranus.txt")),
        'voyager2': Ephemeris(0.2, 'w', get_ephemeris("C:/Users/Jossy/Documents/School/CSC/CSC Project/voyager2.txt")),
              }

# Black figure with Axes panel removed.
fig, ax = plt.subplots()
fig.patch.set_facecolor('k')
ax.axis('off')

# Initialize the objects and pack the Matplotlib artists into a list, e_objs.
e_objs = []
for eph_name, ephemeris in ephemerides.items():
    if eph_name != 'voyager2':
        # Plot trajectory paths for objects other than Voyager 2.
        ax.plot(*ephemeris.get_xy(), c=ephemeris.c, lw=0.5)
    # Circles represent each of the objects; start in initial positions.
    e_circ = Circle(xy=ephemeris.get_xy(0), radius=ephemeris.r,
                    fc=ephemeris.c, zorder=10)
    ax.add_patch(e_circ)
    e_objs.append(e_circ)

# This is the trajectory path for Voyager 2 (initialize as empty.)
e_line, = ax.plot([], [], c=ephemerides['voyager2'].c, lw=0.5)
e_objs.append(e_line)
label = ax.text(15, 15, '', c='w')
e_objs.append(label)

def init():
    for i, ephemeris in enumerate(ephemerides.values()):
        e_objs[i].center = ephemeris.get_xy(0)
    e_line.set_data([], [])
    return e_objs

def reformat_date(date):
    """Reverse date string from YYYY-Mon-DD to DD-Mon-YYYY."""
    return '-'.join(date.split('-')[::-1])

def animate(j):
    """Advance the animation by one time step."""
    for i, ephemeris in enumerate(ephemerides.values()):
        e_circ = e_objs[i]
        e_circ.set_center(ephemeris.get_xy(j))
        e_line.set_data(ephemeris.traj[0][:j], ephemeris.traj[1][:j])
    e_line.set_data(ephemerides['voyager2'].traj[0][:j],
                    ephemerides['voyager2'].traj[1][:j])
    label.set_text(reformat_date(ephemerides['voyager2'].date_series[j]))

    return e_objs

lim = 25
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ani = animation.FuncAnimation(fig, animate, interval=1, init_func=init,
                        blit=True)
plt.show()
