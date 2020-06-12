# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

test_array = [[2, 5, 8, 3 ,0, 5], [0, 4, 6, 5, 2, 3]]

plt.imshow(test_array, cmap='viridis')
plt.colorbar()
plt.show()

# def heatmap2d(arr: np.ndarray):
#     plt.imshow(arr, cmap='viridis')
#     plt.colorbar()
#     plt.show()
#
#
# test_array = [[2, 5, 8, 3 ,0, 5], [0, 4, 6, 5, 2, 3]]
# heatmap2d(test_array)