from config import *
from codegen_types import *
import os.path as path
from shared_library_extension import *

def generate_makefile_item(target: str, dependencies: list[str], commands: list[str]) -> str:
    out = f"{target}:"
    for dependency in dependencies: out += f" {dependency}"
    for command in commands: out += f"\n	{command}"
    out += "\n\n"
    return out

def codegen(files: list[ParsedGenFile]) -> str:
    out = ""

    libs: list[str] = []
    for file in files:
        if not file.has_code(): continue

        lib_path = f"build{path.sep}{file.libpath_no_ext()}"
        lib_name = f"{lib_path}{shared_library_extension()}"

        link_libs: list[str] = []

        for annotation in file.annotations:
            if annotation.name == "LinkWithLib":
                link_libs.append(annotation.args[0])

        #? removed `-I.`
        command = f"gcc -shared -o {lib_name} -fPIC {file.name_no_ext()}.c"
        for lib in link_libs:
            command += f" -l{lib}"

        # todo: #included dependencies
        out += generate_makefile_item(
            lib_name,
            [
                f"{file.name_no_ext()}.c"
            ],
            [
                f"mkdir -p {path.dirname(lib_name)}",
                command
            ]
        )

        libs.append(lib_name)
    
    
    # there's a directory called codegen, so we have to use .PHONY to
    # tell make to use the rule called "codegen" instead of the directory
    out = ".PHONY: codegen\n\n" \
      + generate_makefile_item(
        "all",
        ["codegen", "libraries"], # codegen MUST be before libraries because the C files might need to include c_codegen.h
        []
    ) + generate_makefile_item(
        "libraries",
        libs,
        []
    ) + generate_makefile_item(
        "codegen",
        [],
        [
            f"python codegen{path.sep}main.py"
        ]
    ) + generate_makefile_item(
        "run",
        [
            "all"
        ],
        [
            "dart run"
            #"dart run --enable-vm-service"
        ]
    ) + generate_makefile_item(
        "clean",
        [],
        [
            "rm -rf build",
            f"rm -f {get_config(ConfigField.c_output_path)}",
            f"rm -f {get_config(ConfigField.dart_output_path)}",
            f"rm -f {get_config(ConfigField.cloc_exclude_list_path)}"
        ]
    ) + (
        ''.join([generate_makefile_item(
            # The `cloc` command-line utility MUST be installed, or this won't work.
            # https://github.com/AlDanial/cloc
            "cloc",
            [],
            [
                # exclude generated files so cloc actually shows real results
                f"cloc . --exclude-list={get_config(ConfigField.cloc_exclude_list_path)}"
            ]
        ) + generate_makefile_item(
            "cloc-by-file",
            [],
            [
                f"cloc . --exclude-list={get_config(ConfigField.cloc_exclude_list_path)} --by-file"
            ]
        )]) if get_config(ConfigField.use_cloc) else ""
    ) + out

    return out