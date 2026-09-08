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
    distance[distance == 0] = np.inf
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
    distance[distance == 0] = np.inf

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
    body_accelerations = []
    planet_x, planet_y, planet_speeds, body_velocities, times, energies = np.empty((0,len(masses))), np.empty((0,len(masses))),[], [], [], []
    dt = DAY_SECONDS / STEPS_PER_DAY
    for i in range(int(time_period * DAYS_PER_YEAR * STEPS_PER_DAY)): # Computes in half days

        accelerations = calculate_acceleration(positions,masses)

        velocities += 0.5 * accelerations * dt
        positions += velocities * dt

        accelerations = calculate_acceleration(positions, masses)

        velocities += 0.5 * accelerations * dt

        planet_x = np.append(planet_x, [positions[:, 0]], axis=0)
        planet_y = np.append(planet_y, [positions[:, 1]], axis=0)
        planet_speeds.append(np.linalg.norm(velocities, axis=1))
        body_velocities.append(velocities[:, :2].copy())
        body_accelerations.append(accelerations[:,:2].copy())
        times.append((i + 1) * dt)

        energy = calculate_energy(masses, positions, velocities)
        energies.append(energy)

    return planet_x, planet_y, np.array(planet_speeds), np.array(body_velocities), np.array(times), np.array(energies), np.array(body_accelerations)

# Velocity Verlet

#Todo
# Make it so sun feels gravitational force