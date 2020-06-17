"""
Example for creating axes, including empty axes with text.
"""

from biosim.island import TheIsland
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

# fig = plt.figure()
# grid = fig.add_gridspec(ncols=3, nrows=3, wspace=0.2, hspace=0.4)
# ax1 = fig.add_subplot(grid[0, 0])
# ax3 = fig.add_subplot(grid[0, 2])
# ax4 = fig.add_subplot(grid[1, 0], anchor='E')
# ax6 = fig.add_subplot(grid[1, 2], anchor='W')
# ax7 = fig.add_subplot(grid[2, 0])
# ax8 = fig.add_subplot(grid[2, 1])
# ax9 = fig.add_subplot(grid[2, 2])
# fig.show()

fig = plt.figure()
ax1 = fig.add_subplot(3, 3, 1)
ax3 = fig.add_subplot(3, 3, 3)
ax4 = fig.add_subplot(3, 3, 4)
ax6 = fig.add_subplot(3, 3, 6)
ax7 = fig.add_subplot(3, 3, 7)
ax8 = fig.add_subplot(3, 3, 8)
ax9 = fig.add_subplot(3, 3, 9)
fig.show()

# Making the island, with some animals
geogr = """WWWWW
WWLHW
WDDLW
WWWWW
"""

# Same island, different parts of the code needs the island in different form, fix this later
geogr_island = """\
           WWWWW
           WWLHW
           WDDLW
           WWWWW"""

# # New and bigger island
# geogr = """WWWWWWWWW
# WWLHLLDDW
# WDDLDHHLW
# WLWLDDHWW
# WLLHDLLLW
# WWWWWWWWW
# """
#
# geogr_island = """\
#            WWWWWWWWW
#            WWLHLLDDW
#            WDDLDHHLW
#            WLWLDDHWW
#            WLLHDLLLW
#            WWWWWWWWW"""


ini_animals = [{'loc': (2, 4),
                'pop': [{'species': 'Herbivore',
                         'age': 5,
                         'weight': 20} for _ in range(200)]
                + [{'species': 'Carnivore',
                    'age': 5,
                    'weight': 20} for _ in range(20)]
                },
               {'loc': (3, 3),
                'pop': [{'species': 'Herbivore',
                         'age': 5,
                         'weight': 20} for _ in range(200)]
                + [{'species': 'Carnivore',
                    'age': 5,
                    'weight': 20} for _ in range(20)]}
               ]

island = TheIsland(geogr_island, ini_animals)
num_of_years = 100

# Fontsizes to be used on the titles of all plots
font = 8
# Fontsizes to be used on the axes of all plots
font_axes = 8

# Colors to be used for the different landscapes on the island
#                   R    G    B
rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
             'L': (0.0, 0.6, 0.0),  # dark green
             'H': (0.5, 1.0, 0.5),  # light green
             'D': (1.0, 1.0, 0.5)}  # light yellow

geogr_rgb = [[rgb_value[column] for column in row]
             for row in geogr.splitlines()]

# ax1
# ===========
# ax1 = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
ax1.imshow(geogr_rgb)
ax1.set_xticks(range(len(geogr_rgb[0])))
ax1.set_xticklabels(range(1, 1 + len(geogr_rgb[0])), fontsize=font_axes)
ax1.set_yticks(range(len(geogr_rgb)))
ax1.set_yticklabels(range(1, 1 + len(geogr_rgb)), fontsize=font_axes)

# ax1 = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
# ax1.axis('off')
ax1.set_title('The island', fontsize=font)

# ax3
# ===========
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
# ax3.legend()

ax3.set_title('Animals count', fontsize=font)
list_xticks = [0, int(num_of_years/4), int(num_of_years/2), int(num_of_years*3/4), num_of_years]
# list_xticks = [0, 25, 50, 75, 100]
ax3.set_xticks(list_xticks)
ax3.set_xticklabels(list_xticks, fontsize=font_axes)
# ax3.set_xlabel('Years')
# ax3.set_ylabel('Number of animals')

# ax4
# =============
herbis_lists = []
carnis_lists = []
for row in range(island.row):
    herbis_row = []
    carnis_row = []
    for col in range(island.col):
        herbis, carnis = island.give_animals_in_cell(row + 1, col + 1)
        herbis_row.append(len(herbis))
        carnis_row.append(len(carnis))
    herbis_lists.append(herbis_row)
    carnis_lists.append(carnis_row)

im = ax4.imshow(herbis_lists, cmap='viridis')
ax4.set_title('Herbivore distribution', fontsize=font)
fig.colorbar(im, ax=ax4, orientation='vertical')
ax4.set_xticks(range(len(geogr_rgb[0])))
ax4.set_xticklabels(range(1, 1 + len(geogr_rgb[0])), fontsize=font_axes)
ax4.set_yticks(range(len(geogr_rgb)))
ax4.set_yticklabels(range(1, 1 + len(geogr_rgb)), fontsize=font_axes)

# ax6
# ===============
im = ax6.imshow(carnis_lists, cmap='viridis')
ax6.set_title('Carnivore distribution', fontsize=font)
fig.colorbar(im, ax=ax6, orientation='vertical')
ax6.set_xticks(range(len(geogr_rgb[0])))
ax6.set_xticklabels(range(1, 1 + len(geogr_rgb[0])), fontsize=font_axes)
ax6.set_yticks(range(len(geogr_rgb)))
ax6.set_yticklabels(range(1, 1 + len(geogr_rgb)), fontsize=font_axes)

# ax7
# =================
herbi_fitness = island.collect_fitness_age_weight_herbi()[0]
carni_fitness = island.collect_fitness_age_weight_carni()[0]

ax7.hist(herbi_fitness, bins=20, range=(0, 1), histtype='stepfilled', fill=False, edgecolor='blue')
ax7.hist(carni_fitness, bins=20, range=(0, 1), histtype='stepfilled', fill=False, edgecolor='red')

ax7.set_title('Fitness', fontsize=font)
xticks = np.linspace(0, 1, 5)
ax7.set_xticks(xticks)
ax7.set_xticklabels(xticks, fontsize=font_axes)
# ax7.set_yticklabels(fontsize=font_axes)

# ax8
# ==========
herbi_age = island.collect_fitness_age_weight_herbi()[1]
carni_age = island.collect_fitness_age_weight_carni()[1]

ax8.hist(herbi_age, bins=20, histtype='stepfilled', fill=False, edgecolor='blue')
ax8.hist(carni_age, bins=20, histtype='stepfilled', fill=False, edgecolor='red')
ax8.set_title('Age', fontsize=font)

# ax9
# ============
herbi_weight = island.collect_fitness_age_weight_herbi()[2]
carni_weight = island.collect_fitness_age_weight_carni()[2]

ax9.hist(herbi_weight, bins=20, histtype='stepfilled', fill=False, edgecolor='blue')
ax9.hist(carni_weight, bins=20, range=(0, 40), histtype='stepfilled', fill=False, edgecolor='red')
ax9.set_title('Weight', fontsize=font)


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
