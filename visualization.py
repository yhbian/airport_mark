import numpy as np
import open3d as o3d
# import moviepy.editor as mpy
import mayavi.mlab as mlab


def viz_mayavi(points, vals="distance", viz=True, azimuth=None, elevation=None, distance=None, focalpoint=None):
    x = points[:, 0]  # x position of point
    y = points[:, 1]  # y position of point
    z = points[:, 2]  # z position of point
    # r = lidar[:, 3]  # reflectance value of point
    d = np.sqrt(x ** 2 + y ** 2)  # Map Distance from sensor

    # Plot using mayavi -Much faster and smoother than matplotlib

    if vals == "height":
        col = z
    else:
        col = d

    fig = mlab.figure(bgcolor=(0, 0, 0), size=(640, 640))
    mlab.points3d(x, y, z,
                         col,          # Values used for Color
                         mode="point",
                         colormap='spectral', # 'bone', 'copper', 'gnuplot'
                         # color=(0, 1, 0),   # Used a fixed (r,g,b) instead
                         figure=fig,
                         )
    mlab.view(azimuth=azimuth, elevation=elevation, distance=distance, focalpoint=focalpoint)

    if viz:
        # set visualization view
        # azimuth (0-360), elevation(0-180)
        mlab.show()
    else:
        return mlab


def make_frame(t):
    r"""
    :param t: time parameter, frame
    :return: the t-th frame of the animation
    """
    # acquire pcd fime according to the given frame index t
    start_frame = 300
    if int(start_frame + 10 * t) < 10:
        pcd_path = '/home/mark/Airport/dataset/Benewake_Horn_X2_PointCloud_000{0}.pcd'.format(str(start_frame + int(10 * t)))
    elif int(start_frame + 10 * t) < 100:
        pcd_path = '/home/mark/Airport/dataset/Benewake_Horn_X2_PointCloud_00{0}.pcd'.format(str(start_frame + int(10 * t)))
    else:
        pcd_path = '/home/mark/Airport/dataset/Benewake_Horn_X2_PointCloud_0{0}.pcd'.format(str(start_frame + int(10 * t)))
    print(pcd_path)
    # load pcd file and visualization
    points = o3d.io.read_point_cloud(pcd_path)
    points_np = np.array(points.points)
    mlab = viz_mayavi(points_np, vals="distance", viz=False)

    # crucial
    f = mlab.gcf()
    f.scene._lift()
    return mlab.screenshot()


if __name__ == '__main__':
    # duration = 2
    # animation = mpy.VideoClip(make_frame, duration=duration)
    # animation.write_gif("point_test.gif", fps=5)
    # TODO: keep the camera view when frame goes from 0 to 1, mayavi view matrix
    # initialize a view and then generate a movie according to the view
    pcd = '/home/mark/Airport/dataset/Benewake_Horn_X2_PointCloud_0010.pcd'
    points = o3d.io.read_point_cloud(pcd)
    points = np.array(points.points)
    viz_mayavi(points, vals="distance", viz=True, azimuth=180, elevation=80, distance=40, focalpoint=(0, 0, 0))

    # np.savetxt('/home/mark/Airport/dataset/Benewake_Horn_X2_PointCloud_0002.csv', points_np)
    # viz_mayavi(points_np)
