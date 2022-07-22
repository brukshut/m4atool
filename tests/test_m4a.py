#!/usr/bin/env python

import sys
sys.path.append('..')
import unittest
from m4atool import M4a
import shutil


class M4ATestCase(unittest.TestCase):
    unittest.TestLoader.sortTestMethodsUsing = None
    test_m4a = 'sample-test/x-i-must-not-think-bad-thoughts.m4a'

    def setUp(self):
        print(f"\n>> start: {self.shortDescription()}")
        shutil.copytree('sample', 'sample-test')

    def tearDown(self):
        print(f">> end: {self.shortDescription()}\n")
        shutil.rmtree('sample-test')

    def test_sanitize_tag(self):
        """Test sanitization of tag."""
        lossless = M4a(self.test_m4a)
        tag = 'how low can a punk get? [alternate take]'
        self.assertEqual(
            lossless._sanitize_tag(tag), "How Low Can A Punk Get? (Alternate Take)"
        )

    def test_set_genre(self):
        """Test updating genre tag in lossless file."""
        lossless = M4a(self.test_m4a)
        lossless.set_genre('Rock')
        self.assertEqual(lossless.m4a.tags[M4a.GENRE][0], 'Rock')

    def test_set_artist(self):
        """Test updating artist tag(s) in lossless file."""
        lossless = M4a(self.test_m4a)
        lossless.set_artist('XXX')
        self.assertEqual(lossless.m4a.tags[M4a.ARTIST_SORT_ORDER][0], 'XXX')
        self.assertEqual(lossless.m4a.tags[M4a.ALBUM_ARTIST][0], 'XXX')
        self.assertEqual(lossless.m4a.tags[M4a.ARTIST][0], 'XXX')
        ## reset artist in test lossless file
        lossless.set_artist('X')

    def test_set_album(self):
        """Test updating artist tag(s) in lossless file."""
        lossless = M4a(self.test_m4a)
        lossless.set_album('XXX')
        self.assertEqual(lossless.m4a.tags[M4a.ALBUM_SORT_ORDER][0], 'XXX')
        self.assertEqual(lossless.m4a.tags[M4a.ALBUM][0], 'XXX')
        ## reset artist in test lossless file
        lossless.set_album('X')

    def test_rename(self):
        """Test renaming of lossless file."""
        lossless = M4a(self.test_m4a)
        new_name = 'sample-test/17 X - I Must Not Think Bad Thoughts (Demo -- Remix Version).m4a'
        lossless.rename()
        self.assertEqual(lossless.filename, new_name)


if __name__ == "__main__":
    unittest.main()
