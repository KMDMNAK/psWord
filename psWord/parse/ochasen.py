"""
    this function aim to Only Japanese Documents!!
"""
import MeCab
from . import language
import re

def getOchasen(documents,dictionary_location=None):
    """
        return each sentence's ochasen(word property)
        
        UsedMethods
            sentence_ochasen
            document2sentences
    """
    language_sign="ja"
    dictionary_String=""
    if(dictionary_location!=None):
        dictionary_String="-d {0}".format(dictionary_location)
    handler=language.getHandler(language_sign,tagger=MeCab.Tagger("{0} -Ochasen".format(dictionary_String)))
    
    all_ochasen_list=[]
    c=1
    for document in documents:
        ochasen_list=[]
        sentences=handler.extractSentences(document)
        #print(sentences)
        document_ochasen_list=[]
        for sentence in sentences:
            sentence_ochasen=handler.extractWords(sentence)[0]#[0]は文字列化のため
            sentences_ochasen_list=[]
            for word_property in sentence_ochasen.split("\n")[:-2]:#-2はEOSと空列の除去のため
                sentences_ochasen_list.append(word_property.split("\t"))
            #print(sentences_ochasen_list)
            document_ochasen_list.append(sentences_ochasen_list)
        all_ochasen_list.append(document_ochasen_list)
    return all_ochasen_list

def getSentenceOchasen(ochasened_documents):
    """
        return splited MeCab owakati list
    """
    ochasened_split_documents=[]
    for ochasened_sentence in ochasened_documents:
        for w in ochasened_sentence:
            ochasened_split_sentence=[]
            for each_ochasened_word in w.split("\n"):
                ochasened_split_sentence.append(each_ochasened_word.split("t"))
        ochasened_split_documents.append(ochasened_split_sentence[:-2])
    return ochasened_split_documents

def getSpecificWord(document_ochasens,pattern,negative,word_index=2,class_index=3):
    """
        Parameters
        ____
            negative : 指定した品詞に該当しない単語をreturn
            word_index : 活用前の単語を取得
            class_index : 品詞の種類を取得
        ____
        助詞以外のwordを取得する.
        単語は活用前を取得する.(index=2)
        品詞:index=3
    """
    documents=[]
    for document in document_ochasens:
        sentences=[]
        for sentence in document:
            words=[]
            for word in sentence:
                isMatched=(re.search(pattern,word[class_index])!=None)
                if(negative&isMatched):
                    continue
                elif((not negative)&(not isMatched)):
                    continue
                words.append(word[word_index])
            sentences.append(words)
        documents.append(sentences)
    return documents

def getProperNoun(document_ochasens):
    """
        固有名詞の抽出
    """
    return getSpecificWord(document_ochasens,r'名詞-一般|固有名詞|名詞-.*?接続',negative=False)
def getNonJoshi(document_ochasens):
    return getSpecificWord(document_ochasens,r'助.*?詞|連体詞|非自立|記号|数',negative=True)
