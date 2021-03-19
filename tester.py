import cv2
import numpy as np

# Load sample image
img_bgr = cv2.imread("H:\\frame1.png")


# Convert from BGR to YUV
img_yuv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YUV)

# Converting directly back from YUV to BGR results in an (almost) identical image
img_bgr_restored = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

diff = img_bgr.astype(np.int16) - img_bgr_restored
print("mean/stddev diff (BGR => YUV => BGR)", np.mean(diff), np.std(diff))

# Create YUYV from YUV
y0 = np.expand_dims(img_yuv[...,0][::,::2], axis=2)
u = np.expand_dims(img_yuv[...,1][::,::2], axis=2)
y1 = np.expand_dims(img_yuv[...,0][::,1::2], axis=2)
v = np.expand_dims(img_yuv[...,2][::,::2], axis=2)
img_yuyv = np.concatenate((y0, u, y1, v), axis=2)
img_yuyv_cvt = img_yuyv.reshape(img_yuyv.shape[0], img_yuyv.shape[1] * 2, int(img_yuyv.shape[2] / 2))
print(img_yuyv.shape[1])
# Convert back to BGR results in more saturated image.
img_bgr_restored = cv2.cvtColor(img_yuyv_cvt, cv2.COLOR_YUV2BGR_YUYV)
cv2.imshow("converted", img_bgr_restored)
cv2.waitKey(0)

diff = img_bgr.astype(np.int16) - img_bgr_restored
print("mean/stddev diff (BGR => YUV => YUYV => BGR)", np.mean(diff), np.std(diff))