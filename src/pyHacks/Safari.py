import os


import plistlib
from shutil import copy
import subprocess

from tempfile import gettempdir
import sys
import atexit


def readinglistUrls():
    BOOKMARKS_PLIST = "~/Library/Safari/Bookmarks.plist"
    bookmarksFile = os.path.expanduser(BOOKMARKS_PLIST)

    # Make a copy of the bookmarks and convert it from a binary plist to text
    tempDirectory = gettempdir()
    copy(bookmarksFile, tempDirectory)
    bookmarksFileCopy = os.path.join(tempDirectory, os.path.basename(bookmarksFile))

    def removeTempFile():
        os.remove(bookmarksFileCopy)

    atexit.register(removeTempFile)  # Delete the temp file when the script finishes

    converted = subprocess.call(["plutil", "-convert", "xml1", bookmarksFileCopy])

    if converted != 0:
        print("Couldn't convert bookmarks plist from xml format")
        sys.exit(converted)

    with open(bookmarksFileCopy, "rb") as f:
        plist = plistlib.load(f)

    # There should only be one Reading List item, so take the first one
    readingList = [
        item
        for item in plist["Children"]
        if "Title" in item and item["Title"] == "com.apple.ReadingList"
    ][0]

    urls = []
    if "Children" in readingList:
        for item in readingList["Children"]:
            url = item["URLString"]
            urls.append(url)

    return urls
