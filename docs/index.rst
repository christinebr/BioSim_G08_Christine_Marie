.. BioSim documentation master file, created by
   sphinx-quickstart on Fri Jun  5 10:55:19 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BioSim's documentation!
===================================

This is our exam project in the course INF200, advanced programing,
at NMBU, completed in June 2020.

BioSim simulates the population dynamics on the fictional island Rossumøya.
Rossumøya has two species of animals, herbivores and carnivores, and four different
types of landscape, lowland, highland, desert and water. The goal of the project
is to test if both the species are able to survive on the island over time and
with different scenarios.

The user interface of the package is given by :mod:`biosim.simulation`.
The :class:`BioSim` instance represents each simulation. Users kan call the :meth:`BioSim.simulate` method on these instances as often as wanted to
simulate a given number of years. It's also possible to add new animals on the
island between calls.

The simulation can also handle other islands, as long as
they follow the requirements: only consisting of the prescribed four types of
landscapes, and all outer cell should be water cells. The geography of the
island must be specified when initialising the :class:`BioSim` instance.

Contents
-----------

.. toctree::
   :maxdepth: 2

   animal
   cell
   island
   simulation


Indices and tables
---------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
