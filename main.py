import gui

app = gui.Interface()
app.start()

#Todo
# make sun feel gravitational force
# add milky way button to reset to milky way
# vectorise gravity computation using numpy broadcasting
# in settings add (show orbital trails, show planet names, show velocity vectors, animation speed)
# add collisions
# Add validation for impossible/extreme inputs.
# Make draggable tab class
# Add different simulation presets
# edit architecture main.py, physics(/constants.py,gravity.py,integrators.py,simulation.py)
#   gui(/interface.py,widgets.py), presets(/solarsystem.py)