# -*- coding: UTF-8 -*-
from logging import exception
import os
import sys
from tabnanny import check
import pandas as pd
# from IPython.display import display
import collections
import zipfile
import shutil
import json

import compaire_algorithms

import time
import constant

language_dict = {
    'python': [".py"],
    'C': [".c"],
    'pascal': [".PAS", ".pas"],
    'assembler': [".ASM", ".asm"]
}

algorithm_func_dict = {
    'shingle': 'shingle_compaire_2_files',
    'jaccard': 'Jaccard_compaire_2_files'
}


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
            if os.path.isdir(fullname):
                 return language_identification(fullname)
        raise Exception("No program files in directory.")
    else:
        raise Exception("No such directory exists.")


def compaire_all_files_in_dir (sol_dir, algorithm, language, cod, lim, comments_ignore=True):

    response = {}
    tmp = sol_dir.split('/')
    response["folder"] = tmp[len(tmp)-1]
    filenames_list = files_list_in_dir(sol_dir, language)
    files_arr = []
    for i in range(len(filenames_list)):
        name = filenames_list[i].split('/')
        files_arr.append({i: name[len(name)-1]})
    response["file_accordance"] = files_arr

    df_output = []
    suspects = []
    for _ in range(len(filenames_list)):
        df_output.append([0] * len(filenames_list))

    for filename1_number in range(len(filenames_list)):
        for filename2_number in range(filename1_number, len(filenames_list)):
            if filename1_number != filename2_number:
                filename1=filenames_list[filename1_number]
                filename2=filenames_list[filename2_number]
                
                compaire_2_files = getattr(compaire_algorithms, algorithm_func_dict[algorithm])
                new_value = compaire_2_files(filename1, filename2, cod, comments_ignore)

                # Write suspects
                name1 = filename1.split('/')
                name1 = name1[len(name1)-1]
                name2 = filename2.split('/')
                name2 = name2[len(name2)-1]
                if new_value >= lim:
                    addDict = {"1st_suspect":name1, "2nd_suspect":name2, "similarity": new_value}
                    suspects.append(addDict)

                df_output[filename1_number][filename2_number] = new_value
                
                new_dict = collections.Counter()
                new_dict[new_value] = 1
                dict_counter.update(new_dict)


    response["suspects"] = suspects

    df = pd.DataFrame(df_output)
    # display(df)
    # print(response)

    return(response, df)


def check_in_uploaded_files(filename, algorithm, lim, comments_ignore=True):
    dir_name = filename.split('.')[0]
    with zipfile.ZipFile(f"uploads/{filename}", 'r') as zip_ref:
        zip_ref.extractall(f"uploads/{dir_name}")
    sol_dir = f"uploads/{dir_name}"
    language = language_identification(sol_dir)

    response, df = compaire_all_files_in_dir(sol_dir, algorithm, language, 'utf-8', lim, comments_ignore)

    # delete_all_files_and_dir
    os.remove(f"uploads/{filename}")
    shutil.rmtree(f"uploads/{dir_name}")

    return response, df



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
        compaire_all_files_in_dir(sol_dir, "shingle", 'python', 'utf-8', 20, True)

    else:
        try:
            sol_dir = 'programs/' + todo 
            language = language_identification(sol_dir)
            compaire_all_files_in_dir(sol_dir, "shingle", language, 'utf-8', 20, True)
        except Exception as err: 
            print("Incorrect argument. " + str(err))
    
    my_dict = dict(dict_counter)
    my_time = time.time() - start_time
    print("--- %s seconds ---" % my_time, sum(my_dict.values())/my_time, "comparisons/s")
    print()
    if len(my_dict):
        print(my_dict)


# Start program
dict_counter = collections.Counter()
if __name__=="__main__":
    main()