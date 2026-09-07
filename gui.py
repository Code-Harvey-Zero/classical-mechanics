import numpy as np

import physics
import widgets
import plotting
import tkinter as tk
import customtkinter as ctk

class Interface:
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

    def __init__(self):
        self.window = ctk.CTk()
        self.window.title('Orbital Simulator')
        self.window.minsize(1366,768)

        self.background_frame = ctk.CTkFrame(self.window, fg_color='#1e1e2e')
        self.background_frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

        self.menu_frame = ctk.CTkFrame(self.window, fg_color='#64748B', corner_radius=10, border_width=1, border_color = '#CBD5E1', bg_color='#1e1e2e')
        self.menu_frame.place(relx=0.015, rely=0.01, relwidth=0.3, relheight=0.97)

        self.star_widget = widgets.StarWidget(self.menu_frame, fg_color='#64748B')
        self.star_widget.pack(padx=10, pady=10)

        self.tab_frame = ctk.CTkTabview(self.menu_frame, fg_color='#64748B', corner_radius=10, bg_color='#64748B', border_color='#1e1e2e', border_width=2)
        self.tab_frame.pack(fill='both',expand=True,padx=10,pady=10)
        # ToDO we may not need this here we can put it inside update simulation
        self.tab_frame.add('Settings')

        self.orbit_frame = ctk.CTkFrame(self.window)
        self.orbit_frame.place(relx=0.3, y = 0, relwidth = 0.7, relheight = 1)

        self.energy_frame = ctk.CTkFrame(self.window, border_color='#CBD5E1', border_width=1, corner_radius=5, fg_color='#1e1e2e')

        self.general_widget = widgets.GeneralSettings(self.menu_frame, fg_color='#64748B')
        self.general_widget.pack(padx=10, pady=10)

        self.button_frame = ctk.CTkFrame(self.menu_frame, fg_color='#64748B')
        self.button_frame.pack(fill='x', padx=10, pady=10)

        self.run = ctk.CTkButton(self.button_frame, text='Run', command=self.update_simulation, bg_color='#64748B')
        self.run.pack(side='right', padx=5)

        self.milky_way = ctk.CTkButton(self.button_frame, text='Reset', command=self.reset, bg_color='#64748B')
        self.milky_way.pack(side='left', padx=5)

        self.show_energy = tk.IntVar()
        self.energy_check_box = ctk.CTkCheckBox(self.tab_frame.tab('Settings'), text='Show Energy Plot',
                                           variable=self.show_energy, onvalue=1, offvalue=0, command=self.energy_plot_show)
        self.energy_check_box.pack(pady=(40, 10))

        self.plotter = plotting.Plotter(self.orbit_frame, self.energy_frame)

        self.number_of_planets = int(self.general_widget.get_parameters()['number_of_planets'])

        self.planet_widgets = []

        self.menu_frame.lift()
        self.update_simulation()

        self.window.protocol('WM_DELETE_WINDOW', self.closing)

    def create_tabs(self):
        while len(self.planet_widgets) < self.number_of_planets:
            i = len(self.planet_widgets)
            if i < len(self.planets_data):
                self.tab_frame.add(self.planets_data[i]['name'])
                self.planet_tab = self.tab_frame.tab(self.planets_data[i]['name'])

                self.planet_tab.columnconfigure((0, 1), weight=1)

                self.planet_widget = widgets.PlanetWidget(
                    self.planet_tab,
                    tabview=self.tab_frame,
                    tab_name=[self.planets_data[i]['name']],
                    fg_color='#64748B',
                    defaults={
                        'planet_mass': self.planets_data[i]['planet_mass'],
                        'planet_radius': self.planets_data[i]['planet_radius'],
                        'planet_position': self.planets_data[i]['planet_position'],
                        'planet_velocity': self.planets_data[i]['planet_velocity']
                    }
                )

            else:
                tab_name = f'Planet {i}'
                self.tab_frame.add(tab_name)
                self.planet_tab = self.tab_frame.tab(tab_name)

                self.planet_tab.columnconfigure((0, 1), weight=1)

                self.planet_widget = widgets.PlanetWidget(
                    self.planet_tab,
                    tabview=self.tab_frame,
                    tab_name=tab_name,
                    fg_color='#64748B',
                    defaults = {
                        'planet_mass': self.planets_data[7]['planet_mass']*1.1,
                        'planet_radius': self.planets_data[7]['planet_radius']*1.1,
                        'planet_position': self.planets_data[7]['planet_position'] * 1.1,
                        'planet_velocity': self.planets_data[7]['planet_velocity']*1.1,
                    }
                )

            self.planet_widget.pack(
                fill='both',
                expand=True,
                padx=10,
                pady=10
            )
            self.planet_widgets.append(self.planet_widget)
        while len(self.planet_widgets) > self.number_of_planets:
            i = len(self.planet_widgets) - 1
            self.planet_widget = self.planet_widgets.pop(i)
            if i < len(self.planets_data):
                self.tab_name = self.planets_data[i]['name']
            else:
                tab_name = f'Planet {i}'
                self.tab_name = tab_name
            self.tab_frame.delete(self.tab_name)
            self.planet_widget.destroy()

    def get_simulation_parameters(self):


        self.masses = []
        self.positions = []
        self.velocities = []
        self.radii = []

        self.params = self.star_widget.get_parameters()
        self.masses.append(self.params['star_mass'] * physics.SOLAR_MASS)
        self.positions.append([0,0])
        self.velocities.append([0,0])
        self.radii.append(self.params['star_radius'] ** 2 * 30)

        for i in range(self.number_of_planets):
            self.params = self.planet_widgets[i].get_parameters()

            self.masses.append(
                self.params['planet_mass'] * physics.EARTH_MASS
            )

            self.positions.append([
                self.params['planet_position'] * physics.AU,
                0
            ])

            self.velocities.append([
                0,
                self.params['planet_velocity'] * 1_000
            ])

            self.radii.append(
                (self.params['planet_radius'] ** 0.7 * 4) ** 2
            )

        self.params = self.general_widget.get_parameters()
        self.time_period = self.params['time_period']

        return (self.time_period, np.array(self.masses), np.array(self.positions),
                np.array(self.velocities), self.radii)

    def update_simulation(self):

        self.number_of_planets = int(
            self.general_widget.get_parameters()['number_of_planets']
        )

        self.create_tabs()

        (self.time_period, self.masses, self.positions,
         self.velocities, self.radii) = self.get_simulation_parameters()

        print("Mars:", self.positions[4] / physics.AU, self.velocities[4] / 1000)

        self.planet_x, self.planet_y, self.planet_velocities, self.times, self.energies = physics.simulate_orbit(
            self.time_period,
            self.positions,
            self.velocities,
            self.masses
        )

        self.plotter.create_plots(self.planet_x, self.planet_y,
                             self.radii, self.times, self.energies)

    def energy_plot_show(self):
        if self.show_energy.get() == 1:
            self.energy_frame.place(relx=0.75, rely=-0.00, relwidth=0.25, relheight=0.26)
        else:
            self.energy_frame.place_forget()

    def reset(self):
        for body in widgets.Body.all_instances:
            body.reset()

        self.update_simulation()

    def closing(self):
        self.window.quit()
        self.window.destroy()
        try:
            for after_id in self.window.tk.eval('after info').split():
                self.window.after_cancel(after_id)
        except:
            pass

    def start(self):
        self.window.mainloop()