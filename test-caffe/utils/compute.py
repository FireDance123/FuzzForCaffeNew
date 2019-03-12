import os
os.environ['GLOG_minloglevel'] = '2'
import caffe
import numpy as np
import time
import struct
from PIL import Image
from utils import mutate_functions_by_bytes

# 设置网络结构
net_file = 'E:/PycharmProjects/test-caffe/net/deploy.prototxt'
# E:/PycharmProjects/test-caffe/net

# 添加训练之后的参数
caffe_model = 'E:/PycharmProjects/test-caffe/net/bvlc_reference_caffenet.caffemodel'

# 均值文件
mean_file = 'E:/PycharmProjects/test-caffe/net/ilsvrc_2012_mean.npy'

imagenet_labels_filename = 'E:/PycharmProjects/test-caffe/net/synset_words.txt'


def compute(im):
    net = caffe.Net(net_file, caffe_model, caffe.TEST)

    # 得到data的形状，这里的图片是默认matplotlib底层加载的
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

    # 把channel放到前面
    transformer.set_transpose('data', (2, 0, 1))
    transformer.set_mean('data', np.load(mean_file).mean(1).mean(1))

    # 图片像素放大到[0-255]
    transformer.set_raw_scale('data', 255)

    # RGB-->BGR转换
    transformer.set_channel_swap('data', (2, 1, 0))

    # 加载图片
    # im = caffe.io.load_image()

    # im = mutate_functions_by_bytes.mutate(im)
    # im = mutate_functions_by_bytes.do_basic_mutations(im)
    # im = np.clip(im, a_min=0, a_max=1)

    # # 用上面的transformer.preprocess来处理刚刚加载的图片
    net.blobs['data'].data[...] = transformer.preprocess('data', im)
    # since = time.time()
    # 前向传播
    # out = net.forward(start='data', end='conv1')
    out = net.forward(start='data', end='conv1')
    # out1 = net.forward(start='data', end='prob')

    # time_elapsed = time.time() - since
    # print(time_elapsed)
    # print(net.layers[0].forward_cpu())
    # # 加载标签
    labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')
    #
    # # 最终的结果：当前这个图片属于哪个物体的概率（列表表示）
    # output_conv1 = out['conv1']
    output_prob = out['conv1']
    # # 找出最大的哪个概率
    # print('predicted class is:', output_prob.argmax())
    # print(labels[output_prob.argmax()])
    # return output_conv1
    return output_prob

if __name__ == '__main__':
    im = caffe.io.load_image('E:/caffe-windows/examples/images/cat.jpg')
    # print(im)
    compute(im)