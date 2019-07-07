import re

NECESSARRY_STOP_WORDS=set(["\n",'\u3000'])
JAPANESE=["ja","jp","JP","jpn","JPN","japan","japanese","Japan","Japanese","JAPANESE","JAPAN"]
ENGLISH=["en","EN","english","eng","ENG","ENGLISH"]

JAPANESE_STOP_SPLITWORDS=r'は を に へ です する から たり ながら れる られ など ます いる こと ため なぜ べき よう まで たち あ い う え お か き く け こ さ し す せ そ た ち つ て と な に ぬ ね の は ひ ふ へ ほ ま み む め も や ゆ よ ら り る れ ろ わ を ん が で 。 、 「 」 ？ ? < > ＜ ＞ \u3000 ・ ! ！ . : ： ; ； = ＝ ^ ＾ '
ENGLISH_STOP_SPLITWORDS='at in on and or this that'

def makeStopWords(splitword):
    return set(splitword.split())|NECESSARRY_STOP_WORDS

"""
if(language in JAPANESE):
            self.stop_words=makeStopWords(JAPASENE_STOP_SPLITWORDS)
            self.extractWords():
            
"""

class LanguageHandler:
    """Based on ENGLISH!!"""
    def __init__(self,STOP_SPLITWORDS,**kwargs):
        self.stop_words=makeStopWords(STOP_SPLITWORDS)
    def extractSentences(self,document):
        pass
    def extractWords(self,sentence):
        pass
    def extractNonStopWords(self,words):
        """
            return non stop word and **len(word)>0**
        """
        non_stop_words=[]
        for word in words:
            if((not word in self.stop_words)&(len(word)>0)):
                non_stop_words.append(word)
        return non_stop_words
    
class EnglishHandler(LanguageHandler):
    def extractSentences(self,document):
        """
            split document to each sentences
        Return
            ______
            sentences(2-D string list)
            ______
        """
        return document.split(".")
    
    def extractWords(self,sentence):
        return sentence.split(" ")
    
class JapaneseHandler(LanguageHandler):
    def __init__(self,STOP_SPLITWORDS,**kwargs):
        super().__init__(STOP_SPLITWORDS)
        self.tagger=kwargs["tagger"]
        
    def extractSentences(self,document):
        sentences=re.split(r'｡|。|\n',document)
        if(sentences[-1]==""):
            sentences=sentences[:-1]
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
                    sentences[start_index]+=str_
        """
        return sentences
    
    def extractWords(self,sentence):
        return self.tagger.parse(sentence).split(" ")

def getHandler(sign,**kwargs):
    if(sign in JAPANESE):
        return JapaneseHandler(JAPANESE_STOP_SPLITWORDS,**kwargs)
    elif(sign in ENGLISH):
        return EnglishHandler(ENGLISH_STOP_SPLITWORDS,**kwargs)
    
