from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings

# ======================
# Configure ImageMagick
# ======================
def configure_imagemagick():
    change_settings({"IMAGEMAGICK_BINARY": "magick"})
    print("✅ ImageMagick 1.0.3 configured.")

# Call the function to configure ImageMagick
configure_imagemagick()

# Load the video clip
video = VideoFileClip("聖稜-雪山的脊樑.mp4")

# Create the label for the top-left corner
label2 = TextClip("聖稜-雪山的脊樑", fontsize=20, color='white', font="SimHei")
label2 = label2.set_position(("left", "top")).set_start(0).set_duration(video.duration)

# Combine the video and the label
final_clip = CompositeVideoClip([video, label2])

# Output the final video
final_clip.write_videofile("聖稜-雪山的脊樑labeled.mp4", codec="libx264", audio=True, fps=24)
