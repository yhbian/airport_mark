import os
import cv2
import time

# make video from images


def pic2video(path, size):
    r"""
    :param path: file path
    :param size: image_size
    :return:
    """
    # acquire all files in the path
    filelist = sorted(os.listdir(path))[700:]

    # fps means how many pictures written into the video
    fps = 12

    # output_dir
    output_dir = r"/home/mark/Airport/video" + str(int(time.time())) + ".mp4"

    # different video has different encoding, e.g. 'I','4','2','0' is .avi
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    video = cv2.VideoWriter(output_dir, fourcc, fps, size)

    for item in filelist:
        # whether the file ends with .png
        if item.endswith('.png'):
            item = path + '/' + item
            # read with opencv, channels=BGR, 0-255
            img = cv2.imread(item)
            # write the image into the video
            video.write(img)

    video.release()


if __name__ == '__main__':
    pic2video(r'/home/mark/Airport/frames', size=(640, 587))
