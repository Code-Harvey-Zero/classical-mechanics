import numpy as np

import physics
import matplotlib.pyplot as plt
import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

import catppuccin
import matplotlib as mpl

animation_1 = None
animation_2 = None
orbit_line = None
planet_dot = None
energy_line=None
planet_x = None
planet_y = None
times = None
energies = None

def closing():
    window.quit()
    window.destroy()
    try:
        for after_id in window.tk.eval('after info').split():
            window.after_cancel(after_id)
    except:
        pass

def reset():
    for configure in variable_configurations:
        sld = sliders[configure['name']]
        sld.set(configure['default'])
    update_simulation()

def update_data(frame):
    orbit_line.set_data(
        planet_x[:frame + 1] / physics.AU,
        planet_y[:frame + 1] / physics.AU
    )

    planet_dot.set_offsets([
        planet_x[frame] / physics.AU,
        planet_y[frame] / physics.AU
    ])

    return orbit_line, planet_dot

def update_energy(frame):
    energy_line.set_data(np.array(times)[:frame + 1] / (physics.DAY_SECONDS * physics.DAYS_PER_YEAR),
        ((np.array(energies)[:frame + 1] - energies[0]) / abs(energies[0]) ) * 100)

    return energy_line,

def energy_plot_show():
    if show_energy.get() == 1:
        energy_frame.place(relx=0.76, rely=-0.01, relwidth=0.25, relheight=0.26)
    else:
        energy_frame.place_forget()


def update_simulation():
    global animation_1, animation_2, orbit_line, planet_dot, energy_line
    global planet_x, planet_y, energies, times

    if animation_1 is not None:
        if animation_1.event_source is not None:
            animation_1.event_source.stop()
        animation_1 = None

    if animation_2 is not None:
        if animation_2.event_source is not None:
            animation_2.event_source.stop()
        animation_2 = None

    # first of all get the required data from the planets FROM SLIDERS
    star_mass = sliders['star_mass'].get() * physics.SOLAR_MASS
    planet_mass = sliders['planet_mass'].get() * physics.EARTH_MASS

    planet_position = np.array([sliders['planet_position'].get(), 0], dtype=float) * physics.AU
    planet_velocity = np.array([0, sliders['planet_velocity'].get()], dtype=float) * 1_000
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

    ax1.plot(planet_x/physics.AU, planet_y/physics.AU, alpha=0)
    orbit_line, = ax1.plot([planet_x[0]/physics.AU],[planet_y[0]/physics.AU],label='Orbit', color='C0')

    # Layering from the widest outer glow down to the intense core
    ax1.scatter([0] * 5, [0] * 5, s=[300, 160, 70, 24, 6],
                color=['red', 'darkorange', 'orange', 'gold', 'white'],
                alpha=[0.03, 0.08, 0.2, 0.5, 1.0], edgecolors='none', label='Central Body')

    planet_dot = ax1.scatter(planet_x[0] / physics.AU, planet_y[0] / physics.AU, label= 'Planetary Body', color = '#00BFFF')

    ax1.set_xlabel('x position (AU)')
    ax1.set_ylabel('y position (AU)')
    ax1.axis('equal')
    ax1.set_title('Orbital Path')
    ax1.legend(loc='upper left')


    ax2.plot(
        np.array(times) / (physics.DAY_SECONDS * physics.DAYS_PER_YEAR),
        ((np.array(energies) - energies[0]) / abs(energies[0]) ) * 100, alpha=0
    )

    energy_line, = ax2.plot([0], [0])

    ax2.axhline(0 ,linestyle = 'dashed')

    ax2.set_xlabel('Time (years)')
    ax2.set_ylabel('Energy Error (%)')
    ax2.set_title('Energy Percentage Error vs Time')

    orbit_plot.tight_layout()
    energy_plot.tight_layout()

    orbit_canvas.draw_idle()
    energy_canvas.draw_idle()

    animation_1 = FuncAnimation(
        orbit_plot,
        update_data,
        frames=len(planet_x),
        interval=5,
        blit=True,
        repeat=False
    )

    animation_2 = FuncAnimation(energy_plot, update_energy, frames=len(planet_x), interval = 5, blit = True, repeat= False)
    # Make Tkinter GUI
mpl.style.use(catppuccin.PALETTE.mocha.identifier)

window = ctk.CTk()

window.title('Orbital Simulator')

try:
    icon = tk.PhotoImage(file='orbit_icon.png')
    window.iconphoto(False, icon)
