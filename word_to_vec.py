import numpy as np
from gensim.models import word2vec
#from tqdm import tqdm
import os


def build_wordvec(vocab_list, size, model=None):
    if model is None:
        model = word2vec.Word2Vec.load('word2vec/word2vec.model')
    vec_feature = []
    for text in vocab_list:
        vec = np.zeros(size).reshape((1, size))
        count = 0
        for word in text:
            try:
                vec += model[word].reshape((1, size))
                count += 1
            except KeyError:
                continue
        if count != 0:
            vec /= count

        vec_feature.append(vec.tolist()[0])

    return vec_feature


def word2vec_model(vocab_list, dim):
    if os.path.exists('word2vec/corpus.txt'):
        os.remove('word2vec/corpus.txt')
    for i in range(len(vocab_list)):
        open('word2vec/corpus.txt', 'a+', encoding='utf-8').write(vocab_list[i] + '\n')
    model = word2vec.Word2Vec(word2vec.LineSentence('word2vec/corpus.txt'), size=dim, min_count=3)
    model.save('word2vec/word2vec.model')

    return model
