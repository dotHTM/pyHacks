from __future__ import annotations
import logging
import os
from textwrap import dedent

from typing import Optional, Sequence

from pyHacks.Shared import loggingArgs


class Template:
    defaultPyVersion = 3
    defaultPyMinorVersion = 9

    pyprojectPath = "pyproject.toml"
    sourceDirectory = "src"

    @staticmethod
    def pyproject(
        name: str,
        sourceDirectory: str = sourceDirectory,
        pythonVersion: int = defaultPyVersion,
        pythonMinorVersion: int = defaultPyMinorVersion,
    ) -> str:
        return dedent(
            f"""\
                [project]
                name = "{name}"
                version = "0.0.1"
                dependencies = []


                [build-system]
                requires = ["setuptools"]
                build-backend = "setuptools.build_meta"

                [tool.setuptools.packages.find]
                where = ["{sourceDirectory}"]

                [project.scripts]
                # commandLineName = "module.cli:main"


                [tool.black]
                line-length = 88
                target-version = ['py{pythonVersion}{pythonMinorVersion}']
                include = '\\.pyi?$'
                extend-exclude = '''
                # A regex preceded with ^/ will apply only to files and directories
                # in the root of the project.
                ^/foo.py  # exclude a file named foo.py in the root of the project (in addition to the defaults)
                '''

                [tool.pyright]
                pythonVersion = '{pythonVersion}.{pythonMinorVersion}'
                venvPath = ''
                venv = ''
            """
        )


def init_py_project(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, nargs="?")

    parser.add_argument("--major", type=int, default=Template.defaultPyVersion)
    parser.add_argument("--minor", type=int, default=Template.defaultPyMinorVersion)

    parser.add_argument("--source", type=str, default=Template.sourceDirectory)

    outputGroup = parser.add_argument_group("Output")
    outputGroup.add_argument("--debug", "-d", action="count")
    outputGroup.add_argument("--verbose", "-v", action="count")

    args = parser.parse_args(argv)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose:
        logging.basicConfig(level=logging.INFO)

    workingDirectory = os.path.abspath("./")
    print(os.path.basename(workingDirectory), args.name)
    if not args.name:
        args.name = os.path.basename(workingDirectory)
    elif os.path.basename(workingDirectory) != args.name:
        os.makedirs(args.name, exist_ok=True)
        workingDirectory += "/" + args.name

    print(os.path.basename(workingDirectory), args.name)

    exit()

    if not os.path.isfile(Template.pyprojectPath):
        logging.info(f"File '{Template.pyprojectPath}' does not exist, writing...")
        with open(Template.pyprojectPath, "w") as f:
            f.write(
                Template.pyproject(
                    name=args.name,
                    pythonVersion=args.major,
                    pythonMinorVersion=args.minor,
                )
            )
            logging.info("Written.")
    else:
        logging.info(f"File '{Template.pyprojectPath}' already exists, skipping.")

    os.makedirs(args.source, exist_ok=True)

    return 0
