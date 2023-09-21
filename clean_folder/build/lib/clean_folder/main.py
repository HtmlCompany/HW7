from pathlib import Path
import os
import sys
import shutil

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"

TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

CATEGORIES = {'Archives': ['.rar', '.zip', '.gz', '.tar'], 
              'Audio': ['.mp3', '.ogg', '.wav', '.amr'],
              'Video': ['.avi', '.mp4', '.mov', '.mkv'],
              'Documents': ['.doc', '.docx', '.txt', '.pdf', '.xls', '.xlsx', '.pptx', '.odt', '.ods'],
              'Images': ['.jpeg', '.png', '.jpg', '.gif']}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"

TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for c, t in zip(tuple(CYRILLIC_SYMBOLS), TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

REZERV = list(CATEGORIES.keys())

def get_categories(file:Path) -> str:
    ext = file.suffix.lower()
    for cats, exts in CATEGORIES.items():
        if ext in exts:
            return cats
    return "Else"

def move_file(file:Path, category:str, root_dir:Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    file.replace(target_dir.joinpath(file.name))

def sort_folder(path:Path) -> None:
    for item in path.glob("**/*"):
        if item.is_file():
            category = get_categories(item)
            move_file(item, category, path)

def del_empty_folders(path:Path):
    for folder in path.glob("**/*"):
        counter = 0
        if not (folder.name in REZERV) and folder.is_dir():
            for root_dir, dirs, files in os.walk(folder):
                if (not dirs) and (not files):
                    os.rmdir(root_dir)
                    counter += 1
                    if counter > 0:
                        del_empty_folders(path)
def rename_files(path:Path):
    for el in path.glob("**/*"):
        if el.is_dir():
            for old_path in el.glob('*'):
                if old_path.is_file():
                    new_path = el.joinpath(normalized(old_path.stem) + old_path.suffix)
                    os.rename(old_path, new_path)

def normalized(file_name:str):
    new_name = file_name.replace('-', '_').replace(' ', '_'
                ).replace('$', '_').replace('~', '_').replace('@', '_'
                ).replace('#', '_').replace('#', '_').replace('№', '_') 
    return new_name.translate(TRANS)

def unpack_arc(path:Path):
    for arc in path.glob('**/*'):
        if arc.name == 'Archives':
            arc_path = arc
            for el in arc.glob('*'):
                if el.is_file():
                    unpack_path = arc_path.joinpath(el.stem)
                    if not unpack_path.exists():
                        unpack_path.mkdir()
                    arc_name = el
                    shutil.unpack_archive(arc_name, unpack_path)

def main() -> str:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "This is not a path"
    
    if not path.exists():
        return "No path to folder"
    
    sort_folder(path)

    del_empty_folders(path)

    unpack_arc(path)

    rename_files(path)

    return "All right"

if __name__ == '__main__':
    print(main())