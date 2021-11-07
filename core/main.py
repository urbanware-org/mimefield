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
            __exit(0, "No mismatches found with the given criteria")

    if verbose:
        files_mismatch.sort()
        for mismatch in files_mismatch:
            print("  - Type mismatch: '%s'" % mismatch)

        if len(files_mismatch) > 1:
            __exit(1, "Type mismatches found (%s in total), see above" %
                   len(files_mismatch))
        else:
            __exit(1, "Type mismatch found, see above")


def __exit(exit_code, message=""):
    if message:
        print(message + ".")
    sys.exit(exit_code)


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
