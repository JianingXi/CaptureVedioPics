from moviepy.editor import VideoFileClip
import os

def crop_video_by_ratio(input_path, top_ratio=0.1, bottom_ratio=0.1, left_ratio=0.2, right_ratio=0.2):
    """
    裁剪视频的上下左右边缘，按给定比例裁剪。

    参数:
    - input_path (str): 视频文件的完整路径。
    - top_ratio (float): 裁剪上边缘比例（0~1）。
    - bottom_ratio (float): 裁剪下边缘比例（0~1）。
    - left_ratio (float): 裁剪左边缘比例（0~1）。
    - right_ratio (float): 裁剪右边缘比例（0~1）。

    返回:
    - output_path (str): 裁剪后视频的输出路径。
    """
    # 读取视频
    clip = VideoFileClip(input_path)
    w, h = clip.size

    # 计算裁剪边界
    x1 = int(w * left_ratio)
    x2 = int(w * (1 - right_ratio))
    y1 = int(h * top_ratio)
    y2 = int(h * (1 - bottom_ratio))

    # 执行裁剪
    cropped = clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)

    # 构造输出路径
    base, ext = os.path.splitext(input_path)
    output_path = base + "_cropped" + ext

    # 导出视频
    cropped.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # 关闭资源
    clip.close()
    cropped.close()

    return output_path



input_video = r"C:\Users\xijia\Desktop\新建文件夹\abc.mp4"
cut_ratio = 0.15
# crop_video_by_ratio(input_video, top_ratio=cut_ratio, bottom_ratio=cut_ratio, left_ratio=cut_ratio, right_ratio=cut_ratio)
crop_video_by_ratio(input_video, top_ratio=0.15, bottom_ratio=0.1, left_ratio=0.1, right_ratio=0.15)