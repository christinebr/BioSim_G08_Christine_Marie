"""
Example for creating axes, including empty axes with text.
"""

from biosim.island import TheIsland
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

fig = plt.figure()
grid = fig.add_gridspec(ncols=3, nrows=3, wspace=0.4, hspace=0.3)
ax1 = fig.add_subplot(grid[0, 0])
ax3 = fig.add_subplot(grid[0, 2])
ax4 = fig.add_subplot(grid[1, 0])
ax5 = fig.add_subplot(grid[1, 2])
ax7 = fig.add_subplot(grid[2, 0])
ax8 = fig.add_subplot(grid[2, 1])
ax9 = fig.add_subplot(grid[2, 2])
fig.show()

# Making the island, with some animals
geogr = """WWWWW
WWLHW
WDDLW
WWWWW
"""


############## Secound island, different parts of the code needs the island in different form, fix this later #########
geogr_island = """\
           WWWWW
           WWLHW
           WDDLW
           WWWWW"""

ini_animals = [{'loc': (2, 3),
                 'pop': [{'species': 'Herbivore',
                          'age': 5,
                          'weight': 20} for _ in range(200)]
                        + [{'species': 'Carnivore',
                            'age': 5,
                            'weight': 20} for _ in range(20)]
                },
               {'loc': (3,3),
                'pop': [{'species': 'Herbivore',
                          'age': 5,
                          'weight': 20} for _ in range(200)]
                        + [{'species': 'Carnivore',
                            'age': 5,
                            'weight': 20} for _ in range(20)]}
                ]

island = TheIsland(geogr_island, ini_animals)
num_of_years = 100

# Colors to be used for the different landscapes on the island
#                   R    G    B
rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
             'L': (0.0, 0.6, 0.0),  # dark green
             'H': (0.5, 1.0, 0.5),  # light green
             'D': (1.0, 1.0, 0.5)}  # light yellow

geogr_rgb = [[rgb_value[column] for column in row]
             for row in geogr.splitlines()]


# ax1 = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
ax1.imshow(geogr_rgb)
ax1.set_xticks(range(len(geogr_rgb[0])))
ax1.set_xticklabels(range(1, 1 + len(geogr_rgb[0])))
ax1.set_yticks(range(len(geogr_rgb)))
ax1.set_yticklabels(range(1, 1 + len(geogr_rgb)))

ax1 = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
ax1.axis('off')

### ax3
years = list(range(num_of_years))
# Makes list of years
herbi_count = []
# List with total number of herbivores each year
carni_count = []
# Ditto for carnivores
for year in years:
    _, total_herbis, total_carnis = island.total_num_animals_on_island()
    # Number of herbivores and carnivores on the island
    herbi_count.append(total_herbis)
    carni_count.append(total_carnis)
    island.annual_cycle()

ax3.plot(years, herbi_count, label='Herbivores')
ax3.plot(years, carni_count, label='Carnivores')
#ax3.legend()

ax3.set_title('Animals count')
#ax3.set_xlabel('Years')
#ax3.set_ylabel('Number of animals')

###
# axes for text
axt = fig.add_axes([0.4, 0.8, 0.2, 0.2])  # llx, lly, w, h
axt.axis('off')  # turn off coordinate system

template = '\n\nYear: {:5d}\n\nHerbivores - blue\nCarnivores - red'
txt = axt.text(0.5, 0.5, template.format(0),
               horizontalalignment='center',
               verticalalignment='center',
               transform=axt.transAxes)  # relative coordinates

plt.pause(0.01)  # pause required to make figure visible

input('Press ENTER to begin counting')

for k in range(30):
    txt.set_text(template.format(k))
    plt.pause(0.1)  # pause required to make update visible

plt.show()
