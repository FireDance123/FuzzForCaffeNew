import caffe
import numpy as np
import time

# 设置网络结构
net_file = 'mnist/lenet.prototxt'

# 添加训练之后的参数
caffe_model = 'mnist/mnist_iter_10000.caffemodel'

# 处理图片
net = caffe.Net(net_file, caffe_model, caffe.TEST)

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
print(net.blobs['data'].data.shape)

transformer.set_transpose('data', (2, 0, 1))
transformer.set_raw_scale('data', 255)
# transformer.set_channel_swap('data', (2, 1, 0))

im = caffe.io.load_image('mnist/mnist_image/mnist_test/0/mnist_test_3.png')
im = caffe.io.load_image('mnist/0.jpg')
print(im.shape)

net.blobs['data'].data[...] = transformer.preprocess('data', im)
out = net.forward()

label_filename = 'mnist/synset_words.txt'
labels = np.loadtxt(label_filename, str, delimiter='\t')

output_prob = out['prob'][0]

print('预测的数字是：', labels[output_prob.argmax()])



