"""
Example for creating axes, including empty axes with text.
"""

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


# ax1 = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
ax1.imshow(geogr_rgb)
ax1.set_xticks(range(len(geogr_rgb[0])))
ax1.set_xticklabels(range(1, 1 + len(geogr_rgb[0])))
ax1.set_yticks(range(len(geogr_rgb)))
ax1.set_yticklabels(range(1, 1 + len(geogr_rgb)))

ax1 = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
ax1.axis('off')

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
