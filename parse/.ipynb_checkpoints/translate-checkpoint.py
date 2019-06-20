import googletrans

def get_transtext(text,dest='ja'):
    """
        dest which is the language to read in ["ja","en"]
    """
    translator=googletrans.Translator()
    return translator.translate(text,dest=dest).text
