import cv2
import glob
import os
import grouping as grp

def read_frames(path, frame_step=5, frame_index=0):
    frames = []
    cap = cv2.VideoCapture(path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_index % frame_step == 0:
            frames.append(frame)  # save frame here

        frame_index += 1
    cap.release()

    return frames

def read_media(folder_path):
    VIDEO_EXTS = (".mp4", ".avi", ".mov", ".mkv")
    videos = {}
    for path_name in folder_path:
        ext = path_name.lower()
        if ext.endswith(VIDEO_EXTS):
            timestamp = path_name.split("_")[2]  # '20251202160015'
            frames = read_frames(path_name, frame_step=25)
            if frames:
                videos[timestamp] = frames

    return videos


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_path = "F:/DCIM/DJI_001/*.*"
    vid_paths = sorted(glob.glob(input_path))
    vid_short_paths = vid_paths[:10]
    videos = read_media(vid_short_paths)

    groups = grp.group_images_by_time(videos, window_hours=6, window_minutes=1)
    print(f"Total groups formed: {len(groups)}")
    grp.save_groups_to_subfolders(groups, base_folder="./videos")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
