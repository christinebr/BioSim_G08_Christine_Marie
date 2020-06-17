Simulation
===========
This module runs simulations. The user has to provide specifications
like the number of years, the island, in the form of a
multiline string, initial animals and where to place them on the island.

It plots a map of the island, a graph with the amount of herbivores
and carnivores on the island, two heatmaps showing the distribution
of herbivores and carnivores, and three histograms showing fitness
age and weight distribution of herbivores and carnivores. These plots are updated
with specified time intervals that can be specified by the user, else default
value is one. The different plots show how the animal population of the island
changes with time.

If wanted the module can store pictures at specified intervals,
if so the user has to provide specifications for this. If no
specifications are given, the module will not store any pictures.
It's also possible to make the module make a movie from the
stored pictures.

To make a movie the user must have the program ``ffmpeg`` installed. This could be
installed using ``conda install ffmpeg`` in your preferred terminal.


The BioSim class
______________________
.. autoclass:: biosim.simulation.BioSim
   :members:
