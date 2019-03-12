import numpy as np


def absolute_coverage_function(output, shape_length):
    '''
    基于输出值得绝对值之和计算覆盖
    :param coverages_batches:
    :return:
    '''
    coverage = 0
    if shape_length == 1:
        for idx in range(output.shape[0]):
            coverage += np.abs(output[idx])
    elif shape_length == 3:
        for i in range(output.shape[0]):
            for j in range(output.shape[1]):
                for k in range(output.shape[2]):
                    coverage += np.abs(output[i][j][k])

    return np.array([coverage])

def raw_coverage_function(output, shape_length):
    coverage = 0
    if shape_length == 1:
        for idx in range(output.shape[0]):
            coverage += output[idx]
    elif shape_length == 3:
        for i in range(output.shape[0]):
            for j in range(output.shape[1]):
                for k in range(output.shape[2]):
                    coverage += output[i][j][k]
    return np.array([coverage])




