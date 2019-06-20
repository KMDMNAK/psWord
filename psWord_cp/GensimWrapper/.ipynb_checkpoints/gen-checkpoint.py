import gensim

def get_model():
    return gensim.models.KeyedVectors.load_word2vec_format("model.vec")