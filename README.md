# m4atool

`m4atool.py` is a python utility for manipulating Apple Lossless files. This utility is intended to facilitate the bulk modification of Lossless files with an `*m4a` extension. Although proprietary, the Apple Lossless format has been reversed engineered. See https://mutagen.readthedocs.io/en/latest/api/mp4.html?highlight=mp4#module-mutagen.mp4.

## Setup

Create a virtual environment and install required packages.
```
user% python -m venv venv
user% source venv/bin/activate
user% pip install -r requirements.txt
user% pip install .
```
## Usage
```
user% m4atool
usage: m4atool [-h] [--basedir BASEDIR] [--debug] [--filename FILENAME] [--rename] [--sanitize] [--album ALBUM] [--artist ARTIST]
               [--genre GENRE]
m4atool: error: Please specify --basedir or --filename.
```
## Functionality

- It requires either a base directory argument or a filename argument.
- If a directory argument is given, the directory is recursed producing a list of m4a files.
- It allows sanitizing of album, album artist, artist, genre and track title tags tags, ensuring that they follow a consistent format that avoids certain characters.
- It permits bulk updating of album, artist, and genre tags.
- It renames files using a preferred format that is composed of several existing tags.

## Sanitizing Tags

The tags for album, album artist, artist, genre and track titles are sanitized using the following rules.

- All strings in tags are capitalized, so `How Low Can a punk Get?` becomes `How Low Can A Punk Get?`
- All square brackets in tags are converted to parentheses.
- All backslash characters are converted to ` -- `.
- All single dashes with whitespace padding are converted to ` -- `.

## Renaming Files

- The utility will extract tags from the Lossless file and use them to construct a new file name.
- The default format is `01 {artist} - {track_title}.m4a` with the first field a zero padded track number.
- The utility will rename the file `01 Checkmate.m4a` to `01 Hot Snakes - Checkmate.m4a`.
- The tags will be sanitized first using the rules mentioned above, thus `18 How Low can a Punk get? [studio take].m4a` is renamed to `18 Bad Brains - How Low Can A Punk Get? (Studio Take).m4a`.

## Bulk Tag Updates

- The album, artist, and genre tags can be overridden and updated on all files.

## Testing

There are unittests for M4a class in the `tests` directory.
```
(venv) user% cd tests/
(venv) user% ls
(venv) user% python -m unittest test_m4a.py
```