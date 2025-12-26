import cv2
import glob
import grouping as grp

def read_media(folder_path):
    IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
    images = {}
    for path_name in folder_path:
        timestamp = path_name.split("_")[2]  # '20251202160015'
        ext = path_name.lower()
        if ext.endswith(IMAGE_EXTS):
            img = cv2.imread(path_name)
            if img is None:
                print(f"Failed to read {path_name}")
                continue
            images[timestamp] = img

    return images


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_path = "F:/DCIM/DJI_001/*.*"
    image_paths = sorted(glob.glob(input_path))
    images, videos = read_media(image_paths)

    groups = grp.group_images_by_time(images, window_hours=6, window_minutes=1)
    print(f"Total groups formed: {len(groups)}")
    grp.save_groups_to_subfolders(groups, base_folder="./images")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
