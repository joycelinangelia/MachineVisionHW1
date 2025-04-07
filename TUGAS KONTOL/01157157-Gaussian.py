import cv2
import numpy as np
import torch
import torch.nn.functional as F
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
# Gaussian Blur using PyTorch (Full Frame)
# ======================
def gaussian_blur_torch(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = gray.astype(np.float32) / 255.0

    # Convert to a 4D tensor for convolution (N, C, H, W)
    tensor = torch.tensor(gray[None, None, :, :], dtype=torch.float32)

    kernel = torch.tensor([[1, 4, 6, 4, 1],
                           [4, 16, 24, 16, 4],
                           [6, 24, 36, 24, 6],
                           [4, 16, 24, 16, 4],
                           [1, 4, 6, 4, 1]], dtype=torch.float32)
    kernel = kernel / kernel.sum()  # Normalize the kernel
    kernel = kernel[None, None, :, :]

    # Perform 2D convolution (without padding)
    blurred = F.conv2d(tensor, kernel, padding=2)

    # Convert the tensor back to a numpy array
    blurred = blurred.squeeze().cpu().numpy() * 255
    blurred = blurred.astype(np.uint8)

    # Convert the result back to BGR color space
    blurred_bgr = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)

    return blurred_bgr

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
# Optional Subtitles
# ======================
def generate_subtitles(duration):
    subtitles = [
        {"start": 0, "end": 4, "text": "這是第一行字幕"},
        {"start": 5, "end": 8, "text": "這是第二行字幕"},
        {"start": 9, "end": 12, "text": "這是第三行字幕"},
    ]

    subtitle_clips = []
    for sub in subtitles:
        clip = (TextClip(sub["text"], fontsize=40, font="Arial-Bold",
                         color='white', stroke_color='black', stroke_width=2)
                .set_position(("center", "bottom"))
                .set_start(sub["start"])
                .set_duration(sub["end"] - sub["start"]))
        subtitle_clips.append(clip)

    return subtitle_clips

# ======================
# Add text to the top-left corner of the video
# ======================
def add_text_to_video(clip, text="Gaussian by PyTorch"):
    text_clip = (TextClip(text, fontsize=20, font="Arial", color="white")
                 .set_position(("left", "top"))
                 .set_start(0)
                 .set_duration(clip.duration))
    
    return CompositeVideoClip([clip, text_clip])

# ======================
# Final Video Assembly
# ======================
def create_clean_gaussian_video():
    configure_imagemagick()

    input_video = "homework_1_test_video.mp4"
    processed_clip = process_video(input_video, gaussian_blur_torch)

    # Add the text "Gaussian by PyTorch" to the top-left corner of the video
    processed_clip_with_text = add_text_to_video(processed_clip)

    output_name = "01157157-Gaussian.mp4"  # Updated file name
    processed_clip_with_text.write_videofile(output_name, codec="libx264", audio=False, fps=24)
    print(f"🎉 Video saved as {output_name}")

# ======================
# Entry Point
# ======================
if __name__ == "__main__":
    create_clean_gaussian_video()
