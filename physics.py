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
def calculate_acceleration(positions,masses):
    separation = positions[None, :, :] - positions[:, None, :]
    distance = np.linalg.norm(separation, axis=2)
    np.fill_diagonal(distance, np.inf)
    vector_acceleration = (
            G
            * masses[None, :, None]
            * separation
            / distance[:, :, None] ** 3
    )
    vector_acceleration = np.sum(vector_acceleration, axis=1)


    return vector_acceleration

def calculate_energy(masses, positions, velocities):
    speeds = np.linalg.norm(velocities, axis=1)

    kinetic_energy = np.sum(
        0.5 * masses * speeds**2
    )

    separation = positions[None, :, :] - positions[:, None, :]
    distance = np.linalg.norm(separation, axis=2)

    np.fill_diagonal(distance, np.inf)

    potential = -G * masses[:, None] * masses[None, :] / distance

    potential_energy = np.sum(
        np.triu(potential, k=1)
    )

    total_energy = potential_energy + kinetic_energy

    return total_energy


def simulate_orbit(time_period, positions, velocities, masses):
    positions = np.array(positions, dtype=float)
    velocities = np.array(velocities, dtype=float)
    masses = np.array(masses, dtype=float)
    planet_x, planet_y, planet_velocities, times, energies = np.empty((0,len(masses))), np.empty((0,len(masses))), [], [], []
    dt = DAY_SECONDS / STEPS_PER_DAY
    for i in range(int(time_period * DAYS_PER_YEAR * STEPS_PER_DAY)): # Computes in half days

        accelerations = calculate_acceleration(positions,masses)
        if i % (STEPS_PER_DAY * 100) == 0:
            mars_distance = np.linalg.norm(positions[4]) / AU
            print(
                f"Time: {i / STEPS_PER_DAY:.1f} days, "
                f"Mars distance: {mars_distance:.3f} AU"
            )
        # NOW WE NEED TO FIND THE NEW POSITION AND VELOCITY VECTOR AND MAP THEM INTO VARIABLES AND SPLIT THEM INTO COMPONENT

        velocities += 0.5 * accelerations * dt
        positions += velocities * dt



        accelerations = calculate_acceleration(positions, masses)

        velocities += 0.5 * accelerations * dt

        planet_x = np.append(planet_x, [positions[:, 0]], axis=0)
        planet_y = np.append(planet_y, [positions[:, 1]], axis=0)
        planet_velocities.append(np.linalg.norm(velocities, axis=1))
        times.append((i + 1) * dt)

        energy = calculate_energy(masses, positions, velocities)
        energies.append(energy)


    return np.array(planet_x), np.array(planet_y), np.array(planet_velocities), np.array(times), np.array(energies)

# Velocity Verlet

#Todo
# Make it so sun feels gravitational force