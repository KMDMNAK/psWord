from Scraping_tool import tag_search as xml

#sorted(frequency.items(),key=lambda x:-x[1])
#whether word isn't a single Kanji
#re.search('[\u4E00-\u9FD0]',word)




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
