
import cv2
import os
import imageio  # 可选，用于调试或参考
from PIL import Image
from datetime import timedelta


# === 配置 ===
video_path = r"D:\Alpha\StoreLatestYears\Store2025\B教学_教学与人才培养_A02_教学竞赛\D20250314_教师教学创新竞赛_省级_课程思政赛道\D20250221_2025教创赛_省赛提交\Z01_提交材料\01课堂教学实录视频及相关文件\信号与系统+线性系统与非线性系统.mp4"  # 替换为你的视频路径
output_dir = "./output"  # 输出目录
interval_seconds = 15  # 每隔多久录制一个 GIF，单位：秒
gif_duration = 5  # 每个 GIF 持续多长时间，单位：秒
target_width = 400  # 输出 GIF 的目标宽度

# === 创建输出目录 ===
os.makedirs(output_dir, exist_ok=True)
print(f"[INFO] 输出文件将保存在：{os.path.abspath(output_dir)}")

# === 打开视频 ===
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"[ERROR] 无法打开视频文件：{video_path}")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    print("[ERROR] 无法获取视频帧率（FPS），可能是视频编码不被支持或文件损坏")
    exit()
print(f"[INFO] 视频帧率：{fps:.2f} fps")

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"[INFO] 视频总帧数：{total_frames}")

interval_frames = int(fps * interval_seconds)
gif_frames_count = int(fps * gif_duration)
print(f"[INFO] 每隔 {interval_seconds} 秒录制一个 {gif_duration} 秒的 GIF（共 {gif_frames_count} 帧）")

# === 初始化变量 ===
timestamps = []
frame_idx = 0
gif_idx = 0

while cap.isOpened():
    # 计算当前段的起始时间
    timestamp_seconds = frame_idx / fps
    timestamp = str(timedelta(seconds=int(timestamp_seconds)))

    frames = []
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)

    for i in range(gif_frames_count):
        success, frame = cap.read()
        if not success:
            print(f"[WARN] 在连续读取时，第 {frame_idx + i} 帧读取失败，结束当前 GIF 的录制")
            break

        # 压缩帧分辨率（保持宽高比）
        height, width = frame.shape[:2]
        new_height = int(height * (target_width / width))
        frame_resized = cv2.resize(frame, (target_width, new_height), interpolation=cv2.INTER_AREA)

        # 转换 BGR 为 RGB，确保颜色正确（后续 Pillow 转换时使用 RGB 图像）
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        frames.append(frame_rgb)

    if not frames:
        print("[INFO] 无更多帧可读取，结束录制")
        break

    gif_filename = f"gif_segment_{gif_idx:03d}.gif"
    gif_path = os.path.join(output_dir, gif_filename)

    # 利用 PIL 控制调色板转换和抖动
    pil_frames = [Image.fromarray(frame) for frame in frames]
    # 使用自适应调色板和 Floyd-Steinberg 抖动，保留更多颜色渐变效果
    pil_frames = [
        frame.convert('P', palette=Image.ADAPTIVE, dither=Image.FLOYDSTEINBERG)
        for frame in pil_frames
    ]

    # 计算每帧显示时长（单位：毫秒）
    duration_per_frame = int((gif_duration / len(pil_frames)) * 1000)

    try:
        # 保存 GIF；使用 loop=0 以保证无限循环播放
        pil_frames[0].save(
            gif_path,
            format='GIF',
            save_all=True,
            append_images=pil_frames[1:],
            duration=duration_per_frame,
            loop=0,
            optimize=False  # 关闭 optimize 可保留完整调色板信息
        )
        print(f"[OK] 保存 GIF 片段 {gif_idx:03d}: {gif_filename} (起始时间：{timestamp})")
    except Exception as e:
        print(f"[ERROR] 保存 GIF 失败：{gif_path}\n错误信息：{e}")
        break

    timestamps.append(f"{gif_filename}\t{timestamp}")
    gif_idx += 1
    frame_idx += interval_frames
    if frame_idx >= total_frames:
        break

cap.release()

# === 写入时间戳文件 ===
txt_path = os.path.join(output_dir, "timestamps.txt")
with open(txt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(timestamps))

print(f"[DONE] 共保存 {gif_idx} 个循环播放的 GIF 文件。时间戳写入：{txt_path}")
