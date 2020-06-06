# -*- coding: utf-8 -*-
import numpy as np

class TheIsland:
    """
    Keeps control of the island.

    Takes a matrix with the landscape types of each cell.
    """

    def __init__(self, landscape_of_cells):
        self.landscapes = landscape_of_cells
        self.row, self.colon = landscape_of_cells.shape[0], landscape_of_cells.shape[1]

    def test_if_island_legal(self):
        """
        Test if the island follows the specifications.
        The string tha specify the island must only contain legal letters, i.e. L, H, W and D
        All the outermost cells must be of the water type.

        Returns
        -------
        Raises ValueError if any of the specifications is violated.

        Todo: This might be better to do in the __init__ section, and/or in biosim
        """
        pass

    def migration(self):
        """
        Makes migration happen, updates amount of animals in each cell
        Returns
        -------

        """
        pass

    def annual_cycle(self):
        """
        Makes the year happen.
        1. Animals eats, first herbivores, then carnivores
        2. Animals procreates
        3. Animals migrates
        4. Animals age
        5. Animals looses weight
        6. Animals die

        Returns
        -------
        Updates the list of animals for the two species at the end of the year.
        """
        
