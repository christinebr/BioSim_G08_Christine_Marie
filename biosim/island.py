# -*- coding: utf-8 -*-
from biosim.cell import Highland, Lowland, Desert, Water
import textwrap


class TheIsland:
    """ This class will represent an island. """

    def __init__(self, landscape_of_cells, animals_on_island=None):
        """
        Create an island consisting of cells based on landscape-types.

        Parameters
        ----------
        landscape_of_cells: [str] multiline python string representing the
                            landscape of the island.
        animals_on_island: [list of dicts] list of dictionaries with location
                           of cell and population of animals in that cell.
        """
        # Check conditions for geography of island
        self.check_if_island_legal(landscape_of_cells)

        # Make landscape into list of lists
        self.landscape = self.landscape_to_list_of_lists(landscape_of_cells)
        self.row, self.colon = len(self.landscape), len(self.landscape[0])

        # Create empty island, then construction of cells
        self.island_cells = [[[] for _ in range(self.colon)] for _ in range(self.row)]
        self.construct_island_with_cells()

        if animals_on_island:
            self.animals_on_island = animals_on_island
        else:
            self.animals_on_island = []

        self.add_animals_on_island(self.animals_on_island)

    @staticmethod
    def check_if_island_legal(geogr):
        """
        Checks if the landscape of the island follows the specifications.
            - only have 'W' around edges
            - no other characters than 'L', 'H', 'D' and 'W'
            - all lines in the string must have equal length

        Raises
        -------
        ValueError: if any of the specifications is violated.
        """
        geogr = textwrap.dedent(geogr)
        geogr_split = geogr.split('\n')
        len_first_line = len(geogr_split[0])
        for line in geogr_split:
            if len(line) != len_first_line:
                raise ValueError("All lines must have the same length.")

        for top, bottom in zip(geogr_split[0], geogr_split[-1]):
            if top != 'W' or bottom != 'W':
                raise ValueError("North or south of island is not only water.")

        for line in geogr_split:
            if line[0] != 'W' or line[-1] != 'W':
                raise ValueError("West or east side of island is not only water.")

        for line in geogr_split:
            for element in line:
                if element not in ['W', 'D', 'L', 'H']:
                    raise ValueError("Forbidden character, only 'W', 'D', 'L' and 'H' allowed.")

    @staticmethod
    def landscape_to_list_of_lists(landscape):
        """
        Makes a landscape string into a nested list (list of lists).

        Parameters
        ----------
        landscape: [str] multiline string representing the landscape of
                   the island

        Returns
        -------
        [list of lists] an inner list is a row and an element of an inner list
        is the landscape of that cell.
        """
        landscape = textwrap.dedent(landscape)
        landscape_split = landscape.split('\n')
        return [list(line) for line in landscape_split]

    def construct_island_with_cells(self):
        """
        Construction the island by initialising a class for each of the
        landscape types. For each cell the class is initialized with no
        animals.

        Returns
        -------
        None
        """
        for x, row in enumerate(self.landscape):
            for y, cell in enumerate(row):
                if cell == 'W':
                    self.island_cells[x][y] = Water(animals_list=None)
                elif cell == 'L':
                    self.island_cells[x][y] = Lowland(animals_list=None)
                elif cell == 'H':
                    self.island_cells[x][y] = Highland(animals_list=None)
                elif cell == 'D':
                    self.island_cells[x][y] = Desert(animals_list=None)

    def add_animals_on_island(self, new_animals):
        """
        Add animals on island by adding animals to specified cells.

        Parameters
        ----------
        new_animals: [list of dicts] list of dictionaries with location
                     of cell and population of animals in that cell.

        Returns
        -------
        None

        Raises
        ------
        ValueError: if animals are being placed in water cells where they
                    can't stay
        """
        for dictionary in new_animals:
            x, y = dictionary['loc']  # Location of a cell
            landscape_type = self.landscape[x-1][y-1]  # Landscape type of cell
            if landscape_type == 'W':
                raise ValueError("Animals can't stay in water")
            else:
                self.island_cells[x-1][y-1].add_new_animals_to_cell(dictionary['pop'])
                # add new animals to cell

    def all_animals_eat(self):
        """
        Letting the animals on the island eat.
        Looping through the cells of the island and letting the animals in
        each cell eat.

        Returns
        -------
        None
        """
        for row in self.island_cells:
            for cell in row:
                cell.animals_in_cell_eat()

    def animals_procreate(self):
        """
        Letting animals on the island procreate
        Looping through the cells of the island and giving the animals in the
        cells the change to procreate.

        Returns
        -------
        None
        """
        for row in self.island_cells:
            for cell in row:
                cell.birth()

    def where_can_animals_migrate_to(self, row, col):
        """
        Check if any of the neighboring adjacent cells are water, and
        returns the directions animals can migrate to.

        Parameters
        ----------
        row: [int] row number as python uses it
        col: [int] colon number as python uses it

        Returns
        -------
        directions: [list] list with possible directions
            - can move in all directions: ['North', 'East', 'South', 'West']
            - can only move to east and south: ['East', 'South']
        """
        directions = []
        if self.landscape[row-1][col] != 'W':
            directions.append('North')

        if self.landscape[row][col+1] != 'W':
            directions.append('East')

        if self.landscape[row+1][col] != 'W':
            directions.append('South')

        if self.landscape[row][col-1] != 'W':
            directions.append('West')

        return directions

    def migration(self):
        """
        Makes migration happen, updates amount of animals in each cell
        Returns
        -------
        Method in cell: updates self.herbi_list and self.carni_list
        # Animals staying in the cell
        self.herbi_list = herbi_stay
        self.carni_list = carni_stay

        # Returning the animals which want to migrate
        return herbi_move, carni_move
        """
        # Make ghost island to store migrating animals
        ghost_island = [[[] for _ in range(self.colon)] for _ in range(self.row)]

        for x, row in enumerate(self.island_cells):
            for y, cell in enumerate(row):
                if self.landscape[x][y] != 'W':
                    pos_dir = self.where_can_animals_migrate_to(x, y)
                    north, east, south, west = cell.animals_migrate()
                    if 'North' in pos_dir:
                        ghost_island[x-1][y] += north
                    else:
                        ghost_island[x][y] += north

                    if 'East' in pos_dir:
                        ghost_island[x][y+1] += east
                    else:
                        ghost_island[x][y] += east

                    if 'South' in pos_dir:
                        ghost_island[x + 1][y] += south
                    else:
                        ghost_island[x][y] += south

                    if 'West' in pos_dir:
                        ghost_island[x][y - 1] += west
                    else:
                        ghost_island[x][y] += west

        for x, row in enumerate(self.island_cells):
            for y, cell in enumerate(row):
                cell.add_animals_after_migration(ghost_island[x][y])

        return ghost_island

    def possible_relocations(self):
        pass

    def all_animals_age(self):
        """
        Animals in each cell age
        """
        for row in self.island_cells:
            for cell in row:
                if cell:  # nothing happens in water cell
                    cell.aging_of_animals()

    def all_animals_losses_weight(self):
        """
        Animals in each cell losses weight (end of year)
        """
        for row in self.island_cells:
            for cell in row:
                if cell:  # nothing happens in water cell
                    cell.weight_loss_end_of_year()

    def animals_die(self):
        for row in self.island_cells:
            for cell in row:
                if cell:  # nothing happens in water cell
                    cell.death()

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
        self.all_animals_eat()
        self.animals_procreate()
        self.migration()
        self.all_animals_age()
        self.all_animals_losses_weight()
        self.animals_die()

    def give_animals_in_cell(self, row, col):
        """
        Give lists of herbivores and carnivores in a given cell

        Parameters
        ----------
        row: [int] row number for cell
        col: [int] colon number for cell

        Returns
        -------
        herbis: [list] list of herbivores in cell
        carnis: [list] list of carnivores in cell
        """
        herbis = self.island_cells[row-1][col-1].herbi_list
        carnis = self.island_cells[row-1][col-1].carni_list
        return herbis, carnis

    def herbis_and_carnis_on_island(self):
        """

        Returns
        -------
        herbi_island: [list] island with number of herbivores in each cell
        carni_island: [list] island with number of carnivores in each cell
        """
        herbi_island = [[[] for _ in range(self.colon)] for _ in range(self.row)]
        carni_island = [[[] for _ in range(self.colon)] for _ in range(self.row)]
        for x, row in enumerate(self.island_cells):
            for y, cell in enumerate(row):
                herbi_island[x][y] = len(cell.herbi_list)
                carni_island[x][y] = len(cell.carni_list)
        return herbi_island, carni_island

    def total_num_animals_on_island(self):
        """Returns total number of animals on the island

        Returns:
        ----------
        Total number of animals on the island
        """
        tot_herbi = 0
        tot_carni = 0
        for row in self.island_cells:
            for cell in row:
                tot_herbi += len(cell.herbi_list)
                tot_carni += len(cell.carni_list)
        tot_animal = tot_herbi + tot_carni
        return tot_animal, tot_herbi, tot_carni

    def collect_fitness_age_weight_herbi(self):
        """

        Returns
        -------
        fitness_herbi: [list] fitness
        age_herbi: [list]
        weight_herbi: [list]

        """
        fitness_herbi = []
        age_herbi = []
        weight_herbi = []
        for row in self.island_cells:
            for cell in row:
                fitness, age, weight = cell.collect_fitness_age_weight_herbi()
                fitness_herbi += fitness
                age_herbi += age
                weight_herbi += weight

        return fitness_herbi, age_herbi, weight_herbi

    def collect_fitness_age_weight_carni(self):
        """

        Returns
        -------
        fitness_herbi: [list] fitness
        age_herbi: [list]
        weight_herbi: [list]

        """
        fitness_herbi = []
        age_herbi = []
        weight_herbi = []
        for row in self.island_cells:
            for cell in row:
                fitness, age, weight = cell.collect_fitness_age_weight_carni()
                fitness_herbi += fitness
                age_herbi += age
                weight_herbi += weight

        return fitness_herbi, age_herbi, weight_herbi


