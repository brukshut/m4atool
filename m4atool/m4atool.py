import logging
from mutagen import mp4
import pathlib
import re
import shutil


class M4a:
    """Provides functions for manipulating tags and filenames
    of Apple Lossless files with an .m4a extension."""

    # Apple Lossless tag names.
    ALBUM = "©alb"
    ALBUM_SORT_ORDER = "soal"
    ALBUM_ARTIST = "aART"
    ARTIST = "©ART"
    ARTIST_SORT_ORDER = "soar"
    GENRE = "©gen"
    TRACK_NUMBER = "trkn"
    TRACK_TITLE = "©nam"
    TRACK_TITLE_SORT_ORDER = "sonm"
    YEAR = "©day"
    EXT = ".m4a"

    def __init__(self, filename, debug=False):
        self.filename = str(pathlib.Path(filename).resolve())
        self.basedir = str(pathlib.Path(filename).parent.resolve())
        self.debug = debug

        log_level = logging.DEBUG if self.debug else logging.INFO
        log_format = "%(asctime)s %(filename)s %(funcName)s %(message)s"
        logging.basicConfig(level=log_level, format=log_format)

        try:
            self.m4a = mp4.MP4(self.filename)
        except mp4.MP4StreamInfoError:
            logging.info(f"{self.filename} is not an m4a")

    def generate_filename(self) -> str:
        """Generate new filename from existing tags. Returns str.

        The filename is sanitized to remove any filesystem special characters.
        By default, The generated filename uses the following format:
        [track_number] [artist] - [track_title]

        Returns:
            str: new filename
        """
        self.sanitize_tags()
        artist = self.m4a.tags[self.ARTIST][0]
        track_title = self.m4a.tags[self.TRACK_TITLE][0]
        # Pad track number with leading zero if single digit.
        track_number = str(self.m4a.tags[self.TRACK_NUMBER][0][0]).zfill(2)
        return f"{self.basedir}/{track_number} {artist} - {track_title}.m4a"

    def rename(self) -> str:
        """Rename m4a file using name generated from existing tags.

        Returns:
            str: new filename
        """
        newname = self.generate_filename()
        if not self.filename == newname:
            try:
                logging.info(f"renaming {self.filename} to {newname}")
                shutil.move(self.filename, newname)
                self.filename = newname

            except FileNotFoundError:
                logging.debug(f"{newname} not found")

            except PermissionError:
                logging.debug(f"cannot rename {self.filename} to {newname}")

        return newname

    def sanitize_tag(self, tag: str) -> str:
        """Sanitize characters in tag. Returns string.

        Ensures that tags follow a consistent format.
        Converts all words in tag to upper case.
        Removes special filesystem characters if present.
        Converts square brackets to parentheses.
        Backslashes and whitespace padded dashes are
        converted to double emphasis unicode character.
        Example: Devil Doll (Demo/Remix Version).m4a
        becomes Devil Doll (Demo \u2014 Remix Version).m4a

        Returns:
            str: sanitized tag
        """

        # The em dash is used as separator character.
        separator = " -- "
        # em_dash = "\u2014"

        # Replace single dash with whitespace padding.
        dash_rgx = re.compile(r"(?<=[^-]{1,1})\s+-\s*(?=[^-]+)")
        tag = re.sub(dash_rgx, separator, tag)

        # Replace forward slashes with separator character.
        slash_rgx = re.compile(r"(?<=[^\/]{1,1})\s*\/+\s*(?=[^\/]+)")
        tag = re.sub(slash_rgx, separator, tag)

        # Convert square brackets to parentheses.
        tag = tag.translate(tag.maketrans("[]", "()"))

        # capitalize lower case words in tag
        tag = " ".join(
            [
                word.title() if not re.search(r"^\(?[0-9A-Z]", word) else word
                for word in tag.split()
            ]
        )
        return tag

    def sanitize_tags(self) -> None:
        """Sanitize several tags to follow a consistent format."""
        tag_names = (
            M4a.ALBUM,
            M4a.ALBUM_SORT_ORDER,
            M4a.ALBUM_ARTIST,
            M4a.ARTIST,
            M4a.ARTIST_SORT_ORDER,
            M4a.TRACK_TITLE,
            M4a.TRACK_TITLE_SORT_ORDER,
        )
        for tag_name in tag_names:
            try:
                clean_tag = self.sanitize_tag(self.m4a.tags[tag_name][0])
                self.set_tag(tag_name, clean_tag)
            except KeyError:
                logging.debug(f"{self.filename} tag name {tag_name} not found")

    def set_tag(self, tag_name: str, tag_value: str) -> None:
        """Update existing tag value."""
        try:
            if not self.m4a.tags[tag_name][0] == tag_value:
                log_message = f"{self.filename}: set {tag_name} to {tag_value}"
                logging.debug(log_message)
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
