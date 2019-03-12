import caffe
import numpy as np
import time
import struct
from PIL import Image
from utils import mutate_functions_by_bytes
# 设置网络结构
net_file = 'E:/caffe-windows/models/bvlc_reference_caffenet/deploy.prototxt'

# 添加训练之后的参数
caffe_model = 'E:/caffe-windows/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'

# 均值文件
mean_file = 'E:/Anaconda3/envs/Python3.5/Lib/site-packages/caffe/imagenet/ilsvrc_2012_mean.npy'

# 处理图片
# 把上面添加的两个变量都作为一个参数构造一个Net
net = caffe.Net(net_file, caffe_model, caffe.TEST)

# 得到data的形状，这里的图片是默认matplotlib底层加载的
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
# print(net.blobs['data'].data.shape)
# matplotlib加载的image是像素[0-1],图片的数据格式[weight,high,channels]，RGB
# caffe加载的图片需要的是[0-255]像素，数据格式[channels,weight,high],BGR，那么就需要转换

# 把channel放到前面
transformer.set_transpose('data', (2, 0, 1))
transformer.set_mean('data', np.load(mean_file).mean(1).mean(1))

# 图片像素放大到[0-255]
transformer.set_raw_scale('data', 255)

# RGB-->BGR转换
transformer.set_channel_swap('data', (2, 1, 0))

# 加载图片
im = caffe.io.load_image('E:/caffe-windows/examples/images/cat.jpg')
# im1 = np.random.uniform(low=0.0, high=1.0, size=(360, 480, 3))
# print(im[0])
# print(type(im[0][0][0]))
# im1_list = im.tolist()
# print(im1_list[0][0])
# im1_list = mutate_functions_by_bytes.mutate(im1_list)
# print(im[0][0])
# im = mutate_functions_by_bytes.mutate(im)
# im1 = mutate_functions_by_bytes.do_basic_mutations(im)
# print(im)
# im = np.clip(im, a_min=0, a_max=1)
# im[0][0][0] = 0.9
# print(im[0])
# print(type(im[0][0][0]))
# print(im[0][0])
# print(im1[0][0])



# print(im1_list[0][0])


# print(im1.shape)
# print(im1)
# print(im.shape)
# print(im[0][0])
# print(im)
# # 用上面的transformer.preprocess来处理刚刚加载的图片
net.blobs['data'].data[...] = transformer.preprocess('data', im)
# net.blobs['data'].data[...] = transformer.preprocess('data', im1)
# print(net.blobs['data'].data.shape)
# print(len(net.blobs['data'].data[...]))
# print(net.blobs['data'].data[3])
# # caffe.set_device(0)
# # caffe.set_mode_gpu()
# # since = time.time()
for layer_name, blob in net.blobs.items():
    print('layer name:', layer_name, ', shape:', blob.data.shape)
#
# for layer_name, param in net.params.items():
#     print('layer name: ', layer_name, ', weights:', param[0].data.shape, ', biases:', param[1].data.shape)
# 前向传播
# out = net.forward()
out = net.forward(start='conv1', end='pool1')
# print(out['pool1'][0])
# conv1_feature = np.float64(net.blobs['conv1'].data)
# pool1_feature = np.float64(net.blobs['pool1'].data)
# print(conv1_feature.shape)
# print(pool1_feature.shape)
# print(pool1_feature[0][0][0])
# print(feature[0])
# time_elapsed = time.time() - since
# print(time_elapsed)
# print(len(out['prob'][0]))
# print(max(out['prob'][0]))
# print(type(out['prob'][0]))
# out_list = out['prob'][0].tolist()
# print(out_list.index(max(out_list)))
# print(out['prob'][1])
#
# # 加载标签
# imagenet_labels_filename = 'E:/caffe-windows/data/ilsvrc12/synset_words.txt'
# labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')
#
# # 最终的结果：当前这个图片属于哪个物体的概率（列表表示）
# output_prob = out['prob'][0]
# # 找出最大的哪个概率
# print('predicted class is:', output_prob.argmax())
# print(labels[output_prob.argmax()])
# print(len(output_prob))