if __name__ == "__main__":
    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 25}
                          for _ in range(10)]}]
    # Simplest island possible
    land = """\
                WWW
                WLW
                WWW"""
    isl = TheIsland(landscape_of_cells=land, animals_on_island=ini_herbs)
    print("Original landscape given in:\n", isl.landscape)
    isl.construct_island_with_cells()
    print("Landscape used in TheIsland-class\n", isl.island_cells)
    isl.add_animals_on_island(ini_herbs)
    print(isl.island_cells[1][1].get_params())

    print("Weight of one herbivore:", isl.island_cells[1][1].herbi_list[0].weight)
    isl.all_animals_eat()
    print("Weight of one herbivore:", isl.island_cells[1][1].herbi_list[0].weight)

    print("Animals in cell before birth:", len(isl.island_cells[1][1].herbi_list))
    isl.animals_procreate()
    print("Animals in cell after birth:", len(isl.island_cells[1][1].herbi_list))

    print("Age of one herbivore:", isl.island_cells[1][1].herbi_list[0].age)
    isl.all_animals_age()
    print("Age of one herbivore:", isl.island_cells[1][1].herbi_list[0].age)

    print("Weight of one herbivore:", isl.island_cells[1][1].herbi_list[0].weight)
    isl.all_animals_losses_weight()
    print("Weight of one herbivore:", isl.island_cells[1][1].herbi_list[0].weight)

    print("Animals in cell before death:", len(isl.island_cells[1][1].herbi_list))
    isl.animals_die()
    print("Animals in cell after death:", len(isl.island_cells[1][1].herbi_list))

    # Start of year:
    print("\nBEFORE ANNUAL CYCLE")
    print("Weight of one herbivore:", isl.island_cells[1][1].herbi_list[0].weight)
    print("Animals in cell:", len(isl.island_cells[1][1].herbi_list))
    print("Age of one herbivore:", isl.island_cells[1][1].herbi_list[0].age)

    isl.annual_cycle()
    print("\nAFTER ANNUAL CYCLE")
    print("Weight of one herbivore:", isl.island_cells[1][1].herbi_list[0].weight)
    print("Animals in cell:", len(isl.island_cells[1][1].herbi_list))
    print("Age of one herbivore:", isl.island_cells[1][1].herbi_list[0].age)

    new = [{'loc': (2, 2),
            'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 10},
                    {'species': 'Herbivore', 'age': 8, 'weight': 25},
                    {'species': 'Herbivore', 'age': 5, 'weight': 15},
                    {'species': 'Carnivore', 'age': 6, 'weight': 10},
                    {'species': 'Carnivore', 'age': 3, 'weight': 8},
                    {'species': 'Carnivore', 'age': 43, 'weight': 8}]
            }
           ]

    print("\nAnimals in cell before:",
          len(isl.island_cells[1][1].herbi_list+isl.island_cells[1][1].carni_list))
    isl.add_animals_on_island(new_animals=new)
    print("Animals in cell after:",
          len(isl.island_cells[1][1].herbi_list+isl.island_cells[1][1].carni_list))

    bigger_island = """\
                        WWWWW
                        WLLLW
                        WHDHW
                        WLDLW
                        WWWWW"""

    animals_isl2 = [{'loc': (3, 3),
                     'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 30}
                             for _ in range(200)]
                     }]
                    # {'loc': (2, 3),
                    #  'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 30}
                    #          for _ in range(10)]
                    #  }
                    # ]

    isl2 = TheIsland(landscape_of_cells=bigger_island)
    print("Original landscape given in:\n", isl2.landscape)
    isl2.construct_island_with_cells()
    print("Landscape used in TheIsland-class\n", isl2.island_cells)
    isl2.add_animals_on_island(new_animals=animals_isl2)
    print(isl2.give_animals_in_cell(2, 2))
    print("before migration")
    print(isl2.migration())
    print(isl2.migration())
    print(isl2.migration())
    print(isl2.migration())
    print(isl2.migration())
    print(isl2.migration())
    print(isl2.migration())
    print(isl2.migration())
    print("after migration")
    herb, carn = isl2.give_animals_in_cell(2, 2)
    print(f"\nAnimals in (2, 2):", len(herb + carn))
    herb, carn = isl2.give_animals_in_cell(2, 3)
    print(f"Animals in (2, 3):", len(herb + carn))
    herb, carn = isl2.give_animals_in_cell(2, 4)
    print(f"Animals in (2, 4):", len(herb + carn))
    herb, carn = isl2.give_animals_in_cell(3, 2)
    print(f"\nAnimals in (3, 2):", len(herb + carn))
    herb, carn = isl2.give_animals_in_cell(3, 3)
    print(f"Animals in (3, 3):", len(herb + carn))
    herb, carn = isl2.give_animals_in_cell(3, 4)
    print(f"Animals in (3, 4):", len(herb + carn))
    herb, carn = isl2.give_animals_in_cell(4, 2)
    print(f"\nAnimals in (4, 2):", len(herb + carn))
    herb, carn = isl2.give_animals_in_cell(4, 3)
    print(f"Animals in (4, 3):", len(herb + carn))
    herb, carn = isl2.give_animals_in_cell(4, 4)
    print(f"Animals in (4, 4):", len(herb + carn))
