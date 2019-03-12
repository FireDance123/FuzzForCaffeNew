import hashlib
import logging
import random
import string
import time
from collections import defaultdict
from pathlib import Path
import coverage
import os
os.environ['GLOG_minloglevel'] = '2'
import caffe
from utils import mutate_functions_by_bytes


class shouldTrace:
    trace = True

    def __init__(self, filename):
        self.source_filename = filename


class Tracer(coverage.PyTracer):

    def __init__(self):
        super().__init__()
        self.trace_arcs = True

        def should_trace(filename, frame):
            res = shouldTrace(filename)
            if filename == 'fuzzer.py':
                res.trace = False
            return res

        self.data = {}
        self.trace = None
        self.should_trace = should_trace
        self.should_trace_cache = {}

    @property
    def edges(self):
        return self.data


#  模糊测试器
class Fuzzer:

    def __init__(self, target, corpus_dir):
        '''
        :param target: 待测方法
        :param corpus_dir:语料库目录
        '''
        self.target = target
        self.corpus = []
        self.corpus_dir = corpus_dir
        self.edges = defaultdict(set)

        to_import = list(corpus_dir.iterdir())
        # 导入原始corpus
        for path in to_import:
            try:
                self.import_testcase(path)
            except Exception as exc:
                print("{} crashes `{}`, please fix.".format(path, path.read_bytes()))
                raise exc

        if not to_import:  # 没有原始语料库
            logging.error("No corpus found")
            exit()

        if not self.edges:  # 没有覆盖信息
            logging.error("No coverage found!")
            exit()
        # print(len(self.corpus))
        print('-------------初始化完成------------------')
    def import_testcase(self, path):
        '''
        导入原始测试用例
        :param path:
        :return:
        '''
        testcase = caffe.io.load_image(path)
        self.test_one_input(testcase)

    # 将数据投入待测方法运行
    def get_edges_from_input(self, data):
        '''
        将数据投入待测方法运行
        :param data:
        :return:
        '''
        tracer = Tracer()
        tracer.start()
        crashed = None
        try:
            self.target(data)
        except Exception as exc:
            crashed = exc
            # self.write_crash_to_disk(data)
            raise exc
        tracer.stop()
        return tracer.edges, crashed

    # 判断是否为新覆盖
    def test_one_input(self, data):
        '''
        判断是否为新覆盖
        :param data:
        :return:
        '''
        trace_edges, _ = self.get_edges_from_input(data)
        # print(trace_edges)
        has_new = False
        for name, edges in trace_edges.items():
            if edges is None:
                continue
            edges = set(edges)
            if edges - self.edges[name]:
                has_new = True
            self.edges[name] |= edges
        if has_new:
            self.corpus.append(data)
            # self.write_to_disk(bytes(data))
        return has_new

    def write_to_disk(self, data):
        name = hashlib.sha1(data).hexdigest()
        dest = self.corpus_dir.joinpath(name)
        if not dest.exists():
            dest.write_bytes(data)
    def write_crash_to_disk(self, data):
        '''
        将异常写入磁盘
        :param data:
        :return:
        '''
        name = 'crash-' + hashlib.sha1(data).hexdigets()
        dest = self.corpus_dir.joinpath(name)
        if not dest.exists():
            print("Writing crash to {}...".format(dest))
            dest.write_bytes(data)

    def generate_input(self):
        assert self.corpus
        # 选择数据变异
        data = random.choice(self.corpus)
        mutated_data = mutate_functions_by_bytes.mutate(data)
        return mutated_data

    def print_status(self, info, num_execs, start):
        '''
        打印状态
        :param info:
        :param num_execs:
        :param start:
        :return:
        '''
        elapsed = max(int(time.time() - start), 1)
        exec_s = num_execs // elapsed
        cov = sum(len(edges) for edges in self.edges.values())
        print('#{} {} cov: {} corpus: {} exec/s: {}'.format(
            num_execs, info, cov, len(self.corpus), exec_s))

    def print_pulse(self, num_execs, start):
        self.print_status("pulse", num_execs, start)

    def print_new(self, num_execs, start):
        self.print_status("new", num_execs, start)

    def fuzz(self):
        '''
        执行模糊测试
        :return:
        '''
        num_execs = 0  # 执行次数
        start = time.time()  # 开始时间
        while True:
            data = self.generate_input()  # 获取数据
            has_new = self.test_one_input(data)
            if has_new:
                self.print_new(num_execs, start)
            elif bin(num_execs).count('1') == 1:
                self.print_pulse(num_execs, start)
            num_execs += 1
