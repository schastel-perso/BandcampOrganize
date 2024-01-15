usage: ./bandcamp_zip_archive.py [-h] [-w WORKDIR] [-o TARGETDIR] [--doit]
                                 [--band_album_delimiter_dash_delimiter BAND_ALBUM_DELIMITER_DASH_DELIMITER]
                                 [--reuse_existing_band_directory]
                                 zipfile

Organize the files in a Bandcamp zip archive

positional arguments:
  zipfile               The Bandcamp zip file to work with

options:
  -h, --help            show this help message and exit
  -w WORKDIR, --workdir WORKDIR
                        Working directory (default: /tmp/bandcamp)
  -o TARGETDIR, -t TARGETDIR, --targetdir TARGETDIR
                        The target directory (final directory is targetdir/band/album)
                        (default: /home/sc/Music)
  --doit
  --band_album_delimiter_dash_delimiter BAND_ALBUM_DELIMITER_DASH_DELIMITER
                        Position of the - that delimits the band and the album (default: 1)
  --reuse_existing_band_directory
                        Reuse existing band directory if an uppercase match is found
                        (default: False)
