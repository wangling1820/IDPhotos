# wangling
# 2020-05-23
# Reference:
#     微信公众号：搬运代码吧


import os
import argparse

import numpy as np
import cv2 as cv


# 对证件照进行三种颜色的换底操作
def change_color(image_path='./myimage.jpg', output_path='.'):
      # 读入数据
      image = cv.imread(image_path)

      h, w, ch = image.shape

      data = image.reshape((-1, 3))
      # 数据转换，计算更快
      data = np.float32(data)

      # 设置聚类
      criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
      num_clusters = 4
      # label就是各个像素点的所属的类别标签，通常第一个像素点的标签就是背景色的标签
      _, label, _ = cv.kmeans(data, num_clusters, None, criteria, num_clusters, cv.KMEANS_RANDOM_CENTERS)

      # 找到背景像素的类别
      indx = label[0][0]

      # 生成掩膜
      mask = np.ones((h, w), dtype=np.uint8) * 255
      label = np.reshape(label, (h, w))

      mask[label == indx] = 0
      
      # 处理掩膜，使得生成的图像更加完美
      se = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
      cv.erode(mask, se, mask)
      mask = cv.GaussianBlur(mask, (5, 5), 0)

      # 白色背景[255, 255, 255]
      bg_w = np.ones(image.shape, dtype=np.float) * 255

      # 红色背景 注意：opencv中的像素三通道的排列顺序为BGR，而非RGB。所以红色为[0, 0, 255]， 蓝色为[255, 0, 0]
      red = np.array([0, 0, 255])
      bg_r = np.tile(red, (h, w, 1))
      
      # 蓝色背景
      blue = np.array([255, 0, 0])
      bg_b = np.tile(blue, (h, w, 1))

      # alpha 即为需要保留的部分，则 1-alpha 为要去除的背景，此处可以看作两张图像的加权融合
      alpha = mask.astype(np.float32) / 255
      fg= alpha[..., None] * image
      bg = 1 - alpha[..., None]
      new_image_white = fg + bg * bg_w
      new_image_red = fg + bg * bg_r
      new_image_blue = fg + bg * bg_b

      # 保存图片
      w_path = os.path.join(output_path, 'white.jpg')
      r_path = os.path.join(output_path, 'red.jpg')
      b_path = os.path.join(output_path, 'blue.jpg')

      cv.imwrite(w_path, new_image_white.astype(np.uint8))
      cv.imwrite(r_path, new_image_red.astype(np.uint8))
      cv.imwrite(b_path, new_image_blue.astype(np.uint8))

      print('OK done!')


if __name__ == '__main__':
      ap = argparse.ArgumentParser()
      ap.add_argument('-i', '--image', default='./image.jpg', help='path to the input image.')
      ap.add_argument('-p', '--path', default='.', help='path to the output image.')
      args = vars(ap.parse_args())

      change_color(args['image'], args['path'])