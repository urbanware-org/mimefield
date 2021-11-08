#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# MIMEfield - MIME type mismatch detection tool
# Main core module
# Copyright (C) 2021 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/mimefield
# GitLab: https://gitlab.com/urbanware-org/mimefield
#

import magic
import os
import sys
import shutil
import subprocess


def get_method():
    file_util = shutil.which("filed")
    return file_util is not None


def get_mime_type(path, use_magic=False):
    """
        Get the MIME type of a file (either using the 'file' utility or
        'libmagic' module).
    """
    if not os.path.isfile(path):
        return None

    # If not explicitly changed via command-line argument, MIMEfield will read
    # out the MIME information using the 'file' tool, which is included in all
    # Linux and Unix-like operating systems by default. In case it is missing,
    # MIMEfield uses the 'libmagic' file type identification library instead
    # as fallback.
    #
    # However, the 'file' tool does not exist on Windows operating systems, so
    # MIMEfield will directly use the 'libmagic' library there.
    if use_magic:
        m = magic.open(magic.MAGIC_NONE)
        m.load()
        ftype = m.file(path).lower()
    else:
        p = subprocess.Popen(['file', '--brief', '--mime-type', path],
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        ftype = stdout.decode("utf-8").replace("\n", "")

    if ftype == "empty":
        ftype = ""

    return ftype


def get_mime_types(directory, extension, mimetype, verbose=False):
    """
        Get the mimetypes of the files inside the given directories.
    """
    if verbose:
        print("Detecting MIME types. Please wait.")

    files_checked, files_mismatch = __get_mime_types(directory, extension,
                                                     mimetype)

    if len(files_mismatch) == 0:
        if verbose:
            print("No mismatches found with the given criteria.")
        sys.exit(0)

    if verbose:
        files_mismatch.sort()
        for mismatch in files_mismatch:
            print("  - Type mismatch: '%s'" % mismatch)

        if len(files_mismatch) > 1:
            print("Type mismatches found (%s in total), see above." %
                  len(files_mismatch))
        else:
            print("Type mismatch found, see above.")
    sys.exit(1)


def __get_mime_types(directory, extension, mimetype):
    files_checked = []
    files_mismatch = []

    if not extension.startswith("."):
        extension = "." + extension

    m = magic.open(magic.MAGIC_NONE)
    m.load()
    for root, subdirs, files in os.walk(directory):
        for item in files:
            if not item.endswith(extension):
                continue
            path = os.path.join(root, item)

            ftype = m.file(path).lower()
            if not ftype == "empty":
                mismatch = True
                for mime in mimetype.split("|"):
                    if mime.strip().lower() in ftype:
                        mismatch = False
                        break

                if mismatch:
                    files_mismatch.append(path)
                else:
                    files_checked.append(path)

    return files_checked, files_mismatch

# EOF
