#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# MIMEfield - MIME type mismatch detection tool
# Main core module
# Copyright (C) 2022 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/mimefield
# GitLab: https://gitlab.com/urbanware-org/mimefield
#

import os
import shutil
import subprocess
import sys

try:
    import magic
except:
    pass

def file_util():
    """
        Determine if the 'file' utility is installed on the system.
    """
    file_util_path = shutil.which("file")
    return file_util_path is not None


def get_mime_type(path, extension, mimetype, method, ignore_empty=False,
                  cut_off=False, maximum=0):
    """
        Get the MIME type of a single file or all files from a directory and
        its sub-directories.
    """

    try:
        maximum = int(maximum)
    except:
        maximum = 0

    if os.path.isfile(path):
        return __get_mime_type(path, method, ignore_empty=False)

    while "|" * 2 in mimetype:
        mimetype = mimetype.replace("|" * 2, "|").strip("|")

    files_checked, files_mismatch = __get_mime_types(path, extension,
                                                     mimetype, method,
                                                     ignore_empty,
                                                     maximum)

    if not maximum == 0 and len(files_checked) >= maximum:
        print("No mismatches found with the given criteria (limited to "
              "%s items)." % str(maximum))
        sys.exit(0)
    if len(files_mismatch) == 0:
        print("No mismatches found with the given criteria.")
        sys.exit(0)

    print()
    count = 0
    files_mismatch.sort()
    for mismatch in files_mismatch:
        count += 1
        file_path = mismatch[0]
        ftype = mismatch[1].split(",")[0]
        if cut_off:
            file_path = \
                file_path.replace(path, "").strip("/").strip("\\")[:64]
            ftype = ftype[:64]
        if count == 1:
            print("┌─ Type mismatch:")
        else:
            print("├─ Type mismatch:")
        print("├──── File:   %s" % file_path)
        if count == len(files_mismatch):
            print("└──── Type:   %s" % ftype)
        else:
            print("├──── Type:   %s" % ftype)
            print("│")
    print()

    if count > 1:
        if maximum == 0:
            print("Type mismatches found (%s in total), see above."
                  % len(files_mismatch))
        else:
            if len(files_mismatch) > maximum:
                print("Type mismatches found (%s in total, limited to %s "
                      "items), see above." % (len(files_mismatch),
                                              str(maximum)))
            else:
                print("Type mismatches found (%s in total), see above." %
                      len(files_mismatch))
    else:
        print("Type mismatch found, see above.")
    sys.exit(1)


def __get_mime_type(path, method, ignore_empty):
    """
        Get the MIME type of a single file.
    """
    # The 'file' utility is included in all (or most) Unix-like operating
    # systems (such as Linux and BSD) by default. However, it does not exist
    # on Windows operating systems, so the 'libmagic' library is (or must) be
    # used there.
    ftype = ""

    if method == "both" or method == "file":
        if not file_util():
            raise Exception(
                "The 'file' utility is not available on this system")
        proc = subprocess.Popen(['file', '--brief', '--mime-type', path],
                                stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        ftype = stdout.decode("utf-8").replace("\n", "")

        proc = subprocess.Popen(['file', '--brief', path],
                                stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        ftype += "|" + stdout.decode("utf-8").replace("\n", "").split(",")[0]

    if method == "both" or method == "magic":
        try:
            m = magic.open(magic.MAGIC_NONE)
        except:
            raise Exception(
                "The Python module 'magic' does not seem to be installed")
        m.load()
        if m.file(path) is not None:
            output = m.file(path).split(",")[0]
            if not ftype.endswith(output):
                if method == "both":
                    separator = "|"
                else:
                    separator = ""
                ftype += separator + m.file(path).split(",")[0]

    for item in ftype.split("|"):
        if item == "inode/x-empty" or item == "empty" or item == "":
            if item == "inode/x-empty":
                if ignore_empty:
                    ftype = None
            else:
                if ignore_empty:
                    ftype = None
                else:
                    ftype = "(empty)"

    return ftype


def __get_mime_types(path, extension, mimetype, method, ignore_empty,
                     maximum):
    """
        Recursively get the MIME type of all files from a directory and its
        sub-directories.
    """
    files_checked = []
    files_mismatch = []
    is_maximum = False

    if not extension.startswith("."):
        extension = "." + extension

    for root, subdirs, files in os.walk(path):
        for item in files:
            if not item.endswith(extension):
                continue

            file_path = os.path.join(root, item)
            ftype = __get_mime_type(file_path, method, ignore_empty)
            if ftype is not None:
                mismatch = True
                for mime in mimetype.split("|"):
                    if mime.strip().lower() in ftype.lower():
                        mismatch = False
                        break

                if mismatch:
                    files_mismatch.append([file_path, ftype])
                else:
                    files_checked.append(file_path)

            if len(files_checked) == maximum:
                is_maximum = True
                break

        if is_maximum:
            break

    return files_checked, files_mismatch

# EOF
