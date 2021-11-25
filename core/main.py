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

import os
import re
import shutil
import subprocess
import sys


def file_util():
    """
        Determine if the 'file' utility is installed on the system.
    """
    file_util_path = shutil.which("file")
    return file_util_path is not None


def get_mime_type(path, use_magic=False):
    """
        Get the MIME type of a single file.
    """
    if not os.path.isfile(path):
        return None

    # In case the both the 'file' utility and 'libmagic' are installed on
    # the system, the preferred method must be given. If the utility is
    # missing, 'libmagic' is the only supported method to read out the MIME
    # information from a file.
    #
    # The 'file' utility is included in all (or most) Unix-like operating
    # systems (such as Linux and BSD) by default. However, it does not exist
    # on Windows operating systems, so the 'libmagic' library is used there.
    if use_magic:
        try:
            import magic
        except Exception as e:
            raise Exception("Required module 'magic' is not installed")
        m = magic.open(magic.MAGIC_NONE)
        m.load()
        ftype = m.file(path)
    else:
        p = subprocess.Popen(['file', '--brief', '--mime-type', path],
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        ftype = stdout.decode("utf-8").replace("\n", "")

    if ftype == "empty":
        ftype = ""

    return ftype


def get_mime_types(directory, extension, mimetype, use_magic=False,
                   verbose=False):
    """
        Check all files with the given extension inside the given directory
        as well as all its sub-directories and print type MIME mismatches
        (if existing and if verbose).
    """
    if verbose:
        if use_magic:
            method = "'libmagic' module"
        else:
            method = "'file' utility"

        print("Detecting MIME types via %s. Please wait." % method)

    files_checked, files_mismatch = __get_mime_types(directory, extension,
                                                     mimetype, use_magic)

    if len(files_mismatch) == 0:
        if verbose:
            print("No mismatches found with the given criteria.")
        sys.exit(0)

    if verbose:
        files_mismatch.sort()
        for mismatch in files_mismatch:
            path = mismatch[0]
            ftype = re.sub(", Title.*$", "", mismatch[1], flags=re.I)

            print("  - Type mismatch found:")
            print("      - File:   %s" % path)
            print("      - Type:   %s" % ftype)

        if len(files_mismatch) > 1:
            print("Type mismatches found (%s in total), see above." %
                  len(files_mismatch))
        else:
            print("Type mismatch found, see above.")
    sys.exit(1)


def __get_mime_types(directory, extension, mimetype, use_magic=False):
    """
        Recursively get all files with the given extension inside the given
        directory and check each for mismatches.
    """
    files_checked = []
    files_mismatch = []

    if not extension.startswith("."):
        extension = "." + extension

    for root, subdirs, files in os.walk(directory):
        for item in files:
            if not item.endswith(extension):
                continue
            path = os.path.join(root, item)

            ftype = get_mime_type(path, use_magic).lower()
            if ftype is not None:
                mismatch = True
                for mime in mimetype.split("|"):
                    if mime.strip().lower() in ftype:
                        mismatch = False
                        break

                if mismatch:
                    files_mismatch.append([path, ftype])
                else:
                    files_checked.append(path)

    return files_checked, files_mismatch

# EOF
