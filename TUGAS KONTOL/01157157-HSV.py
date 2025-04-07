import cv2
import numpy as np
import torch
from moviepy.editor import (
    VideoFileClip, ImageSequenceClip,
    TextClip, CompositeVideoClip
)
from moviepy.config import change_settings

# ======================
# Configure ImageMagick
# ======================
def configure_imagemagick():
    change_settings({"IMAGEMAGICK_BINARY": "magick"})
    print("✅ ImageMagick 1.0.3 configured.")

# ======================
# Convert to HSV color space using PyTorch
# ======================
def convert_to_hsv_torch(frame):
    # Convert the frame from BGR to HSV using OpenCV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return hsv_frame

# ======================
# Process video frames
# ======================
def process_video(input_path, operation):
    clip = VideoFileClip(input_path).without_audio()
    frames = []

    for frame in clip.iter_frames(fps=24, dtype='uint8'):
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        processed = operation(frame_bgr)
        processed_rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
        frames.append(processed_rgb)

    return ImageSequenceClip(frames, fps=24)

# ======================
# Add text to the top-left corner of the video
# ======================
def add_text_to_video(clip, text="HSV color space by PyTorch"):
    text_clip = (TextClip(text, fontsize=20, font="Arial", color="white")
                 .set_position(("left", "top"))
                 .set_start(0)
                 .set_duration(clip.duration))
    
    return CompositeVideoClip([clip, text_clip])

# ======================
# Final Video Assembly
# ======================
def create_hsv_video():
    configure_imagemagick()

    input_video = "homework_1_test_video.mp4"
    processed_clip = process_video(input_video, convert_to_hsv_torch)

    # Add the text "HSV by PyTorch" to the top-left corner of the video
    processed_clip_with_text = add_text_to_video(processed_clip)

    output_name = "01157157-HSV.mp4"  # Updated file name
    processed_clip_with_text.write_videofile(output_name, codec="libx264", audio=False, fps=24)
    print(f"🎉 Video saved as {output_name}")

# ======================
# Entry Point
# ======================
if __name__ == "__main__":
    create_hsv_video()
