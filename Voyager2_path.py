#Importing all the necessary libraries and modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

#assigning a list of the spatial objects to a variable name

space_bodies = ['earth', 'mars', 'jupiter', 'saturn', 'uranus', 'voyager2']

#defining a function that can read the data from the given file through the years

def get_trajectory(filename):
    """Get the trajectory data from given file."""

    def get_line(line):
        """Get a single line of the data file, returning position (x,y,z)."""
        x, y, z = line[4:26], line[30:52], line[56:78]
        return float(x), float(y), float(z)

    dates, xyz = [], []
    with open(filename) as data_file:
        while not data_file.readline().strip() == '$$SOE':
            pass
        while True:
            line = data_file.readline().rstrip()
            if line == '$$EOE':
                break
            if 'A.D.' in line:
                date = line[25:36]
                if date.startswith('1988-Jul'): 
		
	#Take a pause from reading the data
                    break
                dates.append(date)
            elif line.startswith(' X ='):
                xyz.append(get_line(line))

    return dates, np.array(xyz).T
	
	
	#Defining a class that represents the trajectory of a celestial body.

class Trajectory:
    """This class represents the trajectory of a celestial object"""

    def __init__(self, r, c, trajectory):
        """
        Initilize the Trajectory object with a radius r of the circle to plot,
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
        try:
            return self.traj[0][i], self.traj[1][i]
        except IndexError:
            pass


# Initialize the Trajectory objects for each of the objects.
ephemerides = {
        'earth': Trajectory(0.3, 'tab:red', get_trajectory('C:/Users/user/Desktop/CSC project/earth.txt')),
        'mars': Trajectory(0.3, 'tab:blue', get_trajectory('C:/Users/user/Desktop/CSC project/mars.txt')),
        'jupiter': Trajectory(0.6, 'w', get_trajectory('C:/Users/user/Desktop/CSC project/jupiter.txt')),
        'saturn': Trajectory(0.5, 'brown', get_trajectory('C:/Users/user/Desktop/CSC project/saturn.txt')),
        'uranus': Trajectory(0.4, 'tab:green', get_trajectory('C:/Users/user/Desktop/CSC project/uranus.txt')),
        'voyager2': Trajectory(0.2, 'tab:orange', get_trajectory('C:/Users/user/Desktop/CSC project/voyager2.txt')),
              }

# Black figure with Axes panel removed.
fig, ax = plt.subplots()
fig.patch.set_facecolor('k')
ax.axis('off')

# Initialize the objects and put the Matplotlib artists into a list, e_objs.
e_objs = []
for eph_name, ephemeris in ephemerides.items():
    if eph_name != 'voyager2':
        # Plot trajectory paths for other celestial objects.
        ax.plot(*ephemeris.get_xy(), c=ephemeris.c, lw=0.5)
    # Circles represent each of the objects; start in initial positions.
    e_circ = Circle(xy=ephemeris.get_xy(0), radius=ephemeris.r,
                    fc=ephemeris.c, zorder=10)
    ax.add_patch(e_circ)
    e_objs.append(e_circ)

# Trajectory path for Voyager 2 initialized empty.
e_line, = ax.plot([], [], c=ephemerides['voyager2'].c, lw=0.5)
e_objs.append(e_line)
label = ax.text(15, 15, '', c='w')
e_objs.append(label)

def initialise():
    "Initialising function to draw a clear frame"
    for i, ephemeris in enumerate(ephemerides.values()):
        e_objs[i].center = ephemeris.get_xy(0)
    e_line.set_data([], [])
    return e_objs

def reformat_date(date):
    """Change date string format from YYYY-Mon-DD to DD-Mon-YYYY."""
    return '-'.join(date.split('-')[::-1])

def animate(j):
    """Advance the animation by one time step."""
    for i, ephemeris in enumerate(ephemerides.values()):
        e_circ = e_objs[i]
        e_circ.set_center(ephemeris.get_xy(j))
        e_line.set_data(ephemeris.traj[0][:j], ephemeris.traj[1][:j])
    e_line.set_data(ephemerides['voyager2'].traj[0][:j],
                    ephemerides['voyager2'].traj[1][:j])
    try:
        label.set_text(reformat_date(ephemerides['voyager2'].date_series[j]))
    except IndexError:
        pass
    return e_objs

limit = 25
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
reference_holder = animation.FuncAnimation(fig, animate, interval=1, init_func=initialise,
                        blit=True)
plt.show()
