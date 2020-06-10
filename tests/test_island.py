# -*- coding: utf-8 -*-

from biosim.island import TheIsland
import pytest


class TestingTheIsland:

    @pytest.fixture()
    def initial_island(self):
        """
        Makes a simple test-model to use in tests
        Returns
        -------
        A simple test-model
        """
        test_island = """\
                            WWWWW
                            WLLLW
                            WHWHW
                            WLDLW
                            WWWWW"""
        test_animals = [{'loc': (2, 3),
                         'pop': [{'species': 'Herbivore',
                                  'age': 5,
                                  'weight': 20} for _ in range(200)] +
                                 [{'species': 'Carnivore',
                                  'age': 5,
                                  'weight': 20} for _ in range(20)]}
                        ]

        self.island = TheIsland(landscape_of_cells=test_island, animals_on_island=test_animals)
        return self.island

    def test_if_check_size(self):
        """
        Tests if the island class raises a ValueError if given an island with
        different lengths of the lines
        """
        test_island = """\
                            WWWWW
                            WLLLW
                            WHHW
                            WLDLW
                            WWWWW"""

        with pytest.raises(ValueError):
            TheIsland(test_island)

    def test_if_valueerror_if_not_island(self):
        """
        Tests if the island class raises a ValueError if given an island without
        water around the edges
        """
        test_island = """\
                            WWWWW
                            WLLLW
                            WHHWH
                            WLDLW
                            WWWWW"""

        with pytest.raises(ValueError):
            TheIsland(test_island)

    def test_not_possible_give_illegal_lanscape(self):
        """
        Tests if the island class raises a ValueError if given an island with
        a illegal type of landscape.
        """
        test_island = """\
                            WWWWW
                            WLLLW
                            WHHOW
                            WLDLW
                            WWWWW"""

        with pytest.raises(ValueError):
            TheIsland(test_island)


    def test_that_number_of_animals_is_updated(self, initial_island):
        """
        Tests that number of animals before the year starts is updated by the end of the year.
        todo: must make sure that animals are born?
              or just check that age/weight have been updated?
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
