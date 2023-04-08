# -*- coding: UTF-8 -*-
from math import sqrt
import os
import codecs
import re
import constant
import textdistance

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


def genshingle (source):
    import binascii
    shingleLen = constant.NGRAM_LEN
    out_set = set()
    out_arr = []
    for i in range(len(source)-(shingleLen-1)):
        new = binascii.crc32(' '.join( [x for x in source[i:i+shingleLen]] ).encode('utf-8'))
        out_arr.append(new)
        out_set.add(new)

    return out_set, out_arr


def shingle_compaire_2_files (text1, text2):

    text1 = text1["text_set"]
    text2 = text2["text_set"]

    same_count = len(text1.intersection(text2))

    return round(same_count*2/float(len(text1) + len(text2))*100, 2)

def Jaccard_compaire_2_files (text1, text2):

    text1 = text1["text_set"]
    text2 = text2["text_set"]

    same_count = len(text1.intersection(text2))
    source_count = len(text1.union(text2))

    return round(float(same_count)/source_count*100, 2)

def Ochiai_compaire_2_files (text1, text2):

    text1 = text1["text_set"]
    text2 = text2["text_set"]

    same_count = len(text1.intersection(text2))

    return round(sqrt(float(same_count**2)/(len(text1) * len(text2)))*100, 2)


def Levenshtein_distance_compaire_2_files (text1, text2):

    text1 = text1["text_arr"]
    text2 = text2["text_arr"]

    distance = textdistance.levenshtein.distance(text1, text2)
    source_len = max(len(text1), len(text2))

    return round((1.0-float(distance)/source_len)*100, 2)