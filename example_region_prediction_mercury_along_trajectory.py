#example region prediction along orbit trajectory 

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from region_prediction_mercury_simple import get_region
from matplotlib.colors import ListedColormap, BoundaryNorm

R_M = 2440 

#coordinates circle (spacecraft position 1)
r = 2 * R_M
#circle in x-z-plane
theta = np.linspace(0, 2*np.pi, 100)
x_circle = 1 + r*np.cos(theta) + 0.5*R_M
y_circle = np.zeros(len(theta))
z_circle = r*np.sin(theta)

#coordinates circle (spacecraft position 2) 
r2 = 2.5 * R_M
theta2 = np.linspace(0.5*np.pi, 2.5*np.pi, 100)
x_circle2 = 1 + r2*np.cos(theta2) + 0.8*R_M
y_circle2 = np.zeros(len(theta2))
z_circle2 = r2*np.sin(theta2)

region = get_region(x_circle, y_circle, z_circle, r_hel_AU = 0.38, di = 50, aberration_angle_deg = 0)
region2 = get_region(x_circle2, y_circle2, z_circle2, r_hel_AU = 0.38, di = 50, aberration_angle_deg = 0)


#find indices where region is the same
indices_same_region = np.where(region == region2)
#print('Indices where region is the same: ', indices_same_region)
#print('Number of indices where region is the same: ', len(indices_same_region[0]))

cmap = ListedColormap(['#808080', '#ADD8E6', '#00008B', '#90EE90', '#006400', '#FFFF00'])
norm = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], cmap.N)


# Plot region prediction along orbit trajectory
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# Left subplot: without red indication of same region
ax1.set_title('Region Estimation along Orbit Trajectory')
ax1.plot(x_circle/R_M, z_circle/R_M, 'k')
ax1.plot(x_circle2/R_M, z_circle2/R_M, 'red')

sc1 = ax1.scatter(x_circle/R_M, z_circle/R_M, c=region, cmap=cmap, norm=norm)
sc2 = ax1.scatter(x_circle2/R_M, z_circle2/R_M, c=region2, cmap=cmap, norm=norm)
ax1.set_xlabel('x in MSO in RM')
ax1.set_ylabel('z in MSO in RM')
ax1.grid()
ax1.set_xlim(4, -2)
ax1.set_ylim(-3, 3)
# Add grey circle for planet (r = 1RM)
circle1 = plt.Circle((0, 0), 1, color='lightgrey', fill=True)
ax1.add_artist(circle1)
# Equal axis
ax1.set_aspect('equal')

# Right subplot: with red indication of same region
ax2.set_title('Region Estimation - Same Region in Red')
ax2.plot(x_circle/R_M, z_circle/R_M, 'k')
ax2.plot(x_circle2/R_M, z_circle2/R_M, 'red')

#sc3 = ax2.scatter(x_circle/R_M, z_circle/R_M, c=region, cmap=cmap, norm=norm)
#sc4 = ax2.scatter(x_circle2/R_M, z_circle2/R_M, c=region2, cmap=cmap, norm=norm)
# Mark points in red where region is the same
ax2.scatter(x_circle[indices_same_region]/R_M, z_circle[indices_same_region]/R_M, c='red', label='SC1 + Sc2 in same region')
ax2.scatter(x_circle2[indices_same_region]/R_M, z_circle2[indices_same_region]/R_M, c='red')
ax2.set_xlabel('x in MSO in RM')
ax2.set_ylabel('z in MSO in RM')
ax2.grid()
ax2.set_xlim(4, -2)
ax2.set_ylim(-3, 3)
# Add grey circle for planet (r = 1RM)
circle2 = plt.Circle((0, 0), 1, color='lightgrey', fill=True)
ax2.add_artist(circle2)
# Equal axis
ax2.set_aspect('equal')

# Add colorbar
cbar = fig.colorbar(sc2, ax=[ax1, ax2], orientation='horizontal', pad=0.1, ticks=[1, 2, 3, 4, 5, 6])
cbar.set_label('Region')
# Description of regions for colorbar
cbar.set_ticklabels(['Inside Planet', 'Magnetosphere', 'Magnetopause', 'Magnetosheath', 'Bowshock', 'Solar Wind'])


#plot region prediction as timeline 
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize = (10, 8))
plt.suptitle('Region Estimation for two spacecrafts')
ax1.plot(x_circle/R_M, 'g--', label = 'x of sc1')
ax1.plot(y_circle/R_M, 'r--', label = 'y of sc1')
ax1.plot(z_circle/R_M, 'b--', label = 'z of sc1')
ax2.plot(x_circle2/R_M, 'g:', label = 'x of sc2')
ax2.plot(y_circle2/R_M, 'r:', label = 'y of sc2')
ax2.plot(z_circle2/R_M, 'b:', label = 'z of sc2')
ax1.set_ylabel('Pos S/C1 in MSO in RM')
ax2.set_ylabel('Pos S/C2 in MSO in RM')
ax1.legend(loc = 'upper right')
ax2.legend(loc = 'upper right')
ax1.grid()
ax2.grid()
ax3.plot(region, 'k', label = 'Region Prediction S/C1')
ax3.set_ylabel('Region')
#set labels on y axis: 
ax3.set_yticks([1, 2, 3, 4, 5, 6])
ax3.set_yticklabels(['Inside Planet', 'Magnetosphere', 'Magnetopause', 'Magnetosheath', 'Bowshock', 'Solar Wind'])
ax3.legend(loc = 'upper right')
ax4.plot(region2, 'k', label = 'Region Prediction S/C2')
ax4.set_ylabel('Region')
#set labels on y axis:
ax4.set_yticks([1, 2, 3, 4, 5, 6])
ax4.set_yticklabels(['Inside Planet', 'Magnetosphere', 'Magnetopause', 'Magnetosheath', 'Bowshock', 'Solar Wind'])
ax4.legend(loc = 'upper right')
ax4.set_xlabel('Time')
plt.tight_layout()
#mark background light grey when regions are the same
for i in range(len(indices_same_region[0])):
    ax3.axvspan(indices_same_region[0][i], indices_same_region[0][i] + 1, color = 'lightgrey', alpha = 0.5, label = 'same Region')
    ax4.axvspan(indices_same_region[0][i], indices_same_region[0][i] + 1, color = 'lightgrey', alpha = 0.5, label = 'same Region')
plt.show()


