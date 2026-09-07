import numpy as np

import physics
import widgets
import plotting
import tkinter as tk
import customtkinter as ctk


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

def energy_plot_show():
    if show_energy.get() == 1:
        energy_frame.place(relx=0.75, rely=-0.00, relwidth=0.25, relheight=0.26)
    else:
        energy_frame.place_forget()

def create_tabs():
    while len(planet_widgets) < number_of_planets:
        i = len(planet_widgets)
        tab_frame.add(planets_data[i]['name'])
        planet_tab = tab_frame.tab(planets_data[i]['name'])

        planet_tab.columnconfigure((0, 1), weight=1)

        planet_widget = widgets.PlanetWidget(
            planet_tab,
            tabview=tab_frame,
            tab_name=[planets_data[i]['name']],
            fg_color='#64748B',
            defaults={
                'planet_mass': planets_data[i]['planet_mass'],
                'planet_radius': planets_data[i]['planet_radius'],
                'planet_position': planets_data[i]['planet_position'],
                'planet_velocity': planets_data[i]['planet_velocity']
            }
        )

        planet_widget.pack(
            fill='both',
            expand=True,
            padx=10,
            pady=10
        )
        planet_widgets.append(planet_widget)
    while len(planet_widgets) > number_of_planets:
        i = len(planet_widgets) - 1
        planet_widget = planet_widgets.pop(i)
        tab_name = planets_data[i]['name']
        tab_frame.delete(tab_name)
        planet_widget.destroy()

def get_simulation_parameters():
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

        planet_radii.append(
            (params['planet_radius'] ** 0.7 * 4) ** 2
        )

    return (star_mass, star_radius, time_period, np.array(planet_masses), np.array(planet_position),
            np.array(planet_velocity), planet_radii)


def update_simulation():
    global planet_x, planet_y, energies, times, number_of_planets

    number_of_planets = int(
        general_widget.get_parameters()['number_of_planets']
    )

    create_tabs()

    star_mass, star_radius,time_period, planet_masses, planet_position, planet_velocity, planet_radii = get_simulation_parameters()

    planet_x, planet_y, planet_velocities, times, energies = physics.simulate_orbit(
        time_period,
        planet_position,
        planet_velocity,
        star_mass,
        planet_masses
    )

    plotter.create_plots(planet_x, planet_y, star_radius,
                         planet_radii, times, energies)


# make GUI

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
        'planet_radius': 0.38,
        'planet_mass': 0.055
    },
    {
        'name': 'Venus',
        'planet_position': 0.72,
        'planet_velocity': 35.0,
        'planet_radius': 0.95,
        'planet_mass': 0.815
    },
    {
        'name': 'Earth',
        'planet_position': 1.00,
        'planet_velocity': 29.8,
        'planet_radius': 1.00,
        'planet_mass': 1.00
    },
    {
        'name': 'Mars',
        'planet_position': 1.52,
        'planet_velocity': 24.1,
        'planet_radius': 0.53,
        'planet_mass': 0.107
    },
    {
        'name': 'Jupiter',
        'planet_position': 5.20,
        'planet_velocity': 13.1,
        'planet_radius': 11.21,
        'planet_mass': 317.8
    },
    {
        'name': 'Saturn',
        'planet_position': 9.58,
        'planet_velocity': 9.7,
        'planet_radius': 9.45,
        'planet_mass': 95.2
    },
    {
        'name': 'Uranus',
        'planet_position': 19.20,
        'planet_velocity': 6.8,
        'planet_radius': 4.01,
        'planet_mass': 14.5
    },
    {
        'name': 'Neptune',
        'planet_position': 30.05,
        'planet_velocity': 5.4,
        'planet_radius': 3.88,
        'planet_mass': 17.1
    }
]



number_of_planets = int(general_widget.get_parameters()['number_of_planets'])

planet_widgets = []

create_tabs()

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
plotter = plotting.Plotter(orbit_frame, energy_frame)

update_simulation()

window.protocol('WM_DELETE_WINDOW', closing)

window.mainloop()

#Todo
# Add validation for impossible/extreme inputs.
# Make draggable tab class
# Change architecture