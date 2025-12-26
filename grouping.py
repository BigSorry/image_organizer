from datetime import datetime, timedelta
import os
import cv2

def group_images_by_time(images_dict, window_hours=4, window_minutes=30):
    """
    images_dict: dict[timestamp_str -> OpenCV image]
    Returns: list of groups, each group is list of (timestamp, image)
    """
    # Sort items by timestamp
    items = sorted(images_dict.items(), key=lambda x: datetime.strptime(x[0], "%Y%m%d%H%M%S"))

    groups = []
    current_group = [items[0]]  # (timestamp, image)
    prev_dt = datetime.strptime(items[0][0], "%Y%m%d%H%M%S")

    for ts, img in items[1:]:
        curr_dt = datetime.strptime(ts, "%Y%m%d%H%M%S")

        if curr_dt - prev_dt <= timedelta(hours=window_hours, minutes=window_minutes):
            current_group.append((ts, img))
        else:
            groups.append(current_group)
            current_group = [(ts, img)]
        prev_dt = curr_dt

    groups.append(current_group)
    return groups

def save_groups_to_subfolders(groups, base_folder="output_groups"):
    """
    groups: list of groups, each group is list of (timestamp, OpenCV image)
    Saves each image in a subfolder named after the group index, using the timestamp as filename.
    """
    os.makedirs(base_folder, exist_ok=True)

    for i, group in enumerate(groups, 1):
        group_folder = os.path.join(base_folder, f"group_{i}")
        os.makedirs(group_folder, exist_ok=True)

        for ts_str, img in group:
            # Save using timestamp as filename
            dt = datetime.strptime(ts_str, "%Y%m%d%H%M%S")
            readable_ts = dt.strftime("%d-%m-%Y_%H-%M-%S")
            cv2.imwrite(readable_ts, img)

        print(f"Saved group {i} with {len(group)} images to {group_folder}")