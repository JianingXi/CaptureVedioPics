import cv2
import os


def capture_frames(video_path, output_folder, num_frames=100):
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 获取视频的总帧数
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 计算截取帧的间隔
    frame_interval = total_frames // num_frames

    # 初始化计数器
    count = 0
    saved_count = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # 每隔 frame_interval 帧截取一张图像
        if count % frame_interval == 0 and saved_count < num_frames:
            # 保存截取的帧
            cv2.imwrite(os.path.join(output_folder, f"frame_{saved_count + 1:03d}.jpg"), frame)
            saved_count += 1

        count += 1

    # 释放视频文件
    cap.release()
    print(f"截取完成，共保存了 {saved_count} 张截图")


# 示例用法
# video_path = r'C:\MyPython\CaptureVedioPics'  # 替换为你的视频路径
# output_folder = './output_frames'  # 替换为输出文件夹路径
# capture_frames(video_path, output_folder)



# 示例用法
video_path = r'C:\Users\xijia\Desktop\DoingPlatform\教创赛省赛提交\D20250314_线性系统和非线性系统录像\D0407_新版\信号与系统-4-7压缩版.mp4'
output_folder = './test4'  # 替换为输出文件夹路径 must be English
capture_frames(video_path, output_folder, 50)
