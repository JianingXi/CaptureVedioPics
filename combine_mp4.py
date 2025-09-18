from moviepy.editor import VideoFileClip, concatenate_videoclips
import os


def merge_videos(video_path1, video_path2, output_path):
    """
    合并两个MP4视频文件

    参数:
    video_path1 (str): 第一个视频文件的路径
    video_path2 (str): 第二个视频文件的路径
    output_path (str): 合并后视频的输出路径
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(video_path1):
            raise FileNotFoundError(f"文件不存在: {video_path1}")
        if not os.path.exists(video_path2):
            raise FileNotFoundError(f"文件不存在: {video_path2}")

        # 加载视频文件
        clip1 = VideoFileClip(video_path1)
        clip2 = VideoFileClip(video_path2)

        # 合并视频
        final_clip = concatenate_videoclips([clip1, clip2])

        # 输出合并后的视频 - 使用aac音频编码
        final_clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",  # 使用aac编码替代mp3
            threads=4,  # 使用多线程加速
            preset="fast",  # 编码速度预设
            ffmpeg_params=["-movflags", "+faststart"]  # 优化网络播放
        )

        # 关闭视频剪辑对象以释放资源
        clip1.close()
        clip2.close()
        final_clip.close()

        print(f"视频合并完成！输出文件: {output_path}")

    except Exception as e:
        print(f"合并视频时出错: {e}")


# 使用示例
if __name__ == "__main__":
    # 输入视频文件路径
    video1 = r"C:\Users\xijia\Downloads\简历打磨（硕士毕业前）-视频-1.mp4"
    video2 = r"C:\Users\xijia\Downloads\简历打磨（硕士毕业前）-视频-2.mp4"

    # 输出视频文件路径（建议使用英文路径）
    output = r"C:\Users\xijia\Downloads\merged_video.mp4"

    # 合并视频
    merge_videos(video1, video2, output)