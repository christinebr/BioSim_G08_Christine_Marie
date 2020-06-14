from biosim.animals import Herbivores, Carnivores

if __name__ == "__main__":

    h3 = Herbivores(weight=80, age=16)
    print(h3.fitness())
    old_param = h3.get_params()
    print(old_param)
    h3.set_params({'w_half': 2.0, 'beta': 0.8})
    new_param = h3.get_params()
    print(new_param)

    herbis = [{'species': 'Herbivore', 'age': 10, 'weight': 15},
              {'species': 'Herbivore', 'age': 8, 'weight': 20},
              {'species': 'Herbivore', 'age': 1, 'weight': 5},
              {'species': 'Herbivore', 'age': 35, 'weight': 30}]

    carnis = [{'species': 'Carnivore', 'age': 43, 'weight': 29},
              {'species': 'Carnivore', 'age': 30, 'weight': 23},
              {'species': 'Carnivore', 'age': 3, 'weight': 30},
              {'species': 'Carnivore', 'age': 1, 'weight': 12}]

    print("HERBIVORES")
    for herb in herbis:
        h = Herbivores(weight=herb['weight'], age=herb['age'])
        print(f"Weight:        {h.weight}")
        print(f"Age:           {h.age}")
        print(f"Fodder:        {h.get_params()['F']}")
        print(f"Fitness:       {h.fitness():.3f}")
        print(f"Prob of birth: {h.birth(num=9)}")
        print(f"Prob of death: {h.probability_death():.3f}\n")

    print("CARNIVORES")
    for carb in carnis:
        c = Carnivores(weight=carb['weight'], age=carb['age'])
        print(f"Weight:        {c.weight}")
        print(f"Age:           {c.age}")
        print(f"Fitness:       {c.fitness():.3f}")
        print(f"Prob of birth: {c.birth(num=9)}")
        print(f"Prob of death: {c.probability_death():.3f}\n")
