# -*- coding: utf-8 -*-

from biosim.cell import SingleCell
import pytest
from copy import deepcopy
import random


class TestSingleCell:

    @pytest.fixture()
    def initial_cell_class(self):
        animals = [{'species': 'Herbivore', 'age': 10, 'weight': 15},
                   {'species': 'Herbivore', 'age': 40, 'weight': 20},
                   {'species': 'Carnivore', 'age': 30, 'weight': 3.5}]
        self.cell = SingleCell(animals_list=animals)
        return self.cell

    def test_that_all_animals_age(self, initial_cell_class):
        """
        Tests that method age makes all animals get one year older.
        The sum of the age in the test-sett increases with 3 per year.
        """
        cell_old = deepcopy(self.cell.get_animals())
        self.cell.aging_of_animals()
        cell_new = self.cell.get_animals()
        sum_old_age = 0
        sum_new_age = 0
        for old, older in zip(cell_old, cell_new):
            sum_old_age += old['age']
            sum_new_age += older['age']
        assert sum_old_age + len(self.cell.animals_list) == sum_new_age

    def test_that_newborns_weights_something(self, initial_cell_class, mocker):
        """
        Tests that the birth method assigns a weight to the newborn animal.
        """
        mocker.patch('random.random', return_value=1)
        self.cell.birth()
        nonexsistent_newborns = 0
        for animal in self.cell.animals_list:
            if animal['age'] == 0 and animal['weight'] <= 0:
                nonexsistent_newborns += 1

        assert nonexsistent_newborns == 0

    def test_that_mother_looses_weight(self, initial_cell_class, mocker):
        """
        Tests that the birth method makes the mother loose weight.
        """
        mocker.patch('random.random', return_value=0)
        mocker.patch('random.gauss', return_value=7)
        old_list_of_animals = deepcopy(self.cell.get_animals())
        self.cell.birth()
        new_list_of_animals = self.cell.get_animals()
        old_weights = []
        new_weights = []
        correct_weights = []
        for old_animal, new_animal in zip(old_list_of_animals, new_list_of_animals):
            # zip will use the shortest list, in this case old_list, to decide the length of the
            # zipped list. This way the newborns will not count.
            old_weights.append(old_animal['weight'])
            new_weights.append(new_animal['weight'])

            if old_animal['species'] == 'Herbivore':
                weight_of_newborn = random.gauss(8, 1.5)
                weight_limit = 3.5 * (8 + 1.5)
                if old_animal['weight'] > weight_limit:
                    correct_weights.append(old_animal['weight'] - 1.2 * weight_of_newborn)
                else:
                    correct_weights.append(old_animal['weight'])
            else:
                weight_of_newborn_carn = random.gauss(6, 1.0)
                weight_limit = 3.5 * (6 + 1.0)
                if old_animal['weight'] > weight_limit:
                    correct_weights.append(old_animal['weight'] - 1.1 * weight_of_newborn_carn)
                else:
                    correct_weights.append(old_animal['weight'])

        assert new_weights == correct_weights

    def test_no_zombies(self, initial_cell_class, mocker):
        """
        Tests that dead animals does not continue to exist (no zombies welcome on this island).

        The first test checks that an animal of weight zero disappears. Also checks that the two
            animals that are supposed to survive actually does so.
        The second test checks that when all animals dies, all of them disappears.

        Todo: Make more tests on this
            Test that herbivores eaten by a carnivore does not survive
        """
        mocker.patch('random.random', return_value=1)
        old_list_of_animals = deepcopy(self.cell.get_animals())
        self.cell.get_animals()[1]['weight'] = 0
        self.cell.death()
        new_list_of_animals = self.cell.get_animals()
        assert len(new_list_of_animals) == len(old_list_of_animals) - 1

        mocker.patch('random.random', return_value=0)
        self.cell.death()
        list_of_animals = self.cell.get_animals()
        assert len(list_of_animals) == 0

    def test_that_newborn_same_speci_as_parent(self):
        """
        Tests that herbivores only gives birth to herbivores and carnivores only gives birth to
        carnivores.
        """
        pass

    def test_only_carnivores_eat_meat(self, initial_cell_class):
        """
        Test that only carnivores kill and eat other animals.
        """
        pass

    def test_no_cannibalism(self, initial_cell_class):
        """
        Test that carnivores only kill and eat herbivores.
        """
        pass
