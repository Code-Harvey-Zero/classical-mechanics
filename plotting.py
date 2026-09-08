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

    def create_plots(self, planet_x, planet_y, velocities,radii, times, energies, acceleration):
        self.planet_x = planet_x
        self.planet_y = planet_y
        self.velocities = velocities
        self.acceleration = acceleration
        self.radii = radii
        self.number_of_bodies = len(radii)
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
        for i in range(self.number_of_bodies):
            line, = self.ax1.plot([], [], zorder=1, color='#74C7EC', alpha =0)
            self.orbit_lines.append(line)

        planet_colors = [
            'orange', # Sun
            '#A6A6A6',  # Mercury
            '#E8C46A',  # Venus
            '#4A90E2',  # Earth
            '#D95F39',  # Mars
            '#C9A66B',  # Jupiter
            '#D8C28F',  # Saturn
            '#67D5D5',  # Uranus
            '#4169A1'  # Neptune
        ]

        if self.number_of_bodies > 9:
            extra_colors = plt.cm.tab20(
                np.linspace(0, 1, self.number_of_bodies - 9)
            )
            planet_colors = planet_colors + list(extra_colors)
        else:
            planet_colors = planet_colors[:self.number_of_bodies]

        self.planet_dots = self.ax1.scatter(self.planet_x[0] / physics.AU, self.planet_y[0] / physics.AU,color=planet_colors[:self.number_of_bodies], label='FIX', s=self.radii,zorder=2)
        self.velocity_vectors = self.ax1.quiver(self.planet_x[0] / physics.AU, self.planet_y[0] / physics.AU,
                                                self.velocities[0,:,0], self.velocities[0,:,1], color='#F38BA8',
                                                    scale=5e3,width=0.002,
                                                    headwidth=2.5,
                                                    headlength=3,
                                                    headaxislength=2.5,
                                                    alpha=0)

        self.acceleration_vectors = self.ax1.quiver(self.planet_x[0] / physics.AU, self.planet_y[0] / physics.AU,
                                                self.acceleration[0,:,0], self.acceleration[0,:,1], color='#A6E3A1',
                                                    scale=6,width=0.002,
                                                    headwidth=2.5,
                                                    headlength=3,
                                                    headaxislength=2.5,
                                                    alpha=0)

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
        for i in range(self.number_of_bodies):
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
        self.velocity_vectors.set_offsets(
            np.column_stack((
                self.planet_x[frame, :] / physics.AU,
                self.planet_y[frame, :] / physics.AU
            ))
        )
        u = self.velocities[frame, :, 0]
        v = self.velocities[frame, :, 1]

        speed = np.sqrt(u ** 2 + v ** 2)

        u = u / np.sqrt(speed)
        v = v / np.sqrt(speed)

        self.velocity_vectors.set_UVC(
            u, v   # vy
        )

        self.acceleration_vectors.set_offsets(
            np.column_stack((
                self.planet_x[frame, :] / physics.AU,
                self.planet_y[frame, :] / physics.AU
            ))
        )
        u = self.acceleration[frame, :, 0]
        v = self.acceleration[frame, :, 1]

        acceleration_mag = np.sqrt(u ** 2 + v ** 2)

        u = u / np.sqrt(acceleration_mag)
        v = v / np.sqrt(acceleration_mag)

        self.acceleration_vectors.set_UVC(
            u, v   # vy
        )

        return self.orbit_lines + [self.planet_dots] + [self.velocity_vectors] + [self.acceleration_vectors]

    def update_energy(self, frame):
        self.energy_line.set_data(np.array(self.times)[:frame + 1] / (physics.DAY_SECONDS * physics.DAYS_PER_YEAR),
                             ((np.array(self.energies)[:frame + 1] - self.energies[0]) / abs(self.energies[0])) * 100)

        return self.energy_line,