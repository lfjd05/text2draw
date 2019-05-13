import os
from PIL import Image
import numpy as np


resize_x = 28
resize_y = 28


# 制作数据集
def create_record(path):
    # 找到类的名字
    class_name = os.listdir(path)

    img_raw = []
    label_raw = []
    for index, name in enumerate(class_name):
        class_path = path + "/" + name+"/"
        for img_name in os.listdir(class_path):
            if img_name.endswith('.png'):
                img_path = class_path + img_name
                img = Image.open(img_path)
                img = img.convert("RGB")
                img = img.resize((resize_x, resize_y))
                img_raw.append(np.asarray(img, dtype='float32'))  # 将图片转化为原生bytes
                label_raw.append(index)
    return class_name, np.asarray(img_raw), np.asarray(label_raw)


if __name__ == '__main__':
    sample_path = '../../png_data'
    class_list, X, Y = create_record(sample_path)
    print('数据大小', X.shape, Y.shape)
