# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct
from struct import unpack
from scipy import interpolate
from googletrans import Translator
import pylab as pl
import os


def unpack_drawing(file_handle):
    key_id, = unpack('Q', file_handle.read(8))
    countrycode, = unpack('2s', file_handle.read(2))
    recognized, = unpack('b', file_handle.read(1))  # 是否被识别
    timestamp, = unpack('I', file_handle.read(4))
    n_strokes, = unpack('H', file_handle.read(2))
    image = []
    for i in range(n_strokes):
        n_points, = unpack('H', file_handle.read(2))
        fmt = str(n_points) + 'B'
        x = unpack(fmt, file_handle.read(n_points))
        y = unpack(fmt, file_handle.read(n_points))
        image.append((x, y))

    return {
        'key_id': key_id,
        'countrycode': countrycode,
        'recognized': recognized,
        'timestamp': timestamp,
        'image': image
    }


def unpack_drawings(filename):
    with open(filename, 'rb') as f:
        while True:
            try:
                yield unpack_drawing(f)
            except struct.error:
                break


def draw_plot(draw_pack, class_name_para):
    id = draw_pack['key_id']
    image_array = draw_pack['image']

    if not os.path.exists('png_data/{}'.format(class_name_para)):
        os.makedirs('png_data/{}'.format(class_name_para))

    if draw_pack["recognized"]:  # 识别对了的才是正确的图像
        for a_pen in image_array:  # 一笔
            x = a_pen[0]
            y = a_pen[1]
            # 插值
            f = interpolate.interp1d(x, y, kind='slinear')
            pl.plot(x, y, 'k')
        ax = pl.gca()  # 所有笔画画在一起
        ax.xaxis.set_ticks_position('top')
        ax.invert_yaxis()
        pl.axis('off')
        pl.savefig("png_data/%s/%s.png" % (class_name_para, id))
        pl.close()


translator = Translator(service_urls=['translate.google.com.hk', 'translate.google.co.kr'])
for root, _, file_names in os.walk('D:/pycharm_programme/画画数据'):
    for file_name in file_names:  # 一个种类的.bin文件
        i = 0
        class_name = file_name.split('_')[-1].replace('.bin', '')
        class_name_translation = translator.translate(class_name, src='en', dest='zh-CN').text
        for drawing in unpack_drawings(os.path.join(root, file_name)):
            # do something with the drawing
            draw_plot(drawing, class_name_translation)
            if i == 1:  # 每个种类画500个图
                break
            else:
                i += 1
