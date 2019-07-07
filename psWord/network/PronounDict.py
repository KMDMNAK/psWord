import networkx as nx
import matplotlib.pyplot as plt
from .Connection import connection

class PronounDict:
    """
        word_dict(dict):{word_name:connection,...}
        document_number(int): number of documents.
            all integers under this is used
        
        example)
            pd=pronoun_dict()
            pd.documents_connection(documents)
    """
    
    def __init__(self):
        self.word_dict={}
        self.document_number=0
        self.edges=[]
        self.word_list=[]
    
    def documents2connect(self,documents):
        """
            加工前のdocumentsを挿入、getNoJoshiを施してから、
            documents_connectを実行
        """
        from ..parse import ochasen
        #freq,words=mw.get_wordfrequency(documents)
        ochasens=ochasen.getOchasen(documents)
        words=ochasen.getNonJoshi(ochasens)
        self.documents_connect(words)
        
    def documents_connect(self,documents,document_numbers=None):
        """
            documents : already owakatied documents
            document_numbers : 
        """
        if(document_numbers==None):
            document_numbers=[w for w in range(len(documents))]
            self.document_number=len(documents)
        if(self.document_number!=len(document_numbers)):
            raise Error("mismatch document and numbers")
        for document,document_number in zip(documents,document_numbers):
            self.document_connect(document,document_number)
        self.documents=documents
    def document_connect(self,document,document_number):
        for sentence in document:
            self.sentence_connect(sentence,document_number)
    
    def sentence_connect(self,sentence,document_number):
        """
            sentence間のconnectを更新
        """
        for w in range(len(sentence)-1):
            for after_word in sentence[w+1:]:
                self.word_connection(sentence[w],after_word,document_number)
                
    def word_connection(self,word1,word2,number):
        self.connect(word1,word2,number)
        self.connect(word2,word1,number)
    
    def connect(self,from_word,to_word,number):
        #connection class
        if(self.word_dict.get(from_word)==None):
            self.word_list.append(from_word)
            self.word_dict[from_word]=connection(from_word)
        if(self.word_dict.get(to_word)==None):
            self.word_list.append(to_word)
        self.edges.append([self.word_list.index(from_word),self.word_list.index(to_word)])
        self.word_dict[from_word].add(to_word,number)
        
        
    def make_edges(self,nodes):
        """
            nodesにおける誘導部分グラフをreturn
            無向辺を前提とする.
        """
        edges=[]
        for w in range(len(nodes)-1):
            for after_w in range(w+1,len(nodes)):
                if(self.word_dict[nodes[w]].connect_dict.get(nodes[after_w])!=None):
                    edges.append([w,after_w])
        return nodes,edges
    
    def plot_graph(self,width=3,for_graph=False):
        #make edges
        graph=nx.Graph()
        graph.add_nodes_from([w for w in range(len(self.word_list))])
        graph.add_edges_from(self.edges)
        pr = nx.pagerank(graph)
        return pr
    
    def plot_word(self,*words):
        """
            plot specific words and their neighbor(誘導部分グラフ)
        """
        
        G,nodes=nx.Graph(),list(words).copy()
        for word in words:
            nodes.extend(list(self.word_dict[word].connect_dict.keys()))
        nodes,edges=self.make_edges(nodes)
        #print(nodes)
        #print(edges)
        G.add_nodes_from([w for w in range(len(nodes))])
        G.add_edges_from(edges)
        
        pos=nx.spring_layout(G)
        nx.draw_networkx_edges(G,pos,alpha=0.1,edge_color='r')
        nx.draw_networkx_nodes(G,pos,node_size=3)
        labels={}
        for i in range(len(nodes)):
            labels[i]=nodes[i]
        nx.draw_networkx_labels(G,pos,labels=labels,font_size=10, font_family="IPAexGothic", font_weight="bold")
        plt.axis("off")
        plt.show()
        
    def pagerank(self):
        graph=nx.Graph()
        graph.add_nodes_from([w for w in range(len(self.word_list))])
        graph.add_edges_from(self.edges)
        pr = nx.pagerank(graph)
        return pr
    
class Error(Exception):
    def __init__(self,message):
        print(message)
