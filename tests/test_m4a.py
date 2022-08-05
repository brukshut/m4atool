#!/usr/bin/env python

from m4atool import M4a
from pyfakefs.fake_filesystem_unittest import TestCase
import os
import unittest


class M4ATestCase(TestCase):
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures")
    test_m4a = f"{fixture_path}/go-speak-for-the-earth.m4a"

    def setUp(self):
        self.setUpPyfakefs()
        self.fs.add_real_file(self.test_m4a, read_only=False)
        print(f">> start: {self.shortDescription()}\n")

    def tearDown(self):
        print(f">> end: {self.shortDescription()}\n")

    def test_sanitize_tag(self):
        """Test sanitization of dash and blackslash characters in tags."""
        lossless = M4a(self.test_m4a, debug=True)
        dirty_tag = "speak For the earth [live on WFMU]"
        clean_tag = "Speak For The Earth (Live On WFMU)"
        assert dirty_tag != clean_tag
        self.assertEqual(lossless.sanitize_tag(dirty_tag), clean_tag)
        words = ["foo - bar ", "foo -bar", "foo/bar", "foo // bar", "foo -- bar"]
        for word in words:
            print(f"{word} --> {lossless.sanitize_tag(word)}")
            self.assertEqual(lossless.sanitize_tag(word), "Foo -- Bar")

    def test_sanitize_tag_backslash(self):
        """Test sanitization of square brackets in tag."""
        lossless = M4a(self.test_m4a, debug=True)
        dirty_tag = "speak For the earth [demo/WFMU]"
        clean_tag = "Speak For The Earth (Demo -- WFMU)"
        print(f"{dirty_tag} --> {clean_tag}")
        self.assertEqual(lossless.sanitize_tag(dirty_tag), clean_tag)

    def test_m4a_set_genre(self):
        """Test updating genre tag in lossless file."""
        lossless = M4a(self.test_m4a, debug=True)
        lossless.set_genre("DIY")
        self.assertEqual(lossless.m4a.tags[M4a.GENRE][0], "DIY")

    def test_m4a_set_artist(self):
        """Test updating artist tag(s) in lossless file."""
        lossless = M4a(self.test_m4a, debug=True)
        lossless.set_artist("Go! (NYC)")
        for tag in [M4a.ARTIST, M4a.ARTIST_SORT_ORDER, M4a.ALBUM_ARTIST]:
            self.assertEqual(lossless.m4a.tags[tag][0], "Go! (NYC)")

    def test_m4a_set_album(self):
        """Test updating artist tag(s) in lossless file."""
        lossless = M4a(self.test_m4a, debug=True)
        new_album_name = "Your Power Means Nothing (Live On WFMU)"
        lossless.set_album(new_album_name)
        for tag in [M4a.ALBUM_SORT_ORDER, M4a.ALBUM]:
            self.assertEqual(lossless.m4a.tags[tag][0], new_album_name)

    def test_m4a_rename(self):
        """Test renaming of lossless file."""
        lossless = M4a(self.test_m4a, debug=True)
        new_name = lossless.generate_filename()
        print(f"{lossless.filename} --> {new_name}")
        lossless.rename()
        self.assertEqual(lossless.filename, new_name)


if __name__ == "__main__":
    unittest.main()
