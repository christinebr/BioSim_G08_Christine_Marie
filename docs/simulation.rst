Simulation
===========
The :class:`BioSim` class is used to run simulations. The user has to provide
specifications like the number of years, the island in the form of a
multiline string, and initial animals and where to place them on the island.
To run a simulation the user have to call the ``simulation`` method.

The :class:`BioSim` class also takes care of the visualization of the
simulation. The visualization consists of a plot of the island, a graph with
the amount of herbivores and carnivores on the island, two heatmaps showing
the distribution of herbivores and carnivores, and three histograms showing
fitness, age and weight distribution of herbivores and carnivores. These plots
are updated with time intervals that can be specified by the user, if not
the default value is 1 (every year). The different plots show how the animal
population of the island changes with time, and how they move around on the
island.

If wanted the module can store pictures at specified intervals,
if so the user has to provide specifications for this. If no such
specifications are given, or the specifications given are insufficient, the
module will not store any pictures.

It's also possible to make a movie from the stored pictures by calling the
``make_movie`` method after a simulation. Note: for this to work the parameter
``img_years`` in the ``simulation`` method must be specified.

To make a movie the user must have ``ffmpeg`` installed.
This could be installed by writing ``conda install ffmpeg`` in your preferred
terminal window. Make sure to install in the same environment that you are
using to run the simulation module.


The BioSim class
______________________
.. autoclass:: biosim.simulation.BioSim
   :members:
