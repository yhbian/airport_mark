# -*- coding: utf-8 -*-
import numpy as np
import glob
from traits.api import *
from traitsui.api import *
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene
import open3d as o3d
import os


class FieldViewer(HasTraits):

    def __init__(self, pcd_list):
        super(FieldViewer, self).__init__()
        self.pcd_list = pcd_list

    a = Range(700, 800, 1)
    plotbutton = Button("plot now")
    scene = Instance(MlabSceneModel, ())  # mayavi scene

    view = View(
        Item('plotbutton', show_label=False),
        VGroup(
            Item(name='scene',
                 editor=SceneEditor(scene_class=MayaviScene),  # config mayavi editor
                 resizable=True,
                 height=300,
                 width=350
                 ),
            Item('a')
        ),
        width=500, resizable=True, title="airport point cloud"
    )

    def _plotbutton_fired(self):
        # self.plot()
        self.plot_pc()

    def _a_changed(self):
        self.plot_pc()

    def plot_pc(self):
        frame_idx = self.a
        pcd_file = self.pcd_list[frame_idx]

        # load point clouds and convert into numpy.array
        points = o3d.io.read_point_cloud(pcd_file)
        points = np.array(points.points)

        # plot the scene
        x = points[:, 0]  # x position of point
        y = points[:, 1]  # y position of point
        z = points[:, 2]  # z position of point
        # r = lidar[:, 3]  # reflectance value of point
        d = np.sqrt(x ** 2 + y ** 2)  # Map Distance from sensor

        # fig = self.scene.mlab.figure(bgcolor=(0, 0, 0))
        self.scene.mlab.points3d(x, y, z,
                             d,
                             mode="point",
                             colormap='spectral',
                             )

        # lock the initial view point
        self.scene.mlab.view(azimuth=180, elevation=80, distance=40, focalpoint=(0, 0, 0))


if __name__ == '__main__':

    # acquire pcd_list
    dataset_path = '/home/mark/Airport/dataset'
    output_path = '/home/mark/Airport/frames'
    pcd_list = sorted(glob.glob(os.path.join(dataset_path, '*.pcd')))

    # initialize the iteration window with pcd_list
    app = FieldViewer(pcd_list=pcd_list)
    app.configure_traits()
