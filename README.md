# IDPhotos(更换证件照底色)
对证件照进行底色更换，目前可以将任意底片颜色的证件照处理成常用的红色、白色和蓝色底片的证件照。
## 环境要求
- Python 3.x
- opencv-python 
- numpy
## 使用方法
```sh
$ python main.py -i your_image_file -p your_path_to_output_image
# 比如
# python mian.py -i ./image.jpg -p . 
# OK done!
```
## PS
只能处理背景整洁的正装证件照！！！
## 处理前后的效果图
### 处理前的原图
![原图](./figures/image.jpg)<br>
### 生成的三种不同背景颜色的照片
![红色背景](./figures/red.jpg)<br>
![蓝色背景](./figures/blue.jpg)<br>
![白色背景](./figures/white.jpg)<br>
# 虽然，但是这个网站好像更高效：https://www.remove.bg/zh
使用方法：首先上传图片，去除现有背景，然后点击编辑，增加所需要的底色，最后下载。
