# -*- coding: UTF-8 -*-
import os
import codecs
import re
import constant
import editdistance

def get_text (filename, cod, comments_ignore):

    with codecs.open(filename, 'r', encoding=cod, errors='ignore') as file:
        text = file.read()
        
        if comments_ignore:
            _, file_extension = os.path.splitext(filename)

            if file_extension in [".py", ".PY"]:
                text = re.sub('#.*\n?', '', text)

            if file_extension in [".c", ".C", ".cpp", ".CPP"]:
                text = re.sub('//.*?\n|/\*.*?\*/', '', text)

            if file_extension in [".pas", ".PAS"]:
                text = re.sub('//.*?\n|{.*?}', '', text)

        return re.findall(r"[\w']+", text.replace('\n', ' ').lower())


def genshingle (source, shingleLen):
    import binascii
    out = set()
    for i in range(len(source)-(shingleLen-1)):
        out.add (binascii.crc32(' '.join( [x for x in source[i:i+shingleLen]] ).encode('utf-8')))

    return out


def shingle_compaire (source1, source2):
    same_count = len(source1.intersection(source2))

    value = round(same_count*2/float(len(source1) + len(source2))*100, 2)

    return value


def shingle_compaire_2_files (filename1, filename2, cod, comments_ignore=True):

    text1 = get_text(filename1, cod, comments_ignore) # Текст 1 для сравнения
    text2 = get_text(filename2, cod, comments_ignore) # Текст 2 для сравнения

    cmp1 = genshingle(text1, constant.NGRAM_LEN)
    cmp2 = genshingle(text2, constant.NGRAM_LEN)

    return shingle_compaire(cmp1,cmp2)


def Jaccard_index_compare (source1, source2):
    same_count = len(source1.intersection(source2))
    source_count = len(source1.union(source2))

    value = round(float(same_count)/source_count*100, 2)

    return value


def Jaccard_compaire_2_files (filename1, filename2, cod, comments_ignore=True):

    text1 = get_text(filename1, cod, comments_ignore) # Текст 1 для сравнения
    text2 = get_text(filename2, cod, comments_ignore) # Текст 2 для сравнения

    cmp1 = genshingle(text1, constant.NGRAM_LEN)
    cmp2 = genshingle(text2, constant.NGRAM_LEN)

    return Jaccard_index_compare(cmp1,cmp2)


def Otsuka_Ochiai_square_coefficient(source1, source2):
    same_count = len(source1.intersection(source2))

    value = round(float(same_count**2)/(len(source1) * len(source2))*100, 2)

    return value


def Ochiai_compaire_2_files (filename1, filename2, cod, comments_ignore=True):

    text1 = get_text(filename1, cod, comments_ignore) # Текст 1 для сравнения
    text2 = get_text(filename2, cod, comments_ignore) # Текст 2 для сравнения

    cmp1 = genshingle(text1, constant.NGRAM_LEN)
    cmp2 = genshingle(text2, constant.NGRAM_LEN)

    return Otsuka_Ochiai_square_coefficient(cmp1,cmp2)


def Levenshtein_distance_compaire_2_files (filename1, filename2, cod, comments_ignore=True):

    text1 = get_text(filename1, cod, comments_ignore) # Текст 1 для сравнения
    text2 = get_text(filename2, cod, comments_ignore) # Текст 2 для сравнения

    distance = editdistance.eval(text1, text2)
    source_len = max(len(text1), len(text2))

    return round(float(source_len - distance)/source_len*100, 2)