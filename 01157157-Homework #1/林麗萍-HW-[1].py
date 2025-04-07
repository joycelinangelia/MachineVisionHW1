from moviepy.editor import VideoFileClip, clips_array, CompositeAudioClip, vfx

# ===========================
# Load the 6 video clips
# ===========================
video1 = VideoFileClip("homework_1_test_video.mp4")
video2 = VideoFileClip("01157157-Gaussian.mp4")
video3 = VideoFileClip("01157157-HSV.mp4")
video4 = VideoFileClip("聖稜-雪山的脊樑labeled.mp4")  # Replace with actual filenames
video5 = VideoFileClip("01157157-Histogram.mp4")  # Replace with actual filenames
video6 = VideoFileClip("01157157-LogGray.mp4")  # Replace with actual filenames

# ===========================
# Resize videos to fit in the grid (optional)
# ===========================
video_width = 640  # You can set the size of each video in the grid
video_height = 360  # Adjust the size accordingly

video1_resized = video1.resize(newsize=(video_width, video_height))
video2_resized = video2.resize(newsize=(video_width, video_height))
video3_resized = video3.resize(newsize=(video_width, video_height))
video4_resized = video4.resize(newsize=(video_width, video_height))
video5_resized = video5.resize(newsize=(video_width, video_height))
video6_resized = video6.resize(newsize=(video_width, video_height))

# ===========================
# Arrange the clips in a 2x3 grid (2 rows and 3 columns)
# ===========================
final_clip = clips_array([[video1_resized, video2_resized, video3_resized],
                          [video4_resized, video5_resized, video6_resized]])

# ===========================
# Get audio from both video files
# ===========================
background_audio1 = VideoFileClip("homework_1_test_video_subtitle.mp4").audio
background_audio2 = VideoFileClip("calm background for video 121519.mp4").audio

# ===========================
# Set the start time for the second audio track
# ===========================
background_audio2 = background_audio2.set_start(background_audio1.duration)

# ===========================
# Combine the two audio tracks using CompositeAudioClip
# ===========================
combined_audio = CompositeAudioClip([background_audio1, background_audio2])

# ===========================
# Ensure the video duration matches the audio length
# ===========================
final_audio_duration = combined_audio.duration
final_clip_duration = final_clip.duration

if final_clip_duration < final_audio_duration:
    # Ensure that the video loops seamlessly by trimming the last frame to remove the gap
    video_to_loop = final_clip.subclip(0, final_clip_duration)  # Trim the last frame if necessary
    final_clip = video_to_loop.fx(vfx.loop, duration=final_audio_duration)
# ===========================
# Set the combined audio for the final video
# ===========================
final_clip = final_clip.set_audio(combined_audio)
final_clip = final_clip.subclip(0, 61)  # ⏱️ Trim to 1 minute 1 second

# ===========================
# Output the final video as 林麗萍-HW.mp4
# ===========================
final_clip.write_videofile("林麗萍-HW.mp4", codec="libx264", audio=True, fps=24)
