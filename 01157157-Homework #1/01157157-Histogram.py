import cv2
import numpy as np
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
# Apply Histogram Equalization to V channel (Brightness) in HSV space
# ======================
def histogram_equalization_v(frame):
    # Convert the frame from BGR to HSV using OpenCV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Split the HSV image into H, S, V channels
    h, s, v = cv2.split(hsv_frame)
    
    # Apply histogram equalization to the V (value) channel
    v_equalized = cv2.equalizeHist(v)
    
    # Merge the equalized V channel back with the original H and S channels
    hsv_equalized = cv2.merge([h, s, v_equalized])
    
    # Convert the result back to BGR color space for display
    bgr_equalized = cv2.cvtColor(hsv_equalized, cv2.COLOR_HSV2BGR)
    
    return bgr_equalized

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
def add_text_to_video(clip, text="Histogram Equalization of V by PyTorch"):
    text_clip = (TextClip(text, fontsize=20, font="Arial", color="white")
                 .set_position(("left", "top"))
                 .set_start(0)
                 .set_duration(clip.duration))
    
    return CompositeVideoClip([clip, text_clip])

# ======================
# Final Video Assembly
# ======================
def create_histogram_equalized_video():
    configure_imagemagick()

    input_video = "聖稜-雪山的脊樑.mp4"  # The input video name
    processed_clip = process_video(input_video, histogram_equalization_v)

    # Add the text "Histogram Equalization of V by PyTorch" to the top-left corner of the video
    processed_clip_with_text = add_text_to_video(processed_clip)

    output_name = "01157157-Histogram.mp4"  # Updated output file name
    processed_clip_with_text.write_videofile(output_name, codec="libx264", audio=False, fps=24)
    print(f"🎉 Video saved as {output_name}")

# ======================
# Entry Point
# ======================
if __name__ == "__main__":
    create_histogram_equalized_video()
