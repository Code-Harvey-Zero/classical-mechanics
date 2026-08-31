import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import catppuccin
import matplotlib as mpl
from mpl_toolkits import mplot3d



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


def update_simulation():
    # first of all get the required data from the planets FROM SLIDERS
    star_mass = star_mass_slider.get() * SOLAR_MASS
    planet_mass = planet_mass_slider.get() * EARTH_MASS

    planet_position = np.array([planet_position_slider.get(), 0]) * AU
    planet_velocity = np.array([0, planet_velocity_slider.get()]) * 1_000

    time_period = time_period_slider.get()

    planet_x, planet_y, planet_velocities, times, energies = simulate_orbit(
        time_period,
        planet_position,
        planet_velocity,
        star_mass,
        planet_mass
    )



    ax1.clear()
    ax2.clear()

    ax1.plot(planet_x / AU, planet_y / AU, label = 'Orbit')
    ax1.scatter(0,0, label = 'Central body', color = 'orange')

    ax1.set_xlabel('x position (AU)')
    ax1.set_ylabel('y position (AU)')
    ax1.axis('equal')
    ax1.set_title('Orbital Path')
    ax1.legend(loc='upper left')


    ax2.plot(
        np.array(times) / (DAY_SECONDS * DAYS_PER_YEAR),
        np.array(energies)
    )

    ax2.set_xlabel('Time (years)')
    ax2.set_ylabel('Total Energy (J)')
    ax2.set_title('Total Energy vs Time')

    canvas.draw_idle()




# Make Tkinter GUI
mpl.style.use(catppuccin.PALETTE.mocha.identifier)

window = tk.Tk()

window.title('Orbital Simulator')

icon = tk.PhotoImage(master=window, file='orbit_icon.png')
window.iconphoto(False, icon)

window.geometry('600x600')
window.minsize(1024,768)

#layout widgets
menu_frame = ttk.Frame(window)
main_frame = ttk.Frame(window)

menu_frame.place(x = 0, y = 0, relwidth=0.3, relheight= 1)
main_frame.place(relx=0.3, y = 0, relwidth = 0.7, relheight = 1)

star_mass_var = tk.DoubleVar(value=1.00)
star_mass_var.trace_add("write", lambda *args: update_simulation())

planet_mass_var = tk.DoubleVar(value=1.00)
planet_mass_var.trace_add("write", lambda *args: update_simulation())

planet_position_var = tk.DoubleVar(value=1.00)
planet_position_var.trace_add("write", lambda *args: update_simulation())

planet_velocity_var = tk.DoubleVar(value=30.00)
planet_velocity_var.trace_add("write", lambda *args: update_simulation())

time_period_var = tk.IntVar(value=1)
time_period_var.trace_add("write", lambda *args: update_simulation())

star_mass_slider = ctk.CTkSlider(menu_frame, from_=0.1, to=5, variable=star_mass_var, number_of_steps=1000)
planet_mass_slider = ctk.CTkSlider(menu_frame, from_=0.1, to=10, variable=planet_mass_var, number_of_steps=1000)
planet_position_slider = ctk.CTkSlider(menu_frame, from_=0.1, to=5, variable=planet_position_var, number_of_steps=1000)
planet_velocity_slider = ctk.CTkSlider(menu_frame, from_=0, to=100, variable=planet_velocity_var, number_of_steps=1000)
time_period_slider = ctk.CTkSlider(menu_frame, from_=1, to=5, variable=time_period_var, number_of_steps=100)

star_mass_slider.set(1)
planet_mass_slider.set(1)
planet_position_slider.set(1)
planet_velocity_slider.set(30)
time_period_slider.set(1)

star_mass_box = tk.Entry(menu_frame, width=5, textvariable=star_mass_var)
star_mass_box.bind("<Return>", lambda event: menu_slider_1.set(to=star_mass_var.get()))

planet_mass_box = tk.Entry(menu_frame, width=5, textvariable=planet_mass_var)
planet_mass_box.bind("<Return>", lambda event: menu_slider_2.set(to=planet_mass_var.get()))

planet_position_box = tk.Entry(menu_frame, width=5, textvariable=planet_position_var)
planet_position_box.bind("<Return>", lambda event: menu_slider_3.set(to=planet_position_var.get()))

planet_velocity_box = tk.Entry(menu_frame, width=5, textvariable=planet_velocity_var)
planet_velocity_box.bind("<Return>", lambda event: menu_slider_4.set(to=planet_velocity_var.get()))

time_period_box = tk.Entry(menu_frame, width=5, textvariable=time_period_var)
time_period_box.bind("<Return>", lambda event: menu_slider_5.set(to=time_period_var.get()))

star_mass_label = tk.Label(menu_frame, text='Star Mass (Solar Masses):')
planet_mass_label = tk.Label(menu_frame, text='Planet Mass (Earth Masses):')
planet_position_label = tk.Label(menu_frame, text='Planet x Position (AU):')
planet_velocity_label = tk.Label(menu_frame, text='Planet y Velocity (km/s):')
time_period_label = tk.Label(menu_frame, text='Time Period (years):')

menu_frame.columnconfigure((0,1), weight = 1)
menu_frame.rowconfigure((0,1,2,3,4,5,6,7, 8, 9), weight = 1)

star_mass_slider.grid(row = 1, column = 0, sticky = 'ne')
planet_mass_slider.grid(row = 3, column = 0, sticky = 'ne')
planet_position_slider.grid(row = 5, column = 0, sticky = 'ne')
planet_velocity_slider.grid(row = 7, column = 0, sticky = 'ne')
time_period_slider.grid(row = 9, column = 0, sticky = 'ne')


star_mass_label.grid(row=0, sticky = 's')
planet_mass_label.grid(row=2, sticky = 's')
planet_position_label.grid(row=4, sticky = 's')
planet_velocity_label.grid(row=6, sticky = 's')
time_period_label.grid(row=8, sticky = 's')

star_mass_box.grid(row=1,column=1, sticky = 'nw')
planet_mass_box.grid(row=3,column=1, sticky = 'nw')
planet_position_box.grid(row=5,column=1, sticky = 'nw')
planet_velocity_box.grid(row=7,column=1, sticky = 'nw')
time_period_box.grid(row=9,column=1, sticky = 'nw')

fig = plt.figure()
fig.tight_layout()

ax1 = fig.add_subplot(1, 2, 1) # ADD projection='3d' to make plot 3d
ax2 = fig.add_subplot(1,2,2)

canvas = FigureCanvasTkAgg(fig, master = main_frame)
canvas.get_tk_widget().pack(fill='both', expand=True)

update_simulation()

window.mainloop()

# USE A BETTER MODEL TO FIND ORBIT ('INTEGRATION') HAS TOO MANY STEPS AND LEADS TO ENERGY DRIFT
# IF WE CAN GET THE ORBIT TO SHOW CONSERVATION OF ENERGY WE HAVE A GOOD MODEL

#FORMAT ALL GRIDS AND WIDGETS BETTER

#CREATE NEW FILE STRUCTURE
#Move physics into physics.py
#Move simulate orbit into simulation.py
#main.py only responsible for starting application 