import gensim

def getModel(dictionary_pass):
    """
        get word's vector from the dictionary
    """
    return gensim.models.KeyedVectors.load_word2vec_format(dictionary_pass)
