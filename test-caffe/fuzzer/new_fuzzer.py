import hashlib
import logging
import random
import string
import time
from collections import defaultdict
from pathlib import Path
import coverage
# import os
# os.environ['GLOG_minloglevel'] = '2'
import caffe
from utils import mutate_functions_by_bytes
from utils.corpus import seed_corpus
from utils.corpus import InputCorpus
from utils.coverage_functions import absolute_coverage_function
from utils.sample_functions import uniform_sample_function
from utils.corpus import CorpusElement
from utils.corpus import seed_corpus
import numpy as np

class Fuzzer:
    def __init__(self, target, input_corpus, coverage_function, mutation_function):
        '''
        :param target: 待测方法
        :param corpus_dir:语料库目录
        '''
        self.target = target
        # self.corpus_dir = corpus_dir
        self.coverage_funcntion = coverage_function
        # self.sample_function = sample_function
        self.mutation_function = mutation_function
        self.edges = defaultdict(set)
        self.input_corpus = input_corpus
        self.crashes = 0
        print('初始化完成, 当前corpus数量:', len(self.input_corpus.corpus))


    # 判断是否为新覆盖
    def test_one_input(self, corpus_element):
        '''
        判断是否为新覆盖
        :param data:
        :return:
        '''
        data = corpus_element.data
        # output = self.target(data)
        # print('-------------------data--------------------')
        # print(data)
        outputs = self.target(data)
        output = outputs[0]
        # print('------------------------output----------------------')
        # print(output)
        coverage = self.coverage_funcntion(output, len(output.shape))
        # print('-----------------------coverate-------------------------------------')
        # print(coverage)
        # print(coverage[0])
        if np.isnan(coverage[0]):
            self.crashes += 1
        corpus_element.coverage = coverage
        corpus_element.output = output
        has_new = self.input_corpus.maybe_add_to_corpus(corpus_element)
        # print(corpus_element.output)
        return has_new

    def test_inputs(self, corpus_elemets):
        has_new = False
        data_batches = []
        for corpus_elemet in corpus_elemets:
            data_batches.append(corpus_elemet.data)
        data_batches = np.array(data_batches)

        outputs = self.target(data_batches)
        for i in range(len(corpus_elemets)):
            coverage = self.coverage_funcntion(outputs[i], len(outputs[i].shape))
            print(coverage)
            corpus_elemets[i].coverage = coverage
            corpus_elemets[i].output = outputs[i]
            has_new = self.input_corpus.maybe_add_to_corpus(corpus_elemets[i])
            if has_new:
                has_new = True
        return has_new
    # def write_to_disk(self, data):
    #     name = hashlib.sha1(data).hexdigest()
    #     dest = self.corpus_dir.joinpath(name)
    #     if not dest.exists():
    #         dest.write_bytes(data)
    #
    # def write_crash_to_disk(self, data):
    #     '''
    #     将异常写入磁盘
    #     :param data:
    #     :return:
    #     '''
    #     name = 'crash-' + hashlib.sha1(data).hexdigets()
    #     dest = self.corpus_dir.joinpath(name)
    #     if not dest.exists():
    #         print("Writing crash to {}...".format(dest))
    #         dest.write_bytes(data)

    def generate_input(self):
        assert self.input_corpus.corpus
        # 选择数据变异
        # corpus_element = self.sample_function(self.input_corpus)
        corpus_element = self.input_corpus.sample_input()
        # print('-----------------------原始data-----------------------------')
        # print(corpus_element.data)
        mutated_data = self.mutation_function(corpus_element.data)
        new_corpus_element = CorpusElement(data=mutated_data, coverage=None, output=None, parent=corpus_element)
        # print(new_corpus_element.data[0][0])
        return new_corpus_element

    def generate_inputs(self, size=10):
        assert self.input_corpus.corpus

        corpus_element = self.input_corpus.sample_input()

        mutated_data_batches = self.mutation_function(corpus_element.data, size=size)
        new_corpus_elements = []
        for i in range(size):
            new_corpus_element = CorpusElement(data=mutated_data_batches[i], coverage=None, output=None, parent=corpus_element)
            new_corpus_elements.append(new_corpus_element)

        return new_corpus_elements


    def fuzz(self):
        '''
        执行模糊测试
        :return:
        '''
        start_time = time.time()
        num_execs = 0  # 执行次数
        while num_execs < 120:
            corpus_element = self.generate_input()  # 获取数据
            has_new = self.test_one_input(corpus_element)
            # new_corpus_elements = self.generate_inputs()
            # has_new = self.test_inputs(new_corpus_elements)
            # if has_new:
                # print('新覆盖, 当前corpus数量:', len(self.input_corpus.corpus))
            # else:
                # print('无新覆盖, 当前corpus数量：', len(self.input_corpus.corpus))
                # print(len(self.input_corpus.corpus))
            num_execs += 1
        print('耗时：', time.time() - start_time)
        print('crash数量：', self.crashes)
