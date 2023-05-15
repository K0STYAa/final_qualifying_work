import shutil
import constant
import manual_run

def add_changed_file(source_file):
    # задаем новый путь файла
    destination_file = source_file[:source_file.find(".")] + "_synthetic"+source_file[source_file.find("."):]

    # копируем файл с изменением имени
    shutil.copyfile(source_file, destination_file)

    # открываем новый файл и заменяем пробелы и добавляем комментарии
    with open(destination_file, "r+") as f:
        lines = f.readlines()  # считываем все строки из файла
        f.seek(0)  # перемещаем указатель на начало файла
        f.truncate()  # очищаем файл
        for line in lines:
            new_line = line.replace(" ", "   ")  # заменяем один пробел на три
            f.write(new_line)  # записываем новую строку в файл
            if source_file[source_file.find("."):] == ".py":
                f.write(f"  # комментарий: {line.strip()}\n")  # добавляем комментарий к строке python
            elif source_file[source_file.find("."):] in [".c", ".cpp"]:
                f.write(f"  // комментарий: {line.strip()}\n")  # добавляем комментарий к строке c, c++
        f.close()

    # print(f"Файл {destination_file} успешно создан с изменениями и комментариями.")

# add_changed_file("uploads/tmp.py")
# for alg in ["shingle", "jaccard", "ochiai", "levenshtein"]:
#     response, df = manual_run.compaire_all_files_in_dir("uploads", alg, "python", 'utf-8', constant.DEFAULT_LIM, True)