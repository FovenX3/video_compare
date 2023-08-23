# video_compare
对比两个视频有差异的帧，如web源与bd源哪里作画修正了/圣光没了等


# requirement
opencv-python  
tqdm  
scikit-image


# 设置视频的帧偏移量（potplayer【d】前一帧【f】后一帧【tab】右上角看当前帧）
video1offset = 0  
video2offset = 0

# 设置每秒要比较的帧数（可以为小数0.5就是两秒一帧）
frames_per_second = 1

# 设置裁剪百分比（避免有的web源和bd源最外圈一丁点不一样或对比带硬字幕台标logo等，裁切掉周围只对比中心）
crop_percentage = 95

# 降采样分辨率（提升效率）
target_width = 960  
target_height = 540

