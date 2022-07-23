# m4atool

`m4atool.py` is a python utility for manipulating Apple Lossless files. This utility is intended to facilitate the perform bulk modification of Lossless files. The Apple Lossless format is proprietary but has been reversed engineered. See https://mutagen.readthedocs.io/en/latest/api/mp4.html?highlight=mp4#module-mutagen.mp4.

## Setup

Create a virtual environment and install required modules.
```
user% python -m venv venv
user% source venv/bin/activate
user% pip install -r requirements.txt
Collecting mutagen==1.45.1
  Using cached mutagen-1.45.1-py3-none-any.whl (218 kB)
Installing collected packages: mutagen
Successfully installed mutagen-1.45.1
```

## Installation
```
[shiloh.local:~/Desktop/workspace/m4atool] brukshut% pip install .
Processing /Users/brukshut/Desktop/workspace/m4atool
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Installing backend dependencies ... done
  Preparing metadata (pyproject.toml) ... done
Requirement already satisfied: mutagen in /Users/brukshut/.pyenv/versions/3.9.11/lib/python3.9/site-packages (from m4atool==0.0.1) (1.45.1)
Building wheels for collected packages: m4atool
  Building wheel for m4atool (pyproject.toml) ... done
  Created wheel for m4atool: filename=m4atool-0.0.1-py3-none-any.whl size=5940 sha256=63b10a10d279a3af0e64b2d640b283d737303908a7c44371dd1f0bcec6db6c18
  Stored in directory: /private/var/folders/pr/h3bb2fjs7kzfc2tjhtw237ww0000gn/T/pip-ephem-wheel-cache-c2_4nxcb/wheels/23/ca/56/cf0f084c9ce7597e868ffd7cce73942d902c907ed5a84bcd83
Successfully built m4atool
Installing collected packages: m4atool
  Attempting uninstall: m4atool
    Found existing installation: m4atool 0.0.1
    Uninstalling m4atool-0.0.1:
      Successfully uninstalled m4atool-0.0.1
Successfully installed m4atool-0.0.1
```

## Usage
```
user% ./m4atool.py
usage: m4atool.py [-h] --basedir BASEDIR [--rename] [--debug] [--album ALBUM] [--artist ARTIST] [--genre GENRE]
m4atool.py: error: the following arguments are required: --basedir/-b
```
## Functionality

- It requires a base directory argument that is recursively searched, generating a list of all files with an `.m4a` extension.
- It sanitizes album, album artist, artist, genre and track title tags tags, ensuring that they follow a consistent format that avoids certain characters.
- It permits bulk updating of album, artist, and genre tags.
- It renames files using a preferred format that is composed of several existing tags.

## Sanitizing Tags

The tags for album, album artist, artist, genre and track titles are sanitized using the following rules.

- All strings in tags are capitalized, so `How Low Can a punk Get?` becomes `How Low Can A Punk Get?`
- All square brackets in tags are converted to parentheses.
- All backslash characters are converted to ` -- ` with leading and trailing whitespace.
- All single dashes are converted to ` -- ` with leading and trailing whitespace.

## Renaming Files

- The utility will extract tags from the downloaded file and use them to construct a new file name.
- The desired format is `00 {artist} - {track_title}.m4a` with the first field a zero padded track number.
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