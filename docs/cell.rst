The Cell
===========
The cell keeps track of animals of both species, the amount of
fodder and the type of landscape in the area. There are four
types of landscape, lowland, highland, dessert and water, which
are represented with subclasses. Animals can not stay in the
water. All animals can stay in the dessert, but herbivores will
find no food. Both lowland and highland provide fodder. There
are parameters for the amount of fodder that appear in a cell
of a certain type of landscape in the beginning of the
year, these can be changed by the user. The cell makes sure
animals eat, give birth, die and lose weight as supposed. It
also checks how many animals wants to migrate and the direction
they wants to migrate. Animals who wants to migrate are sorted
out of the cells, only animals who don't want to migrate stays
in the cell. Animals who wants to migrate, but are not allowed
to has to be added once more.

The SingleCell class
___________________
.. autoclass:: biosim.cell.SingleCell
   :members:

The Water subclass
________________________
.. autoclass:: biosim.cell.Water
   :members:

The Desert subclass
_______________________
.. autoclass:: biosim.cell.Desert
   :members:

The Lowland subclass
________________________
.. autoclass:: biosim.cell.Lowland
   :members:

The Highland subclass
_______________________
.. autoclass:: biosim.cell.Highland
   :members:
