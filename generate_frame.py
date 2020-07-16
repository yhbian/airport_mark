import numpy as np
import open3d as o3d
import glob
import mayavi.mlab as mlab
import os
from tqdm import tqdm
import visualization
from pc_preprocess import process


def generate_frames(pcd_list, output_dir, azimuth=None, elevation=None, distance=None, focalpoint=None):
    r"""
    :param pcd_list: pcd file list
    :param output_dir: output_dir of generated frame
    :param azimuth: azimuth angle in range 0-360
    :param elevation: elevation angle in range 0-180
    :param distance: distance frame view point to object
    :param focalpoint: focal point of the camera
    # four last params provide camera view, we generate frames according to the camera view
    """
    for pcd_file in tqdm(pcd_list):
        points = o3d.io.read_point_cloud(pcd_file)
        points_np = np.array(points.points)

        # if process is needed
        points_np = process(points_np)

        mlab = visualization.viz_mayavi(points_np, vals="distance", viz=False,
                                        azimuth=azimuth, elevation=elevation, distance=distance, focalpoint=focalpoint)

        # save the file
        filename = os.path.join(output_dir, pcd_file.split('/')[-1][:-4] + '.png')
        mlab.savefig(filename=filename)


def generate_one_frame(pcd_file, output_dir, azimuth=None, elevation=None, distance=None, focalpoint=None):
    points = o3d.io.read_point_cloud(pcd_file)
    points_np = np.array(points.points)
    mlab = visualization.viz_mayavi(points_np, vals="distance", viz=False,
                                        azimuth=azimuth, elevation=elevation, distance=distance, focalpoint=focalpoint)

    # save the file
    filename = os.path.join(output_dir, pcd_file.split('/')[-1][:-4] + '.png')
    mlab.savefig(filename=filename)


def batch_generate_frames(pcd_list, output_path, start_frame, end_frame, view_dict):
    for i in range(100):
        if start_frame + (i + 1) * 20 < end_frame:
            batch = pcd_list[start_frame + i * 20: start_frame + (i + 1) * 20]
            generate_frames(batch, output_path,
                            azimuth=view_dict['azimuth'],
                            elevation=view_dict['elevation'],
                            distance=view_dict['distance'],
                            focalpoint=view_dict['focal_point'])


if __name__ == '__main__':
    dataset_path = '/home/mark/Airport/dataset'
    output_path = '/home/mark/Airport/frames/projection_view_3'
    pcd_list = sorted(glob.glob(os.path.join(dataset_path, '*.pcd')))

    # generate png according to list
    start_frame = 700

    # initialize view
    default_view_dict = {'azimuth': 180, 'elevation': 80, 'distance': 40, 'focal_point': (0, 0, 0)}
    projection_1_view_dict = {'azimuth': 180, 'elevation': 90, 'distance': 40, 'focal_point': (0, 0, 0)}
    projection_2_view_dict = {'azimuth': 180, 'elevation': 0, 'distance': 150, 'focal_point': (50, 0, 100)}
    projection_3_view_dict = {'azimuth': 270, 'elevation': 90, 'distance': 200, 'focal_point': (50, 0, 0)}

    # generate frames
    view_dict = projection_3_view_dict
    batch_generate_frames(pcd_list, output_path, start_frame, len(pcd_list), view_dict)

    # generate png according to a single file
    # idx = 10
    # pcd_file = pcd_list[idx]
    # generate_one_frame(pcd_file, output_path)

