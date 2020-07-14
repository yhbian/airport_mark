import matplotlib.pyplot as plt
import open3d as o3d
import glob
import os
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# TODO: this file try to visualize the pc and save as png using matplotlib


output_path = '/home/mark/Airport/frames'

# acquire a pcd file path
dataset_path = '/home/mark/Airport/dataset'
pcd_list = sorted(glob.glob(os.path.join(dataset_path, '*.pcd')))
idx = 122
pcd_file = pcd_list[idx]

# get point clouds (numpy)
points = o3d.io.read_point_cloud(pcd_file)
points = np.array(points.points)

# plot with plt and mpl_toolkits
fig = plt.figure()
ax = Axes3D(fig)

# setting point-wise colors
colors = points[:, 3:]/255  # RGBA(0-1)

ax.scatter(points[:, 0], points[:, 1], points[:, 2],
           cmap='spectral',
           # c=colors,
           s=0.5,
           linewidth=0,
           alpha=1,
           marker=".")

plt.title('Point Cloud')
ax.axis('scaled')  # {equal, scaled}
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
