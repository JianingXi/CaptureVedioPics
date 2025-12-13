import subprocess
import os

# ===================================
# 配置
# ===================================
input_video = r"C:\MyDocument\ToDoList\D20_DoingPlatform\D20251119_关于开展中国医学教育课程思政案例库案例征集活动的通知\附件\课堂实录节选.mp4"
output_video = r"C:\MyDocument\ToDoList\D20_DoingPlatform\D20251119_关于开展中国医学教育课程思政案例库案例征集活动的通知\附件\课堂实录节选_750MB_高画质.mp4"

target_size_mb = 750      # 目标体积
audio_bitrate = 160       # kbps
ffmpeg = "ffmpeg"
ffprobe = "ffprobe"

# ===================================
# 获取时长
# ===================================
def get_duration(path):
    cmd = [
        ffprobe, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

duration = get_duration(input_video)

# ===================================
# 反算视频码率
# ===================================
target_bits = target_size_mb * 1024 * 1024 * 8
audio_bits = audio_bitrate * 1000 * duration
video_bitrate = int((target_bits - audio_bits) / duration / 1000)

print(f"🎯 使用视频码率 ≈ {video_bitrate} kbps")

# ===================================
# Pass 1
# ===================================
subprocess.run([
    ffmpeg, "-y",
    "-i", input_video,
    "-c:v", "libx264",
    "-preset", "veryslow",
    "-b:v", f"{video_bitrate}k",
    "-pass", "1",
    "-an",
    "-f", "mp4",
    "NUL"
])

# ===================================
# Pass 2
# ===================================
subprocess.run([
    ffmpeg, "-y",
    "-i", input_video,
    "-c:v", "libx264",
    "-preset", "veryslow",
    "-b:v", f"{video_bitrate}k",
    "-pass", "2",
    "-c:a", "aac",
    "-b:a", f"{audio_bitrate}k",
    output_video
])

print("✅ 高画质压缩完成（veryslow）")
