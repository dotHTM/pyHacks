import logging
import os
from textwrap import dedent
from typing import Optional
from subprocess import run
from pprint import pp
from typing import Optional, Sequence


class Template:
    workspaceExtention: str = "sublime-workspace"
    projectExtention: str = "sublime-project"
    project: str = dedent(
        """
            {
                "folders":
                [
                    {
                        "path": "./"
                    },
                ],
                "build_systems":[
                    {
                        "name": "Project Build",
                        "cmd": ["env"],
                        // "shell_cmd": "env",
                    }
                ]
            }
        """,
    )

    gitIgnoreRules: list[str] = [
        f"*.{workspaceExtention}",
    ]


def initProject(name: str):
    projectPath = f"./{name}.{Template.projectExtention}"

    if not os.path.isfile(projectPath):
        with open(projectPath, "w") as f:
            f.write(Template.project)
            logging.info(f"Wrote Project File '{f.name}'.")
    else:
        logging.info(f"Project File '{projectPath}' already exists.")

    addIgnore = list(Template.gitIgnoreRules)

    gitPreExists = False
    if not os.path.isdir(".git"):
        logging.info("Initializing git.")
        run("git init")
        gitPreExists = True
    else:  # git already exists, then ignore the project file to avoid poluting in projects where others don't use subl
        logging.info("Existing git, adding project to ignore list.")
        addIgnore.append(f"*.{Template.projectExtention}")

    existingIgnore = []
    if os.path.isfile(".gitignore"):
        with open(".gitignore", "r") as f:
            existingIgnore = f.read().split()
            logging.info("Reading .gitignore file.")

    with open(".gitignore", "a") as f:
        for line in addIgnore:
            if line not in existingIgnore:
                f.write(line + "\n")
                logging.info(f"gitignore added {line}")


def initProject_main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, nargs="?")
    parser.add_argument("--debug", "-d", action="count")
    parser.add_argument("--verbose", "-v", action="count")
    args = parser.parse_args(argv)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose:
        logging.basicConfig(level=logging.INFO)

    if not args.name:
        workingDirectory = os.path.abspath("./")
        args.name = os.path.basename(workingDirectory)

    initProject(name=args.name)

    return 0
