import numpy as np

import physics
import widgets
import matplotlib.pyplot as plt
import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

import catppuccin
import matplotlib as mpl

animation_1 = None
animation_2 = None
orbit_line_1 = None
planet_dots = None
orbit_line_2 = None
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
    planet_widget_1.reset()
    planet_widget_2.reset()
    update_simulation()

def update_data(frame):
    orbit_line_1.set_data(
        planet_x[:frame + 1, 0] / physics.AU,
        planet_y[:frame + 1, 0] / physics.AU
    )

    orbit_line_2.set_data(
        planet_x[:frame + 1, 1] / physics.AU,
        planet_y[:frame + 1, 1] / physics.AU
    )

    planet_dots.set_offsets(
        np.column_stack((
            planet_x[frame, :] / physics.AU,
            planet_y[frame, :] / physics.AU
        ))
    )

    return orbit_line_1, planet_dots, orbit_line_2

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
    global animation_1, animation_2, orbit_line_1, planet_dots, orbit_line_2, energy_line
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


    params = planet_widget_1.get_parameters()
    params_2 = planet_widget_2.get_parameters()

    # first of all get the required data from the planets FROM SLIDERS
    star_mass = params['star_mass'] * physics.SOLAR_MASS
    planet_masses = np.array((params['planet_mass'], params_2['planet_mass'])) * physics.EARTH_MASS

    planet_position = np.array([[params['planet_position'], 0], [params_2['planet_position'],0]], dtype=float) * physics.AU
    planet_velocity = np.array([[0, params['planet_velocity']], [0, params_2['planet_velocity']]], dtype=float) * 1_000
    time_period = params['time_period']

    planet_x, planet_y, planet_velocities, times, energies = physics.simulate_orbit(
        time_period,
        planet_position,
        planet_velocity,
        star_mass,
        planet_masses
    )



    ax1.plot(planet_x/physics.AU, planet_y/physics.AU, alpha=0)
    #orbit_line, = ax1.plot(planet_x/physics.AU,planet_y/physics.AU,label='Orbit', color='C0')
    orbit_line_1, = ax1.plot([],[])
    orbit_line_2, = ax1.plot([],[]) # plot first points

    # Layering from the widest outer glow down to the intense core
    ax1.scatter([0] * 5, [0] * 5, s=[300, 160, 70, 24, 6],
                color=['red', 'darkorange', 'orange', 'gold', 'white'],
                alpha=[0.03, 0.08, 0.2, 0.5, 1.0], edgecolors='none', label='Central Body')

    planet_dots = ax1.scatter(planet_x[0] / physics.AU, planet_y[0] / physics.AU, label= 'Planetary Body', color = '#00BFFF')

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

    animation_1 = FuncAnimation(orbit_plot,update_data,frames=len(planet_x),interval=2,blit=True,repeat=False)

    #animation_2 = FuncAnimation(energy_plot, update_energy, frames=len(planet_x), interval = 5, blit = True, repeat= False)
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

menu_frame.add('Planet 1')
menu_frame.add('Planet 2')
menu_frame.add('Settings')

background_frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
menu_frame.place(relx=0.015, rely=0.01, relwidth=0.3, relheight=0.97)
orbit_frame.place(relx=0.3, y = 0, relwidth = 0.7, relheight = 1)

menu_frame.lift()

planet_1_tab = menu_frame.tab('Planet 1')
planet_2_tab = menu_frame.tab('Planet 2')

planet_1_tab.columnconfigure((0, 1), weight=1)
planet_2_tab.columnconfigure((0,1), weight=1)

planet_widget_1 = widgets.PlanetWidget(planet_1_tab, fg_color='#64748B')
planet_widget_1.pack(fill='both',expand=True,padx=10,pady=10)
planet_widget_2 = widgets.PlanetWidget(planet_2_tab, fg_color='#64748B')
planet_widget_2.pack(fill='both',expand=True,padx=10,pady=10)



button_frame = ctk.CTkFrame(planet_1_tab)
button_frame.pack(fill='x',padx=10,pady=10)

run = ctk.CTkButton(button_frame,text='Run',command=update_simulation, bg_color='#64748B')
run.pack(side='right', padx=5)

milky_way = ctk.CTkButton(button_frame,text='Reset',command=reset, bg_color='#64748B')
milky_way.pack(side='left', padx=5)

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


#Todo correct energy graph
# change display of GUI
# Add validation for impossible/extreme inputs.
# Make draggable tab class
# Combine animation Functions?
# Change architecture