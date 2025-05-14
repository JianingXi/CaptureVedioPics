from PIL import Image, ImageSequence
import os

def extract_gif_segment(input_gif_path, output_gif_path, start_time, end_time, frame_duration):
    # 打开GIF文件
    with Image.open(input_gif_path) as img:
        frames = []
        duration = img.info['duration']  # 每帧持续时间（毫秒）
        start_frame = start_time * 1000 // duration
        end_frame = end_time * 1000 // duration

        # 提取指定时间段的帧
        for i, frame in enumerate(ImageSequence.Iterator(img)):
            if start_frame <= i <= end_frame:
                frames.append(frame.copy())

        if frames:
            # 保存新GIF
            frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], duration=frame_duration, loop=0)
            print(f"GIF 提取成功: {output_gif_path}")
        else:
            print("指定时间段未找到有效帧")

if __name__ == "__main__":
    input_gif = r"C:\Users\xijia\Desktop\DoingPlatform\D20250428_教创赛省赛决赛答辩\素材\实验课GIF\20250512_1711_Collaborative Electronics Workshop_storyboard_01jv1w7hyjeh9t861apfmfmn9q.gif"  # 输入GIF路径
    output_gif = r"C:\Users\xijia\Desktop\DoingPlatform\D20250428_教创赛省赛决赛答辩\素材\实验课GIF\out.gif"  # 输出GIF路径
    start_time = 0  # 开始时间 (秒)
    end_time = 2.5    # 结束时间 (秒)
    frame_duration = 0.005  # 每帧持续时间 (毫秒)

    extract_gif_segment(input_gif, output_gif, start_time, end_time, frame_duration)
