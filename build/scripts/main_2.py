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
def do_module_codegen(module: str, is_dartsubproject: bool) -> list[ParsedGenFile]:
    parsed_files: list[ParsedGenFile] = []
    for gen_file in all_with_extension(f'{module}/native', '.gen'):
        parsed_files.append(Parser(gen_file).parse())
    
    with open(f'{module}/{"bin/" if is_dartsubproject else ""}generated.dart', 'wt') as fh:
        fh.write(dart.codegen(parsed_files))
    with open(f'{module}/native/c_codegen.h', 'wt') as fh:
        fh.write(c.codegen(parsed_files))

    return parsed_files

# CONFIG
# todo: move some (all?) to commandline
# name of module -> is it a Dart subproject?
MODULES = {'client': True, 'server': True, 'shared': False}
USE_CLOC = True

def main():
    all_genfiles: dict[str, list[ParsedGenFile]] = {}

    for module in MODULES.keys():
        all_genfiles[module] = []
        for gen_file in all_with_extension(f'{module}/native', '.gen'):
            all_genfiles[module].append(Parser(gen_file).parse())
    
    for module, is_dartsubproject in MODULES.items():
        with open(f'{module}/{"bin/" if is_dartsubproject else ""}generated.dart', 'wt') as fh:
            fh.write(dart.codegen(all_genfiles[module] + all_genfiles['shared']))
        with open(f'{module}/native/c_codegen.h', 'wt') as fh:
            fh.write(c.codegen(all_genfiles[module] + all_genfiles['shared']))

    with open('Makefile', 'wt') as fh:
        fh.write(makefile.codegen(all_genfiles))
    
    if USE_CLOC:
        with open('.cloc_exclude_list.txt', 'wt') as fh:
            fh.write(cloc_exclude_list.codegen())

if __name__ == '__main__':
    main()