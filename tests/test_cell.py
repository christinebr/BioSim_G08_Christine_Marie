# -*- coding: utf-8 -*-

from biosim.cell import SingleCell
import pytest


class TestSingleCell:

    @pytest.fixture()
    def initial_cell_class(self):
        animals = [[{'species': 'Herbivore', 'age': 10, 'weight': 40},
                    {'species': 'Herbivore', 'age': 8, 'weight': 29},
                    {'species': 'Herbivore', 'age': 3, 'weight': 10}]]
        self.cell = SingleCell(animals_list=animals)
        return self.cell
