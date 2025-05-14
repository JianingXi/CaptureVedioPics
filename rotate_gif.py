# rotate_gif_with_flip.py
"""
一键运行脚本，使用 Python Pillow 库对 GIF 动画进行：
- 顺时针/逆时针旋转 90° 及 180°
- 水平/垂直镜像翻转
可在 IDE 中按 F5 或双击运行，无需额外依赖。
"""

import sys
import os

# 自动安装 Pillow
try:
    from PIL import Image, ImageSequence, ImageOps
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageSequence, ImageOps

def process_gif(input_path: str, output_path: str,
                angle: int = 0, direction: str = "cw",
                flip: str = None):
    """
    对 GIF 动画进行旋转和镜像翻转操作。
    :param input_path: 输入 GIF 文件路径
    :param output_path: 输出 GIF 文件路径
    :param angle: 旋转角度，支持 0, 90, 180
    :param direction: 'cw' 顺时针 或 'ccw' 逆时针，180° 时忽略
    :param flip: 镜像翻转方式，None, 'horizontal', 'vertical'
    """
    if not os.path.isfile(input_path):
        print(f"❌ 找不到输入文件: {input_path}")
        sys.exit(1)

    # 验证参数
    if angle not in (0, 90, 180):
        print("❌ 仅支持 0, 90 或 180 度旋转")
        sys.exit(1)
    if flip and flip not in ("horizontal", "vertical"):
        print("❌ flip 参数仅支持 'horizontal' 或 'vertical'")
        sys.exit(1)

    # 计算 Pillow 旋转角度（正值为逆时针）
    if angle == 180:
        rot_angle = 180
    elif angle == 90:
        rot_angle = angle if direction.lower() == "ccw" else -angle
    else:
        rot_angle = 0

    # 打开 GIF 并提取帧
    img = Image.open(input_path)
    frames = []
    durations = []
    loop = img.info.get("loop", 0)

    for frame in ImageSequence.Iterator(img):
        durations.append(frame.info.get("duration", 100))
        f = frame.convert("RGBA")

        # 旋转
        if rot_angle != 0:
            f = f.rotate(rot_angle, expand=True)

        # 镜像翻转
        if flip == "horizontal":
            f = ImageOps.mirror(f)
        elif flip == "vertical":
            f = ImageOps.flip(f)

        frames.append(f)

    # 保存 GIF
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        loop=loop,
        duration=durations,
        disposal=2,
        optimize=False
    )
    print(f"✅ 处理后 GIF 已保存到: {output_path}")

if __name__ == "__main__":
    # ——— 用户请根据需要修改参数 ———
    input_path = r"C:\Users\xijia\Desktop\test\test3.gif"
    output_path = r"C:\Users\xijia\Desktop\test\test31.gif"
    angle = 180               # 0, 90, 180
    direction = "ccw"         # 'cw' 或 'ccw'
    flip = None      # None, 'horizontal', 'vertical'
    # ——————————————————————————

    process_gif(input_path, output_path, angle, direction, flip)
