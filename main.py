import cv2
import glob
import os

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
    images = []
    videos = []
    for name in folder_path:
        ext = name.lower()
        if ext.endswith(IMAGE_EXTS):
            img = cv2.imread(name)
            if img is None:
                print(f"Failed to read {name}")
                continue
            images.append(img)
        elif ext.endswith(VIDEO_EXTS) and image_only is False:
            frames = read_frames(name)
            if frames:
                videos.append(frames)

    return images, videos


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_path = "F:/DCIM/DJI_001/*.*"
    image_paths = sorted(glob.glob(input_path))
    image_paths = image_paths[:10]
    images, videos = read_media(image_paths)
    print(images, videos)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
