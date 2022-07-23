import argparse
from m4atool import M4a
import os

def find_m4a_files(basedir, filelist):
    """Return list of files to manipulate."""
    try:
        files = sorted(os.listdir(basedir))
    except FileNotFoundError:
        sys.exit(f"{basedir} does not exist")
    except NotADirectoryError:
        sys.exit(f"{basedir} is not a directory")

    for file in files:
        ## preserve basedir in filename        
        file = f"{basedir}/{file}"
        if not os.path.isdir(file):
            if os.path.splitext(file)[1] == M4a.EXT:
                filelist.append(file)

        ## if we are a directory, recurse
        elif os.path.isdir(file):
            filelist = list_files(file, filelist)

    return filelist  


def arg_parse():
    parser = argparse.ArgumentParser(description='Directory of encoded files')
    parser.add_argument('--basedir', '-b', required=True, help=f'base directory containing m4a files')
    parser.add_argument('--debug', '-d', action='store_true', default=False, help=f'debug')
    parser.add_argument('--rename', '-r', action='store_true', help=f'rename')
    parser.add_argument('--sanitize', '-s', action='store_true', help=f'sanitize tags')
    parser.add_argument('--album', default=None, help=f'album name')
    parser.add_argument('--artist', default=None, help=f'artist name')
    parser.add_argument('--genre', default=None, help=f'genre')
    args = parser.parse_args()
    return args


def main():
    args = arg_parse()
    filelist = []
    for m4a_file in find_m4a_files(args.basedir, filelist):
        m4a = M4a(m4a_file, debug=args.debug)

        if args.artist:
            m4a.set_artist(args.artist)

        if args.sanitize:
            m4a.sanitize_tags()

        if args.album:
           m4a.set_album(args.album)

        if args.genre:
           m4a.set_genre(args.genre)

        if args.rename:
            m4a.rename()


if __name__ == '__main__':
    main()
