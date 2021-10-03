import os
from typing import Iterable, Tuple, List


class NameFix(object):
    def __init__(
            self,
            root_directory: str,
            exclude: Iterable[str],
            max_directory_length: int,
            max_filename_length: int
    ) -> None:
        self.root_directory = root_directory
        exclude = [os.path.join(self.root_directory, entry) for entry in exclude]
        exclude = [entry for entry in exclude if os.path.exists(entry)]
        exclude = [os.path.abspath(entry) for entry in exclude]
        self.exclude_dirs = [entry.lower() for entry in exclude if os.path.isdir(entry)]
        self.exclude_files = [entry.lower() for entry in exclude if os.path.isfile(entry)]
        self.max_directory_length = max_directory_length
        self.max_filename_length = max_filename_length
        self.log: List[Tuple[str, str]] = []

    def run(self) -> None:
        # rename things
        self.log.clear()
        for root, directories, files in os.walk(self.root_directory):
            for directory in directories:
                self._rename(broken=os.path.join(root, os.path.join(root, directory)) + os.sep,
                             fixed=os.path.join(root, self._fix_dir(directory)) + os.sep)
            for file in files:
                if file.lower() in self.exclude_files:
                    return
                self._rename(broken=os.path.join(root, file),
                             fixed=os.path.join(root, self._fix_file(file)))
        # print log
        width = len(str(len(self.log)))
        print('---- RENAME LOG BEGIN ----')
        for index, (before, after) in enumerate(self.log):
            print(f' {str(index + 1).rjust(width)} | BEFORE | "{before}"')
            print(f' {str().rjust(width)} | AFTER  | "{after}"')
        print('---- RENAME LOG END ----')

    def _fix_file(
            self,
            name: str
    ) -> str:
        # fix filename characters
        name, extension = os.path.splitext(name)
        name = name.strip(' ')
        # fix filename length
        extension = extension.strip(' ')
        max_length = self.max_filename_length - len(extension)
        name = name[:max_length]
        # fix filename characters again
        name = name.strip(' ')
        # done
        return name + extension

    def _fix_dir(
            self,
            name: str
    ) -> str:
        return name.strip(' ')[:self.max_directory_length]

    def _rename(
            self,
            broken: str,
            fixed: str
    ) -> None:
        if broken == fixed:
            return
        if any(broken.lower().startswith(entry) for entry in self.exclude_dirs):
            return
        print(f' BROKEN: "{broken}"\n    FIX: "{fixed}"')
        if os.path.exists(fixed):
            print('Cannot fix, target already exists.')
        elif input('Rename this? ') == 'y':
            os.rename(broken, fixed)
            self.log.append((broken, fixed))
            print('Fixed.\n')
        else:
            print('Not fixed.\n')


def main() -> None:
    NameFix(
        root_directory='D:\\',
        exclude=['System Volume Information',
                 '$Recycle.Bin',
                 'RECYCLE?'],
        max_directory_length=255,
        max_filename_length=134
    ).run()


if __name__ == '__main__':
    main()
