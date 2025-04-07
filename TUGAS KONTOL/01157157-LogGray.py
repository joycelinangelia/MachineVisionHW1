import cv2
import numpy as np
from moviepy.editor import (
    VideoFileClip, ImageSequenceClip,
    TextClip, CompositeVideoClip
)
from moviepy.config import change_settings

# ======================
# Configure ImageMagick (Optional)
# ======================
def configure_imagemagick():
    change_settings({"IMAGEMAGICK_BINARY": "magick"})
    print("✅ ImageMagick 1.0.3 configured.")

# ======================
# Apply Logarithmic Transformation to V channel
# ======================
def log_gray_level_mapping_v(frame, c=255):
    # Convert the frame from BGR to HSV using OpenCV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Split the HSV image into H, S, V channels
    h, s, v = cv2.split(hsv_frame)
    
    # Apply log transformation to the V (value) channel
    v_log = c * np.log(1 + v)
    v_log = np.clip(v_log, 0, 255).astype(np.uint8)  # Ensure the values are in the valid range
    
    # Merge the transformed V channel back with the original H and S channels
    hsv_log = cv2.merge([h, s, v_log])
    
    # Convert the result back to BGR color space for display
    bgr_log = cv2.cvtColor(hsv_log, cv2.COLOR_HSV2BGR)
    
    return bgr_log

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
def add_text_to_video(clip, text="Log Gray Level Mapping of V"):
    text_clip = (TextClip(text, fontsize=20, font="Arial", color="white")
                 .set_position(("left", "top"))
                 .set_start(0)
                 .set_duration(clip.duration))
    
    return CompositeVideoClip([clip, text_clip])

# ======================
# Final Video Assembly
# ======================
def create_log_gray_level_mapped_video():
    configure_imagemagick()

    input_video = "聖稜-雪山的脊樑.mp4"  # The input video name
    processed_clip = process_video(input_video, log_gray_level_mapping_v)

    # Add the text "Log Gray Level Mapping of V" to the top-left corner of the video
    processed_clip_with_text = add_text_to_video(processed_clip)

    output_name = "01157157-LogGray.mp4"  # Updated output file name
    processed_clip_with_text.write_videofile(output_name, codec="libx264", audio=False, fps=24)
    print(f"🎉 Video saved as {output_name}")

# ======================
# Entry Point
# ======================
if __name__ == "__main__":
    create_log_gray_level_mapped_video()
