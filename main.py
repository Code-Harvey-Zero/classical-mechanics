import numpy as np

import physics
import widgets
import matplotlib.pyplot as plt
import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

import catppuccin
import matplotlib as mpl

animation_1 = None
animation_2 = None
orbit_lines = []
planet_dots = None
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
    for body in widgets.Body.all_instances:
        body.reset()

    update_simulation()

def update_data(frame):
    for i in range(number_of_planets):
        orbit_lines[i].set_data(
            planet_x[:frame + 1, i] / physics.AU,
            planet_y[:frame + 1, i] / physics.AU
        )

    planet_dots.set_offsets(
        np.column_stack((
            planet_x[frame, :] / physics.AU,
            planet_y[frame, :] / physics.AU
        ))
    )

    return orbit_lines + [planet_dots]

def update_energy(frame):
    energy_line.set_data(np.array(times)[:frame + 1] / (physics.DAY_SECONDS * physics.DAYS_PER_YEAR),
        ((np.array(energies)[:frame + 1] - energies[0]) / abs(energies[0]) ) * 100)

    return energy_line,

def energy_plot_show():
    if show_energy.get() == 1:
        energy_frame.place(relx=0.75, rely=-0.00, relwidth=0.25, relheight=0.26)
    else:
        energy_frame.place_forget()


def update_simulation():
    global animation_1, animation_2, orbit_lines, planet_dots, energy_line
    global planet_x, planet_y, energies, times

    if animation_1 is not None:
        if animation_1.event_source is not None:
            animation_1.event_source.stop()
        animation_1 = None

    if animation_2 is not None:
        if animation_2.event_source is not None:
            animation_2.event_source.stop()
        animation_2 = None

    try:
        ax1.clear()
        ax2.clear()
    except:
        return


    params = star_widget.get_parameters()
    star_mass = params['star_mass'] * physics.SOLAR_MASS
    star_radius = params['star_radius']
    params = general_widget.get_parameters()
    time_period = params['time_period']

    planet_masses = []
    planet_position = []
    planet_velocity = []
    planet_radii = []

    for i in range(number_of_planets):
        params = planet_widgets[i].get_parameters()

        planet_masses.append(
            params['planet_mass'] * physics.EARTH_MASS
        )

        planet_position.append([
            params['planet_position'] * physics.AU,
            0
        ])

        planet_velocity.append([
            0,
            params['planet_velocity'] * 1_000
        ])

        planet_radii.append(params['planet_radius'] ** 2 * 10 )

    planet_masses = np.array(planet_masses)
    planet_position = np.array(planet_position)
    planet_velocity = np.array(planet_velocity)

    planet_x, planet_y, planet_velocities, times, energies = physics.simulate_orbit(
        time_period,
        planet_position,
        planet_velocity,
        star_mass,
        planet_masses
    )


    ax1.plot(planet_x/physics.AU, planet_y/physics.AU, alpha=0)

    orbit_lines = []

    for i in range(number_of_planets):
        line, = ax1.plot([], [], zorder=1, color='#74C7EC')
        orbit_lines.append(line)
    # Layering from the widest outer glow down to the intense core
    ax1.scatter(
        [0] * 5,
        [0] * 5,
        s=np.array([3000, 1600, 700, 240, 60]) * (star_radius**2),
        color=['red', 'darkorange', 'orange', 'gold', 'white'],
        alpha=[0.03, 0.08, 0.2, 0.5, 1.0],
        edgecolors='none',
        label='Central Body',
        zorder=4
    )

    planet_dots = ax1.scatter(planet_x[0] / physics.AU, planet_y[0] / physics.AU, label= ['Planetary Body 1'], s=planet_radii,zorder=2)

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

    animation_1 = FuncAnimation(orbit_plot,update_data,frames=len(planet_x),interval=5,blit=True,repeat=False)

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
menu_frame = ctk.CTkFrame(window, fg_color='#64748B', corner_radius=10, border_width=1, border_color = '#CBD5E1', bg_color='#1e1e2e')
tab_frame = ctk.CTkTabview(menu_frame, fg_color='#64748B', corner_radius=10, bg_color='#64748B', border_color='#1e1e2e', border_width=2)
orbit_frame = ctk.CTkFrame(window)
energy_frame = ctk.CTkFrame(window, border_color='#CBD5E1', border_width=1, corner_radius=5, fg_color='#1e1e2e')




background_frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
menu_frame.place(relx=0.015, rely=0.01, relwidth=0.3, relheight=0.97)
orbit_frame.place(relx=0.3, y = 0, relwidth = 0.7, relheight = 1)

menu_frame.lift()

star_widget = widgets.StarWidget(menu_frame, fg_color='#64748B')
star_widget.pack(padx=10,pady=10)
tab_frame.pack(fill='both',expand=True,padx=10,pady=10)
general_widget = widgets.GeneralSettings(menu_frame, fg_color='#64748B')
general_widget.pack(padx=10,pady=10)

planets_data = [
    {
        'name': 'Mercury',
        'planet_position': 0.39,
        'planet_velocity': 47.4,
        'planet_radius': 0.38
    },
    {
        'name': 'Venus',
        'planet_position': 0.72,
        'planet_velocity': 35.0,
        'planet_radius': 0.95
    },
    {
        'name': 'Earth',
        'planet_position': 1.00,
        'planet_velocity': 29.8,
        'planet_radius': 1.00
    },
    {
        'name': 'Mars',
        'planet_position': 1.52,
        'planet_velocity': 24.1,
        'planet_radius': 0.53
    },
    {
        'name': 'Jupiter',
        'planet_position': 5.20,
        'planet_velocity': 13.1,
        'planet_radius': 11.21
    },
    {
        'name': 'Saturn',
        'planet_position': 9.58,
        'planet_velocity': 9.7,
        'planet_radius': 9.45
    },
    {
        'name': 'Uranus',
        'planet_position': 19.20,
        'planet_velocity': 6.8,
        'planet_radius': 4.01
    },
    {
        'name': 'Neptune',
        'planet_position': 30.05,
        'planet_velocity': 5.4,
        'planet_radius': 3.88
    }
]


number_of_planets = params = int(general_widget.get_parameters()['number_of_planets'])

planet_widgets = []

for i in range(number_of_planets):
    tab_frame.add(planets_data[i]['name'])
    planet_tab = tab_frame.tab(planets_data[i]['name'])

    planet_tab.columnconfigure((0, 1), weight=1)

    planet_widget = widgets.PlanetWidget(
        planet_tab,
        tabview=tab_frame,
        tab_name=[planets_data[i]['name']],
        fg_color='#64748B'
    )

    planet_widget.pack(
        fill='both',
        expand=True,
        padx=10,
        pady=10
    )

    planet_widgets.append(planet_widget)

tab_frame.add('Settings')

button_frame = ctk.CTkFrame(menu_frame, fg_color='#64748B')
button_frame.pack(fill='x',padx=10,pady=10)

run = ctk.CTkButton(button_frame,text='Run',command=update_simulation, bg_color='#64748B')
run.pack(side='right', padx=5)

milky_way = ctk.CTkButton(button_frame,text='Reset',command=reset, bg_color='#64748B')
milky_way.pack(side='left', padx=5)

#settings section
show_energy = tk.IntVar()

energy_check_box = ctk.CTkCheckBox(tab_frame.tab('Settings'), text='Show Energy Plot',
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

#Todo
# Add more planets and then make it a loop
# Make it so user can choose N number of planets (Slider and entry box)
# Add validation for impossible/extreme inputs.
# Make draggable tab class
# Combine animation Functions?
# Change architecture