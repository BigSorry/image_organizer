import cv2
import glob
import grouping as grp

def read_media(folder_path, store_path=True):
    IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
    images = {}
    for path_name in folder_path:
        str_split = path_name.split("_")
        # TODO this works only for phone images named like IMG_20251202_160015.jpg
        date = str_split[3]
        time = str_split[4]
        timestamp = date + time[:6]

        ext = path_name.lower()
        if ext.endswith(IMAGE_EXTS):
            if store_path:
                images[timestamp] = path_name
            else:
                img = cv2.imread(path_name)
                if img is None:
                    print(f"Failed to read {path_name}")
                    continue
                images[timestamp] = img

    return images


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_path = "F:/DCIM/DJI_001/*.*"
    input_path = "C:/Users/Lex/Desktop/china_vakantie_2025/phone/images/*.jpg"
    image_paths = sorted(glob.glob(input_path))

    if image_paths:
        images = read_media(image_paths, store_path=True)
        groups = grp.group_images_by_time(images, window_hours=6, window_minutes=1)
        print(f"Total groups formed: {len(groups)}")
        for i, group in enumerate(groups):
            grp.save_group_image(group, base_folder=f"./images/group{i}/")
            print(f"Saved group {i} with {len(group)} images.")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
