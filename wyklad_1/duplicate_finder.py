import os

from filecmp import cmp as file_cmp
from collections import defaultdict

from file_hasher import get_hash


class DuplicateFinder:
    """Finds duplicates in a given directory tree.

    DuplicateFinder finds duplicates based on file size, file hash or
    file content; it works in a lazy way i.e. it  computes hashes and compares
    file content only when necessary.

    Args:
        dir_base (str): Directory tree base to be searched for file duplicates.

    """

    def __init__(self, dir_base=None):
        self.__seen_files_of_size = defaultdict(list)
        self.__seen_files_of_hash = defaultdict(list)
        self.__collisions = defaultdict(list)
        self.__dir_base = os.getcwd() if dir_base is None else dir_base

    @property
    def duplicates(self):
        """:obj: `list` of :obj: `list` of `str` List of list of duplicated file paths."""
        self.__find_duplicates()
        return self.__collisions

    def __find_duplicates(self):
        for root, dirs, files in os.walk(self.__dir_base):
            for file in files:
                file_path = os.path.join(root, file)
                self.__size_collision_search(file_path)
        self.__prepare_results()

    def __prepare_results(self):
        for first_path, collisions in self.__collisions.items():
            collisions.append(first_path)
        self.__collisions = list(self.__collisions.values())

    def __size_collision_search(self, file_path):
        file_size = os.path.getsize(file_path)
        seen_files_of_size = self.__seen_files_of_size[file_size]
        if seen_files_of_size:
            self.__hash_collision_search(file_path, seen_files_of_size)
        self.__seen_files_of_size[file_size].append(file_path)

    def __hash_collision_search(self, file_path, seen_files_of_size):
        if len(seen_files_of_size) == 1:
            first_file_path = seen_files_of_size[0]
            first_file_hash = get_hash(first_file_path)
            self.__seen_files_of_hash[first_file_hash].append(first_file_path)
        file_hash = get_hash(file_path)
        for collision_candidate in self.__seen_files_of_hash[file_hash]:
            if self.__content_collision_found(file_path, collision_candidate):
                break
        self.__seen_files_of_hash[file_hash].append(file_path)

    def __content_collision_found(self, file_path, collision_candidate):
        equal_content = file_cmp(file_path, collision_candidate)
        if equal_content:
            self.__update_collisions(file_path, collision_candidate)
        return equal_content

    def __update_collisions(self, file_path, collision):
        self.__collisions[collision].append(file_path)


if __name__ == '__main__':
    print(DuplicateFinder('/home/pawkor/daftcode').duplicates)
