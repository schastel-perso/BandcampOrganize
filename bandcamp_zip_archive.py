#!/usr/bin/env python3
import os
import sys
import zipfile
import shutil

def process_arguments():
    import argparse
    parser = argparse.ArgumentParser(
                    prog=sys.argv[0],
                    description='Organize the files in a Bandcamp zip archive',
                    epilog='',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("zipfile", help="The Bandcamp zip file to work with")
    parser.add_argument('-w', '--workdir', help="Working directory", default="/tmp/bandcamp")
    parser.add_argument('-o', '-t', '--targetdir', help="The target directory (final directory is targetdir/band/album)",
                        default=os.environ['HOME'] + '/Music')
    parser.add_argument('--doit', default=False, action="store_true")
    parser.add_argument('--band_album_delimiter_dash_delimiter', default=1, type=int,
                        help="Position of the - that delimits the band and the album")
    parser.add_argument('--reuse_existing_band_directory', default=False, action="store_true",
                        help="Reuse existing band directory if an uppercase match is found")
    return parser.parse_args()


class BandcampArchive:
    def __init__(self, zipfilename, band_album_delimiter_dash_delimiter=1):
        self.zipfilename = zipfilename
        elements = self.zipfilename.split('/')[-1].replace('.zip', '').split('-')
        self.band = "-".join(elements[0:band_album_delimiter_dash_delimiter]).strip()
        print(f'Band: >>{self.band}<<')
        self.album = "-".join(elements[band_album_delimiter_dash_delimiter:]).strip()
        print(f'Album: >>{self.album}<<')

    def compute_targetdir(self, targetdir, override_existing_with_band):
        print(f'Searching for matching band name in {targetdir}')
        band_upper = self.band.upper()
        existing_band = None
        for file in os.listdir(targetdir):
            if file.upper() == band_upper and file != self.band:
                print(f"! Found possible matching bandname in {targetdir}: {file} when band is {self.band}")
                print(f"! Use --reuse_existing_band_directory")
                existing_band = file
        if override_existing_with_band:
            if existing_band is None:
                print('Cannot override band. First album of {self.band} in collection')
                overriden = False
            else:
                print(f'Band overriden: {existing_band} instead of {self.band}')
                overriden = True
                self.band = existing_band
        else:
            if existing_band is not None:
                print(f'targetdir not overriden')
            overriden = False
        print(f'debug: returning {targetdir}/{self.band}/{self.album}, {overriden}')
        return f'{targetdir}/{self.band}/{self.album}', overriden

    # def pretend_reorganize(self, workdir, targetdir):
    #     print("If --doit is used, here is what will be executed:")
    #     print(f'os.makedirs({workdir})')
    #     print(f'Unzip the zip archive into {workdir}, that is, create the following files:')
    #     with zipfile.ZipFile(self.zipfilename, 'r') as zip_ref:
    #         file_list = zip_ref.namelist()
    #         for filename in file_list:
    #             print(f' {filename}')
    #     print(f'os.makedirs({targetdir})')
    #     for filename in file_list:
    #         print(f'mv {workdir}/{filename} {targetdir}')
    #     print('If happy, add --doit')

    # def reorganize(self, workdir, targetdir, doit: bool):
    #     print(f'os.makedirs({workdir})')
    #     if doit: os.makedirs(workdir)
    #     print(f'Unzip the zip archive into {workdir}, that is, create the following files:')
    #     with zipfile.ZipFile(self.zipfilename, 'r') as zip_ref:
    #         if doit: zip_ref.extractall(workdir)
    #         file_list = zip_ref.namelist()
    #         for filename in file_list:
    #             print(f' {filename}')
    #     print(f'os.makedirs({targetdir})')
    #     if doit: os.makedirs({targetdir})
    #     for filename in file_list:
    #         print(f'mv {workdir}/{filename} {targetdir}')
    #         if doit: os.rename('{workdir}/{filename}', '{targetdir}')
    #     if doit: os.remove(workdir)
    #     if not doit: print('If happy, add --doit')

    def reorganize(self, workdir, targetdir, doit=False, override_with_existing_band=False):
        finaltargetdir, overriden = self.compute_targetdir(targetdir, override_with_existing_band)
        print(f'finaltargetdir={finaltargetdir}; overriden={overriden}')
        print(f'os.makedirs({workdir})')
        if doit: os.makedirs(workdir)
        print(f'Unzip the zip archive into {workdir}, that is, create the following files:')
        with zipfile.ZipFile(self.zipfilename, 'r') as zip_ref:
            if doit: zip_ref.extractall(workdir)
            file_list = zip_ref.namelist()
            for filename in file_list:
                print(f' {filename}')
        print(f'os.makedirs({finaltargetdir})')
        if doit: os.makedirs(f'{finaltargetdir}')
        for filename in file_list:
            print(f'mv {workdir}/{filename} {finaltargetdir}')
            if doit: shutil.move(f'{workdir}/{filename}', f'{finaltargetdir}')
        print(f'os.remove({workdir})')
        if doit: os.rmdir(f'{workdir}')
        if not doit: print('If happy, add --doit')


if __name__ == '__main__':
    arguments = process_arguments()
    bandcamp_archive = BandcampArchive(zipfilename=arguments.zipfile,
                                       band_album_delimiter_dash_delimiter=arguments.band_album_delimiter_dash_delimiter)
    bandcamp_archive.reorganize(workdir=arguments.workdir, targetdir=arguments.targetdir,
                                doit=arguments.doit,
                                override_with_existing_band=arguments.reuse_existing_band_directory)

