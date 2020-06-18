Simulation
===========
This module runs simulations. The user has to provide specifications
like the number of years, the island in the form of a
multiline string, and initial animals and where to place them on the island.

The class plots a map of the island, a graph with the amount of herbivores
and carnivores on the island, two heatmaps showing the distribution
of herbivores and carnivores, and three histograms showing fitness,
age and weight distribution of herbivores and carnivores. These plots are updated
with time intervals that can be specified by the user, else default
value is 1. The different plots show how the animal population of the island
changes with time.

If wanted the module can store pictures at specified intervals,
if so the user has to provide specifications for this. If no such
specifications are given, or the specifications givven are insufficient, the
module will not store any pictures.

It's also possible to make the module construct a movie from the
stored pictures.

To make a movie the user must have ``ffmpeg`` installed.
This could be installed by writing ``conda install ffmpeg`` in your preferred
terminal window. Make sure to install in the same environment that you are
using to run the simulation module.


The BioSim class
______________________
.. autoclass:: biosim.simulation.BioSim
   :members:
