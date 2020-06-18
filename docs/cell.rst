Cell
===========
The cell keeps track of animals of both species, the amount of
fodder and the cell is of a specified landscape type. There are four
types of landscape: lowland, highland, desert and water, which
are represented with subclasses. The :class:`Lowland` class, :class:`Highland`
class,  :class:`Desert` class and :class:`Water` class are subclasses of the
:class:`SingleCell` class.

Animals can not stay in water. All animals can stay in the dessert, but
herbivores will find no food. Both lowland and highland provide fodder, but
different amount: there are more food in the lowland than in the highland.
There are parameters for the amount of fodder that appear in a cell
of a certain type of landscape in the beginning of the
year, these can be changed by the user.

The cell makes sure animals eat, give birth, die and lose weight as supposed.
It also checks how many animals wants to migrate and the direction
they wants to migrate. Animals who wants to migrate are sorted
out of the cells, only animals who don't migrate stays in the cell.


The SingleCell class
_______________________
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
