import googletrans

def getTranslation(text_list,dest='ja'):
    """
        dest which is the language to read in ["ja","en"]
    """
    translator=googletrans.Translator()
    return [each_translator.text for each_translator in translator.translate(text_list,dest=dest)]

