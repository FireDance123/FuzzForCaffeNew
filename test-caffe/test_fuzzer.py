from pathlib import Path
from fuzzer.fuzzer import Fuzzer
from utils.compute import compute
from fuzzer.new_fuzzer import Fuzzer
from utils.coverage_functions import absolute_coverage_function
from utils.sample_functions import uniform_sample_function
from utils.mutate_functions_by_bytes import mutate
from utils.mutate_functions_by_bytes import mutate_batches
from utils.mutate_functions_by_bytes import mutate_batches

from utils.mutate_functions_by_bytes import do_basic_mutations
from utils.corpus import generate_seed_corpus
from utils.corpus import InputCorpus

if __name__ == '__main__':
    # fuzzer = Fuzzer(target=compute, corpus_dir=Path('corpus'))
    # fuzzer.fuzz()

    # 待测方法
    target = compute
    # corpus目录
    corpus_dir = Path('corpus')
    # 覆盖方法
    coverage_function = absolute_coverage_function
    # 采样方法
    sample_function = uniform_sample_function
    # 变异方法
    mutatation_function = mutate
    # mutatation_function = mutate_batches
    # mutatation_function = do_basic_mutations

    seed_corpus = generate_seed_corpus(corpus_dir=corpus_dir, target=target, coverage_function=coverage_function)

    input_corpus = InputCorpus(seed_corpus=seed_corpus, sample_function=sample_function, threshold=10, algorithm='kdtree')

    # 模糊测试器
    fuzzer = Fuzzer(target=target, input_corpus=input_corpus, coverage_function=coverage_function, mutation_function=mutatation_function)
    fuzzer.fuzz()

    # new_corpus_elements = fuzzer.generate_inputs()
    # fuzzer.test_inputs(new_corpus_elements)
