import logging
import os
from pprint import pprint
from collections import namedtuple

EntityData = namedtuple('EntityData', 'type size children')

logger = logging.getLogger(__name__)


def my_dir_walker_with_size_counting(topdir=None, topname=None):
    if topdir is None:
        topdir = os.getcwd()
    if topname is None:
        topname = topdir

    dir_tree_stack = []

    def inner_walker(curr_dir):
        children = {}
        current_path = os.path.join(*dir_tree_stack, curr_dir)
        entries = os.scandir(current_path)
        dir_tree_stack.append(curr_dir)
        size = 0
        for entry in entries:
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
        dir_tree_stack.pop()
        return size, children

    try:
        topdir_data = EntityData('dir', *inner_walker(topdir))
        return EntityData('dir', topdir_data, {topname: topdir_data})
    except OSError as error:
        logger.error("Unable to compute size for {} because of {}"
                     .format(topdir, error))
        return EntityData('', '', {})

if __name__ == "__main__":
    pprint(my_dir_walker_with_size_counting("/home/pawkor/daftcode"))
