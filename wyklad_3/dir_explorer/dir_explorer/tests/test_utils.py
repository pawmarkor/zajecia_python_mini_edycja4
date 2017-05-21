import tempfile
from pathlib import Path
from dir_explorer.utils import (
    create_tree,
    define_dir,
    define_file,
    create_file_of_size,
    delete_tree,
)

test_tree = define_dir(
    a=define_dir(
        f=define_file(256),
        b=define_dir(
            c=define_file(128),
        ),
        d=define_dir(),
    )
)


def list_of_dir_items(path):
    return [(item.name, item.is_dir()) for item in path.iterdir()]


def test_create_tree():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        create_tree(test_tree, temp_dir_path)
        assert list_of_dir_items(temp_dir_path) == [('a', True)]
        assert set(list_of_dir_items(temp_dir_path / 'a')) == set(
            [
                ('f', False),
                ('b', True),
                ('d', True),
            ]
        )
        assert list_of_dir_items(temp_dir_path / 'a/b') == [('c', False)]
        assert list_of_dir_items(temp_dir_path / 'a/d') == []
        assert (temp_dir_path / 'a/f').stat().st_size == 256
        assert (temp_dir_path / 'a/b/c').stat().st_size == 128


def test_delete_tree():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        create_tree(test_tree, temp_dir_path)
        for subdir_name in test_tree.children.keys():
            delete_tree(temp_dir_path / subdir_name)
            assert not (temp_dir_path / subdir_name).exists()


def test_create_file_of_size():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / 'file'
        create_file_of_size(str(file_path), 63)
        assert file_path.stat().st_size == 63
