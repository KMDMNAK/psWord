import MeCab
from collections import defaultdict
from Scraping_tool import tag_search as xml

import requests
import re

#sorted(frequency.items(),key=lambda x:-x[1])



def getWordFrequency(documents,allword=True,language='ja'):
    """
    return how many times each word appear in documents.
    if allword is false , return 

    Args
    ____
        documents(one-D str list):
        language(str):ja,en
        allword(boolean): whether it return each frequency of each document
    ____
    
    Returns
    ____
        frequency :
        nostopword_documents :
    ____
    """
    
    tagger=MeCab.Tagger("-Owakati")
    
    #this contain word list of each document without stop words.
    nostopword_documents=[]
    for document in documents:
        nostopword_sentences=[]
        sentences=document2sentences(document,language)
        for sentence in sentences:
            nostop_words=[]
            # extracting words depend on language
            
            #____AB TEST_____
            
            """for word in tagger.parse(sentence).split(" ") if(language=='ja') else sentence.split(" "):
                #whether word isn't a single Kanji
                if(((len(word)>1)|(re.search('[\u4E00-\u9FD0]',word)!=None))&(not word in stop_words)):
                    nostop_words.append(word)
            nostopword_sentences.append(nostop_words)"""
            #____END A
            if(language=="ja"):
                stop_words=JAPANESE_STOP_WORDS
            for word in tagger.parse(sentence).split(" ") if(language=='ja') else sentence.split(" "):
                #whether word isn't a single Kanji
                if((len(word)>0)&(not word in stop_words)):
                    nostop_words.append(word)
            nostopword_sentences.append(nostop_words)
            #____END B
            
            #___END TEST___
        nostopword_documents.append(nostopword_sentences)
        
    frequency=[defaultdict(int) for w in range(len(documents))]
    for nostopword_document,each_frequency in zip(nostopword_documents,frequency):
        for sentence in nostopword_document:
            for word in sentence:
                each_frequency[word]+=1
    #frequency=sorted(frequency.items(),key=lambda x:-x[1])
    if(allword):
        frequency=convert2AllWordsFrequency(frequency)
        frequency=sorted(frequency.items(),key=lambda x:-x[1])
    return frequency,nostopword_documents

def getFrequency(ochasened_documents,allword=True,language='ja'):
    """
    """
    frequency=[defaultdict(int) for w in range(len(ochasened_documents))]
    for nostopword_document,each_frequency in zip(ochasened_documents,frequency):
        for sentence in nostopword_document:
            for word in sentence:
                each_frequency[word]+=1
    if(allword):
        frequency=convert_wordfrequency(frequency)
        frequency=sorted(frequency.items(),key=lambda x:-x[1])
    return frequency

def document2sentences(document,language):
    """
        split document to each sentences
        
        Return
        ______
            sentences(2-D string list)
        ______
        
    """
    if(language in JAPANESE):
        sentences=re.split(r'。|\n',document)

        #ToDo 括弧内の。では区切らないようにする必要がある.
        """
        #if(document.find("「")!=-1):
        kakko=0
        for w in range(len(sentences)):
            if("「" in sentences[w]):
                if(kakko==0):
                    start_index=w
                kakko+=1
            if("」" in sentences[w]):
                kakko-=1
                end_index=w
                if((kakko==0)&(start_index!=end_index)):
                    str_=""
                    for index in range(start_index+1,end_index+1):
                        str_+="。"+sentences[w]
                        del(sentences[w])
                    sentences[start_index]+=str_"""
    elif(language in ENGLISH):
        sentences=re.split(".",document)
    return sentences

def convert2AllWordsFrequency(frequencies):
    """
        this convert each document's frequency into all word frequency
        
        Args
        _____
            each_frequency (2-D dict list)
        _____
        
    """
    #{word1:count(int),word2:count(int)...}
    frequency={}
    for each_frequency in frequencies:
        for each_key in each_frequency.keys():
            isEmpty=(frequency.get(each_key)==None)
            if(isEmpty):
                frequency[each_key]=each_frequency[each_key]
                continue
            frequency[each_key]+=each_frequency[each_key]
    return frequency

def getOchasen(documents,language="jp"):
    """
        return each sentence's ochasen(word property)
        
        UsedMethods
            sentence_ochasen
            document2sentences
    """
    ochasen_lists=[]
    for document in documents:
        ochasen_list=[]
        sentences=document2sentences(document,language)
        for sentence in sentences:
            content=sentence_ochasen(sentence)
            if(content==[]):
                continue
            ochasen_list.append(content)
        ochasen_lists.append(ochasen_list)
    return ochasen_lists

tagger= MeCab.Tagger ("-Ochasen")
def sentence_ochasen(sentence):
    """
        return splited MeCab owakati list
    """
    
    ochasen_sentence=tagger.parse(sentence)
    ochasen_list=[]
    for each_owakati in re.split(r'\n',ochasen_sentence):
        ochasen_list.append(re.split(r'\t',each_owakati))
    return ochasen_list[:-2]

def get_specificword(document_ochasen,pattern,negative):
    """
        助詞以外のwordを取得する.
        単語は活用前を取得する.(index-2)
        品詞:index-3
    """
    documents=[]
    for document in document_ochasen:
        sentences=[]
        for sentence in document:
            words=[]
            for word in sentence:
                hinshi=re.search(pattern,word[3])
                if(negative&(hinshi!=None)):
                    continue
                elif((not negative)&(hinshi==None)):
                    continue
                words.append(word[2])
            sentences.append(words)
        documents.append(sentences)
    return documents

def get_pronoun(document_ochasen):
    return get_specificword(document_ochasen,r'名詞-一般|固有名詞|名詞-.*?接続',negative=False)
def get_nojoshi(document_ochasen):
    return get_specificword(document_ochasen,r'助.*?詞|連体詞|非自立|記号|数',negative=True)

import googletrans
def get_transtext(text,dest):
    """
        dest in ["ja","en"]
    """
    translator=googletrans.Translator()
    return translator.translate(text,dest=dest).text

def owakati_rss(url,language='ja'):
    """
    Args
    ____
        language 'ja','en'
    ____
    """
    
    get=req.get(url)
    get.encoding=get.apparent_encoding
    html=get.text
    del(get)
    
    item=xml.get_eachtag(html,"item",["title"],only_text=False)
    check,list_num=item,0#n重リストかを判定する.
    """while(type(check)==list):
        list_num+=1
        check=check[-1]
    for w in list_num:
        pass
    """
    for w in range(len(item)):
        item[w]=item[w][0]
    
    print(item)
    return get_list(item,language=language)

def dependency_parse(documents):
    ochasen_documents=get_ochasen(documents)
    for ochasen_sentences in ochasen_documents:
        for ochasen_sentence in ochasen_sentences:
            dependency_sentence(ochasen_sentence)
            
def dependency_sentence(ochasened_sentence):
    """助詞だけをまず抜き出す."""
    
    print("dep:",ochasened_sentence)
    str_=""
    for w in ochasened_sentence:
        str_+=w[0]
    print(str_)
    connected_word=""
    for w in range(len(ochasened_sentence)):
        if("助詞" in ochasened_sentence[w][3]):
            print(connected_word)
            print(ochasened_sentence[w][0])
            connected_word=""
        else:
            connected_word+=ochasened_sentence[w][0]
    print(connected_word)
    
    input_=input("まずは一次群を選択")
    
    """
        (0-1)-2 (((4-5-6-7-8)-9)-10-11)-12
        (0-)
    """
