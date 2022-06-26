# m4atool

`m4atool.py` is a python utility that uses `mutagen` for manipulating apple lossless files. When you purchase a song from the iTunes store, it comes in an Apple Lossless format with a `.m4a` extension. This utility is intended to make it easy to perform bulk modification of apple lossless files. The Apple lossless format is proprietary but has been reversed engineered. See https://mutagen.readthedocs.io/en/latest/api/mp4.html?highlight=mp4#module-mutagen.mp4.

## Usage
```
user% ./m4atool.py
usage: m4atool.py [-h] --basedir BASEDIR [--rename] [--debug] [--album ALBUM] [--artist ARTIST] [--genre GENRE]
m4atool.py: error: the following arguments are required: --basedir/-b

```
## Functionality

- It requires a base directory argument that is recursively searched, generating a list of all files with an `.m4a` extension.
- It sanitizes album, album artist, artist, genre and track title tags tags, ensuring that they follow a consistent format that avoids certain characters.
- It permits bulk updating of album, album artist, artist and genre tags.
- It renames files using a preferred format.

## Sanitizing Tags

The tags for album, album artist, artist, genre and track titles should use the following rules.

- All strings in tags should be capitalized, so `How Low Can a punk Get?` becomes `How Low Can A Punk Get?`
- All square brackets in tags should be converted to parentheses.

## Renaming Files

- The default filename format for songs downloaded from the Apple Store is `00 track_title.m4a`
- The utility will extract tags from the downloaded file and use them to construct a new file name.
- The desired format is `00 artist - track_title.m4a` with the first field being the zero padded track number.
- The utility will rename a file from the iTunes store named `01 Checkmate.m4a` to `01 Hot Snakes - Checkmate.m4a`
- The tags will be sanitized first using the rules mentioned above, thus `18 How Low can a Punk get? [studio take].m4a` is renamed to `18 Bad Brains - How Low Can A Punk Get? (Studio Take).m4a`.

## Bulk Tag Updates

- The album, artist, and genre tags can be overridden and updated on all files.
