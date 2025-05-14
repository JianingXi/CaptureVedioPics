import os
import subprocess


def convert_mov_to_mp4(input_path, output_path):
    """
    将 .MOV 文件转换为兼容 Office 2016 PPTX 的 .mp4 文件格式。
    """
    # 设置 FFmpeg 转码参数：
    # -c:v libx264：使用 H.264 编码，确保兼容性
    # -crf 23：视觉质量控制，0-51，值越小质量越高，文件越大
    # -preset medium：编码速度，medium 是平衡速度与质量的选择
    # -c:a aac：音频编码为 AAC，确保兼容性
    # -b:a 128k：音频比特率 128kbps，较为通用
    # -pix_fmt yuv420p：像素格式 yuv420p，确保兼容性
    command = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", "libx264",
        "-crf", "23",
        "-preset", "medium",
        "-c:a", "aac",
        "-b:a", "128k",
        "-pix_fmt", "yuv420p",
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"文件已成功转换并保存到：{output_path}")
    except subprocess.CalledProcessError as e:
        print(f"转换失败：{e}")


if __name__ == "__main__":
    # 输入文件路径
    input_mov = r"C:\Users\xijia\Desktop\test\D20240728_IMG_0714.MOV"
    # 输出文件路径
    output_mp4 = r"C:\Users\xijia\Desktop\test\D20240728_IMG_0714.mp4"

    # 执行转换
    convert_mov_to_mp4(input_mov, output_mp4)
