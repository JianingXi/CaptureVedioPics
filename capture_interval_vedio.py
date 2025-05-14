# extract_subclip.py
"""
一键运行脚本，用 FFmpeg 截取视频片段并输出为 MP4：
1. 依赖：系统已安装并添加到 PATH 的 ffmpeg；
2. 调用函数 extract_subclip(input_path, output_path, start_time, end_time)；
3. 在 IDE 中按 F5 或直接双击运行即可。
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

def extract_subclip(input_path: str,
                    output_path: str,
                    start_time: str,
                    end_time: str):
    """
    截取视频片段并输出为 MP4。
    :param input_path: 输入视频路径
    :param output_path: 输出视频路径
    :param start_time: 开始时间，格式 MM:SS 或 HH:MM:SS
    :param end_time: 结束时间，格式 MM:SS 或 HH:MM:SS
    """
    if not os.path.isfile(input_path):
        print(f"❌ 找不到输入文件：{input_path}")
        sys.exit(1)

    start_sec = time_to_seconds(start_time)
    end_sec = time_to_seconds(end_time)
    duration = end_sec - start_sec
    if duration <= 0:
        print("❌ 结束时间必须大于开始时间")
        sys.exit(1)

    cmd = [
        "ffmpeg",
        "-ss", start_time,
        "-i", input_path,
        "-t", f"{duration:.2f}",
        "-c", "copy",
        "-y",
        output_path
    ]

    print("▶️ 正在执行 FFmpeg 命令：")
    print("   " + " ".join(cmd))
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode == 0:
        print(f"✅ 截取完成，输出已保存到: {output_path}")
    else:
        print("❌ FFmpeg 运行出错：")
        print(proc.stderr)
        sys.exit(1)

if __name__ == "__main__":
    ensure_ffmpeg()
    # —— 用户请在此处修改参数 —— #
    input_path  = r"C:\Users\xijia\Desktop\DoingPlatform\D20250428_教创赛省赛决赛答辩\素材\封面电影\20250512_152619.mp4"
    output_path = r"C:\Users\xijia\Desktop\DoingPlatform\D20250428_教创赛省赛决赛答辩\素材\封面电影\a01.mp4"
    start_time  = "00:08"   # 截取起始点
    end_time    = "00:18"   # 截取结束点
    # —————————————————————————— #

    extract_subclip(input_path, output_path, start_time, end_time)
