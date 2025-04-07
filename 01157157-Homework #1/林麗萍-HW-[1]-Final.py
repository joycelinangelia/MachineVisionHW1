from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings

# Function to configure ImageMagick (set to version 1.0.3)
def configure_imagemagick():
    # Set the ImageMagick binary path for version 1.0.3 (adjust if necessary)
    change_settings({"IMAGEMAGICK_BINARY": "magick"})
    print("✅ ImageMagick 1.0.3 configured.")

# ===========================
# Call the function to configure ImageMagick
# ===========================
configure_imagemagick()

# ===========================
# Load the video clip
# ===========================
video = VideoFileClip("林麗萍-HW.mp4")

# ===========================
# Create a label to add to the top-left corner of the video
# ===========================
label = TextClip("homework_1_test_video", fontsize=20, color='white', font="Arial")
label = label.set_position(("left", "top")).set_start(0).set_duration(video.duration)

label2 = TextClip("聖稜-雪山的脊樑", fontsize=20, color='white', font="SimHei")
label2 = label2.set_position(("center", "top")).set_start(0).set_duration(video.duration)

# ===========================
# Define the subtitles (this is your script)
# ===========================
subtitles = '''這個範例示範如何使用pyttsx3與MoviePy為視訊加上字幕、旁白、背景音樂
主要目的是示範一種讓字幕、旁白同步呈現的程式寫法
訣竅是先使用pyttsx3念每一句旁白
藉此計算每一句旁白的時間長度
並決定每一句旁白與字幕在視訊裡的開始時間與結束時間
然後用SubtitlesClip產生字幕
並用CompositeVideoClip混合字幕與來源視訊產生有字幕的目標視訊
接下來使用concatenate_audioclip
將每一句旁白依照已設定好開始時間與結束時間串接起來產生旁白音訊
再用CompositeAudioClip混合旁白音訊、背景音訊、背景音樂產生目標音訊
最後將目標視訊的音訊設定為目標音訊，並輸出至目標視訊檔即可'''

# Split the subtitles into lines
lines = [msg.strip() for msg in subtitles.split('\n') if len(msg) > 0]

# ===========================
# Create Subtitle Clips
# ===========================
subtitle_clips = []
start_time = 0
for idx, line in enumerate(lines):
    # Using a font that supports Mandarin, like 'SimHei'
    subtitle = TextClip(line, fontsize=24, color='white', font="SimHei", bg_color="black")
    subtitle = subtitle.set_position(("center", "bottom")).set_start(start_time).set_duration(5)  # Display each subtitle for 3 seconds
    subtitle_clips.append(subtitle)
    start_time += 5  # Adjust the start time for the next subtitle

# ===========================
# Combine video, label, and subtitles
# ===========================
final_clip = CompositeVideoClip([video, label] + subtitle_clips)

# ===========================
# Output the final video
# ===========================
final_clip.write_videofile("林麗萍-HW-[1]-Final.mp4", codec="libx264", audio=True, fps=24)
