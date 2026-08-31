import numpy as np

#Define constants
G = 6.67430e-11
SOLAR_MASS = 1.989e30
AU = 1.496e11
DAY_SECONDS = 86400
DAYS_PER_YEAR = 365.25
STEPS_PER_DAY = 4
EARTH_MASS = 5.9722e24

# Define functions
def calculate_energy(planet_mass, star_mass, radius, planet_velocity):
    potential_energy = (- G * star_mass * planet_mass) / radius
    planet_speed = np.linalg.norm(planet_velocity)
    kinetic_energy = 0.5 * planet_mass * (planet_speed ** 2)
    total_energy = kinetic_energy + potential_energy
    return total_energy


def simulate_orbit(time_period, planet_position, planet_velocity, star_mass, planet_mass):
    planet_x, planet_y, planet_velocities, times, energies = [], [], [], [], []
    dt = DAY_SECONDS / STEPS_PER_DAY
    for i in range(int(time_period * DAYS_PER_YEAR * STEPS_PER_DAY)): # Computes in quarter days
        planet_x.append(planet_position[0])
        planet_y.append(planet_position[1])
        planet_velocities.append(np.linalg.norm(planet_velocity))
        times.append(i * dt)

        radius = np.linalg.norm(planet_position)
        scalar_acceleration = (star_mass * G / (radius ** 2))

        # now find the negative unit vector of the radius squared in order to find the vector acceleration

        unit_radius = - planet_position / (radius)
        vector_acceleration = scalar_acceleration * unit_radius

        energy = calculate_energy(planet_mass, star_mass, radius, planet_velocity)
        energies.append(energy)
        # NOW WE NEED TO FIND THE NEW POSITION AND VELOCITY VECTOR AND MAP THEM INTO VARIABLES AND SPLIT THEM INTO COMPONENT

        planet_velocity += vector_acceleration * dt
        planet_position += planet_velocity * dt


    return np.array(planet_x), np.array(planet_y), planet_velocities, times, energies