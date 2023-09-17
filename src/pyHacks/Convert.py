from __future__ import annotations
import logging

from typing import Optional, Sequence

import subprocess, os
from tempfile import NamedTemporaryFile


def playdateify_mp3_main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", type=str)
    parser.add_argument(
        "--remove-source-file",
        "--rm",
        action="store_true",
    )
    args = parser.parse_args(argv)

    if not os.path.isfile(args.inputFile):
        logging.error(f"File does not exist '{args.inputFile}'")
        return 1

    parent = os.path.dirname(os.path.abspath(os.path.expanduser(args.inputFile)))

    (filename, ext) = os.path.splitext(os.path.basename(args.inputFile))

    outFile = f"{parent}/{filename}.pd.mp3"

    tempCoverFile = "temp_cover.png"
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            args.inputFile,
            "-an",
            "-vcodec",
            "copy",
            tempCoverFile,
            "-y",
        ]
    )

    subprocess.run(
        [
            "convert",
            tempCoverFile,
            "-resize",
            "100x100",
            # "240x240",
            # "-remap",
            # "pattern:gray50",
            tempCoverFile,
        ]
    )

    subprocess.run(
        [
            "ffmpeg",
            "-i",
            args.inputFile,
            "-acodec",
            "libmp3lame",
            "-ar",
            "44100",
            "-ab",
            "128k",
            "temp_audio.mp3",
            "-y",
        ]
    )

    subprocess.run(
        [
            "ffmpeg",
            "-i",
            "temp_audio.mp3",
            "-i",
            tempCoverFile,
            "-map",
            "0",
            "-map",
            "1:0",
            outFile,
            "-y",
        ]
    )

    [
        "ffmpeg",
        "-i",
        "temp_audio.mp3",
        "-i",
        tempCoverFile,
        "-map",
        "0",
        "-map",
        "1:0",
        "-codec",
        "copy",
        outFile,
        "-y",
    ]

    os.remove(tempCoverFile)

    if args.remove_source_file:
        os.remove(args.inputFile)

    logging.info(args.inputFile, "->", outFile)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
