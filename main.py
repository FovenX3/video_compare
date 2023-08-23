import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from tqdm import tqdm
#pip install opencv-python
#pip install tqdm
#pip install scikit-image

# 设置每秒要比较的帧数（可以为小数0.5就是两秒一帧）
frames_per_second = 1

# 设置裁剪百分比（避免有的web源和bd源最外圈一丁点不一样或对比带硬字幕台标logo等，裁切掉周围只对比中心）
crop_percentage = 95

# 设置视频的帧偏移量（potplayer【d】前一帧【f】后一帧【tab】右上角看当前帧）
video1offset = 0
video2offset = 0

# 降采样分辨率
target_width = 960
target_height = 540

# 两个文件名
capture1 = cv2.VideoCapture("video1.mp4")
capture2 = cv2.VideoCapture("video2.mp4")


for _ in range(video1offset):
    capture1.read()
for _ in range(video2offset):
    capture2.read()


fps = capture1.get(cv2.CAP_PROP_FPS)
frame_count = int(capture1.get(cv2.CAP_PROP_FRAME_COUNT))


skip_frames = int(fps / frames_per_second)


counter = 0
timestamps = []

for _ in tqdm(range(0, frame_count, skip_frames + 1)):
    ret1, frame1 = capture1.read()
    ret2, frame2 = capture2.read()
    if not ret1 or not ret2:
        break
    frame1 = cv2.resize(frame1, (target_width, target_height))
    frame2 = cv2.resize(frame2, (target_width, target_height))
    height, width, _ = frame1.shape
    margin = (100 - crop_percentage) / 2 / 100
    x1, y1 = int(width * margin), int(height * margin)
    x2, y2 = int(width * (1 - margin)), int(height * (1 - margin))
    frame1 = frame1[y1:y2, x1:x2]
    frame2 = frame2[y1:y2, x1:x2]


    score, _ = ssim(frame1, frame2, full=True, multichannel=True,win_size=3)

    # 0-1
    if score < 0.97:
        timestamp = counter / fps
        timestamps.append(timestamp)
        filename1 = f"video1frame{counter}.jpg"
        filename2 = f"video2frame{counter}.jpg"
        cv2.imwrite(filename1, frame1)
        cv2.imwrite(filename2, frame2)

        print(f"发现不同: {timestamp:.2f} 秒")

    for _ in range(skip_frames):
        capture1.read()
        capture2.read()

    counter += skip_frames + 1

print("不同的时间点:", timestamps)
