# speed_segment.py
"""
一键运行脚本，对视频指定区段加速，其他部分保持原速：
1. 依赖：系统已安装并添加到 PATH 的 ffmpeg；
2. 修改下面的 input_path/output_path/start_time/end_time/speed；
3. 在 IDE 中按 F5 或者双击运行即可。
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

def speed_up_segment(input_path: str,
                     output_path: str,
                     start_time: str,
                     end_time: str,
                     speed: float):
    """
    对 input_path 视频的 [start_time, end_time] 段落加速 speed 倍，
    其他部分保持原速，输出到 output_path。
    """
    if not os.path.isfile(input_path):
        print(f"❌ 找不到输入文件：{input_path}")
        sys.exit(1)

    # 转为秒
    t0 = time_to_seconds(start_time)
    t1 = time_to_seconds(end_time)
    if t1 <= t0:
        print("❌ 结束时间必须大于开始时间")
        sys.exit(1)

    # FFmpeg filter_complex 拼接：
    # 图像：trim + setpts + concat
    # 音频：atrim + atempo + concat
    vf = (
        f"[0:v]trim=0:{t0},setpts=PTS-STARTPTS[v0];"
        f"[0:v]trim={t0}:{t1},setpts=PTS-STARTPTS,setpts=PTS/{speed}[v1];"
        f"[0:v]trim={t1},setpts=PTS-STARTPTS[v2];"
        f"[v0][v1][v2]concat=n=3:v=1[outv]"
    )
    af = (
        f"[0:a]atrim=0:{t0},asetpts=PTS-STARTPTS[a0];"
        f"[0:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS,atempo={speed}[a1];"
        f"[0:a]atrim={t1},asetpts=PTS-STARTPTS[a2];"
        f"[a0][a1][a2]concat=n=3:v=0:a=1[outa]"
    )

    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-filter_complex", vf + ";" + af,
        "-map", "[outv]",
        "-map", "[outa]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-y",  # 覆盖输出
        output_path
    ]

    print("▶️ 正在执行 FFmpeg 命令：")
    print("   " + " ".join(cmd))
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode == 0:
        print(f"✅ 输出视频已保存到: {output_path}")
    else:
        print("❌ FFmpeg 运行出错：")
        print(proc.stderr)
        sys.exit(1)

if __name__ == "__main__":
    ensure_ffmpeg()

    # —— 用户参数区 —— #
    input_path  = r"C:\MyDocument\ToDoList\D20_DoingPlatform\D20250627_关于开展第七届全国高校混合式教学设计创新大赛广州医科大学校内初赛的通知0710\A02材料\剪辑GIF\视频\bk-2.mp4"
    output_path = r"C:\MyDocument\ToDoList\D20_DoingPlatform\D20250627_关于开展第七届全国高校混合式教学设计创新大赛广州医科大学校内初赛的通知0710\A02材料\剪辑GIF\bk-2.mp4"
    start_time  = "00:01"    # 加速开始时间
    end_time    = "00:06"    # 加速结束时间
    speed       = 1.00         # 倍速
    # —————————————— #

    speed_up_segment(input_path, output_path, start_time, end_time, speed)