except Exception:
    pass

window.minsize(1366,768)

#layout widgets
background_frame = ctk.CTkFrame(window, fg_color='#1e1e2e')
menu_frame = ctk.CTkTabview(window, fg_color='#64748B', corner_radius=10, border_width=1, border_color = '#CBD5E1', bg_color='#1e1e2e')
orbit_frame = ctk.CTkFrame(window)
energy_frame = ctk.CTkFrame(window, border_color='#CBD5E1', border_width=1, corner_radius=5, fg_color='#1e1e2e')

menu_frame.add('Planet')
menu_frame.add('Settings')

background_frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
menu_frame.place(relx=0.015, rely=0.01, relwidth=0.3, relheight=0.97)
orbit_frame.place(relx=0.3, y = 0, relwidth = 0.7, relheight = 1)

menu_frame.lift()

menu_frame.tab('Planet').columnconfigure((0,1), weight = 1)
menu_frame.tab('Planet').rowconfigure(list(range(5)), weight = 1)

variable_configurations = [
    {'name':'star_mass', 'label':'Star Mass (Solar Masses)', 'min': 0.1, 'max': 5 , 'default': 1, 'step':980},
    {'name':'planet_mass', 'label':'Planet Mass (Earth Masses)', 'min': 0.1, 'max': 10, 'default': 1 , 'step':980},
    {'name':'planet_position', 'label':'Planet x Position (AU)', 'min': 0.1, 'max': 5, 'default': 1 , 'step':980},
    {'name':'planet_velocity', 'label':'Planet y Velocity (km/s)', 'min': 0 , 'max': 100, 'default': 30, 'step':1000},
    {'name':'time_period', 'label':'Time Period (years)', 'min':1 , 'max':5 , 'default':1 , 'step':100}]

variables, sliders = {}, {}

for i, configure in enumerate(variable_configurations):
    row_frame = ctk.CTkFrame(master = menu_frame.tab('Planet'), width = 1)
    row_frame.grid(row=i, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    row_frame.columnconfigure(0, weight=4, uniform='row_col')
    row_frame.columnconfigure(1, weight=4, uniform='row_col')
    row_frame.columnconfigure(2, weight=1, uniform='row_col')


    lbl = ctk.CTkLabel(row_frame,
                       text=configure['label'],
                       font=("Helvetica", 14, "bold"),
                       fg_color='#313244',
                       border_width=1,
                       border_color='',
                       corner_radius=5,
                       padx=15,
                       pady=8)
    lbl.grid(row = 0, column=0, sticky = 'ew', padx = 10, pady = 10)

    var = tk.DoubleVar(value=configure['default'])
    variables[configure['name']] = var

    sld = ctk.CTkSlider(row_frame, from_=configure['min'], to=configure['max'], variable=var,
                        number_of_steps=configure['step'])
    sld.set(configure['default'])

    sliders[configure['name']] = sld
    sld.grid(row=0, column=1, sticky='e')

    box = ctk.CTkEntry(row_frame, width=60, textvariable=var)
    box.grid(row=0, column=2, sticky='w', padx=10)
    box.bind("<Return>", lambda event, name=configure["name"]: sliders[name].set(f"{variables[name].get():.3g}"))

run = ctk.CTkButton(menu_frame.tab('Planet'), text='Run', command = update_simulation)
run.grid(row=10, column = 1)

milky_way = ctk.CTkButton(menu_frame.tab('Planet'), text='Reset', command = reset)
milky_way.grid(row=10, column=0)

#settings section
show_energy = tk.IntVar()

energy_check_box = ctk.CTkCheckBox(menu_frame.tab('Settings'), text='Show Energy Plot',
                                   variable = show_energy, onvalue=1, offvalue=0, command=energy_plot_show)
energy_check_box.pack(pady=(40,10))

#set up
orbit_plot, ax1 = plt.subplots()

energy_plot, ax2 = plt.subplots()

orbit_canvas = FigureCanvasTkAgg(orbit_plot, master = orbit_frame)
orbit_canvas.get_tk_widget().pack(fill='both', expand=True)

energy_canvas = FigureCanvasTkAgg(energy_plot, master=energy_frame)
energy_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

update_simulation()

window.protocol('WM_DELETE_WINDOW', closing)

window.mainloop()

# change energy error graph appearance, and make it a draggable tab
# Make it so enter is required to put input
# Add validation for impossible/extreme inputs.

# Add Another Orbital body