import random
import struct
import string
from utils import data_conversions
from utils import process_after_mutation
import numpy as np

#  随机减少字节
def mutate_erase_bytes(data):
    '''
    随机删除字节
    :param data:
    :return:
    '''
    if len(data) == 0:
        return data
    idx = random.randrange(len(data))
    return data[idx:random.randrange(idx, len(data))]

# 随机插入字节
def mutate_insert_bytes(data):
    '''
    随机删除字节
    :param data:
    :return:
    '''
    if len(data) == 0:
        return data
    idx = random.randrange(len(data))
    new_bytes = get_random_bytes(random.randrange(1, 5))
    return data[:idx] + new_bytes + data[idx:]

# 插入重复字节
def mutate_insert_repeated_bytes(data):
    '''
    插入重复字节
    :param data:
    :return:
    '''
    if len(data) == 0:
        return data
    data = bytearray(data)
    idx = random.randrange(len(data))
    new_byte = get_random_byte()
    sz = random.randrange(5)
    data[idx:idx + sz] = bytes(new_byte) * sz
    data = bytes(data)
    return data


def get_random_bytes(size):
    return bytearray(random.getrandbits(8) for _ in range(size))


def get_random_byte():
    return random.getrandbits(8)

# 随机改变字节
def mutate_change_byte(data):
    '''
    随机改变字节
    :param data:
    :return:
    '''
    if len(data) == 0:
        return data
    data = bytearray(data)
    idx = random.randrange(len(data))
    data[idx] = get_random_byte()
    data = bytes(data)
    return data

# 改变bit
def mutate_change_bit(data):
    '''
    改变bit
    :param data:
    :return:
    '''
    data = bytearray(data)
    idx = random.randrange(len(data))
    data[idx] ^= 1 << random.randrange(8)
    data = bytes(data)
    return data

def mutate_change_ascii_integer(data):
    '''
    :param data:
    :return:
    '''
    data = bytearray(data)
    start = random.randrange(len(data))
    while start < len(data) and chr(data[start]) not in string.digits:
        start += 1
    if start == len(data):
        return bytes(data)

    end = start
    while end < len(data) and chr(data[end]) in string.digits:
        end += 1

    value = int(data[start:end])
    choice = random.randrange(5)
    if choice == 0:
        value += 1
    elif choice == 1:
        value -= 1
    elif choice == 2:
        value //= 2
    elif choice == 3:
        value *= 2
    elif choice == 4:
        value *= value
        value = max(1, value)
        value = random.randrange(value)
    else:
        assert False

    to_insert = bytes(str(value), encoding='ascii')
    data[start:end] = to_insert
    data = bytes(data)
    return data

# def mutate_for_li(li, target_mutation_function):
#
#     for i in range(len(li)):
#         for j in range(len(li[0])):
#             for k in range(len(li[0][0])):
#                 li[i][j][k] = target_mutation_function(li[i][j][k])
#     return li

def mutate_for_li(li, target_mutaion_function):
    '''

    :param li:
    :param target_mutaion_function: 具体的变异方法
    :return:
    '''
    return target_mutaion_function(li)

# 变异
def do_mutate(li, low_num=1, high_num=5):
    '''
    变异次数以及每次变异的方法
    :param li:
    :param low_num:
    :param high_num:
    :return:
    '''
    num_mutations = random.randrange(low_num, high_num)  # 变异次数
    for _ in range(num_mutations):

        choice = random.randrange(4)
        if choice == 0:
            li = mutate_for_li(li, mutate_erase_bytes)
        elif choice == 1:
            li = mutate_for_li(li, mutate_insert_bytes)
        elif choice == 2:
            li = mutate_for_li(li, mutate_change_byte)
        elif choice == 3:
            li = mutate_for_li(li, mutate_insert_repeated_bytes)
        elif choice == 4:
            li = mutate_for_li(li, mutate_change_bit)
        elif choice == 5:
            li = mutate_for_li(li, mutate_change_ascii_integer)
        else:
            assert False
    return li

# 整个变异过程，返回变异后的数据
def mutate(li, prob1=0.2, prob2=0.2, prob3=0.1):
    '''
    :param li: 待变异的数据
    :param prob1:变异概率---->决定是否变异
    :param prob2:变异概率
    :param prob3:变异概率
    :return:
    '''
    if isinstance(li, np.ndarray):
        li = li.tolist()
    # count = 0
    for i in range(len(li)):
        # if not random.choice([False, True]):
        # if random.choice([0, 1, 2, 3, 4]) != 0:
        if random.random() > prob1:
            continue
        for j in range(len(li[0])):
            # if not random.choice([False, True]):
            # if random.choice([0, 1, 2, 3, 4]) != 0:
            if random.random() > prob2:
                continue
            for k in range(len(li[0][0])):
                if random.random() < prob3:
                    # count += 1
                    data = li[i][j][k]
                    # 转化为byte
                    data = data_conversions.converse(data, data_conversions.float_to_byte)
                    # 变异
                    data = do_mutate(data, low_num=1, high_num=3)
                    # 处理
                    data = process_after_mutation.process(data)
                    # 转为double类型
                    data = data_conversions.converse(data, data_conversions.byte_to_float)
                    li[i][j][k] = data
    # print(count)
    if not isinstance(li, np.ndarray):
        li = np.array(li)
    li = np.clip(li, a_min=0.0, a_max=1.0)
    return li


def mutate_batches(li, size=10,  prob1=0.2, prob2=0.2, prob3=0.1):
    results = []
    for i in range(size):
        result = mutate(li, prob1, prob2, prob3)
        results.append(result)
    return results


def do_basic_mutations(data, a_min=0.0, a_max=1.0):
    '''
    添加白噪音
    :param data:
    :param a_min:
    :param a_max:
    :return:
    '''
    sigma = 0.5
    noise = np.random.normal(size=data.shape, scale=sigma)

    mutated_image = noise + data

    mutated_image = np.clip(
        mutated_image, a_min=a_min, a_max=a_max
    )
    return mutated_image