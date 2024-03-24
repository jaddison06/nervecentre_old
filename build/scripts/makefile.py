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

def fs_util(*args: str) -> str:
    return f'python build{path.sep}scripts{path.sep}fs_util.py {" ".join(args)}'

def codegen(modules: dict[str, list[ParsedGenFile]]) -> str:
    out = ''

    for module_name, files in modules.items():
        libs: list[str] = []
        for file in files:
            if not file.has_code(): continue

            lib_path = f"build{path.sep}objects{path.sep}{file.libpath_no_ext()}"
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
                    fs_util('mkdir', path.dirname(lib_name)),
                    command
                ]
            )

            libs.append(lib_name)

        out += generate_makefile_item(
            module_name,
            libs,
            []
        )
    
    out = generate_makefile_item(
        "all",
        ["codegen", "libraries"], # codegen MUST be before libraries because the C files might need to include c_codegen.h
        []
    ) + generate_makefile_item(
        "libraries",
        list(modules.keys()),
        []
    ) + generate_makefile_item(
        "codegen",
        [],
        [
            f"python build{path.sep}scripts{path.sep}main_2.py"
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
            fs_util('rm_dir', 'build/objects')
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