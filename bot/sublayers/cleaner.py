import os
import shutil
from pathlib import Path
from colorama import init, Fore

init(autoreset=True)

extensions = {'video': ['mp4', 'mov', 'avi', 'mkv'],
              'audio': ['mp3', 'wav', 'ogg', 'amr'],
              'images': ['jpg', 'png', 'jpeg', 'svg'],
              'archives': ['zip', 'gz', 'tar'],
              'documents': ['pdf', 'txt', 'doc', 'docx', 'xlsx', 'pptx', 'odt'],
              'others': []}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ#$%&()^+-:;<=>?@[\]{|`~}!"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_", "_", "_", "_", "_", "_",
               "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_","_")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name) -> str:
    '''converts from Cyrillic to Latin and replaces special characters with "_"
    
    Args:
        name: any name's file
    
    Returns:
        str: convert name to Latin
    '''
    name = Path(name).name

    new_name = name.translate(TRANS)
    return new_name


def create_folders_from_list(folder_path, folder_names):
    '''creating folders if they don't exist
    
    Args:
        folder_path: the path to the folder being sorted
        folder_names: folder names taken from the dictionary"extensions[key]"
    '''
    for folder in folder_names:
        try:

            if not os.path.exists(f'{folder_path}/{folder}'):
                os.mkdir(f'{folder_path}/{folder}')

        except FileExistsError:
            pass


file_paths = []
subfolder_paths = []


def paths(path, level=1):
    '''finds the path to attached files and folders
    
    Args: 
        path: the path to the folder being sorted
        level: level of nesting (int)
        
    Returns:
        list: lists of paths to files and subfolders    
    '''
    names_dir = os.listdir(path)

    file_paths.extend([f.path for f in os.scandir(path) if not f.is_dir()])

    subfolder_paths.extend([f.path for f in os.scandir(path) if f.is_dir()])
    for elem in names_dir:

        if os.path.isdir(path + "/" + elem):
            paths(path + "/" + elem, level + 1)
    return file_paths, subfolder_paths


def sort_files(path):
    '''sorts and arranges in folders
    
    Args:
        path: the path to the folder being sorted 
    '''
    ext_list = list(extensions.items())

    for file_path in file_paths:
        file_path = str(file_path)
        extension = file_path.split('.')[-1]

        file_name = file_path.split('/')[-1]

        for dict_key_int in range(len(ext_list)):

            if extension in ext_list[dict_key_int][1]:

                shutil.move(file_path, f'{path}/{ext_list[dict_key_int][0]}/{normalize(file_name)}')

    for ar_file in os.listdir(path + "/" + "archives"):
        try:
            shutil.unpack_archive(path + "/" + "archives" + "/" + ar_file, path + "/" + "archives")
            os.remove(path + "/" + "archives" + "/" + ar_file)

        except shutil.ReadError:
            pass

    names_file = [name for name in os.listdir(path) if os.path.isfile(os.path.join(path,name))]
    for unkn_file in names_file:

            shutil.move(path + "/" + unkn_file, path + "/" + "others" + "/" + normalize(unkn_file)) 


def remove_empty_folders(main_path, level = 1):
    '''deleted empty subfolders
    
    Args: 
        main_path: the path to the folder being sorted
        level: level of nesting (int)
    '''    
    for p in subfolder_paths:
        p = str(p)
        if not os.listdir(p):
            try:
                os.rmdir(p)
                remove_empty_folders(main_path + "/" + p, level + 1)
            except FileNotFoundError:
                pass


def sort():
    '''takes the path, runs the functons and outputs a report of the work done'''
    try:
        main_path = input(Fore.MAGENTA + "Enter path for folder: ")
        create_folders_from_list(main_path, extensions)
        paths(main_path)
        sort_files(main_path)
        remove_empty_folders(main_path)
        print(Fore.MAGENTA + "Your files are sorted.\n" + "Deleting empty folders")
        for name_dir in os.listdir(main_path):
            print(Fore.MAGENTA + f"{name_dir.capitalize()}: ")
            for name_fale in os.listdir(main_path + "/" + name_dir):
                print(Fore.CYAN + f"    - {name_fale}")

    except FileNotFoundError:
            print(Fore.LIGHTRED_EX + "The path was wroning. Try again")


# ------------------------------------------------ADAPTER-------------------------------------------------------

help = ('|You can use following commands:\n'
        '|sort - Sorting the folder\n'
        '|back - Closing the sublayer\n')

commands = {'sort': sort,
            'back': ...}


CONFIG = ({'help': help,
           'commands': commands})


if __name__ == "__main__":
    sort()
