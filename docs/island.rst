The Island
===========
The island main feature is to run the annual cycle which consist of:
    * Feeding: Fodder appear, then herbivores eat the fodder, before carnivores
      eats herbivores
    * Procreation: Animals gives birth
    * Migration: Animals migrate
    * Aging: Every animal age by one year
    * Loss of weight: All animals lose weight
    * Death: Animals dies

An important part of the annual cycle is the migration of animals. Animals are
only allowed to migrate if the cell they want to migrate to is not a water
cell. Animals who are allowed to migrate are added to their new cells, animals
who are not allowed to migrate are added back into their old cell.

The island is also responsible for keeping track of the location
of all cells. All this is implemented in :class:`TheIsland` class.

The Island class
__________________
.. autoclass:: biosim.island.TheIsland
   :members:
