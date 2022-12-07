from abc import ABC, abstractmethod
from io import StringIO
from typing import Dict, IO, List, Self

EXAMPLE = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


class FileABC(ABC):
    def __init__(self, name: str, file_type: str) -> None:
        self.name = name
        self.type = file_type

    def __repr__(self, level: int = 0):
        return "  " * level + f"- {self.name} ({self.type})"

    @abstractmethod
    def get_size(self) -> int:
        ...


class File(FileABC):
    def __init__(self, name: str, size: int) -> None:
        super().__init__(name, "file")
        self.size = size

    def __repr__(self, level: int = 0):
        return "  " * level + f"- {self.name} ({self.type}, size={self.size})"

    def get_size(self) -> int:
        return self.size


class Directory(FileABC):
    def __init__(self, name: str, parent: Self | None) -> None:
        super().__init__(name, "dir")
        self.parent = parent
        self.content: Dict[str, FileABC] = {}

    def __repr__(self, level: int = 0):
        result = super().__repr__(level)
        for f in self.content.values():
            result += "\n" + f.__repr__(level + 1)
        return result

    def __getitem__(self, item: str) -> FileABC:
        return self.content[item]

    def add_file(self, file: FileABC) -> None:
        self.content[file.name] = file

    def get_size(self) -> int:
        return sum([f.get_size() for f in self.content.values()])

    def list_dirs(self, min_size: int = 0, max_size: int | None = None) -> List[Self]:
        dirs: List[Self] = []
        for f in self.content.values():
            if isinstance(f, Directory):
                size = f.get_size()
                if (size >= min_size) and (max_size is None or size <= max_size):
                    dirs.append(f)
                dirs.extend(f.list_dirs(min_size, max_size))

        return dirs


ROOT = Directory("/", None)


def get_command_output(prompt_lines: IO[str]) -> List[str]:
    output: List[str] = []

    while True:
        last_index = prompt_lines.tell()
        line = prompt_lines.readline()
        if not line or line[0] == "$":
            prompt_lines.seek(last_index)
            break
        output.append(line)

    return output


def cd_command(arg: str, current_dir: Directory) -> FileABC:
    match arg:
        case "/":
            return ROOT
        case "..":
            return current_dir.parent
        case _:
            return current_dir[arg]


def ls_command(output: List[str], current_dir: Directory) -> None:
    for line in output:
        dir_or_size, name = line.split()
        if dir_or_size == "dir":
            current_dir.add_file(Directory(name, current_dir))
        else:
            current_dir.add_file(File(name, int(dir_or_size)))


def build_filesystem(prompt_lines: IO[str], current_dir: Directory) -> None:
    line = prompt_lines.readline()
    if not line:  # EOF
        return

    args = line.split()
    if args[0] == "$" and args[1] == "cd":
        current_dir = cd_command(args[2], current_dir)
    elif args[0] == "$" and args[1] == "ls":
        output = get_command_output(prompt_lines)
        ls_command(output, current_dir)

    build_filesystem(prompt_lines, current_dir)


def sum_dirs_size(directory: Directory, max_size: int) -> int:
    dirs = directory.list_dirs(max_size=max_size)

    return sum([d.get_size() for d in dirs])


def find_dir_to_free(directory: Directory, total_space: int, space_needed: int) -> int:
    available_space = total_space - ROOT.get_size()
    space_to_free = space_needed - available_space
    dirs = directory.list_dirs(min_size=space_to_free)

    return min([d.get_size() for d in dirs])


def test_part_1():
    """What is the sum of the total sizes of directories of at most 100_000."""
    build_filesystem(StringIO(EXAMPLE), ROOT)
    assert sum_dirs_size(ROOT, 100_000) == 95_437


def test_part_2():
    """Find the smallest directory size that would free up enough space on the filesystem to run the update."""
    build_filesystem(StringIO(EXAMPLE), ROOT)
    assert find_dir_to_free(ROOT, 70_000_000, 30_000_000) == 24_933_642


if __name__ == "__main__":
    print("=== DAY 7 ===")
    with open("./day_7.txt") as f:
        build_filesystem(f, ROOT)
        print(f"[Part 1] Total sizes of directories of at most 100_000: {sum_dirs_size(ROOT, 100_000)}")
        print(
            f"[Part 2] Smallest directory size to free for the update: {find_dir_to_free(ROOT, 70_000_000, 30_000_000)}"
        )
