import numpy as np
import physics
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import catppuccin
import matplotlib as mpl

def closing():
    window.quit()
    window.destroy()
    try:
        for after_id in window.tk.eval('after info').split():
            window.after_cancel(after_id)
    except:
        pass

def update_simulation():
    # first of all get the required data from the planets FROM SLIDERS
    star_mass = sliders['star_mass'].get() * physics.SOLAR_MASS
    planet_mass = sliders['planet_mass'].get() * physics.SOLAR_MASS

    planet_position = np.array([sliders['planet_position'].get(), 0]) * physics.AU
    planet_velocity = np.array([0, sliders['planet_velocity'].get()]) * 1_000

    time_period = sliders['time_period'].get()

    planet_x, planet_y, planet_velocities, times, energies = physics.simulate_orbit(
        time_period,
        planet_position,
        planet_velocity,
        star_mass,
        planet_mass
    )


    try:
        ax1.clear()
        ax2.clear()
    except:
        return

    ax1.plot(planet_x / physics.AU, planet_y / physics.AU, label ='Orbit')
    ax1.scatter(0,0, label = 'Central body', color = 'orange')

    ax1.set_xlabel('x position (AU)')
    ax1.set_ylabel('y position (AU)')
    ax1.axis('equal')
    ax1.set_title('Orbital Path')
    ax1.legend(loc='upper left')


    ax2.plot(
        np.array(times) / (physics.DAY_SECONDS * physics.DAYS_PER_YEAR),
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

menu_frame.columnconfigure((0,1), weight = 1)
menu_frame.rowconfigure((0,1,2,3,4,5,6,7, 8, 9), weight = 1)

variable_configurations = [
    {'name':'star_mass', 'label':'Star Mass (Solar Masses):', 'min': 0.1, 'max': 5 , 'default': 1, 'step':1000},
    {'name':'planet_mass', 'label':'Planet Mass (Earth Masses):', 'min': 0.1, 'max': 10, 'default': 1 , 'step':1000},
    {'name':'planet_position', 'label':'Planet x Position (AU):', 'min': 0.1, 'max': 5, 'default': 1 , 'step':1000},
    {'name':'planet_velocity', 'label':'Planet y Velocity (km/s):', 'min': 0 , 'max': 100, 'default': 30, 'step':1000},
    {'name':'time_period', 'label':'Time Period (years):', 'min':1 , 'max':5 , 'default':1 , 'step':100}]

variables, sliders = {}, {}

for configure in variable_configurations:

    var = tk.DoubleVar(value=configure['default'])
    variables[configure['name']] = var

    sld = ctk.CTkSlider(menu_frame, from_=configure['min'], to=configure['max'], variable=var,
                        number_of_steps=configure['step'])
    sld.set(configure['default'])
    sliders[configure['name']] = sld

for i, configure in enumerate(variable_configurations):
    label_row = i * 2
    control_row = i * 2 + 1

    lbl = tk.Label(menu_frame, text=configure['label'])
    lbl.grid(row=label_row, column=0, sticky='s')

    sld = sliders[configure['name']]
    sld.grid(row=control_row, column=0, sticky = 'ne')

    var = variables[configure['name']]
    box = tk.Entry(menu_frame, width=5, textvariable=var)
    box.grid(row=control_row, column=1, stick = 'nw')
    box.bind("<Return>", lambda event, name=configure["name"]: sliders[name].set(variables[name].get()))

    var.trace_add("write", lambda *args: update_simulation())


fig = plt.figure()
fig.tight_layout()

ax1 = fig.add_subplot(1, 2, 1) # ADD projection='3d' to make plot 3d
ax2 = fig.add_subplot(1,2,2)

canvas = FigureCanvasTkAgg(fig, master = main_frame)
canvas.get_tk_widget().pack(fill='both', expand=True)

update_simulation()

window.protocol('WM_DELETE_WINDOW', closing)

window.mainloop()

# USE A BETTER MODEL TO FIND ORBIT ('INTEGRATION') HAS TOO MANY STEPS AND LEADS TO ENERGY DRIFT
# IF WE CAN GET THE ORBIT TO SHOW CONSERVATION OF ENERGY WE HAVE A GOOD MODEL

#FORMAT ALL GRIDS AND WIDGETS BETTER