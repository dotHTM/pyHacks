from __future__ import annotations

import logging
from textwrap import dedent
from typing import Optional, Sequence

import psutil

import subprocess
from pyHacks.Shared import loggingArgs
from time import sleep


def caselessStrEquals(lhs, rhs) -> bool:
    return str(lhs).casefold() == str(rhs).casefold()


equals = lambda l, r: l == r


import argparse
from argparse import ArgumentParser, Namespace


def pidFinderArgs(
    parser: ArgumentParser = argparse.ArgumentParser(),
) -> ArgumentParser:
    finder = parser.add_argument_group("Process Finder")
    finder.add_argument(
        "--pid",
        dest="processId",
        type=int,
        help="Find a process by ID",
    )
    finder.add_argument(
        "--name",
        dest="processName",
        type=str,
        help="Find a process by name",
    )
    finder.add_argument(
        "--case-insensitive",
        "-i",
        action="store_true",
        help="Enable case-insensitive search for process name.",
    )
    return parser


def postPidFinderArgs(parser: ArgumentParser) -> Optional[Namespace]:
    args = loggingArgs(parser)

    if args.processName and args.processId:
        logging.error("Please don't supply *both* process name and id")
        parser.print_usage()
        return None

    return args


def processFinder(
    name: Optional[str] = None,
    pid: Optional[int] = None,
    case_insensitive: bool = False,
) -> Optional[psutil.Process]:
    stringComparitor = caselessStrEquals if case_insensitive else equals

    if pid:
        for ps in psutil.process_iter():
            if ps.pid == pid:
                name = ps.name()
                return ps
        else:
            logging.error(f"Could not find process with id '{pid}'.")

    elif name:
        for ps in psutil.process_iter():
            if stringComparitor(ps.name(), name):
                pid = ps.pid
                return ps
        else:
            logging.error(f"Could not find process with name '{name}'.")

    return None


def pidfinder_main(argv: Optional[Sequence[str]] = None) -> int:
    parser = pidFinderArgs()
    ## add whatever other args specific for this command line tool
    args = postPidFinderArgs(parser)
    if not args:
        return 1

    foundPs = processFinder(
        name=args.processName,
        pid=args.processId,
        case_insensitive=args.case_insensitive,
    )

    if foundPs:
        print(f"pid:{foundPs.pid}; name:{foundPs.name()}")

    return 0


def pidKiller_main(argv: Optional[Sequence[str]] = None) -> int:
    parser = pidFinderArgs()
    ## add whatever other args specific for this command line tool

    conditions = parser.add_argument_group("Kill Conditions")

    conditions.add_argument(
        "--memory-over-percent",
        type=float,
        help="A number between 0 and 100, to trigger a kill if the process is over this percent of memory usage.",
        default=100,
    )

    args = postPidFinderArgs(parser)
    if not args:
        parser.print_usage()
        return 1

    if not (0 <= args.memory_over_percent <= 100):
        logging.error(
            "Error: range of --memory-over-percent needs to be between 0 and 100."
        )
        return 1

    foundPs = processFinder(
        name=args.processName,
        pid=args.processId,
        case_insensitive=args.case_insensitive,
    )

    if foundPs:
        try:
            logging.debug(
                dedent(
                    f"""
                        ### System ###
                        cpu:         {psutil.cpu_percent()}
                        memory:      {psutil.virtual_memory().percent}
                        
                        ### Process ###
                        pid:         {foundPs.pid}
                        name:        {foundPs.name()} 
                    """
                )
            )
            triggered = []
            if args.memory_over_percent < psutil.virtual_memory().percent:
                triggered.append(
                    f"System over {args.memory_over_percent}% memory usage."
                )

            if triggered:
                logging.info(f"killing {foundPs.pid} {foundPs.name()}")
                for reason in triggered:
                    logging.info(reason)

                logging.info(
                    subprocess.check_output(["kill", "-9", str(foundPs.pid)]).decode()
                )
        except psutil.AccessDenied:
            logging.error("Error: Access Denied to process.")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
