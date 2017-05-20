import logging
import os
from pprint import pprint
from collections import namedtuple

EntityData = namedtuple('EntityData', 'type size children')

logger = logging.getLogger(__name__)


class EntrySizeComputingError(Exception):
    def __init__(self, path, errors):
        self.errors = errors
        self.path = path

    def __str__(self):
        return "Unable to compute size of {} because of ({})".format(
            self.path,
            ",".join(str(error) for error in self.errors)
        )


def my_dir_walker_with_size_counting(topdir=None):
    if topdir is None:
        topdir = os.getcwd()
    file_data = {}
    dir_tree_stack = []

    def inner_walker(curr_dir):
        children = {}
        current_path = os.path.join(*dir_tree_stack, curr_dir)
        entries = os.scandir(current_path)
        dir_tree_stack.append(curr_dir)
        size = 0
        errors = []
        for entry in entries:
            if entry.is_symlink():
                continue
            file_path = os.path.join(*dir_tree_stack, entry.name)
            try:
                if entry.is_dir():
                    current_size, children1 = inner_walker(entry.name)
                    current_data = EntityData('dir', current_size, children1)
                elif entry.is_file():
                    current_size = entry.stat().st_size
                    current_data = EntityData('file', current_size, [])
            except (OSError, EntrySizeComputingError) as an_error:
                logger.error("Unable to compute size for {} because of ({})"
                             .format(file_path, an_error))
                errors.append(an_error)
            else:
                children[entry.name] = current_data
                size += current_size
        dir_tree_stack.pop()
        if errors:
            raise EntrySizeComputingError(current_path, errors)
        return size, children

    try:
        file_data[topdir] = EntityData('dir', *inner_walker(topdir))
    except (OSError, EntrySizeComputingError) as error:
        logger.error("Unable to compute size for {} because of ({})"
                     .format(topdir, error))
    return file_data

if __name__ == "__main__":
    pprint(my_dir_walker_with_size_counting("/home/pawkor/daftcode"))
