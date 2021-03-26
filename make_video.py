import os
import cv2
import time
import numpy as np
from tqdm import tqdm


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


def video2frames(video_path, idx):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"please check the existence of the source video {idx}!")

    frames = []
    input_movie = cv2.VideoCapture(video_path)

    # convert video to frame list 
    while True:
        ret, frame = input_movie.read()
        if not ret:
            break
        frames.append(frame)

    input_movie.release()
    cv2.destroyAllWindows()
    return frames


def concate_videos(video1, video2, output_file, fps=25):
    # convert to valid frames
    frames1, frames2 = video2frames(video1, 1), video2frames(video2, 2)
    assert len(frames1) * len(frames2)

    # get shape
    shape1, shape2 = frames1[0].shape, frames2[0].shape
    assert frames1[0].shape == frames2[0].shape
    h, w = shape1[0], shape1[1]

    if len(frames1) < len(frames2):
        num_frames = len(frames1)
    else:
        num_frames = len(frames2)

    # init writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v") # *"MJPG" should save as .avi 
    writer = cv2.VideoWriter(output_file,
                             fourcc,
                             fps, # fps
                             (w * 2, h)
                             ) # resolution
    # make video
    i = 0
    pbar = tqdm(total=num_frames)
    print("Generating video ...")
    while i < num_frames:
        cated = np.hstack((frames1[i], frames2[i]))
        cv2.waitKey(1)
        writer.write(cated)
        i += 1
        pbar.update(1)
    
    writer.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Input videos information.')
    parser.add_argument('--video', type=str)
    parser.add_argument('--root', type=str, default='')
    parser.add_argument('--model1', type=str, default='')
    parser.add_argument('--model2', type=str, default='')
    parser.add_argument('--fps', type=int, default=25)
    args = parser.parse_args()

    video1 = os.path.join(args.root, args.model1) + '/' + args.video
    video2 = os.path.join(args.root, args.model2) + '/' + args.video
    output_file = 'stacked_' + args.video
    concate_videos(video1, video2, output_file, args.fps)
