from datetime import datetime, timedelta
import os
import cv2

def group_images_by_time(image_dict, window_hours=4, window_minutes=30):
    """
    images: dict[timestamp_str -> image]
    timestamp_str format: YYYYMMDDHHMMSS
    """
    # Convert keys once and sort
    items = sorted(
        image_dict.items(),
        key=lambda x: datetime.strptime(x[0], "%Y%m%d%H%M%S")
    )

    groups = []
    current_group = [items[0][1]]
    prev_dt = datetime.strptime(items[0][0], "%Y%m%d%H%M%S")

    for ts, img in items[1:]:
        curr_dt = datetime.strptime(ts, "%Y%m%d%H%M%S")

        if curr_dt - prev_dt <= timedelta(hours=window_hours, minutes=window_minutes):
            current_group.append(img)
        else:
            groups.append(current_group)
            current_group = [img]

        prev_dt = curr_dt

    groups.append(current_group)
    return groups

def save_groups_to_subfolders(groups, base_folder="output_groups"):
    os.makedirs(base_folder, exist_ok=True)

    for i, group in enumerate(groups, 1):
        group_folder = os.path.join(base_folder, f"group_{i}")
        os.makedirs(group_folder, exist_ok=True)

        for j, img in enumerate(group, 1):
            # Save as "image_1.jpg", "image_2.jpg", etc.
            filename = os.path.join(group_folder, f"image_{j}.jpg")
            cv2.imwrite(filename, img)

        print(f"Saved group {i} with {len(group)} images to {group_folder}")