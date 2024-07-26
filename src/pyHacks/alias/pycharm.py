from __future__ import annotations

from typing import Optional, Sequence
import re
from pprint import pp


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("FILE", type=str)
    args = parser.parse_args(argv)

    path_match_regex = (
        r"^(?P<path>[^:]*)(?::(?P<line>\d+))?(?::(?P<column>\d+))?:?(?: (?P<code>.*))?"
    )

    matched = re.match(path_match_regex, args.FILE)

    print(">", args.FILE)
    pp(matched.groupdict())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
