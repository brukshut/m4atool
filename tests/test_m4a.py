#!/usr/bin/env python

import sys
sys.path.append('..')
import os
from m4atool import M4a
import pathlib
import shutil
import unittest

class M4ATestCase(unittest.TestCase):
    unittest.TestLoader.sortTestMethodsUsing = None
    test_m4a = 'go-speak-for-the-earth.m4a'

    def setUp(self):
        print(f"\n>> start: {self.shortDescription()}")

    def tearDown(self):
        print(f">> end: {self.shortDescription()}\n")

    def get_lossless(self):
        shutil.copy(f"sample/{self.test_m4a}", self.test_m4a)
        return M4a(pathlib.Path(self.test_m4a).resolve(), debug=True)

    def cleanup(self, filename):
        os.remove(filename)

    def test_sanitize_tag(self):
        """Test sanitization of tag."""
        lossless = self.get_lossless()
        dirty_tag = 'speak For the earth [live on WFMU]'
        clean_tag = 'Speak For The Earth (Live On WFMU)'
        self.assertEqual(lossless.sanitize_tag(dirty_tag), clean_tag)
        self.cleanup(lossless.filename)

    def test_set_genre(self):
        """Test updating genre tag in lossless file."""
        lossless = self.get_lossless()
        lossless.set_genre('DIY')
        self.assertEqual(lossless.m4a.tags[M4a.GENRE][0], 'DIY')
        self.cleanup(lossless.filename)

    def test_set_artist(self):
        """Test updating artist tag(s) in lossless file."""
        lossless = self.get_lossless()
        lossless.set_artist('Go! (NYC)')
        for tag in [M4a.ARTIST, M4a.ARTIST_SORT_ORDER, M4a.ALBUM_ARTIST]:
            self.assertEqual(lossless.m4a.tags[tag][0], 'Go! (NYC)')
        self.cleanup(lossless.filename)

    def test_set_album(self):
        """Test updating artist tag(s) in lossless file."""
        lossless = self.get_lossless()
        new_album_name = 'Your Power Means Nothing (Live On WFMU)'
        lossless.set_album(new_album_name)
        for tag in [M4a.ALBUM_SORT_ORDER, M4a.ALBUM]:
            self.assertEqual(lossless.m4a.tags[tag][0], new_album_name)
        self.cleanup(lossless.filename)


    def test_rename(self):
        """Test renaming of lossless file."""
        lossless = self.get_lossless()
        new_name = lossless.generate_filename()
        print(f"{lossless.filename} --> {new_name}")
        lossless.rename()
        self.assertEqual(lossless.filename, new_name)
        self.cleanup(new_name)

if __name__ == "__main__":
    unittest.main()