import matplotlib.pyplot as plt
import cv2

def plot_image_groups(groups):
    for i, group in enumerate(groups, 1):
        plt.figure(figsize=(4 * len(group), 4))

        for idx, img in enumerate(group, 1):
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            plt.subplot(1, len(group), idx)
            plt.imshow(img_rgb)
            plt.axis("off")

        plt.suptitle(f"Group {i}")
        plt.show()