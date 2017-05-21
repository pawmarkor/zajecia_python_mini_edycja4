import sys

from dir_explorer.file_walker import EntityData, EntityType


def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def create_struct(tree, curr_path):
    for name, obj in tree.items():
        curr_path = curr_path / name
        if obj.is_dir():
            curr_path.mkdir(parents=True, exist_ok=True)
            create_struct(obj.children, curr_path)
        elif obj.is_file():
            create_file_of_size(str(curr_path), obj.size)
        curr_path = curr_path.parent


def define_file(size):
    return EntityData(EntityType.FILE, size, None)


def define_dir(**children):
    return EntityData(EntityType.DIR, None, children)


def create_file_of_size(file_path, size):
    with open(file_path, "wb") as out:
        out.seek(size - 1)
        out.write(b"\0")


# XXX: os.walk would look better here but there is no equivalent in pathlib
def delete_folder(path):
    try:
        for sub in path.iterdir():
            if sub.is_dir():
                delete_folder(sub)
            else:
                try:
                    sub.unlink()
                except FileNotFoundError:
                    pass
        path.rmdir()
    except FileNotFoundError:
        pass
