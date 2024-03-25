import os
import os.path as path
from sys import argv
from shutil import rmtree

def fs_util(*args: str):
    for target in args[2:]:
        match args[1]:
            case 'rm_file':
                if path.exists(target):
                    os.remove(target)
            case 'rm_dir':
                if path.exists(target):
                    rmtree(target)
            case 'mkdir':
                if not path.exists(target):
                    os.makedirs(target)
            case _: pass

if __name__ == '__main__': fs_util(*argv)