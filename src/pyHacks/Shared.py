import argparse
from argparse import ArgumentParser, Namespace
from typing import Optional, Sequence
import logging


class Defaults:
    detailFormat = "[ %(asctime)s ] %(levelname)s : %(message)s"
    midFormat = "%(levelname)s : %(message)s"
    basicFormat = "%(message)s"


def loggingArgs(
    parser: ArgumentParser,
    argv: Optional[Sequence[str]] = None,
    format: str = "",
) -> Namespace:
    """Patch on logging arguments, collect args, set logging, return args."""

    outputGroup = parser.add_argument_group("Output")

    outputGroup.add_argument("--debug", "-d", action="count")
    outputGroup.add_argument("--verbose", "-v", action="count")

    args = parser.parse_args(argv)

    if args.debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format=Defaults.detailFormat if not format else format,
        )
    elif args.verbose:
        logging.basicConfig(
            level=logging.INFO,
            format=Defaults.basicFormat if not format else format,
        )
    else:
        logging.basicConfig(
            level=logging.WARN,
            format=Defaults.basicFormat if not format else format,
        )

    return args
