# -*- coding: utf-8 -*-

from biosim.island import TheIsland
from biosim.cell import Highland
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
                                  'weight': 20} for _ in range(200)]
                        + [{'species': 'Carnivore',
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

    def test_that_number_of_animals_is_updated(self, initial_island, mocker):
        """
        Tests that number of animals before the year starts is updated by the end of the year.
        """
        mocker.patch('random.random', return_value=0)
        # Makes sure animals are born and killed but do not die
        num_animals_before, h, c = self.island.total_num_animals_on_island()
        self.island.annual_cycle()
        num_animals_after, h, c = self.island.total_num_animals_on_island()
        assert num_animals_after != num_animals_before

    def test_give_params_cell(self, initial_island):
        """
        Check that it's possible to create new parameters for cell.
            - check update of cell-params -> f_max
        """
        new_param = {'f_max': 400.0}
        param = self.island.island_cells[2][1].get_params()
        assert param['f_max'] == 300.0
        self.island.set_cell_params('H', new_param)
        assert param['f_max'] == 400.0

    def test_set_params_animals(self, initial_island):
        """Tests that it is possible to update parameters for animals."""

        new_param = {'xi': 2.0}
        param = self.island.island_cells[1][2].herbi_list[0].get_params()
        assert param['xi'] == 1.2
        self.island.set_animal_params('Herbivore', new_param)
        param = self.island.island_cells[1][2].herbi_list[0].get_params()
        assert param['xi'] == 2.0

    def test_complete_cycle(self, initial_island, mocker):
        """
        Checks that all steps in the annual cycle are made.

        Todo: This might be better put into a lott of different tests, but some of the point is to
            check that all the methods could work together on the same sett. Numbers are used for
            more than one test, should update the variable names after including migration.
            Test for aging funker ikke, sjekk dette
        """
        island = self.island
        animals = island.island_cells[1][2].herbi_list + island.island_cells[2][3].carni_list

        # Eating
        sum_weight_spring = 0
        for animal in animals:
            sum_weight_spring += animal.weight
        island.all_animals_eat()
        sum_weight_after_eating = 0
        for animal in animals:
            sum_weight_after_eating += animal.weight
        assert sum_weight_spring < sum_weight_after_eating

        # procreating
        mocker.patch('random.random', return_value=0)
        # makes sure there are newborns, and animals eaten later
        num_animals_spring = island.total_num_animals_on_island()
        island.animals_procreate()
        num_animals2 = island.total_num_animals_on_island()
        assert num_animals_spring < num_animals2

        # Migration
        # Add this later

        # Aging
        # sum_age_before = 0
        # for animal in animals:
        #     sum_age_before += animal.age
        # island.all_animals_age()
        # sum_age_after = 0
        # for animal in animals:
        #     sum_age_after += animal.age
        # assert sum_age_before + island.total_num_animals_on_island()[0] == sum_age_after

        # Loss of weight
        island.all_animals_losses_weight()
        sum_weight3 = 0
        for animal in animals:
            sum_weight3 += animal.weight
        assert sum_weight3 < sum_weight_after_eating

        # death
        mocker.patch('random.random', return_value=0.9) # makes sure not all animals die
        animals[3].weight = 0 # Makes sure at least one animal dies
        island.animals_die()
        assert num_animals2 > island.total_num_animals_on_island()
