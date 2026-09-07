import numpy as np
import physics

import catppuccin
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation


class Plotter():
    mpl.style.use(catppuccin.PALETTE.mocha.identifier)

    def __init__(self, orbit_frame, energy_frame):
        self.orbit_frame = orbit_frame
        self.energy_frame = energy_frame

        self.animation_1 = None
        self.animation_2 = None
        self.orbit_lines = []
        self.planet_dots = None
        self.energy_line = None
        self.orbit_plot, self.ax1 = plt.subplots()
        self.energy_plot, self.ax2 = plt.subplots()
        self.orbit_canvas = FigureCanvasTkAgg(self.orbit_plot,master=self.orbit_frame)
        self.energy_canvas = FigureCanvasTkAgg(self.energy_plot,master=self.energy_frame)

        self.orbit_canvas.get_tk_widget().pack(fill='both', expand=True)

        self.energy_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

    def create_plots(self, planet_x, planet_y,
                     star_radius,planet_radii, times, energies):
        self.planet_x = planet_x
        self.planet_y = planet_y
        self.star_radius = star_radius
        self.planet_radii = planet_radii
        self.number_of_planets = len(planet_radii)
        self.times = times
        self.energies = energies

        if self.animation_1 is not None:
            if self.animation_1.event_source is not None:
                self.animation_1.event_source.stop()
            self.animation_1 = None

        if self.animation_2 is not None:
            if self.animation_2.event_source is not None:
                self.animation_2.event_source.stop()
            self.animation_2 = None

        try:
            self.ax1.clear()
            self.ax2.clear()
        except:
            return

        self.ax1.plot(self.planet_x/physics.AU, self.planet_y/physics.AU, alpha=0)

        self.orbit_lines = []
        for i in range(self.number_of_planets):
            line, = self.ax1.plot([], [], zorder=1, color='#74C7EC')
            self.orbit_lines.append(line)

        self.ax1.scatter(
            [0] * 5,
            [0] * 5,
            s=np.array([3000, 1600, 700, 240, 60]) * (self.star_radius**2),
            color=['red', 'darkorange', 'orange', 'gold', 'white'],
            alpha=[0.03, 0.08, 0.2, 0.5, 1.0],
            edgecolors='none',
            label='Central Body',
            zorder=4
        )
        planet_colors = [
            '#A6A6A6',  # Mercury
            '#E8C46A',  # Venus
            '#4A90E2',  # Earth
            '#D95F39',  # Mars
            '#C9A66B',  # Jupiter
            '#D8C28F',  # Saturn
            '#67D5D5',  # Uranus
            '#4169A1'  # Neptune
        ]
        self.planet_dots = self.ax1.scatter(self.planet_x[0] / physics.AU, self.planet_y[0] / physics.AU,color=planet_colors[:self.number_of_planets], label= ['Planetary Body 1'], s=self.planet_radii,zorder=2)

        self.ax1.set_xlabel('x position (AU)')
        self.ax1.set_ylabel('y position (AU)')
        self.ax1.axis('equal')
        self.ax1.set_title('Orbital Path')
        self.ax1.legend(loc='upper left')


        self.ax2.plot(
            np.array(self.times) / (physics.DAY_SECONDS * physics.DAYS_PER_YEAR),
            ((np.array(self.energies) - self.energies[0]) / abs(self.energies[0]) ) * 100, alpha=0
        )

        self.energy_line, = self.ax2.plot([0], [0])

        self.ax2.axhline(0 ,linestyle = 'dashed')

        self.ax2.set_xlabel('Time (years)')
        self.ax2.set_ylabel('Energy Error (%)')
        self.ax2.set_title('Energy Percentage Error vs Time')

        self.orbit_plot.tight_layout()
        self.energy_plot.tight_layout()

        self.orbit_canvas.draw_idle()
        self.energy_canvas.draw_idle()

        self.animation_1 = FuncAnimation(self.orbit_plot,self.update_data,frames=len(self.planet_x),interval=5,blit=True,repeat=False)

        self.animation_2 = FuncAnimation(self.energy_plot, self.update_energy, frames=len(self.planet_x), interval = 5, blit = True, repeat= False)

    def update_data(self, frame):
        for i in range(self.number_of_planets):
            self.orbit_lines[i].set_data(
                self.planet_x[:frame + 1, i] / physics.AU,
                self.planet_y[:frame + 1, i] / physics.AU
            )

        self.planet_dots.set_offsets(
            np.column_stack((
                self.planet_x[frame, :] / physics.AU,
                self.planet_y[frame, :] / physics.AU
            ))
        )

        return self.orbit_lines + [self.planet_dots]

    def update_energy(self, frame):
        self.energy_line.set_data(np.array(self.times)[:frame + 1] / (physics.DAY_SECONDS * physics.DAYS_PER_YEAR),
                             ((np.array(self.energies)[:frame + 1] - self.energies[0]) / abs(self.energies[0])) * 100)

        return self.energy_line,