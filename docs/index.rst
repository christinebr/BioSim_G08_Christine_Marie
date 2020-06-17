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
types of landscape, lowland, highland, desert an water. The goal of the project
is to test if animals will go extinct in different scenarios.

The user interface of the package is given by :mod:`biosim.simulation`.
The :class:`BioSim` instance represents each simulation. On these instances the
the :meth:`BioSim.simulate` method can be called as often as wanted to
simulate a given number of years.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   animal
   cell
   island
   simulation


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
