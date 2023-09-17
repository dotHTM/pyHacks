from __future__ import annotations

from typing import Optional, Sequence


from subprocess import run
import logging


import os


class Constants:
    iLifeSlideshows = [
        "Floating",
        "Flipup",
        "Reflections",
        "Origami",
        "ShiftingTiles",
        "SlidingPanels",
        "PhotoMobile",
        "HolidayMobile",
        "PhotoWall",
        "VintagePrints",
        "KenBurns",
        "Classic",
    ]


def setScreenSaverStyle(styleKey: str = "") -> bool:
    if styleKey not in Constants.iLifeSlideshows:
        logging.error(
            f"StyleKey not in list: '{styleKey}'\n\n{Constants.iLifeSlideshows}"
        )
        return False
    else:
        run(
            [
                "/usr/bin/defaults",
                "-currentHost",
                "write",
                "com.apple.ScreenSaver.iLifeSlideshows",
                "styleKey",
                "-string",
                styleKey,
            ]
        )
        return True


def setScreenSaverImageFolder(imageFolderPath: str = "") -> bool:
    if not os.path.isdir(imageFolderPath):
        logging.error(f"Path not directory: '{imageFolderPath}'")
        return False
    else:
        run(
            [
                "/usr/bin/defaults",
                "-currentHost",
                "write",
                "com.apple.ScreenSaverPhotoChooser",
                "SelectedFolderPath",
                imageFolderPath,
            ]
        )
        run(
            [
                "/usr/bin/defaults",
                "-currentHost",
                "write",
                "com.apple.ScreenSaverPhotoChooser",
                "ShufflesPhotos",
                "-bool",
                "true",
            ]
        )
        return True


def kill_cfprefsd():
    run(["killall", "cfprefsd"])


def setScreenSaver_main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--style", type=str, choices=Constants.iLifeSlideshows)
    parser.add_argument("--imageFolder", type=str)
    args = parser.parse_args(argv)

    if args.style:
        setScreenSaverStyle(args.style)
    if args.imageFolder:
        setScreenSaverImageFolder(args.imageFolder)
    if any([args.style, args.imageFolder]):
        kill_cfprefsd()

    return 0
