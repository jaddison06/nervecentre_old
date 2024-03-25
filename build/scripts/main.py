import os
import os.path as path

from codegen_types import *
from parse import *
from config import *

import dart
import c
import makefile

def all_with_extension(directory: str, ext: str) -> list[str]:
    if not ext.startswith('.'): ext = f'.{ext}'

    out: list[str] = []
    for root, _, files in os.walk(directory):
        for file in files:
            if path.splitext(file)[-1] == ext:
                out.append(path.join(root, file))
    
    return out

MODULES = ['client', 'server', 'shared']

def main():
    all_genfiles: dict[str, list[ParsedGenFile]] = {}

    for module in MODULES:
        all_genfiles[module] = []
        for gen_file in all_with_extension(f'{module}/native', '.gen'):
            all_genfiles[module].append(Parser(gen_file).parse())
    
    for module in MODULES:
        with open(f'{module}/generated.dart', 'wt') as fh:
            fh.write(dart.codegen(all_genfiles[module] + all_genfiles['shared']))
        with open(f'{module}/native/c_codegen.h', 'wt') as fh:
            fh.write(c.codegen(all_genfiles[module] + all_genfiles['shared']))

    with open('Makefile', 'wt') as fh:
        fh.write(makefile.codegen(all_genfiles))


if __name__ == '__main__':
    main()