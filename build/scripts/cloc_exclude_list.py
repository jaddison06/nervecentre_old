from config import *

def codegen(modules: list[str]) -> str:
    # Files and directories that we don't want cloc to count.
    out = "\n".join([
        ".dart_tool",
        ".vscode",
        "build",
        "Makefile",
        '.cloc_exclude_list.txt',
        *map(lambda module: f'{module}/generated.dart', modules),
        *map(lambda module: f'{module}/native/c_codegen.h', modules)
    ])

    return out
