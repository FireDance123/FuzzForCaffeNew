import random

def uniform_sample_function(input_corpus):
    '''
    每个元素被选中的概率相同
    :param input_corpus:
    :return:
    '''
    result = random.choice(input_corpus.corpus)
    # print(result)
    return random.choice(input_corpus.corpus)
    # return result

def recent_sample_function(input_corpus):
    corpus = input_corpus.corpus
    reservoir = corpus[-5:] + [random.choice(corpus)]
    choiced = random.choice(reservoir)
    # return random.choice(reservoir)
    print(choiced)
    return choiced
