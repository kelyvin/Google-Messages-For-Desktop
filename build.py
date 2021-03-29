#!/usr/bin/env python
import os
import subprocess
from subprocess import Popen
import sys
import zipfile
from datetime import datetime
from pathlib import Path
import json
import shutil

import logging
import logging.handlers

from glob import glob

log_location = "./logs"
log_filename = "messagesbuild.log"
date_format = '%m/%d/%Y %H:%M:%S'

file_date_format = '%Y%m%d%H%M%S'
PATH_TO_ZIP = '/home/dale/python/jumarmarket/pnlcalc'
OUT_PATH = '/mnt/Dropbox/DEV'
FILENAME = '{0}_pnlcalc.zip'.format(datetime.now().strftime(file_date_format))
package_filename = './package.json'
distribution_folder = './dist'
output_folders = ['./Linux', './Mac', './Windows']
build_command = ['/usr/bin/npm', 'run', 'build:all']
zip_config = {'Linux': ['Linux', 'linux'], 'Mac': ['Mac', 'mac'], 'Windows': ['Windows', 'windows'],
              'Windows_Tray': ['Windows', 'windows-tray']}


def run_command(commands:list):
    print("running {0}".format(" ".join(commands)))
    p = Popen(commands, stdout=subprocess.PIPE)
    p.wait()
    print("".join([str(x) for x in commands]) + ": Success Code - " + str(p.returncode))
    return p.returncode, p.communicate()[0].decode('utf-8')

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dir, files in os.walk(path):
        for file_name in files:

            ziph.write(os.path.join(root, file_name), arcname='.' + PATH_TO_ZIP)

class MessageHandler:
    logger = None
    # https://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log-file

    def __init__(self):
        if not Path(log_location).exists():
            os.mkdir(Path(log_location))
        self.logger = logging.getLogger()
        if not len(self.logger.handlers):
            self.logger.setLevel(logging.DEBUG)
            # get console handler
            console_handler = logging.StreamHandler(sys.stdout)
            # get file handler
            log_full_path = Path(log_location, log_filename)
            file_handler = logging.handlers.TimedRotatingFileHandler(filename=log_full_path, when='MIDNIGHT',
                                                                     interval=1, backupCount=30)
            # create formatter
            formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s',
                                          datefmt=date_format)
            # add formatter to handlers
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)
            # set levels on handlers
            console_handler.setLevel(logging.INFO)
            file_handler.setLevel(logging.INFO)
            # sdd handlers to logger
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def log(self, lvl, msg):
        self.logger.log(lvl, msg)

class BuildMessages:
    _version:str = None

    def __init__(self):
        self._version = self.get_package_version()

    def clean(self):
        if Path(distribution_folder).exists():
            print("Removing {0}".format(str(Path(distribution_folder).absolute())))
            shutil.rmtree(Path(distribution_folder))
        for output_folder in output_folders:
            zipfiles = Path(output_folder).glob('*.zip')
            for zipfile in zipfiles:
                print("removing: {0}".format(zipfile))
                os.remove(zipfile)

    def get_package_version(self):
        with open(package_filename, 'rb') as f:
            run_info = json.loads(f.read())
            version = run_info.get('version')
        return version

    def create_output_files(self):
        for k, v in zip_config.items():
            path_to_zip = Path(distribution_folder, k)
            full_out_path = Path(v[0], "google-messages-{0}_v{1}".format(v[1], self._version))
            print("zipping {0} to {1}".format(path_to_zip, full_out_path))
            shutil.make_archive(full_out_path, 'zip', path_to_zip)



    def build(self):
        _, _ = run_command(build_command)









if __name__ == '__main__':
    print(os.getcwd())
    nativefier_version = (run_command(["nativefier", "--version"]))[1]
    print("printing nativefier version")
    print(nativefier_version)

    build_messages = BuildMessages()
    build_messages.clean()
    build_messages.build()
    build_messages.create_output_files()









    print("program finished")

"""

 
dir = 'path/to/dir'
shutil.rmtree(dir)
"""