# -*- coding: utf-8 -*-

from biosim.animals import Herbivores


class TestHerbivores:

    def test_constructor_default(self):
        """ Test that the class Herbivores creates an instance."""
        h = Herbivores()
        assert isinstance(h, Herbivores)
