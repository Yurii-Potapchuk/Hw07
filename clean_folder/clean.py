import sys
import shutil
from pathlib import Path
from clean_folder.normalize import normalize


CATEDORIES = {"Audio": [".mp3", ".aiff", ".wav"],
              "Video": [".mkv", ".mov"],
              "Document": [".docx", ".pptx", ".doc", ".txt", ".pdf", ".xlsx"],
              "Image": [".jpeg", ".png", ".svg"],
              "Archive": [".zip", ".tar"],
              "Python": [".py", ".json", ".pyc"],
              "Unknown ext": [], }
dict_of_files = {}
dict = {}
dict_of_ext = {}
dict_ext = {}


def move_file(path: Path, root_dir: Path,  categories: str):
    target_dir = root_dir.joinpath(categories)
    if not target_dir.exists():
        print(f"Make {target_dir}")
        target_dir.mkdir()
    # print(target_dir.joinpath(f"{normalize(path.stem)}{path.suffix}"))
    path.replace(target_dir.joinpath(f"{normalize(path.stem)}{path.suffix}"))


def unpack_archive(path: Path):
    archive_folder = "Archive"
    ext = [".zip", ".tar"]

    for el in path.glob(f"**/*"):  # Обираю цей варіант суто для розширення охоплення пошуку, якщо наприклад якийсь архів не було відсортовано в папку Архів. Логічно що ми передаємо такі само розширення в функцію, але наприклад тут вже можна додати більше розширень задля охоплення більше файлів.
        if el.suffix in ext:
            filename = el.stem
            arch_dir = path.joinpath(path/archive_folder/filename)
            arch_dir.mkdir()
            shutil.unpack_archive(el, arch_dir)
        else:
            continue


def delete_empty_folder(path: Path):

    folders_to_delete = [f for f in path.glob("**")]
    for folder in folders_to_delete[::-1]:
        try:
            folder.rmdir()
        except OSError:
            continue


def get_categories(path: Path) -> str:
    ext = path.suffix.lower()
    for cat, exts in CATEDORIES.items():
        if ext in exts:
            return cat
    return "Unknown ext"


def sort_folder(path: Path):
    for item in path.glob("**/*"):
        # print(item.is_dir(), item.is_file())
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)


def files_sorter(path: Path):  # Ось тут маю проблему(((
    for item in path.glob("**/*"):
        if item.is_file():
            # print(item)
            cat = get_categories(item)
            if dict_of_files.get(cat):
                dict_of_files[cat].append(item.name)
            else:
                dict_of_files[cat] = [item.name]
    dict.update(dict_of_files)
    print("\n{:_^70}\n".format("Files found in folders:"))
    for el, val in dict.items():
        print(f'{el}:  {val}')


def files_ext(path: Path):
    for item in path.glob('**/*'):
        if item.is_file():
            cat = get_categories(item)
            if dict_of_ext.get(cat):
                dict_of_ext[cat].add(item.suffix)
            else:
                dict_of_ext[cat] = {item.suffix}

    dict_ext.update(dict_of_ext)
    print("\n{:_^70}\n".format("Files extensions found in files:"))
    for el, val in dict_ext.items():
        print(f'{el} : {val}')
        

def main():
    try:
        # do not forget to change path lib sys.argv[1]
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return f"Folder with path {path} don't exist."

    sort_folder(path)
    delete_empty_folder(path)
    unpack_archive(path)
    files_sorter(path)
    files_ext(path)


if __name__ == "__main__":
    print(main())
