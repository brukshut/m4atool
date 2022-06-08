#!/usr/bin/env python

##
## m4atool.py
##
## Utility for manipulating apple lossless metadata.
##
import argparse
from mutagen import mp4
import os
import re
import string
import sys

class M4a:
    EXT = '.m4a'
    ALBUM = '©alb'
    ALBUM_ARTIST = 'aART'
    ARTIST = '©ART'
    GENRE = '©gen'
    TRACK_NUMBER = 'trkn'
    TRACK_TITLE = '©nam'

    def __init__(self, filename):
        self.filename = filename
        try:
            self.m4a = mp4.MP4(self.filename)
        except mp4.MP4StreamInfoError:
            print(f"{self.filename} is not an m4a")


    def rename(self):
        """ rename m4a file using standard format """
        ## sanitize existing tags before proceeding
        print(f"sanitizing {self.filename}")
        self.sanitize_tags()
        basedir = os.path.dirname(self.filename)
        artist = self._sanitize_filename(self.m4a.tags[self.ARTIST][0])
        track_title = self._sanitize_filename(self.m4a.tags[self.TRACK_TITLE][0])
        track_number = str(self.m4a.tags[self.TRACK_NUMBER][0][0]).zfill(2)
        new_name = f"{basedir}/{track_number} {artist} - {track_title}.m4a"

        try:
            print(f"renaming {self.filename} to {new_name}")
            os.rename(self.filename, new_name)
        except PermissionError:
            print(f"cannot rename {self.filename} to {new_name}")

        return new_name


    def set_tag(self, tag_name, tag_value):
        """ override existing tag value """
        print(f"Setting {tag_name} to {tag_value}")
        self.m4a.tags[tag_name] = tag_value
        self.m4a.save()

    
    def _sanitize_filename(self, tag):
        """ sanitize filenames for output """
        tag = tag.replace(' - ', ' -- ')
        tag = tag.replace('/', ' -- ')
        return tag


    def _sanitize_tag(self, tag):
        """ sanitize characters in tag """
        tag = string.capwords(tag)
        tag = tag.translate(tag.maketrans('[]', '()'))

        ## We don't want F.V.K. to look like F.v.k.
        rgx = r'([A-Za-z]\.){2,}'
        if re.search(rgx, tag):
            tag = re.sub(rgx, re.search(rgx, tag).group().upper(), tag)
        return tag


    def sanitize_tags(self):
        """ sanitize tags to follow a consistent format """
        for tag_name in [self.ALBUM, self.ALBUM_ARTIST, self.ARTIST, self.TRACK_TITLE, self.GENRE]:
            if not self.m4a.tags[tag_name][0] == self._sanitize_tag(self.m4a.tags[tag_name][0]):
                self.m4a.tags[tag_name][0] = self._sanitize_tag(self.m4a.tags[tag_name][0])
        self.m4a.save()


def list_files(basedir, filelist=[]):
    """ return list of files to manipulate """
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
    parser = argparse.ArgumentParser(description="Directory of encoded files")
    parser.add_argument("-b", "--basedir", required=True, help=f'basedir of files')
    parser.add_argument("-r", "--rename", action='store_true', help=f'rename')
    parser.add_argument("--dry-run", default=False)
    parser.add_argument("--album", default=None, help=f'album name')
    parser.add_argument("--album-artist", dest='album_artist', default=None, help=f'album artist')
    parser.add_argument("--artist", default=None, help=f'artist name')
    parser.add_argument("--genre", default=None, help=f'genre')
    args = parser.parse_args()
    return args

def main():
    args = arg_parse()
    for file in list_files(args.basedir):
        m4a = M4a(file)

        if args.artist:
            m4a.set_tag(m4a.ARTIST, args.artist)

        if args.album_artist:
           m4a.set_tag(m4a.ALBUM_ARTIST, args.album_artist)

        if args.genre:
           m4a.set_tag(m4a.GENRE, args.genre)

        if args.rename:
            m4a.rename()

## main
if __name__ == '__main__':
    main()

