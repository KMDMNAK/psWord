class connection:
    def __init__(self,word):
        self.word=word
        self.connect_dict={}#word:[number,set(document_numbers)]
        self.document_numbers=set()
        
    def add(self,connect_word,document_number):
        if(connect_word!=self.word):
            self.document_numbers.add(document_number)
            if(self.connect_dict.get(connect_word)==None):
                self.connect_dict[connect_word]=set([document_number])
            else:
                self.connect_dict[connect_word].add(document_number)
                #print("copy:",copy,"\n",self.word,"\n")
                #self.connect_dict[connect_word]=copy
                self.sorting()
                
    def sorting(self):
        #self.connect_dict=dict(sorted(self.connect_dict.items(),key=lambda x:-x[1][0]))
        self.connect_dict=dict(sorted(self.connect_dict.items(),key=lambda x:-len(x[1])))