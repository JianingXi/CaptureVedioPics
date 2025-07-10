import cv2
import numpy as np

def blur_video_multi_region(input_path, output_path, blur_tasks, debug=False):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("❌ 无法打开视频：", input_path)
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, codec, fps, (width, height))

    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        t = frame_idx / fps  # 当前时间（秒）

        for task in blur_tasks:
            x1, y1, x2, y2 = task['region']
            start, end = task['start_time'], task['end_time']
            fade = task.get('fade_duration', 0.5)
            ksize_max = task.get('ksize_max', 41)

            # 防止区域越界
            x1 = max(0, min(x1, frame.shape[1]-1))
            x2 = max(0, min(x2, frame.shape[1]))
            y1 = max(0, min(y1, frame.shape[0]-1))
            y2 = max(0, min(y2, frame.shape[0]))
            if x2 <= x1 or y2 <= y1:
                continue

            if start <= t <= end:
                # 时间渐变系数 alpha
                if t < start + fade:
                    alpha = (t - start) / fade
                elif t > end - fade:
                    alpha = (end - t) / fade
                else:
                    alpha = 1.0
                alpha = np.clip(alpha, 0.0, 1.0)

                # 动态模糊核大小（奇数）
                ksize_val = max(3, int(ksize_max * alpha))
                if ksize_val % 2 == 0:
                    ksize_val += 1
                ksize = (ksize_val, ksize_val)

                # 设置渐出范围
                margin = task.get("fade_margin", 60)

                # 外扩区域（模糊影响范围）
                mask_x1 = max(0, x1 - margin)
                mask_y1 = max(0, y1 - margin)
                mask_x2 = min(frame.shape[1], x2 + margin)
                mask_y2 = min(frame.shape[0], y2 + margin)

                # 提取包含region及边界的区域
                full_roi = frame[mask_y1:mask_y2, mask_x1:mask_x2].copy()
                blurred_roi = cv2.GaussianBlur(full_roi, ksize, 0)

                h, w = full_roi.shape[:2]

                # 创建羽化遮罩，仅作用于 region 外的过渡区
                mask = np.zeros((h, w), dtype=np.float32)
                inner_x1 = x1 - mask_x1
                inner_y1 = y1 - mask_y1
                inner_x2 = x2 - mask_x1
                inner_y2 = y2 - mask_y1

                # region 内强制设置为1（后续强替换）
                mask[inner_y1:inner_y2, inner_x1:inner_x2] = 1.0

                # 高斯羽化整块（region 外渐变）
                blur_kernel = margin * 2 + 1
                if blur_kernel % 2 == 0:
                    blur_kernel += 1
                mask = cv2.GaussianBlur(mask, (blur_kernel, blur_kernel), 0)
                mask = np.clip(mask, 0, 1)
                mask *= alpha  # 时间渐变控制
                mask = np.expand_dims(mask, axis=2)
                mask = np.repeat(mask, 3, axis=2)

                # 先融合全区域（仅渐出部分起效）
                blended_roi = full_roi * (1 - mask) + blurred_roi * mask

                # 然后 region 部分 强制 100% 替换（避免“反而变淡”）
                blended_roi[inner_y1:inner_y2, inner_x1:inner_x2] = blurred_roi[inner_y1:inner_y2, inner_x1:inner_x2]

                # 写入回原图
                frame[mask_y1:mask_y2, mask_x1:mask_x2] = blended_roi.astype(np.uint8)

                if debug:
                    print(f"[Frame {frame_idx:05d} | {t:.2f}s] 区域=({x1},{y1},{x2},{y2}) α={alpha:.2f} 核={ksize_val}")
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()
    print("✅ 多区域模糊处理完成，输出文件：", output_path)


if __name__ == "__main__":
    input_video = r"C:\MyDocument\ToDoList\D20_DoingPlatform\D20250627_关于开展第七届全国高校混合式教学设计创新大赛广州医科大学校内初赛的通知0710\A02材料\剪辑GIF\bk-4.mp4"
    output_video = r"C:\MyDocument\ToDoList\D20_DoingPlatform\D20250627_关于开展第七届全国高校混合式教学设计创新大赛广州医科大学校内初赛的通知0710\A02材料\剪辑GIF\bkb-4.mp4"
    blur_tasks = [
        {
            "region": (1000, 270, 1130, 300),
            "start_time": -1.0,
            "end_time": 10.0,
            "fade_duration": 0.5,
            "ksize_max": 41,
            "fade_margin": 60
        },
    ]

    """
    blur_tasks = [
        {
            "region": (1150, 600, 1400, 650),
            "start_time": -1.0,
            "end_time": 1.0,
            "fade_duration": 0.5,
            "ksize_max": 41,
            "fade_margin": 60
        },
        {
            "region": (1000, 670, 1400, 700),
            "start_time": 2.0,
            "end_time": 6.0,
            "fade_duration": 0.5,
            "ksize_max": 41,
            "fade_margin": 60
        },
    ]
    """

    # 启用调试：显示红框与打印输出
    blur_video_multi_region(input_video, output_video, blur_tasks, debug=False)
