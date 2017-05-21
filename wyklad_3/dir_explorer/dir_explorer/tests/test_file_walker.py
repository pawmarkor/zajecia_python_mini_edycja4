import tempfile
from pathlib import Path
from dir_explorer.utils import (
    create_tree,
    define_dir,
    define_file,
)
from dir_explorer.file_walker import (
    my_dir_walker_with_size_counting,
    EntityData,
)

test_tree = define_dir(
    size=386,
    a=define_dir(
        size=386,
        f=define_file(256),
        b=define_dir(
            size=130,
            c=define_file(128),
            x=define_file(1),
            y=define_file(1),
        ),
        d=define_dir(size=0),
    )
)


def test_my_dir_walker_with_size_counting():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        create_tree(test_tree, temp_dir_path)
        result = my_dir_walker_with_size_counting(
            topdir=temp_dir_path / 'a',
            topname='a',
        )
        assert result == test_tree


def test_for_not_existing_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        result = my_dir_walker_with_size_counting(
            topdir=temp_dir_path / 'a',
            topname='a',
        )
        assert result == EntityData('', '', {})
