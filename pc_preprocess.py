r"""
This file try to exclude *ground points* and *building points* from a reasonable margin
"""
import numpy as np


def process(pc, x_margin=-1000, y_margin=-5, z_margin=1):
    r"""
    :param pc: list of numpy.array point cloud with world axis
    :param x_margin: if x <= x_margin, exclude
    :param y_margin: if y <= y_margin, exclude
    :param z_margin: if z <= z_margin, exclude, for ground points
    :return: processed data
    """
    new_pc = []
    num_points = len(pc)

    # for point in pc:
    #     if point[0] > x_margin and point[1] > y_margin and point[2] > z_margin:
    #         new_pc.append(point)

    for idx in range(num_points):
        if pc[idx][0] > x_margin and pc[idx][1] > y_margin and pc[idx][2] > z_margin:
            new_pc.append(pc[idx])

    new_pc = np.array(new_pc)
    return new_pc
