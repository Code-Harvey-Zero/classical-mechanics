import numpy as np

#Define constants
G = 6.67430e-11
SOLAR_MASS = 1.989e30
AU = 1.496e11
DAY_SECONDS = 86400
DAYS_PER_YEAR = 365.25
STEPS_PER_DAY = 2
EARTH_MASS = 5.9722e24

# Define functions
def calculate_acceleration(planet_position, star_mass,planet_masses, radius):
    scalar_acceleration = (star_mass * G / (radius ** 2))
    unit_radius = -planet_position / radius[:, None]
    vector_acceleration = scalar_acceleration[:, None] * unit_radius

    for i in range(len(planet_masses)):
        for j in range(len(planet_masses)):
            if i == j:
                continue
            seperation_vector = planet_position[j] - planet_position[i]
            seperation = np.linalg.norm(seperation_vector)
            if seperation ==0:
                continue
            else:
                vector_acceleration[i] += (planet_masses[j] * G * seperation_vector) / (seperation**3)
    # now find the negative unit vector of the radius squared in order to find the vector acceleration



    return vector_acceleration

def calculate_energy(planet_masses, star_mass, radius, planet_velocity):
    potential_energy = (- G * star_mass * planet_masses) / radius
    planet_speed = np.linalg.norm(planet_velocity)
    kinetic_energy = 0.5 * planet_masses * (planet_speed ** 2)
    total_energy = kinetic_energy + potential_energy
    return total_energy


def simulate_orbit(time_period, planet_position, planet_velocity, star_mass, planet_masses):
    planet_position = np.array(planet_position, dtype=float)
    planet_velocity = np.array(planet_velocity, dtype=float)
    planet_x, planet_y, planet_velocities, times, energies = np.empty((0,2)), np.empty((0,2)), [], [], []
    dt = DAY_SECONDS / STEPS_PER_DAY
    for i in range(int(time_period * DAYS_PER_YEAR * STEPS_PER_DAY)): # Computes in quarter days
        radius = np.linalg.norm(planet_position, axis=1)

        vector_acceleration = calculate_acceleration(planet_position, star_mass,planet_masses, radius)

        # NOW WE NEED TO FIND THE NEW POSITION AND VELOCITY VECTOR AND MAP THEM INTO VARIABLES AND SPLIT THEM INTO COMPONENT

        planet_velocity += 0.5 * vector_acceleration * dt
        planet_position += planet_velocity * dt

        radius = np.linalg.norm(planet_position, axis=1)

        vector_acceleration = calculate_acceleration(planet_position, star_mass, planet_masses, radius)

        planet_velocity += 0.5 * vector_acceleration * dt

        planet_x = np.append(planet_x, [planet_position[:, 0]], axis=0)
        planet_y = np.append(planet_y, [planet_position[:, 1]], axis=0)
        planet_velocities.append(np.linalg.norm(planet_velocity))
        times.append((i + 1) * dt)

        energy = calculate_energy(planet_masses, star_mass, radius, planet_velocity)
        energies.append(energy)


    return np.array(planet_x), np.array(planet_y), np.array(planet_velocities), np.array(times), np.array(energies)

# Velocity Verlet