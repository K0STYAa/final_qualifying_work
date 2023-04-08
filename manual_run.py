# -*- coding: UTF-8 -*-
import os
import sys
import pandas as pd
# from IPython.display import display
import collections
import zipfile
import shutil

import compaire_algorithms

import time

language_dict = {
    'python': [".py"],
    'C': [".c"],
    'Cpp': [".cpp", ".CPP"],
    'pascal': [".PAS", ".pas"],
    'assembler': [".ASM", ".asm"]
}

algorithm_func_dict = {
    'shingle': 'shingle_compaire_2_files',
    'jaccard': 'Jaccard_compaire_2_files',
    'ochiai': 'Ochiai_compaire_2_files',
    'levenshtein': 'Levenshtein_distance_compaire_2_files'
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
        raise Exception("No program files in directory")
    else:
        raise Exception("No such directory exists")


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

    clear_files = []
    for filename_number in range(len(filenames_list)):
        text = compaire_algorithms.get_text(filenames_list[filename_number], cod, comments_ignore)
        text_set, text_arr = compaire_algorithms.genshingle(text)
        clear_files.append({"text_set": text_set, "text_arr": text_arr})

    for filename1_number in range(len(filenames_list)):
        df_output[filename1_number][filename1_number] = 1
        for filename2_number in range(filename1_number, len(filenames_list)):
            if filename1_number != filename2_number:
                
                compaire_2_files = getattr(compaire_algorithms, algorithm_func_dict[algorithm])
                new_value = compaire_2_files(clear_files[filename1_number], clear_files[filename2_number])

                # Write suspects
                def get_f_name(filename_number):
                    filename=filenames_list[filename_number]
                    name = filename.split('/')
                    return name[len(name)-1]
                name1 = get_f_name(filename1_number)
                name2 = get_f_name(filename2_number)
                if new_value >= lim:
                    addDict = {"1st_suspect":name1, "2nd_suspect":name2, "similarity": new_value}
                    suspects.append(addDict)

                df_output[filename1_number][filename2_number] = new_value
                df_output[filename2_number][filename1_number] = new_value
                
                new_dict = collections.Counter()
                new_dict[new_value] = 1
                dict_counter.update(new_dict)


    response["suspects"] = suspects

    df = pd.DataFrame(df_output)
    # print(df_output)
    # df.to_csv("tmp.csv")
    # print(response)

    return(response, df)


def check_in_uploaded_files(filename, algorithm, lim, comments_ignore=True):
    dir_name = filename.split('.')[0]
    if filename == "zip":
        filename = "zip.zip"
        os.rename("uploads/zip", "uploads/zip.zip")
    with zipfile.ZipFile(f"uploads/{filename}", 'r') as zip_ref:
        zip_ref.extractall(f"uploads/{dir_name}")
    sol_dir = f"uploads/{dir_name}"
    try:
        language = language_identification(sol_dir)
    except Exception as err:
            response = {"error": str(err)}
            print(str(err))
            return response, None


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