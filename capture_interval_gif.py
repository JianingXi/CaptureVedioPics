# capture_interval_gif.py
"""
功能：用 FFmpeg 截取视频并生成指定大小的 GIF
使用方法：
  1. 确保已安装 FFmpeg，并且能够在命令行中执行 `ffmpeg`；
     官方下载与安装：https://ffmpeg.org/download.html
  2. 修改下面的 input_path/output_path/start_time/end_time；
  3. 在 IDE 中按 F5（或双击）运行此脚本。
"""

import os
import sys
import subprocess

def time_to_seconds(t: str) -> float:
    """将 'HH:MM:SS' 或 'MM:SS' 转为秒数"""
    parts = list(map(float, t.split(':')))
    if len(parts) == 2:
        mm, ss = parts
        return mm * 60 + ss
    elif len(parts) == 3:
        hh, mm, ss = parts
        return hh * 3600 + mm * 60 + ss
    else:
        raise ValueError("时间格式错误，应为 MM:SS 或 HH:MM:SS")

def ensure_ffmpeg():
    """检查 ffmpeg 是否可用"""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("❌ 未检测到 ffmpeg，请先安装并将其加入系统 PATH：")
        print("   https://ffmpeg.org/download.html")
        sys.exit(1)

def clip_to_gif(input_path: str,
                output_path: str,
                start_time: str,
                end_time: str,
                width: int = 600,
                fps: int = 15):
    if not os.path.isfile(input_path):
        print(f"❌ 找不到输入文件：{input_path}")
        sys.exit(1)

    # 计算时长
    start_sec = time_to_seconds(start_time)
    end_sec = time_to_seconds(end_time)
    duration = end_sec - start_sec
    if duration <= 0:
        print("❌ 结束时间必须大于开始时间")
        sys.exit(1)

    # 构造 FFmpeg 命令
    # -ss 在输入前定位，-t 指定持续时长，-vf scale=600:-1 保持宽度 600 等比缩放
    cmd = [
        "ffmpeg",
        "-ss", start_time,
        "-i", input_path,
        "-t", f"{duration:.2f}",
        "-vf", f"scale={width}:-1",
        "-r", str(fps),
        "-y",               # 覆盖输出文件
        output_path
    ]

    print("▶️ 正在执行 FFmpeg 命令：")
    print("   " + " ".join(cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print(f"✅ GIF 已保存到: {output_path}")
    else:
        print("❌ FFmpeg 运行出错：")
        print(result.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # ===== 用户请在这里修改 =====
    input_path  = r"C:\MyDocument\ToDoList\D20_DoingPlatform\D20250627_关于开展第七届全国高校混合式教学设计创新大赛广州医科大学校内初赛的通知0710\A02材料\剪辑GIF\bkb-2.mp4"
    output_path = r"C:\MyDocument\ToDoList\D20_DoingPlatform\D20250627_关于开展第七届全国高校混合式教学设计创新大赛广州医科大学校内初赛的通知0710\A02材料\剪辑GIF\bk-2.gif"
    start_time  = "00:00"   # 开始时间，MM:SS 或 HH:MM:SS
    end_time    = "00:09"   # 结束时间
    width       = 800       # 输出 GIF 宽度(px)
    fps         = 15        # 帧率
    # =========================

    ensure_ffmpeg()
    clip_to_gif(input_path, output_path, start_time, end_time, width, fps)
