# -*- coding: utf-8 -*-

from biosim.animals import Herbivores


class TestHerbivores:

    def test_constructor_default(self):
        """ Test that the class Herbivores creates an instance."""
        h = Herbivores()
        assert isinstance(h, Herbivores)

    def test_if_raises_keyerror(self):
        """
        Tests that the Herbivores class raises a KeyError if default parameter names are not used.

        Todo: Denne skal teste at programmet blir avbrutt hvis man gir inn veil key
        """
        pass
