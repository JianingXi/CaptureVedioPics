import cv2
import os
from datetime import timedelta

# === 配置 ===
video_path = r"C:\Users\xijia\Desktop\ddd\20251107_141116.mp4"      # 替换为你的视频路径
output_dir = "./output"               # 输出目录
interval_seconds = 20                  # 截图间隔，单位：秒



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
else:
    print(f"[INFO] 视频帧率：{fps:.2f} fps")

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"[INFO] 视频总帧数：{total_frames}")

interval_frames = int(fps * interval_seconds)
print(f"[INFO] 每隔 {interval_seconds} 秒抽取一帧（即每隔 {interval_frames} 帧）")

# === 初始化变量 ===
timestamps = []
frame_idx = 0
screenshot_idx = 0

while cap.isOpened():
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    success, frame = cap.read()

    if not success:
        print(f"[WARN] 第 {frame_idx} 帧读取失败，结束提取")
        break

    timestamp_seconds = frame_idx / fps
    timestamp = str(timedelta(seconds=int(timestamp_seconds)))
    image_filename = f"screenshot_{screenshot_idx:05d}.jpg"
    image_path = os.path.join(output_dir, image_filename)

    # 保存图片帧
    success_save = cv2.imwrite(image_path, frame)
    if success_save:
        print(f"[OK] 保存帧 {frame_idx} -> {image_filename} (时间点：{timestamp})")
    else:
        print(f"[ERROR] 保存图片失败：{image_path}")
        break

    timestamps.append(f"{image_filename}\t{timestamp}")

    screenshot_idx += 1
    frame_idx += interval_frames

cap.release()

# === 写入时间戳文件 ===
txt_path = os.path.join(output_dir, "timestamps.txt")
with open(txt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(timestamps))

print(f"[DONE] 共保存 {screenshot_idx} 张图片。时间戳写入：{txt_path}")
