import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import catppuccin
import matplotlib as mpl


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
    for i in range(int(time_period * DAYS_PER_YEAR * STEPS_PER_DAY)): # Computes in quarter days
        planet_x.append(planet_position[0])
        planet_y.append(planet_position[1])
        planet_velocities.append(np.linalg.norm(planet_velocity))
        times.append(i * DAY_SECONDS / STEPS_PER_DAY)

        radius = np.linalg.norm(planet_position)
        scalar_acceleration = (star_mass * G / (radius ** 2))

        # now find the negative unit vector of the radius squared in order to find the vector acceleration

        unit_radius = - planet_position / (radius)
        vector_acceleration = scalar_acceleration * unit_radius

        energy = calculate_energy(planet_mass, star_mass, radius, planet_velocity)
        energies.append(energy)
        # NOW WE NEED TO FIND THE NEW POSITION AND VELOCITY VECTOR AND MAP THEM INTO VARIABLES AND SPLIT THEM INTO COMPONENT

        planet_velocity += vector_acceleration * (DAY_SECONDS / STEPS_PER_DAY)
        planet_position += planet_velocity * (DAY_SECONDS / STEPS_PER_DAY)


    return planet_x, planet_y, planet_velocities, times, energies


# first of all get the required data from the planets
star_mass = int(input('Star Mass (Solar Masses): ')) * SOLAR_MASS
planet_mass = int(input('Star Mass (Earth Masses): ')) * EARTH_MASS

pos_input = input('Planet Initial Position (x, y) (AU): ')
planet_position = np.array([float(i) for i in pos_input.split(',')]) * AU

vel_input = input('Planet Initial Velocity (x, y) (km/s): ')
planet_velocity = np.array([float(i) for i in vel_input.split(',')]) * 1_000

time_period = int(input('Orbit Period (years): '))
planet_x, planet_y, planet_velocities, times, energies = [], [], [], [], []

simulate_orbit(time_period,
               planet_position,
               planet_velocity,
               star_mass, planet_mass)

mpl.style.use(catppuccin.PALETTE.mocha.identifier)

fig, ax = plt.subplots()

ax.plot(planet_x, planet_y, label = 'Orbit')
ax.scatter(0,0, label = 'Central body', color = 'orange')

ax.set_xlabel('x position (m)')
ax.set_ylabel('y position (m)')
ax.axis('equal')
ax.legend(loc='upper left')

# plt.plot(
#     np.array(times) / (DAY_SECONDS * DAYS_PER_YEAR),
#     np.array(energies) - energies[0]
# )
#
# plt.xlabel('Time (years)')
# plt.ylabel('Change in Energy (J)')
# plt.axhline(0, linestyle='--')
# plt.show()

# Make Tkinter GUI
window = tk.Tk()

window.title('Orbital Simulator')

icon = tk.PhotoImage(master=window,file='orbit_icon.png')
window.iconphoto(False, icon)

window.geometry('600x600')
window.minsize(600,600)

#layout widgets
menu_frame = ttk.Frame(window)
main_frame = ttk.Frame(window)

menu_frame.place(x = 0, y = 0, relwidth=0.3, relheight= 1)
main_frame.place(relx=0.3, y = 0, relwidth = 0.7, relheight = 1)

ttk.Label(main_frame, background = 'blue').pack(expand= True, fill = 'both')

menu_slider1 = ttk.Scale(menu_frame)
menu_slider2 = ttk.Scale(menu_frame)
menu_slider3 = ttk.Scale(menu_frame)
menu_slider4 = ttk.Scale(menu_frame)

menu_frame.columnconfigure(0, weight = 1)
menu_frame.rowconfigure((0,1,2,3), weight = 1)

menu_slider1.grid(row = 0, column = 0)
menu_slider2.grid(row = 1, column = 0)
menu_slider3.grid(row = 2, column = 0)
menu_slider4.grid(row = 3, column = 0)

canvas = FigureCanvasTkAgg(fig, master = main_frame)
canvas.get_tk_widget().pack()
canvas.draw()

window.mainloop()

# MAKE GRAPH READ SLIDER VALUE IN ORDER TO UPDATE ORBIT, ADD ENERGY PLOT, MAKE GUI LOOK NICE
# USE A BETTER MODEL TO FIND ORBIT ('INTEGRATION') HAS TOO MANY STEPS AND LEADS TO ENERGY DRIFT
# IF WE CAN GET THE ORBIT TO SHOW CONSERVATION OF ENERGY WE HAVE A GOOD MODEL