import argparse
from m4atool import M4a
from pathlib import Path
from typing import Generator
import sys


def find_m4a_files(basedir) -> Generator[Path, None, None]:
    """Recurses a base directory and returns a generator
    representing a list of m4a files."""
    try:
        return Path(basedir).rglob("*.m4a")

    except FileNotFoundError:
        sys.exit(f"{basedir} does not exist")
    except NotADirectoryError:
        sys.exit(f"{basedir} is not a directory")


def arg_parse():
    parser = argparse.ArgumentParser(description="Directory of encoded files")
    parser.add_argument("--basedir", "-b", default=None, help="base directory")
    parser.add_argument(
        "--debug", "-d", action="store_true", default=False, help="debug"
    )
    parser.add_argument("--filename", "-f", default=None, help="filename")
    parser.add_argument("--rename", "-r", action="store_true", help="rename")
    parser.add_argument("--sanitize", "-s", action="store_true", help="sanitize tags")
    parser.add_argument("--album", default=None, help="album name")
    parser.add_argument("--artist", default=None, help="artist name")
    parser.add_argument("--genre", default=None, help="genre")

    args = parser.parse_args()
    if args.basedir is None and args.filename is None:
        parser.error("Please specify --basedir or --filename.")

    if args.basedir and args.filename:
        parser.error("Please specify --basedir or --filename.")

    return args


def main():
    args = arg_parse()

    if args.basedir:
        m4a_files = find_m4a_files(args.basedir)

    if args.filename:
        m4a_files = [args.filename]

    for m4a_file in m4a_files:
        m4a = M4a(m4a_file, debug=args.debug)

        if args.artist:
            m4a.set_artist(args.artist)

        if args.album:
            m4a.set_album(args.album)

        if args.genre:
            m4a.set_genre(args.genre)

        if args.sanitize:
            m4a.sanitize_tags()

        if args.rename:
            m4a.rename()


if __name__ == "__main__":
    main()
