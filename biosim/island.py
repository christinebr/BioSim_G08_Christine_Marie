# -*- coding: utf-8 -*-

class TheIsland:
    """
    Keeps control of the island.

    Todo: Skal landskap ha en defaultverdi?
    """

    def __init__(self, landscape_of_cells):
        self.landscapes = landscape_of_cells

    def test_if_island_legal(self):
        """
        Test if the island follows the specifications.
        The string tha specify the island must only contain legal letters, i.e. L, H, W and D
        All the outermost cells must be of the water type.

        Returns
        -------
        Raises ValueError if any of the specifications is violated.

        Todo: This might be better to do in the __init__ section
        """
        pass

    def annual_cycle(self):
        """
        Makes the year happen.
        1. Food appear
        2. Animals eat, first herbivores, then carnivores
        3. Animals procreate
        4. Animals migrate
        5. Animals age
        6. Animals loos weight
        7. Animals die

        Returns
        -------
        List of animals of the two species at the end of the year.
        """
        pass
