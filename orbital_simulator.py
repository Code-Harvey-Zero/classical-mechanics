import numpy as np
import matplotlib.pyplot as plt

#define constants
G = 6.67430e-11
SOLAR_MASS = 1.989e30
AU = 1.496e11
DAY_SECONDS = 86400
DAYS_PER_YEAR = 365.25

def simulate_orbit(time_period, planet_position, planet_velocity, star_mass):
    for i in range(int(time_period * DAYS_PER_YEAR)): #A year is 365.25 days how to fix this?
        planet_x.append(planet_position[0])
        planet_y.append(planet_position[1])

        radius = np.linalg.norm(planet_position)
        scalar_acceleration = (star_mass * 6.67 * (10 ** -11)) / (radius ** 2)

        # now find the negative unit vector of the radius squared in order to find the vector acceleration

        unit_radius = - planet_position / (radius)
        vector_acceleration = scalar_acceleration * unit_radius

        # NOW WE NEED TO FIND THE NEW POSITION AND VELOCITY VECTOR AND MAP THEM INTO VARIABLES AND SPLIT THEM INTO COMPONENT

        planet_velocity += vector_acceleration * DAY_SECONDS
        planet_position += planet_velocity * DAY_SECONDS



# first of all get the required data from the planets
star_mass = int(input('Star Mass (Solar Masses): ')) * SOLAR_MASS

pos_input = input('Planet Initial Position (x, y) (AU): ')
planet_position = np.array([float(i) for i in pos_input.split(',')]) * AU

vel_input = input('Planet Initial Velocity (x, y) (km/s): ')
planet_velocity = np.array([float(i) for i in vel_input.split(',')]) * 1_000

time_period = int(input('Orbit Period (years): '))
planet_x, planet_y = [],[]

simulate_orbit(time_period, planet_position, planet_velocity, star_mass)

plt.plot(planet_x, planet_y)
plt.show()

