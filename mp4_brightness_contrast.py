import cv2
import numpy as np
from moviepy.editor import VideoFileClip

# =====================================================
# 参数区（只需要调这里）
# =====================================================
INPUT_VIDEO = r"C:\Users\xijia\Desktop\新建文件夹\abc_cropped.mp4"
OUTPUT_VIDEO = r"C:\Users\xijia\Desktop\新建文件夹\abc_enhanced.mp4"

# --- 基础 ---
BRIGHTNESS = 5         # 亮度 [-50, 50]
CONTRAST = 1.3         # 对比度 [0.8, 1.5]
SATURATION = 1.2       # 饱和度 [0.8, 1.4]
WARMTH = 2             # 色温 [-20, 20] 正数偏暖

# --- 观感 ---
GAMMA = 1.05           # gamma >1 提亮暗部
SHARPEN = 0.05          # 锐化强度 [0~1]
DENOISE = 1            # 去噪强度 [0~10]

# =====================================================
# 工具函数
# =====================================================
def adjust_basic(frame):
    frame = frame.astype(np.float32)
    frame = frame * CONTRAST + BRIGHTNESS
    frame = np.clip(frame, 0, 255)
    return frame.astype(np.uint8)

def adjust_saturation(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[..., 1] *= SATURATION
    hsv[..., 1] = np.clip(hsv[..., 1], 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

def adjust_warmth(frame):
    b, g, r = cv2.split(frame.astype(np.int16))
    r += WARMTH
    b -= WARMTH
    frame = cv2.merge([b, g, r])
    return np.clip(frame, 0, 255).astype(np.uint8)

def adjust_gamma(frame):
    inv = 1.0 / GAMMA
    table = np.array([(i / 255.0) ** inv * 255 for i in range(256)]).astype("uint8")
    return cv2.LUT(frame, table)

def sharpen_image(frame):
    if SHARPEN <= 0:
        return frame
    kernel = np.array([[0, -1, 0],
                       [-1, 5 + SHARPEN * 5, -1],
                       [0, -1, 0]])
    return cv2.filter2D(frame, -1, kernel)

def denoise_image(frame):
    if DENOISE <= 0:
        return frame
    return cv2.fastNlMeansDenoisingColored(frame, None, DENOISE, DENOISE, 7, 21)

# =====================================================
# 主处理流程
# =====================================================
def process_frame(frame):
    frame = adjust_basic(frame)
    frame = adjust_saturation(frame)
    frame = adjust_warmth(frame)
    frame = adjust_gamma(frame)
    frame = denoise_image(frame)
    frame = sharpen_image(frame)
    return frame


def main():
    """
    教室偏暗 + 投影
    BRIGHTNESS = 20
    CONTRAST = 1.2
    SATURATION = 1.05
    WARMTH = 6
    GAMMA = 1.1
    SHARPEN = 0.6
    DENOISE = 5

    🧠 屏幕录制 + PPT
    BRIGHTNESS = 5
    CONTRAST = 1.1
    SATURATION = 1.0
    WARMTH = 0
    GAMMA = 1.0
    SHARPEN = 0.8
    DENOISE = 0

    📹 人物偏灰、没精神
    BRIGHTNESS = 10
    CONTRAST = 1.3
    SATURATION = 1.2
    WARMTH = 8
    GAMMA = 1.05
    SHARPEN = 0.5
    DENOISE = 4
    """

    # =====================================================
    # 视频处理
    # =====================================================
    clip = VideoFileClip(INPUT_VIDEO)
    new_clip = clip.fl_image(process_frame)

    new_clip.write_videofile(
        OUTPUT_VIDEO,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        threads=4
    )

    print("✅ 视频综合增强完成")
    print("输出文件：", OUTPUT_VIDEO)

if __name__ == '__main__':
    main()