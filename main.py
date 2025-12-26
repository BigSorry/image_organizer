import cv2
import glob
import os
import grouping as grp
import plot

def read_frames(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        return []

    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()
    return frames

def read_media(folder_path, image_only=True):
    IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
    VIDEO_EXTS = (".mp4", ".avi", ".mov", ".mkv")
    images = {}
    videos = []
    for path_name in folder_path:
        timestamp = path_name.split("_")[2]  # '20251202160015'
        ext = path_name.lower()
        if ext.endswith(IMAGE_EXTS):
            img = cv2.imread(path_name)
            if img is None:
                print(f"Failed to read {path_name}")
                continue
            images[timestamp] = img
        elif ext.endswith(VIDEO_EXTS) and image_only is False:
            frames = read_frames(path_name)
            if frames:
                videos.append(frames)

    return images, videos


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_path = "F:/DCIM/DJI_001/*.*"
    image_paths = sorted(glob.glob(input_path))
    image_paths = image_paths[:10]
    images, videos = read_media(image_paths, image_only=True)

    groups = grp.group_images_by_time(images, window_hours=6, window_minutes=1)
    print(f"Total groups formed: {len(groups)}")
    #grp.save_groups_to_subfolders(groups, base_folder="./images")
    print(images, videos)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
