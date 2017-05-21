import logging
from pathlib import Path
from pprint import pprint
from collections import namedtuple

EntityData = namedtuple('EntityData', 'type size children')

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
                entry_type = 'dir'
                entry_size, entry_children = inner_walker(entry.name)
            elif entry.is_file():
                entry_type = 'file'
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
        return EntityData('dir', topdir_data, {topname: topdir_data})
    except OSError as error:
        logger.error("Unable to compute size for {} because of {}"
                     .format(topdir, error))
        return EntityData('', '', {})


if __name__ == "__main__":
    pprint(my_dir_walker_with_size_counting())
