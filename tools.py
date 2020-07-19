from googletrans import Translator

def cn_to_zh(text):
    translator = Translator()
    result = translator.translate(text, dest='zh-tw')
    return result.text

def zh_to_cn(text):
    translator = Translator()
    result = translator.translate(text, dest='zh-CN')
    return result.text

def load_input_sentence(sent):
    sentence = []
    for letter in sent:
        sentence.append([letter, 'O'])
    return [sentence]
