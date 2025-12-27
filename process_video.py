import cv2
import av
import glob
import os
import grouping as grp

def save_video_from_dict(videos, output_path="output.mp4", fps=30):
    """
    videos: dict of {timestamp: list_of_frames}
    Saves all frames from all videos in chronological order.
    """
    # Flatten frames and preserve order by timestamp
    all_frames = []
    for timestamp in sorted(videos.keys()):
        all_frames.extend(videos[timestamp])

    if not all_frames:
        print("No frames to save!")
        return

    height, width, _ = all_frames[0].shape

    # Open output container
    container = av.open(output_path, mode="w")

    # Add H.264 video stream
    stream = container.add_stream("libx264", rate=fps)
    stream.width = width
    stream.height = height
    stream.pix_fmt = "yuv420p"

    # Encode frames
    for img in all_frames:
        frame = av.VideoFrame.from_ndarray(img, format="bgr24")
        packet = stream.encode(frame)
        if packet:
            container.mux(packet)

    # Flush encoder
    packet = stream.encode(None)
    if packet:
        container.mux(packet)

    container.close()
    print(f"Saved video to {output_path}")

def read_frames(path, width=160, height=90):
    frames = []

    container = av.open(path)
    stream = container.streams.video[0]
    stream.skip_frame = "NONKEY" # decode I-frames only
    stream.thread_type = "AUTO"  # enable multi-threaded decoding

    for frame in container.decode(video=0):
        # frame is guaranteed to be a keyframe (I-frame)
        img = frame.reformat(
            width=width,
            height=height,
            format="bgr24"
        ).to_ndarray()

        frames.append(img)

    return frames

def read_media(folder_path):
    VIDEO_EXTS = (".mp4", ".avi", ".mov", ".mkv")
    videos = {}
    for path_name in folder_path:
        ext = path_name.lower()
        if ext.endswith(VIDEO_EXTS):
            timestamp = path_name.split("_")[2]  # '20251202160015'
            frames = read_frames(path_name)
            print(f"Read {len(frames)} frames from {path_name}")
            if frames:
                videos[timestamp] = frames

    return videos


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_path = "F:/DCIM/DJI_001/*.*"
    vid_paths = sorted(glob.glob(input_path))
    vid_short_paths = vid_paths[:10]
    videos = read_media(vid_short_paths)


    #groups = grp.group_images_by_time(videos, window_hours=6, window_minutes=1)
    save_video_from_dict(videos, "./videos/combined_output.mp4", fps=30)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
