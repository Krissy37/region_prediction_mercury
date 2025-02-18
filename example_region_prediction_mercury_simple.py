# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 15:51:07 2024

@author: kriss
"""

# =============================================================================
# Test Region Prediction Tool (simple version)
# =============================================================================


from region_prediction_mercury_simple import get_region
import numpy as np 
import matplotlib.pyplot as plt
import collections
from matplotlib.colors import ListedColormap, BoundaryNorm

RM = 2440

x_vec = np.linspace(3, -3, 200)*RM
z_vec = np.linspace(-2.5, 2.5, 200)*RM
x_grid, z_grid = np.meshgrid(x_vec, z_vec)

x_mso = x_grid.reshape(-1)
y_mso = np.zeros(len(x_mso))
z_mso = z_grid.reshape(-1)

r_hel_near = 0.31
r_hel_mid = 0.38
r_hel_far = 0.46

res_pred_near = get_region(x_mso, y_mso, z_mso, r_hel_near, di = 100)
res_pred_mid = get_region(x_mso, y_mso, z_mso, r_hel_mid, di = 0)
res_pred_far = get_region(x_mso, y_mso, z_mso, r_hel_far)

region_near = res_pred_near

region_mid = res_pred_mid

region_far = res_pred_far

# counter = collections.Counter(region_quiet)
# print('Region quiet: ', counter)

# counter = collections.Counter(region_disturbed)
# print('Region disturbed: ', counter)


matrix_coord = region_near.reshape(len(x_vec), len(z_vec))

# Define the colormap and normalization
cmap = ListedColormap(['#808080', '#ADD8E6', '#00008B', '#90EE90', '#006400', '#FFFF00'])
norm = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], cmap.N)



#transform matrix for right plotting: 
#z = -2.5 is at the top of the plot
#x = 3 is at the left of the plot
#x = -3 is at the right of the plot
#z = 2.5 is at the bottom of the plot

matrix_coord_near = np.flipud(region_near.reshape(len(x_vec), len(z_vec)))
matrix_coord_mid = np.flipud(region_mid.reshape(len(x_vec), len(z_vec)))
matrix_coord_far = np.flipud(region_far.reshape(len(x_vec), len(z_vec)))

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize = (16, 6))
plt.suptitle('Region Prediction for Mercury')
sc = ax1.imshow(matrix_coord_near, cmap=cmap, norm=norm, extent=[x_vec[0]/RM, x_vec[-1]/RM, z_vec[0]/RM, z_vec[-1]/RM])
ax1.set_xlabel('x in MSO in RM')
ax1.set_ylabel('z in MSO in RM')
ax1.set_title(r'r$_{hel}$ ' + f'= {r_hel_near} AU')
ax1.grid()

ax2.imshow(matrix_coord_mid, cmap=cmap, norm=norm, extent=[x_vec[0]/RM, x_vec[-1]/RM, z_vec[0]/RM, z_vec[-1]/RM])
ax2.set_xlabel('x in MSO in RM')
ax2.set_ylabel('z in MSO in RM')
ax2.set_title(r'r$_{hel}$ ' + f'= {r_hel_mid} AU')
ax2.grid()

ax3.imshow(matrix_coord_far, cmap=cmap, norm=norm, extent=[x_vec[0]/RM, x_vec[-1]/RM, z_vec[0]/RM, z_vec[-1]/RM])
ax3.set_xlabel('x in MSO in RM')
ax3.set_ylabel('z in MSO in RM')
ax3.set_title(r'r$_{hel}$ ' + f'= {r_hel_far} AU')
ax3.grid()

#add colorbar 
cbar = fig.colorbar(sc, ax=[ax1, ax2, ax3], orientation='horizontal', pad=0.1, ticks=[1, 2, 3, 4, 5, 6])
cbar.set_ticklabels(['Mercury', 'Magnetosphere', 'Magnetopause', 'Magnetosheath', 'Bow Shock', 'Solar Wind'])
cbar.set_label('Region')



plt.show()
