from biosim.island import TheIsland

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
