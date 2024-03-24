import os
import os.path as path

from codegen_types import *
from parse import *

import dart
import c
import makefile
import cloc_exclude_list

def all_with_extension(directory: str, ext: str) -> list[str]:
    if not ext.startswith('.'): ext = f'.{ext}'

    out: list[str] = []
    for root, _, files in os.walk(directory):
        for file in files:
            if path.splitext(file)[-1] == ext:
                out.append(path.join(root, file))
    
    return out

# return list of parsed gen files so we can reuse them if needed
def do_module_codegen(module: str) -> list[ParsedGenFile]:
    parsed_files: list[ParsedGenFile] = []
    for gen_file in all_with_extension(f'{module}/native', '.gen'):
        parsed_files.append(Parser(gen_file).parse())
    
    with open(f'{module}/generated.dart', 'wt') as fh:
        fh.write(dart.codegen(parsed_files))
    with open(f'{module}/native/c_codegen.h', 'wt') as fh:
        fh.write(c.codegen(parsed_files))

    return parsed_files

# CONFIG
# todo: move some (all?) to commandline
MODULES = ['client', 'server', 'shared']
USE_CLOC = True

def main():
    all_genfiles: list[ParsedGenFile] = []

    for module in MODULES:
        all_genfiles += do_module_codegen(module)

    with open('Makefile', 'wt') as fh:
        fh.write(makefile.codegen(all_genfiles))
    
    if USE_CLOC:
        fh.write(cloc_exclude_list.codegen())