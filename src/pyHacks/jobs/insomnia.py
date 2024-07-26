from __future__ import annotations

from typing import Optional, Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "seconds",
        type=intl,
    )
    args = parser.parse_args(argv)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

