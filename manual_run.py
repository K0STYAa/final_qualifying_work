# -*- coding: UTF-8 -*-
from logging import exception
import os
import sys
from tabnanny import check
import pandas as pd
from IPython.display import display
import collections
import zipfile
import shutil
import json

from shingles_algorithm import shingle_compaire_2_files

import time


language_dict = {
    'python': [".py"],
    'C': [".c"],
    'pascal': [".PAS", ".pas"],
    'assembler': [".ASM", ".asm"]
}

lim = 20 # Показатель сходства выше которого программа возвращает совпадающие файлы


def files_list_in_dir (sol_dir, language):

    names = os.listdir(sol_dir)
    endings = language_dict[language]
    filenames_list = []

    for name in names:
        fullname = os.path.join(sol_dir, name)
        if os.path.isfile(fullname):
            for ending in endings:
                if name.endswith(ending):
                    filenames_list.append(fullname)
        if os.path.isdir(fullname):
            filenames_list += files_list_in_dir(fullname, language)

    return filenames_list

def language_identification (sol_dir):
    if os.path.exists(sol_dir):
        names = os.listdir(sol_dir)
        for name in names:
            fullname = os.path.join(sol_dir, name)
            if os.path.isfile(fullname):
                _, file_extension = os.path.splitext(fullname)
                for language, extension_list in language_dict.items():
                    for extension in extension_list:
                        if extension == file_extension:
                            return language
        raise Exception("No program files in directory.")
    else:
        raise Exception("No such directory exists.")


def compaire_all_files_in_dir (sol_dir, language, cod, out_file):

    for _ in range(150):
        print("#", end="")
    print("\n")
    print(sol_dir, "\n")
    filenames_list = files_list_in_dir(sol_dir, language)
    for i in range(len(filenames_list)):
        print(i,":", filenames_list[i])

    res = []
    res_arr = []
    for _ in range(len(filenames_list)):
        res.append([0] * len(filenames_list))

    for filename1_number in range(len(filenames_list)):
        for filename2_number in range(filename1_number, len(filenames_list)):
            if filename1_number != filename2_number:
                filename1=filenames_list[filename1_number]
                filename2=filenames_list[filename2_number]
                
                new_value = shingle_compaire_2_files(filename1, filename2, cod)

                # Write in out_file
                name1 = filename1.split('/')
                name1 = name1[len(name1)-1]
                name2 = filename2.split('/')
                name2 = name2[len(name2)-1]
                if new_value >= lim: 
                    addDict = {"1st_suspect":name1, "2nd_suspect":name2, "similarity": new_value}
                    res_arr.append(addDict)

                res[filename1_number][filename2_number] = new_value
                new_dict = collections.Counter()
                new_dict[new_value] = 1
                dict_counter.update(new_dict)

    data = {"suspects": res_arr}
    jsonString = json.dumps(data)
    out_file.write(jsonString)

    df = pd.DataFrame(res)
    print()
    display(df)
    print()

    for i in range(len(res)):
        for j in range(len(res[i])):
            if res[i][j] >= lim:
                print(i,":", filenames_list[i])
                print(j,":", filenames_list[j])
                print(res[i][j], "\n")


def check_in_uploaded_files(filename):
    dir_name = filename.split('.')[0]
    with zipfile.ZipFile(f"uploads/{filename}", 'r') as zip_ref:
        zip_ref.extractall(f"uploads/")
    sol_dir = f"uploads/{dir_name}"
    print(sol_dir)
    language = language_identification(sol_dir)
    out_file = open(f"uploads/suspects_{dir_name}.json", "w")

    compaire_all_files_in_dir(sol_dir, language, 'utf-8', out_file)

    out_file.close()

    # delete_all_files_and_dir
    os.remove(f"uploads/{filename}")
    shutil.rmtree(f"uploads/{dir_name}")


def main():

    start_time = time.time()
    
    # choose what to do
    todo = ''
    try:
        todo = sys.argv[1]
        os.system('cls' if os.name == 'nt' else 'clear')
    except IndexError:
        print('Exception. No arguments')
        return

    if todo == 'python': # Python
        sol_dir = 'programs/different_qsort_solutions/'
        compaire_all_files_in_dir(sol_dir, 'python', 'utf-8', f)

    else:
        try:
            sol_dir = 'programs/' + todo 
            language = language_identification(sol_dir)
            compaire_all_files_in_dir(sol_dir, language, 'utf-8', f)
        except Exception as err: 
            print("Incorrect argument. " + str(err))
    
    my_dict = dict(dict_counter)
    my_time = time.time() - start_time
    print("--- %s seconds ---" % my_time, sum(my_dict.values())/my_time, "comparisons/s")
    print()
    if len(my_dict):
        print(my_dict)


# Start program
f = open("suspects.json", "w")
dict_counter = collections.Counter()
main()
f.close()