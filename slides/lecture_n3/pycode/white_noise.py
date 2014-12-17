from PIL import Image
import numpy as np


def img_to_float_array():
    m = np.asarray(Image.open('cat.png'))
    return m.shape, m.flatten()/255.0

def farray_to_img(v, shape):
    Image.fromarray(np.asanyarray(np.round(v*255), dtype=np.uint8).reshape(shape)).save('cat_noised.png')


shape, v = img_to_float_array()

w = np.random.normal(0, 0.01, (v.shape[0], v.shape[0]))
v = 1 / (1 + np.exp(-np.dot(w, v).flatten()))


farray_to_img(v, shape)

