# -*- coding: utf-8 -*-

from biosim.cell import SingleCell
import pytest
from copy import deepcopy


class TestSingleCell:

    @pytest.fixture()
    def initial_cell_class(self):
        animals = [{'species': 'Herbivore', 'age': 10, 'weight': 40},
                   {'species': 'Herbivore', 'age': 8, 'weight': 29},
                   {'species': 'Herbivore', 'age': 3, 'weight': 10}]
        self.cell = SingleCell(animals_list=animals)
        return self.cell

    def test_that_all_animals_age(self, initial_cell_class):
        """
        Tests that method age makes all animals get one year older.
        The sum of the age in the test-sett increase with 3 per year.
        """
        cell_old = deepcopy(self.cell.get_animals())
        self.cell.aging_of_animales()
        cell_new = self.cell.get_animals()
        sum_old_age = 0
        sum_new_age = 0
        for old, older in zip(cell_old, cell_new):
            sum_old_age += old['age']
            sum_new_age += older['age']
        assert sum_old_age + 3 == sum_new_age

    def test_that_newborns_weights_somehting(self, initial_cell_class):
        """
        Tests that the birth method assigns a weight to the newborn animal.
        """
        cellt = self.cell.birth()
        nonexsistent_newborns = 0
        for animal in cellt:
            if animal['age'] == 0 and animal['weight'] <= 0:
                nonexsistent_newborns += 1

        assert nonexsistent_newborns == 0

    def test_that_mother_looses_weight(self):
        """
        Tests that the birth method makes the mother loos weight according to the weight of the
        newborn animal.
        """
        pass

    def test_that_dead_animals_dissappears(self):
        """
        Tests that dead animals does not continue to exist.
        """
        pass

    def test_that_newborn_same_speci_as_parent(self):
        """
        Tests that herbivores only gives birth to herbivores and carnivores only gives birth to
        carnivores.
        """