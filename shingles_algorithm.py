# -*- coding: UTF-8 -*-
import os
import codecs
import re

def get_text (filename, cod):

    with codecs.open(filename, 'r', encoding=cod, errors='ignore') as file:
        text = file.read()

        _, file_extension = os.path.splitext(filename)

        if file_extension in [".py", ".PY"]:
            text = re.sub('#.*\n?', '', text)

        if file_extension in [".c", ".C", ".cpp", ".CPP"]:
            text = re.sub('//.*?\n|/\*.*?\*/', '', text)

        if file_extension in [".pas", ".PAS"]:
            text = re.sub('//.*?\n|{.*?}', '', text)

        text = text.replace('\n', ' ')

        return text

def canonize (source):
        stop_symbols = '.,!?:;-=\n\r()\t^@#№$%*'

        stop_words = (u'это', u'как', u'так',
        u'и', u'в', u'над',
        u'к', u'до', u'не',
        u'на', u'но', u'за',
        u'то', u'с', u'ли',
        u'а', u'во', u'от',
        u'со', u'для', u'о',
        u'же', u'ну', u'вы',
        u'бы', u'что', u'кто',
        u'он', u'она')

        return ( [x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)] )


def genshingle (source, shingleLen):
    import binascii
    out = [] 
    for i in range(len(source)-(shingleLen-1)):
        out.append (binascii.crc32(' '.join( [x for x in source[i:i+shingleLen]] ).encode('utf-8')))

    return out


def compaire (source1, source2):
    same = 0
    for i in range(len(source1)):
        if source1[i] in source2:
            same += 1

    return round(same*2/float(len(source1) + len(source2))*100, 2)


def shingle_compaire_2_files (filename1, filename2, cod):

    text1 = get_text(filename1, cod) # Текст 1 для сравнения
    text2 = get_text(filename2, cod) # Текст 2 для сравнения

    name1 = filename1.split('/')
    name1 = name1[len(name1)-1]
    name2 = filename2.split('/')
    name2 = name2[len(name2)-1]

    shingleLen = 4 #длина шингла

    cmp1 = genshingle(canonize(text1), shingleLen)
    cmp2 = genshingle(canonize(text2), shingleLen)

    res = compaire(cmp1,cmp2)

    return res