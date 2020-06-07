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
        test_herb = [{'loc': (10, 10),
                      'pop': [{'species': 'Herbivore',
                               'age': 5,
                               'weight': 20}
                              for _ in range(10)]}]
        test_car = []

        self.island = TheIsland(landscape_of_cells=test_island, herbis=test_herb, carnis=test_car)
        return self.island

    def test_that_number_of_animals_is_updated(self, initial_island):
        """
        Tests that number of animals before the year starts is updated by the end of the year.
        """
        pass

    def test_yearly_continuity(self, initial_island):
        """
        Check that the next year starts where the last one ended, i.e. that the updates from last
        year are the initial values in the next one.

        Todo: This might be a better test for biosim
        """
        pass

    def test_give_params(self, initial_island):
        """
        Check that it's possible to create new parameters.
        """
        pass

    def complete_cycle(self, initial_island):
        """
        Checks that all steps in the annual cycle are made.
        """
        pass
