import tkinter as tk
import customtkinter as ctk

class Body(ctk.CTkFrame):

    all_instances=[]

    def __init__(self, master, name='empty', **kwargs):
        super().__init__(master, **kwargs)

        self.name = name
        self.variables = {}
        self.sliders = {}
        self.create_widgets()

        Body.all_instances.append(self)

    def create_widgets(self):

        self.columnconfigure(0, weight=1)

        for i, configure in enumerate(self.variable_configurations):
            self.rowconfigure(i, weight=0)

            row_frame = ctk.CTkFrame(master=self,width=1)

            row_frame.grid(row=i,column=0,sticky="ew",padx=10,pady=5)

            row_frame.columnconfigure(0,weight=4,uniform='row_col')

            row_frame.columnconfigure(1,weight=4,uniform='row_col')

            row_frame.columnconfigure(2,weight=1,uniform='row_col')

            lbl = ctk.CTkLabel(row_frame,text=configure['label'],font=("Helvetica", 14, "bold"),fg_color='#313244',
                border_width=1,border_color='',corner_radius=5,padx=15,pady=8)

            lbl.grid(row=0,column=0,sticky='ew',padx=10,pady=10)

            var = tk.DoubleVar(value=configure['default'])

            self.variables[configure['name']] = var

            sld = ctk.CTkSlider(row_frame,from_=configure['min'],to=configure['max'],variable=var,
                                number_of_steps=configure['step'])

            sld.set(configure['default'])

            self.sliders[configure['name']] = sld

            sld.grid(row=0,column=1,sticky='e')

            box = ctk.CTkEntry(row_frame,width=60,textvariable=var)

            box.grid(row=0,column=2,sticky='w',padx=10)

            box.bind("<Return>",lambda event, name=configure["name"]:self.sliders[name].set(
                    self.variables[name].get()))

    def get_parameters(self):
        return {
            name: variable.get()
            for name, variable in self.variables.items()
        }

    def reset(self):

        for config in self.variable_configurations:
            self.sliders[config['name']].set(
                config['default']
            )





class StarWidget(Body):
    variable_configurations = [
            {'name': 'star_mass', 'label': 'Star Mass (Solar Masses)', 'min': 0.1, 'max': 5, 'default': 1, 'step': 980},
            {'name': 'time_period', 'label': 'Time Period (years)', 'min': 1, 'max': 5, 'default': 1, 'step': 100}]





class PlanetWidget(Body):
    variable_configurations = [
        {'name': 'planet_mass', 'label': 'Planet Mass (Earth Masses)', 'min': 0.1, 'max': 10, 'default': 1,
         'step': 980},
        {'name': 'planet_position', 'label': 'Planet x Position (AU)', 'min': 0.1, 'max': 5, 'default': 1, 'step': 980},
        {'name': 'planet_velocity', 'label': 'Planet y Velocity (km/s)', 'min': 0, 'max': 100, 'default': 30,
         'step': 1000}]