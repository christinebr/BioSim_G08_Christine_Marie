# -*- coding: utf-8 -*-

from biosim.island import TheIsland
import pytest
import numpy as np


class TestingTheIsland:

    @pytest.fixture()
    def initial_island(self):
        """
        Makes a simple test-model to use in tests
        Returns
        -------
        A simple test-model
        """
        test_island = np.array([['W', 'W', 'W', 'W'],
                                ['W', 'L', 'L', 'W'],
                                ['W', 'H', 'H', 'W'],
                                ['W', 'L', 'L', 'W'],
                                ['W', 'W', 'W', 'W']])
        test_herb = [{'species': 'Herbivore', 'age': 10, 'weight': 15},
                     {'species': 'Herbivore', 'age': 40, 'weight': 20},
                     {'species': 'Carnivore', 'age': 30, 'weight': 3.5}]
        test_car = []

        self.island = TheIsland(landscape_of_cells=test_island, herbis=test_herb, carnis=test_car)
        return self.island

    def test_that_somehting(self, initial_island):
        """
        Tests .....
        Parameters
        ----------
        initial_island

        Returns
        -------

        """
        pass
