import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
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
def update_star_mass(value):
    my_label_1.configure(text=f"{float(value):.2f}")
    update_simulation()

def update_planet_mass(value):
    my_label_2.configure(text=f"{float(value):.2f}")
    update_simulation()

def update_planet_position(value):
    my_label_3.configure(text=f"{float(value):.2f}")
    update_simulation()

def update_planet_velocity(value):
    my_label_4.configure(text=f"{float(value):.2f}")
    update_simulation()

def calculate_energy(planet_mass, star_mass, radius, planet_velocity):
    potential_energy = (- G * star_mass * planet_mass) / radius
    planet_speed = np.linalg.norm(planet_velocity)
    kinetic_energy = 0.5 * planet_mass * (planet_speed ** 2)
    total_energy = kinetic_energy + potential_energy
    return total_energy


def simulate_orbit(time_period, planet_position, planet_velocity, star_mass, planet_mass):
    planet_x, planet_y, planet_velocities, times, energies = [], [], [], [], []
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


def update_simulation():
    # first of all get the required data from the planets FROM SLIDERS
    star_mass = menu_slider_1.get() * SOLAR_MASS
    planet_mass = menu_slider_2.get() * EARTH_MASS

    planet_position = np.array([menu_slider_3.get(), 0]) * AU
    planet_velocity = np.array([0, menu_slider_4.get()]) * 1_000

    time_period = 1

    planet_x, planet_y, planet_velocities, times, energies = simulate_orbit(
        time_period,
        planet_position,
        planet_velocity,
        star_mass,
        planet_mass
    )



    ax.clear()

    ax.plot(planet_x, planet_y, label = 'Orbit')
    ax.scatter(0,0, label = 'Central body', color = 'orange')

    ax.set_xlabel('x position (m)')
    ax.set_ylabel('y position (m)')
    ax.axis('equal')
    ax.legend(loc='upper left')

    canvas.draw()


plt.plot(
    np.array(times) / (DAY_SECONDS * DAYS_PER_YEAR),
    np.array(energies) - energies[0]
)

plt.xlabel('Time (years)')
plt.ylabel('Change in Energy (J)')
plt.axhline(0, linestyle='--')
plt.show()

# Make Tkinter GUI
mpl.style.use(catppuccin.PALETTE.mocha.identifier)

window = tk.Tk()

window.title('Orbital Simulator')

icon = tk.PhotoImage(master=window, file='orbit_icon.png')
window.iconphoto(False, icon)

window.geometry('600x600')
window.minsize(600,600)

#layout widgets
menu_frame = ttk.Frame(window)
main_frame = ttk.Frame(window)

menu_frame.place(x = 0, y = 0, relwidth=0.3, relheight= 1)
main_frame.place(relx=0.3, y = 0, relwidth = 0.7, relheight = 1)

ttk.Label(main_frame, background = 'white').pack(expand= True, fill = 'both')


menu_slider_1 = ctk.CTkSlider(menu_frame, from_=0.1, to=5, command=update_star_mass, number_of_steps=990)
menu_slider_2 = ctk.CTkSlider(menu_frame, from_=0.1, to=10, command=update_planet_mass, number_of_steps=490)
menu_slider_3 = ctk.CTkSlider(menu_frame, from_=0.1, to=5, command=update_planet_position, number_of_steps=990)
menu_slider_4 = ctk.CTkSlider(menu_frame, from_=0, to=100, command=update_planet_velocity, number_of_steps=1000)

menu_slider_1.set(1)
menu_slider_2.set(1)
menu_slider_3.set(1)
menu_slider_4.set(30)

my_label_1 = ctk.CTkLabel(menu_frame, text=f'{menu_slider_1.get():.2f}', font=('Helvetica', 18), text_color='black')
my_label_2 = ctk.CTkLabel(menu_frame, text=f'{menu_slider_2.get():.2f}', font=('Helvetica', 18), text_color='black')
my_label_3 = ctk.CTkLabel(menu_frame, text=f'{menu_slider_3.get():.2f}', font=('Helvetica', 18), text_color='black')
my_label_4 = ctk.CTkLabel(menu_frame, text=f'{menu_slider_4.get():.2f}', font=('Helvetica', 18), text_color='black')

menu_frame.columnconfigure(0, weight = 1)
menu_frame.rowconfigure((0,1,2,3,4,5,6,7), weight = 1)

menu_slider_1.grid(row = 0, column = 0)
menu_slider_2.grid(row = 2, column = 0)
menu_slider_3.grid(row = 4, column = 0)
menu_slider_4.grid(row = 6, column = 0)

my_label_1.grid(row=1,column=0)
my_label_2.grid(row=3,column=0)
my_label_3.grid(row=5,column=0)
my_label_4.grid(row=7,column=0)

fig, ax = plt.subplots()

canvas = FigureCanvasTkAgg(fig, master = main_frame)
canvas.get_tk_widget().pack()
canvas.draw()

update_simulation()

window.mainloop()

# MAKE GRAPH READ SLIDER VALUE IN ORDER TO UPDATE ORBIT, ADD ENERGY PLOT, MAKE GUI LOOK NICE
# USE A BETTER MODEL TO FIND ORBIT ('INTEGRATION') HAS TOO MANY STEPS AND LEADS TO ENERGY DRIFT
# IF WE CAN GET THE ORBIT TO SHOW CONSERVATION OF ENERGY WE HAVE A GOOD MODEL

#LABEL, BIND SLIDER TO INPUT FIELD, SIZE GRAPH SO IT OCCUPIES SPACE OF SCREEN