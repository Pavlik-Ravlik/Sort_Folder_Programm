import os
import shutil
from tkinter import Tk
from tkinter.filedialog import askdirectory


EXTENSIONS = {
    "video": ["mp4", "mov", "avi", "mkv"],
    "audio": ["mp3", "wav", "ogg", "amr"],
    "image": ['jpg', 'png', 'jpeg', 'svg', 'bmp', 'odg', 'gif', 'webp'],
    "archive": ["zip", "gz", "tar"],
    "documents": ["pdf", "txt", "doc", "docx", "xlsx", "pptx", "html", "css", 'bin', 'torrent', 'DAT', 'json', 'drawio'],
    "programms": ["exe", "msi"],
}


def choose_folder():
    root = Tk()
    root.withdraw()
    folder_path = askdirectory()
    return os.path.normpath(folder_path)


def normalize_folder_path():
    main = choose_folder()
    a = main.split(':')
    return a[0] + ':' + '\\' + a[1]


main_path = normalize_folder_path()



# Перемістили усі файлі в main_path
def parse_folders(folder_path: str):
    dirpath_filenames = []
    for parse_folder in os.scandir(folder_path):
        if parse_folder.is_dir():
            for dirpath, _, filenames in os.walk(parse_folder.path):
                for a in filenames:
                    dirpath_filenames.append(dirpath + "\\" + a)
    for names_dir in dirpath_filenames:
        name = names_dir.split("\\")[-1]
        os.rename(names_dir, f"{folder_path}\\{name}")


# Створили папки під іменами із словника
def create_folders_from_list(folder_path: str, folder_names: dict):
    for names in folder_names:
        if not os.path.exists(f"{folder_path}\\{names}"):
            os.mkdir(f"{folder_path}\\{names}")


# Получили список путів файлів
def get_file_path(folder_path: str) -> list:
    list_file_path = []
    for i in os.listdir(folder_path):
        list_file_path.append(os.path.join(folder_path, i))
    return list_file_path


# Сортуємо файли по папкам
def sort_files(folder_path: str):
    file_paths = get_file_path(folder_path)
    ext_list = list(EXTENSIONS.items())
    for path in file_paths:
        extension = path.split(".")[-1]
        file_name = path.split("\\")[-1]
        for dict_key_int in range(len(ext_list)):
            if extension in ext_list[dict_key_int][1]:
                os.rename(
                    path, f"{main_path}\\{ext_list[dict_key_int][0]}\\{file_name}"
                )


# Створюємо папки в папці archive
def create_folder_from_archive(folder_path: str):
    archive_path = folder_path + "\\" + "archive"
    for archive in os.listdir(archive_path):
        name = archive.split(".")[0]
        new_folder_path = archive_path + "\\" + name
        if not os.path.exists(new_folder_path):
            os.mkdir(new_folder_path)



# Розпакували архіви до папок під їх назвами та удалили архіви з папки
def unpuck_archives(folder_path: str):
    path_to_folders = folder_path + "\\" + "archive"
    file_name = []
    file_names_ext = []
    for _, _, filenames in os.walk(path_to_folders):
        for i in filenames:
            file_name.append(i.split(".")[0])
        for i in filenames:
            file_names_ext.append(i)
    for a, b in zip(file_name, file_names_ext):
        shutil.unpack_archive(path_to_folders + "\\" + b,
                              path_to_folders + "\\" + a)
    for i in os.scandir(path_to_folders):
        if i.is_file():
            os.remove(i)


# Получили список папок
def get_folders_path(folder_path: str) -> list:
    dirpath_filenames = []
    for i in os.scandir(folder_path):
        if i.is_dir():
            for dirpath, _, _ in os.walk(i.path):
                dirpath_filenames.append(dirpath)
    return dirpath_filenames


# Видаляємо пусті папки
def remove_empty_folders(folder_path_list: list):
    folders_path = get_folders_path(folder_path_list)
    for char in folders_path:
        if not os.listdir(char):
            os.removedirs(char)

def run():
    parse_folders(main_path)
    create_folders_from_list(main_path, EXTENSIONS)
    sort_files(main_path)
    create_folder_from_archive(main_path)
    unpuck_archives(main_path)
    remove_empty_folders(main_path)
    print('Папка сортована')

if __name__ == '__main__':
    run()

