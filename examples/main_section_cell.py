from biosim.cell import Lowland

if __name__ == "__main__":
    animals = [{'species': 'Herbivore', 'age': 1, 'weight': 5},
               {'species': 'Herbivore', 'age': 8, 'weight': 25},
               {'species': 'Herbivore', 'age': 5, 'weight': 15},
               {'species': 'Carnivore', 'age': 6, 'weight': 15},
               {'species': 'Carnivore', 'age': 3, 'weight': 8},
               {'species': 'Carnivore', 'age': 23, 'weight': 12}]

    low = Lowland(animals_list=animals)

    w_before = [ani.weight for ani in (low.herbi_list+low.carni_list)]
    print("Weight before eating:", w_before)
    # Eating
    low.animals_in_cell_eat()
    w_after = [ani.weight for ani in (low.herbi_list+low.carni_list)]
    print("Weight after eating:", w_after)

    print("Number of animals before birth:", len(low.herbi_list + low.carni_list))
    low.birth()
    print("Number of animals after birth:", len(low.herbi_list + low.carni_list))

    north, east, south, west = low.animals_migrate()
    print(north)
    print(east)
    print(south)
    print(west)

    a_before = [ani.age for ani in (low.herbi_list+low.carni_list)]
    print("Age before:", a_before)
    # Animals aging
    low.aging_of_animals()
    a_after = [ani.age for ani in (low.herbi_list + low.carni_list)]
    print("Age after:", a_after)

    w_before = [ani.weight for ani in (low.herbi_list+low.carni_list)]
    print("Weight before loss:", w_before)
    low.weight_loss_end_of_year()
    w_after = [ani.weight for ani in (low.herbi_list+low.carni_list)]
    print("Weight after loss:", w_after)

    print("Number of animals before death:", len(low.herbi_list + low.carni_list))
    low.death()
    print("Number of animals after death:", len(low.herbi_list + low.carni_list))
