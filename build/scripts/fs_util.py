import os
import os.path as path
from sys import argv
from shutil import rmtree

def fs_util(*args: str):
    match args[1]:
        case 'rm_file':
            if path.exists(args[2]):
                os.remove(args[2])
        case 'rm_dir':
            if path.exists(args[2]):
                rmtree(args[2])
        case 'mkdir':
            if not path.exists(args[2]):
                os.makedirs(args[2])
        case _: pass

if __name__ == '__main__': fs_util(*argv)