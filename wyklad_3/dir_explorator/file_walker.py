import logging
from enum import Enum
from pathlib import Path
from pprint import pprint
from collections import namedtuple


class EntityType(Enum):
    FILE = 'FILE'
    DIR = 'DIR'


class EntityData(namedtuple('EntityData', 'type size children')):
    def is_dir(self):
        return self.type == EntityType.DIR

    def is_file(self):
        return self.type == EntityType.FILE


logger = logging.getLogger(__name__)


def my_dir_walker_with_size_counting(topdir=None, topname=None):
    if topdir is None:
        topdir = Path()
    if topname is None:
        topname = topdir
    topdir = str(topdir)
    topname = str(topname)

    current_path = Path()

    def inner_walker(curr_dir):
        nonlocal current_path
        children = {}
        current_path = current_path / curr_dir
        size = 0
        for entry in current_path.iterdir():
            if entry.is_symlink():
                continue
            if entry.is_dir():
                entry_type = EntityType.DIR
                entry_size, entry_children = inner_walker(entry.name)
            elif entry.is_file():
                entry_type = EntityType.FILE
                entry_size = entry.stat().st_size
                entry_children = []
            children[entry.name] = EntityData(
                entry_type,
                entry_size,
                entry_children
            )
            size += entry_size
        current_path = current_path.parent
        return size, children

    try:
        topdir_data = EntityData('dir', *inner_walker(topdir))
        return EntityData('dir', topdir_data.size, {topname: topdir_data})
    except OSError as error:
        logger.error("Unable to compute size for {} because of {}"
                     .format(topdir, error))
        return EntityData('', '', {})


if __name__ == "__main__":
    pprint(my_dir_walker_with_size_counting())
