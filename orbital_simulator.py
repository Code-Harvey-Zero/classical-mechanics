import numpy as np
import matplotlib.pyplot as plt

# first of all get the required data from the planets
mass_star = int(input('Star Mass (kg): '))
mass_planet = int(input('Planet Mass (kg): '))

pos_input = input('Planet Initial Position (x, y) (m): ')
planet_position = np.array([float(i) for i in pos_input.split(',')])

vel_input = input('Planet Initial Velocity (x, y) (m/s): ')
planet_velocity = np.array([float(i) for i in vel_input.split(',')])

time_period = int(input('Orbit Period (years): '))



for i in range(time_period * 365):
    radius_squared = planet_position[0] ** 2 + planet_position[1] ** 2
    scalar_acceleration = (mass_star * 6.67 * (10 ** -11)) / radius_squared

    # now find the negative unit vector of the radius squared in order to find the vector acceleration
    unit_radius = - planet_position / (radius_squared ** 0.5)
    vector_acceleration = scalar_acceleration * unit_radius

    # NOW WE NEED TO FIND THE NEW POSITION AND VELOCITY VECTOR AND MAP THEM INTO VARIABLES AND SPLIT THEM INTO COMPONENT