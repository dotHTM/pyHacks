from __future__ import annotations
import logging
import os
from textwrap import dedent

from typing import Optional, Sequence

from pyHacks.Shared import loggingArgs

from pyHacks.Shared import loggingArgs
from pathlib import Path


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
        source: str = sourceDirectory,
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
                where = ["{source}"]

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

    args = loggingArgs(parser)

    workingDirectory = os.path.abspath("./")

    if not args.name:
        args.name = os.path.basename(workingDirectory)
        logging.info(
            f"No args.name specified. Detecting from working directory. {args.name}"
        )
    elif os.path.basename(workingDirectory) != args.name:
        os.makedirs(args.name, exist_ok=True)
        workingDirectory += "/" + args.name
        logging.info(
            f"Working directory was not named '{args.name}', so created and updated wd. {workingDirectory}"
        )

    projectPath = os.path.join(workingDirectory, Template.pyprojectPath)

    if not os.path.isfile(projectPath):
        logging.info(f"File '{projectPath}' does not exist, writing...")
        with open(projectPath, "w") as f:
            logging.info("writing pyproject template")
            f.write(
                Template.pyproject(
                    name=args.name,
                    pythonVersion=args.major,
                    pythonMinorVersion=args.minor,
                    source=args.source,
                )
            )
            logging.info("Written.")
    else:
        logging.info(f"File '{projectPath}' already exists, skipping.")

    sourceAbsPath = os.path.join(workingDirectory, args.source, args.name)
    sourceInitFileAbsPath = os.path.join(
        workingDirectory, args.source, args.name, "__init__.py"
    )
    logging.info(f"Creating source directory at '{sourceAbsPath}'.")
    os.makedirs(sourceAbsPath, exist_ok=True)
    logging.info(f"touching source init at '{sourceInitFileAbsPath}'.")
    Path(sourceInitFileAbsPath).touch()

    return 0
