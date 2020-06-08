# -*- coding: utf-8 -*-

from biosim.cell import SingleCell
import pytest
from copy import deepcopy
import random
from itertools import zip_longest


class TestSingleCell:

    @pytest.fixture()
    def initial_cell_class(self):
        animals = [{'species': 'Herbivore', 'age': 10, 'weight': 15},
                   {'species': 'Herbivore', 'age': 40, 'weight': 20},
                   {'species': 'Herbivore', 'age': 2, 'weight': 8},
                   {'species': 'Carnivore', 'age': 30, 'weight': 8},
                   {'species': 'Carnivore', 'age': 5, 'weight': 3.5},
                   {'species': 'Carnivore', 'age': 37, 'weight': 5.7}
                   ]
        self.cell = SingleCell(animals_list=animals)
        return self.cell

    def test_that_all_animals_age(self, initial_cell_class):
        """
        Tests that method age makes all animals get one year older.
        The sum of the age in the test-sett increases with a number equal to the number of
        animals every year.
        """
        sum_old = 0
        for animal in self.cell.herbi_list + self.cell.carni_list:
            sum_old += animal.age

        self.cell.aging_of_animals()

        sum_new = 0
        for animal in self.cell.herbi_list + self.cell.carni_list:
            sum_new += animal.age

        assert sum_old + len(self.cell.herbi_list + self.cell.carni_list) == sum_new

    def test_that_newborns_weights_something(self, initial_cell_class, mocker):
        """
        Tests that the birth method assigns a weight to the newborn animal.
        """
        mocker.patch('random.random', return_value=1)
        self.cell.birth()
        nonexsistent_newborns = 0
        for animal in self.cell.herbi_list + self.cell.carni_list:
            if animal.age == 0 and animal.weight <= 0:
                nonexsistent_newborns += 1

        assert nonexsistent_newborns == 0

    def test_that_mother_looses_weight(self, initial_cell_class, mocker):
        """
        Tests that the birth method makes the mother loose weight.
        """
        mocker.patch('random.random', return_value=0)
        mocker.patch('random.gauss', return_value=7)
        # Starts with finding what the weight of the mother should be after giving birth
        correct_weights = []
        weight_limit_herbi = 3.5 * (8 + 1.5)
        weight_new_herbi = random.gauss(8, 1.5)
        weight_limit_carni = 3.5 * (6 + 1.)
        weight_new_carni = random.gauss(6, 1.)
        for herbi in self.cell.herbi_list:
            if herbi.weight > weight_limit_herbi:
                correct_weights.append(herbi.weight - 1.2 * weight_new_herbi)
            else:
                correct_weights.append(herbi.weight)

        for carni in self.cell.carni_list:
            if carni.weight > weight_limit_carni:
                correct_weights.append(carni.weight - 1.1 * weight_new_carni)
            else:
                correct_weights.append(carni.weight)

        # Then find the old weights and the new weights
        old_list_of_animals = self.cell.herbi_list + self.cell.carni_list
        self.cell.birth()
        new_list_of_animals = self.cell.herbi_list + self.cell.carni_list
        new_list_parents = []
        for animal in new_list_of_animals:
            if animal.weight != weight_new_herbi or animal.weight != weight_new_carni:
                new_list_parents.append(animal)

        old_weights = []
        new_weights = []
        for old_animal, new_animal in zip(old_list_of_animals, new_list_parents):
            old_weights.append(old_animal.weight)
            new_weights.append(new_animal.weight)

        assert new_weights == correct_weights

        # mocker.patch('random.random', return_value=0)
        # mocker.patch('random.gauss', return_value=7)
        # old_list_of_animals = deepcopy(self.cell.animals_list)
        # self.cell.birth()
        # new_list_of_animals = self.cell.animals_list
        # old_weights = []
        # new_weights = []
        # correct_weights = []
        # for old_animal, new_animal in zip(old_list_of_animals, new_list_of_animals):
        #     # zip will use the shortest list, in this case old_list, to decide the length of the
        #     # zipped list. This way the newborns will not count.
        #     old_weights.append(old_animal['weight'])
        #     new_weights.append(new_animal['weight'])
        #
        #     if old_animal['species'] == 'Herbivore':
        #         weight_of_newborn = random.gauss(8, 1.5)
        #         weight_limit = 3.5 * (8 + 1.5)
        #         if old_animal['weight'] > weight_limit:
        #             correct_weights.append(old_animal['weight'] - 1.2 * weight_of_newborn)
        #         else:
        #             correct_weights.append(old_animal['weight'])
        #     else:
        #         weight_of_newborn_carn = random.gauss(6, 1.0)
        #         weight_limit = 3.5 * (6 + 1.0)
        #         if old_animal['weight'] > weight_limit:
        #             correct_weights.append(old_animal['weight'] - 1.1 * weight_of_newborn_carn)
        #         else:
        #             correct_weights.append(old_animal['weight'])
        #
        # assert new_weights == correct_weights

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
        old_list_of_animals = self.cell.herbi_list + self.cell.carni_list
        self.cell.herbi_list[1].weight = 0
        self.cell.carni_list[2].weight = 0
        self.cell.death()
        new_list_of_animals = self.cell.herbi_list + self.cell.carni_list
        assert len(new_list_of_animals) == len(old_list_of_animals) - 2

        mocker.patch('random.random', return_value=0)
        self.cell.death()
        list_of_animals = self.cell.herbi_list + self.cell.carni_list
        assert len(list_of_animals) == 0

    def test_that_newborn_same_speci_as_parent(self,initial_cell_class, mocker):
        """
        Tests that herbivores only gives birth to herbivores and carnivores only gives birth to
        carnivores.
        """
        mocker.patch('random.random', return_value=0)
        mocker.patch('random.gauss', return_value=7)
        self.cell.birth()
        mutants = 0
        for herbi in self.cell.herbi_list:
            pass

        assert 0 == 1


    def test_only_carnivores_eat_meat(self, initial_cell_class):
        """
        Test that only carnivores kill and eat other animals.
        """
        pass

    def test_no_cannibalism(self, initial_cell_class):
        """
        Test that carnivores only kill and eat herbivores. Does this by checking that
        the number of carnivores are the same after killing as before.
        """
        carni_before = len(self.cell.carni_list)
        self.cell.animals_in_cell_eat()
        carni_after = len(self.cell.carni_list)
        assert carni_before == carni_after

    def test_herbivores_eaten(self, initial_cell_class):
        """Tests that carnivores eat herbivores"""
        pass

    def possible_no_animals(self):
        """
        Checking that there wil be no problems if no animals are given into the class.
        """
        animals = []
        cellt = SingleCell(animals_list=animals)
        assert len(cellt.herbi_list + cellt.carni_list) == 0

    def test_sorting_correct(self, initial_cell_class):
        """
        Checks that the sorting of animals_list gives lists with the correct numbers of
        herbivores and carnivores.
        """
        assert len(self.cell.herbi_list + self.cell.carni_list) == 6