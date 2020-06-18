# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

__author__ = "Marie Kolvik Valøy, Christine Brinchmann"
__email__ = "mvaloy@nmbu.no, christibr@nmbu.no"

"""
This is where we test how to make the map of the island and make changes in the
map before implementing changes into the main plot section.

Initial code taken from Hans Ekkehard Plesser
from nmbu_inf200_june2020 repository inside the directories examples->plotting
filename: mapping.py
"""

geogr = """WWWWW
WWLHW
WDDLW
WWWWW
"""

# Colors to be used for the different landscapes on the island
#                   R    G    B
rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
             'L': (0.0, 0.6, 0.0),  # dark green
             'H': (0.5, 1.0, 0.5),  # light green
             'D': (1.0, 1.0, 0.5)}  # light yellow

geogr_rgb = [[rgb_value[column] for column in row]
             for row in geogr.splitlines()]

fig = plt.figure()

axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
axim.imshow(geogr_rgb)
axim.set_xticks(range(len(geogr_rgb[0])))
axim.set_xticklabels(range(1, 1 + len(geogr_rgb[0])))
axim.set_yticks(range(len(geogr_rgb)))
axim.set_yticklabels(range(1, 1 + len(geogr_rgb)))

axlg = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
axlg.axis('off')
for ix, name in enumerate(('Water', 'Lowland',
                           'Highland', 'Desert')):
    axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                 edgecolor='none',
                                 facecolor=rgb_value[name[0]]))
    axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

plt.show()
