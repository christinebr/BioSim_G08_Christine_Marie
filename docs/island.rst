The Island
===========
The islands main feature is to run the annual cycle.
    * Feeding: Fodder appear, then herbivores eat the fodder, before carnivores eats herbivores
    * Procreation: Animals gives birth
    * Migration: Animals migrate
    * Aging: Every animal age by one year
    * Loss of weight: All animals lose weight
    * Death: Animals dies.

An important part of this is to check if animals who wants to
migrate are allowed too. i.e. if the cell they wants
to migrate into is not a water cell. Animals who are allowed to
migrate are added in their new cells, animals who are not allowed
to migrate are added back into their old cell.

The island is also responsible for keeping track of locations
of all cells.

The Island class
__________________
.. autoclass:: biosim.island
   :members:
