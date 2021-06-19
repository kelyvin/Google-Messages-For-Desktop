#!/usr/bin/env python
"""
Basic python build script to clean, build and package
Google Message for Desktop
Author: Dale Furrow
License: MIT
"""
import json
import logging
import logging.handlers
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from subprocess import Popen
import argparse
import zipfile

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
            # stdout_handler = logging.StreamHandler(sys.stdout)
            # create formatter
            formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s',
                                          datefmt=date_format)
            # add formatter to handlers
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)
            # stdout_handler.setFormatter(formatter)
            # set levels on handlers
            console_handler.setLevel(logging.INFO)
            file_handler.setLevel(logging.INFO)
            # stdout_handler.setLevel(logging.DEBUG)
            # sdd handlers to logger
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
            # self.logger.addHandler(stdout_handler)
            self.logger.log(level=logging.INFO, msg="Logger initialized")

    def log(self, msg, lvl=logging.INFO):
        self.logger.log(lvl, msg)


MESSAGEHANDLER = MessageHandler()


def run_command(commands: list):
    MESSAGEHANDLER.log("running {0}".format(" ".join(commands)))
    p = Popen(commands, stdout=subprocess.PIPE)
    p.wait()
    MESSAGEHANDLER.log("".join([str(x) for x in commands]) + ": Success Code - " + str(p.returncode))
    std_output = p.communicate()[0].decode('utf-8')
    std_output = '\n'.join([x for x in std_output.splitlines() if len(x) > 0])
    return p.returncode, std_output

def zipdir(dir_path, out_path):
    # ziph is zipfile handle
    with zipfile.ZipFile(file=out_path, mode='w', compression=zipfile.ZIP_LZMA, compresslevel=9) as ziph:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                ziph.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file),
                                           os.path.join(dir_path, '..')))

class BuildMessages:
    _version: str = None

    def __init__(self):
        self._version = self.get_package_version()

    @staticmethod
    def clean():
        MESSAGEHANDLER.log("Cleaning distribution directory and zipfiles...")
        if Path(distribution_folder).exists():
            MESSAGEHANDLER.log("Removing {0}".format(str(Path(distribution_folder).absolute())))
            shutil.rmtree(Path(distribution_folder))
        for output_folder in output_folders:
            zipfiles = Path(output_folder).glob('*.zip')
            for zipfile in zipfiles:
                MESSAGEHANDLER.log("removing: {0}".format(zipfile))
                os.remove(zipfile)

    @staticmethod
    def get_package_version():
        with open(package_filename, 'rb') as f:
            run_info = json.loads(f.read())
            version = run_info.get('version')
        return version

    def package(self):
        MESSAGEHANDLER.log('Zipping output to directories...')
        for k, v in zip_config.items():
            path_to_zip = Path(distribution_folder, k).glob('*/').__next__()
            full_out_path = Path(v[0], "google-messages-{0}_v{1}.zip".format(v[1], self._version))
            MESSAGEHANDLER.log("zipping {0} to {1}".format(path_to_zip, full_out_path))
            zipdir(dir_path=path_to_zip, out_path=full_out_path)

    @staticmethod
    def build():
        MESSAGEHANDLER.log('Building from Nativefier and Electron...')
        ret_code, output = run_command(build_command)
        MESSAGEHANDLER.log("Built with returncode {0}".format(str(ret_code)))
        MESSAGEHANDLER.log("Build output begins...")
        MESSAGEHANDLER.log(str(output))
        MESSAGEHANDLER.log("End Build output...")

def main(args):
    MESSAGEHANDLER.log(args)
    MESSAGEHANDLER.log(os.getcwd())
    build_messages = BuildMessages()
    if args.action == 'clean':
        build_messages.clean()
    elif args.action == 'build':
        build_messages.build()
    elif args.action == 'package':
        build_messages.package()
    elif args.action == 'all':
        build_messages.clean()
        build_messages.build()
        build_messages.package()
    else:
        MESSAGEHANDLER.log("{0}: Unrecognized Command!".format(args))
    MESSAGEHANDLER.log("program finished")



if __name__ == '__main__':
    build_parser = argparse.ArgumentParser('Clean, Build and/or Package Google Messages App')
    build_parser.add_argument('action', metavar='action', nargs='?', type=str, help='accepts: clean, build, package, or all')
    args = build_parser.parse_args()
    main(args)

