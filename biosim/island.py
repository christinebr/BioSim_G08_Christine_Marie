# -*- coding: utf-8 -*-

class TheIsland:
    """
    Keeps control of the island.

    Todo: Skal landskap ha en defaultverdi?
    """

    def __init__(self, landscape_of_cells):
        self.landscapes = landscape_of_cells

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
