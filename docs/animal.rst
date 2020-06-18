Animal
===========
This module represents animals. There are two types of animals:
herbivores and carnivores, which are represented with subclasses
:class:`Herbivores` and :class:`Carnivores`. These are subclasses of the
general :class:`Animal` class. Both herbivores and carnivores have dictionaris
of parameters, which can be changed by the user by the ``set_params`` method.
The :class:`Animal` class provides methods for the probability for dying,
giving birth, and migrating and the fitness, it also keeps track of weight and
age of an animal. The weight of the animal must be updated after eating, giving
birth and at the end of the year, which is implemented by different
``update_weight...`` methods. The age can be updated by an ``update_age``
method.

The Animal class
___________________
.. autoclass:: biosim.animals.Animal
   :members:

The Herbiovores subclass
__________________________
.. autoclass:: biosim.animals.Herbivores
   :members:

The Carnivores subclass
_________________________
.. autoclass:: biosim.animals.Carnivores
   :members:
