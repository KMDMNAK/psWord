import MeCab
from collections import defaultdict
from Scraping_tool import tag_search as xml

#sorted(frequency.items(),key=lambda x:-x[1])


#whether word isn't a single Kanji
#re.search('[\u4E00-\u9FD0]',word)



def getOchasen(documents,language="jp"):
    """
        return each sentence's ochasen(word property)
        
        UsedMethods
            sentence_ochasen
            document2sentences
    """
    handler=language.getHandler(language_sign,tagger=MeCab.Tagger("-Ochasen"))
    
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

def getOchasen(documents,language_sign="ja"):
    """
        return each sentence's ochasen(word property)
        
        UsedMethods
            sentence_ochasen
            document2sentences
    """nonstop_words_documents=[]
    for document in documents:
        nonstop_words_sentences=[]
        sentences=handler.extractSentences(document)
        for sentence in sentences:
            # extracting words depend on language
            words=handler.extractWords(sentence)
            nonstop_words_sentences.append(handler.extractNonStopWords(words))
        nonstop_words_documents.append(nonstop_words_sentences)
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
