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
        self.island.construct_island_with_cells()
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
        num_animals_before = self.island.total_num_animals_on_island()
        self.island.annual_cycle()
        num_animals_after = self.island.total_num_animals_on_island()
        assert num_animals_after != num_animals_before

    def test_give_params_cell(self, initial_island):
        """
        Check that it's possible to create new parameters for cell.
            - check update of cell-params -> f_max
        """
        new_param = {'f_max': 400.0}
        print(self.island.island_cells)
        param = self.island.island_cells[2][1].get_params()
        assert param['f_max'] == 300.0
        self.island.set_cell_params('H', new_param)
        assert param['f_max'] == 400.0

    def test_set_params_animals(self, initial_island):
        """Tests that it is possible to update parameters for animals."""

        # new_params_herbi = {'sigma_birth': 2.0, 'a_half': 35.0}
        # herbi_params = self.island.island_cells
        # assert herbi_params['sigma_birth'] == 1.5
        # assert herbi_params['a_half'] == 40.0
        # self.island.set_animals_params(specie='Herbivore', new_params=new_params_herbi)
        # assert herbi_params['sigma_birth'] == 2.0
        # assert herbi_params['a_half'] == 35.0

    def complete_cycle(self, initial_island):
        """
        Checks that all steps in the annual cycle are made.
        """
        pass
