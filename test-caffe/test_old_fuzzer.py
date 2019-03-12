import os
os.environ['GLOG_minloglevel'] = '2'
from utils.compute import compute
from fuzzer.fuzzer import Fuzzer
from pathlib import Path



if __name__ == '__main__':
    fuzzer = Fuzzer(compute, Path('corpus'))
    fuzzer.fuzz()
