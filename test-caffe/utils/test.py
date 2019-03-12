from utils import mutate_functions_by_bytes
from utils import data_conversions
from utils import process_after_mutation
import random
import struct
import numpy as np
import sys

data1 = [
        [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
        [[11.0, 22.0, 33.0], [44.0, 55.0, 66.0], [77.0, 88.0, 99.0]],
        [[12.0, 23.0, 34.0], [45.0, 56.0, 67.0], [78.0, 89.0, 90.0]]
        ]
data2 = [
        [[-1.0, -2.0, -3.0], [-4.0, -5.0, -6.0], [-7.0, -8.0, -9.0]],
        [[-11.0, -22.0, -33.0], [-44.0, -55.0, -66.0], [-77.0, -88.0, -99.0]],
        [[-12.0, -23.0, -34.0], [-45.0, -56.0, -67.0], [-78.0, -89.0, -90.0]]
        ]
#
# print("原始数据：", data)
# data = data_conversions.double_to_byte(data)
# print("转为bytes:", data)
#
# data = mutate_functions.do_mutate(data)
# print("变异后数据:", data)
#
# data = process_mutations_by_bytes.process_insert_bytes(data)
# print("处理后数据：", data)
#
# data = data_conversions.byte_to_double(data)
# print(data)
# im1 = np.random.uniform(low=0.0, high=1.0, size=(360, 480, 3)).tolist()
corpus = [data1, data2]
# corpus = [im1]
data = random.choice(corpus)
print("原始数据：", data)
# data = data_conversions.double_to_byte(data)
data = data_conversions.converse(data, data_conversions.double_to_byte)
print("转为byte：", data)
# data = mutate_functions_by_bytes.do_mutate(data)
# print(data)
# print(len(data[0][0][0]))

# data = mutate_functions_by_bytes.mutate_for_li(data, mutate_functions_by_bytes.do_mutate)
data = mutate_functions_by_bytes.do_mutate(data, low_num=1, high_num=5)
print("变异后的数据：", data)

# print(len(data))
# print(len(data[0]))
# print(len(data[0][0]))
data = process_after_mutation.process(data)
print("处理后的数据：", data)



data = data_conversions.converse(data, data_conversions.byte_to_double)
print("最后转为double：", data)
#
# data = process_mutations.process_insert_bytes(data)
# print(data)
# data = data_conversions.byte_to_double(data)
# print(data)

# print(type(mutate_functions_by_bytes.get_random_byte()))
# print(struct.pack('>d', float(mutate_functions_by_bytes.get_random_byte())))

