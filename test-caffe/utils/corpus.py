import time
import numpy as np
import pyflann
import caffe
import logging

_BUFFER_SIZE = 50

class CorpusElement(object):

    def __init__(self, data, output,  coverage, parent):
        self.data = data
        self.output = output
        self.coverage = coverage
        self.parent = parent

    def oldest_ancestor(self):
        current_element = self
        generations = 0
        while current_element.parent is not None:
            current_element = current_element.parent
            generations += 1
        return current_element, generations


class InputCorpus(object):

    def __init__(self, seed_corpus, sample_function, threshold, algorithm):

        self.mutations_processed = 0
        self.corpus = []
        self.sample_function = sample_function
        self.start_time = time.time()
        self.current_time = time.time()
        self.log_time = time.time()
        self.updater = Updater(threshold, algorithm)

        for corpus_element in seed_corpus:
            self.corpus.append(corpus_element)
        self.updater.build_index_and_flush(self)

    def maybe_add_to_corpus(self, element):
        self.mutations_processed += 1
        return self.updater.updata_function(self, element)

        # current_time = time.time()

    def sample_input(self):
        return self.sample_function(self)
class Updater(object):

    def __init__(self, threshold, algorithm):
        self.flann = pyflann.FLANN()
        self.threshold = threshold
        self.algorithm = algorithm
        self.corpus_buffer = []
        self.lookup_array = []

    def build_index_and_flush(self, corpus_object):

        self.corpus_buffer[:] = []
        self.lookup_array = np.array(
            [element.coverage for element in corpus_object.corpus]
        )

        self.flann.build_index(self.lookup_array, algorithm=self.algorithm)

    def updata_function(self, corpus_object, element):

        if corpus_object.corpus is None:
            corpus_object.corpus = [element]
            self.build_index_and_flush(corpus_object)
        else:

            _, approx_distance = self.flann.nn_index(
                np.array([element.coverage]), 1, algorithm=self.algorithm
            )

            exact_distances = [
                np.sum(np.square(element.coverage - buffer_elt))
                for buffer_elt in self.corpus_buffer
            ]
            nearest_distance = min(exact_distances + approx_distance.tolist())
            has_new = False
            if nearest_distance > self.threshold:
                corpus_object.corpus.append(element)
                self.corpus_buffer.append(element.coverage)
                if len(self.corpus_buffer) >= _BUFFER_SIZE:
                    self.build_index_and_flush(corpus_object)
                has_new = True
            return has_new


def seed_corpus(inputs, target, coverage_function):

    seed_corpus = []
    for input in inputs:
        # output = target(input)
        output = target(input)[0]
        shape_length = len(output.shape)
        # print(shape_length)
        # print(output.shape[0])
        # print(output)
        coverage = coverage_function(output, shape_length)
        # print(coverage)
        new_element = CorpusElement(data=input, output=output, coverage=coverage, parent=None)
        seed_corpus.append(new_element)
    return seed_corpus

def generate_seed_corpus(corpus_dir, target, coverage_function):

    to_import = list(corpus_dir.iterdir())
    if not to_import:
        logging.error('No corpus found')
        exit()
    inputs = []
    for path in to_import:
        inputs.append(import_testcase(path))

    seed_corpus = []
    for input in inputs:
        # output = target(input)
        output = target(input)[0]
        shape_length = len(output.shape)
        coverage = coverage_function(output, shape_length)
        new_element = CorpusElement(data=input, output=output, coverage=coverage, parent=None)
        seed_corpus.append(new_element)
    return seed_corpus

def import_testcase(path):
    testcase = caffe.io.load_image(path)
    return testcase