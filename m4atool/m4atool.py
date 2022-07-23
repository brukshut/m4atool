import logging
from mutagen import mp4
import pathlib
import re
import string
import shutil
import sys

class M4a:
    ## apple lossless tags names
    ALBUM = '©alb'
    ALBUM_SORT_ORDER = 'soal'
    ALBUM_ARTIST = 'aART'
    ARTIST = '©ART'
    ARTIST_SORT_ORDER = 'soar'
    GENRE = '©gen'
    TRACK_NUMBER = 'trkn'
    TRACK_TITLE = '©nam'
    TRACK_TITLE_SORT_ORDER = 'sonm'
    YEAR = '©day'
    EXT = '.m4a'


    def __init__(self, filename, debug=False):
        self.filename =  str(pathlib.Path(filename).resolve())
        self.basedir = str(pathlib.Path(filename).parent.resolve())
        self.debug = debug

        log_level = logging.DEBUG if self.debug else logging.INFO
        logging.basicConfig(level=log_level, format='%(asctime)s %(filename)s %(funcName)s %(message)s')

        try:
            self.m4a = mp4.MP4(self.filename)
        except mp4.MP4StreamInfoError:
            logging.info(f"{self.filename} is not an m4a")


    def generate_filename(self) -> str:
        """Generate new filename from existing tags."""
        for tag_name in [self.ARTIST, self.TRACK_TITLE]:
            self.sanitize_tag(tag_name)

        artist = self.m4a.tags[self.ARTIST][0]
        track_title = self.m4a.tags[self.TRACK_TITLE][0]
        ## pad track number with leading zero if single digit
        track_number = str(self.m4a.tags[self.TRACK_NUMBER][0][0]).zfill(2)        
        return f"{self.basedir}/{track_number} {artist} - {track_title}.m4a"


    def rename(self) -> str:
        """Rename m4a lossless file."""
        newname = self.generate_filename()
        if not self.filename == newname:
            try:
                logging.info(f"renaming {self.filename} to {newname}")
                shutil.move(self.filename, newname)
                self.filename = newname

            except PermissionError:
                logging.debug(f"cannot rename {self.filename} to {newname}")

        return newname


    def sanitize_tag(self, tag: str) -> str:
        """Sanitize characters in tag."""
        ## convert square brackets to parentheses
        tag = tag.translate(tag.maketrans('[]', '()'))
        ## this needs lookaheads/lookbehinds for whitespace
        tag = tag.replace('-', ' -- ')
        tag = tag.replace('/', ' -- ')
        ## capitalize lower case words in tag
        tag = ' '.join([word.title() if not re.search(r'^\(?[0-9A-Z]', word) else word for word in tag.split()])
        return tag


    def sanitize_tags(self) -> None:
        """Sanitize several tags to follow a consistent format."""
        for tag_name in [self.ALBUM,
                         self.ALBUM_SORT_ORDER,
                         self.ALBUM_ARTIST,
                         self.ARTIST,
                         self.ARTIST_SORT_ORDER,
                         self.TRACK_TITLE,
                         self.TRACK_TITLE_SORT_ORDER]:
            try:
                clean_tag = self.sanitize_tag(self.m4a.tags[tag_name][0])    
                self.set_tag(tag_name, clean_tag)
            except KeyError:
                logging.debug(f"{self.filename} tag name {tag_name} not found")


    def set_tag(self, tag_name: str, tag_value: str) -> None:
        """Override existing tag value."""
        try:
            if not self.m4a.tags[tag_name][0] == tag_value:
                logging.debug(f"{self.filename}: setting {tag_name} to {tag_value}")
                self.m4a.tags[tag_name][0] = tag_value
                self.m4a.save()

        except KeyError:
           logging.debug(f"{self.filename} {tag_name} not found.")


    def set_album(self, album: str) -> None:
        """Update several apple lossless tags for album."""
        for tag in self.ALBUM, self.ALBUM_SORT_ORDER:
            self.set_tag(tag, album)


    def set_artist(self, artist: str) -> None:
        """Update several apple lossless tags for artist."""
        for tag in self.ARTIST, self.ARTIST_SORT_ORDER, self.ALBUM_ARTIST:
            self.set_tag(tag, artist)


    def set_genre(self, genre: str) -> None:
        """Update apple lossless tags for genre."""
        self.set_tag(self.GENRE, genre)
