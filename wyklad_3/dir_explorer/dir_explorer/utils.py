import sys

from dir_explorer.file_walker import EntityData, EntityType
import dir_explorer.configuration as conf


def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def create_tree(tree, curr_path):
    def _create_tree(tree, curr_path):
        for name, obj in tree.items():
            curr_path = curr_path / name
            if obj.is_dir():
                curr_path.mkdir(parents=True, exist_ok=True)
                _create_tree(obj.children, curr_path)
            elif obj.is_file():
                create_file_of_size(str(curr_path), obj.size)
            curr_path = curr_path.parent
    _create_tree(tree.children, curr_path)


# XXX: os.walk would look better here but there is no equivalent in pathlib
def delete_tree(path):
    try:
        for sub in path.iterdir():
            if sub.is_dir():
                delete_tree(sub)
            else:
                try:
                    sub.unlink()
                except FileNotFoundError:
                    pass
        path.rmdir()
    except FileNotFoundError:
        pass


def create_file_of_size(file_path, size):
    with open(file_path, "wb") as out:
        out.seek(size - 1)
        out.write(b"\0")


def define_file(size):
    return EntityData(EntityType.FILE, size, {})


def define_dir(size=None, **children):
    return EntityData(EntityType.DIR, size, children)


demo_tree = {
        conf.explore_dir.name: define_dir(
            dir1=define_dir(
                file11=define_file(128),
                file12=define_file(256),
                file13=define_file(512),
                dir11=define_dir(
                    file111=define_file(63),
                )
            ),
            dir2=define_dir(
                file21=define_file(128),
                file22=define_file(256),
                file23=define_file(512),
                dir21=define_dir(
                    file211=define_file(63),
                    file212=define_file(74),
                ),
                dir22=define_dir(
                    file221=define_file(29),
                    dir221=define_dir(),
                )
            )
        )
    }
