import numpy as np
import random
import struct

#  随机减少字节
def mutate_erase_bytes(data):
    idx = random.randrange(len(data))
    # print(len(data))
    # print('index is: ', idx)
    return data[idx:random.randrange(idx, len(data))]
# 随机插入字节
def mutate_insert_bytes(data):
    idx = random.randrange(len(data))
    new_bytes = get_random_bytes(random.randrange(1, 5))
    return data[:idx] + new_bytes + data[idx:]
# 插入重复字节
def mutate_insert_repeated_bytes(data):
    idx = random.randrange(len(data))
    new_byte = get_random_byte()
    sz = random.randrange(16)
    data[idx:idx + sz] = bytearray(new_byte) * sz
    return data


def get_random_bytes(size):
    # Use random here so we can fix the seed for tests.
    return bytearray(random.getrandbits(8) for _ in range(size))


def get_random_byte():
    return random.getrandbits(8)
# 随机改变字节
def mutate_change_byte(self, data):
    idx = random.randrange(len(data))
    data[idx] = self.get_random_byte()
    return data
# 改变bit
def mutate_change_bit(data):
    idx = random.randrange(len(data))
    data[idx] ^= 1 << random.randrange(8)
    return data


# im1 = np.random.uniform(low=0.0, high=1.0, size=(360, 480, 3))
def int_to_byte(li):
    for i in range(len(li)):
        for j in range(len(li[0])):
            for k in range(len(li[0][0])):
                # print(li[i][j][k])
                # print(bytes(li[i][j][k]))
                li[i][j][k] = bytes([li[i][j][k]])
    return li

def byte_to_int(li):
    for i in range(len(li)):
        for j in range(len(li[0])):
            for k in range(len(li[0][0])):
                # print(li[i][j][k])
                # print(bytes(li[i][j][k]))
                li[i][j][k] = int.from_bytes(li[i][j][k], byteorder='little', signed=True)
    return li

def float_to_byte(li):
    for i in range(len(li)):
        for j in range(len(li[0])):
            for k in range(len(li[0][0])):
                li[i][j][k] = struct.pack('>f', li[i][j][k])
    return li

def byte_to_float(li):
    for i in range(len(li)):
        for j in range(len(li[0])):
            for k in range(len(li[0][0])):
                li[i][j][k] = struct.unpack('>f', li[i][j][k])[0]
    return li

def double_to_byte(li):
    for i in range(len(li)):
        for j in range(len(li[0])):
            for k in range(len(li[0][0])):
                li[i][j][k] = struct.pack('>d', li[i][j][k])
    return li

def byte_to_double(li):
    for i in range(len(li)):
        for j in range(len(li[0])):
            for k in range(len(li[0][0])):
                li[i][j][k] = struct.unpack('>d', li[i][j][k])[0]
    return li

def do_mutate(li):
    for i in range(len(li)):
        for j in range(len(li[0])):
            for k in range(len(li[0][0])):
                # print(type(li[i][j][k]))
                li[i][j][k] = mutate_insert_bytes(li[i][j][k])
                # print(len(li[i][j][k]))
                # idx = random.randrange(len(li[i][j][k]))
                # while idx + 4 > len(li[i][j][k]):
                #     idx = random.randrange(len(li[i][j][k]))
                # li[i][j][k] = li[i][k][k][idx: idx + 5]
    return li

def process_insert_bytes(li):
    for i in range(len(li)):
        for j in range(len(li[0])):
            for k in range(len(li[0][0])):
                result = bytes()
                data = li[i][j][k]
                # print(data)
                # print(len(data))
                idx = random.randrange(len(data))
                while idx + 8 > len(data):
                    idx = random.randrange(len(data))
                # print('idx:', idx)
                # for start in range(idx, idx+8):
                for index in range(0, 8):
                    # print(start)
                    result += bytes([data[index]])
                # print(len(result))
                li[i][j][k] = result
    # idx = random.randrange(start=1, stop=len(data))
    # while idx + 4 > len(data):
    #     idx = random.randrange(start=1, stop=len(data))
    # result = bytes()
    # for i in range(idx, idx+4):
    #     result += bytes([data[i]])
    # return result
    return li

data = [
        [[-1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
        [[11.0, 22.0, 33.0], [44.0, 55.0, 66.0], [77.0, 88.0, 99.0]],
        [[12.0, 23.0, 34.0], [45.0, 56.0, 67.0], [78.0, 89.0, 90.0]]
        ]

print("原始数据：", data)
data = double_to_byte(data)
print("转为bytes:", data)

data = do_mutate(data)
print("变异后数据:", data)

data = process_insert_bytes(data)
print("处理后数据：", data)

data = byte_to_double(data)
print(data)

# d = 1.5
# d = struct.pack('>d', d)
# print(len(d))
# d = struct.unpack('>d', d)[0]
# print(type(d))