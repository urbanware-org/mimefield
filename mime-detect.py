#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# MIMEfield - MIME type mismatch detection tool
# MIME mismatch detection script
# Copyright (C) 2021 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/mimefield
# GitLab: https://gitlab.com/urbanware-org/mimefield
#

import os
import sys


def main():
    from core import clap
    from core import common
    from core import main

    try:
        p = clap.Parser()
    except Exception as e:
        print("%s: error: %s" % (os.path.basename(sys.argv[0]), e))
        sys.exit(1)

    p.set_description("Detect MIME type mismatches.")
    # p.set_epilog("Further information and usage examples can be found "
    #             "inside the documentation file for this script.")

    # Required arguments
    p.add_avalue("-e", "--extension", "File extension to check the MIME type "
                 "for", "extension", None, True)
    p.add_avalue("-m", "--mime", "MIME type string (or a part of it, case "
                 "insensitive, multiple enclosed with quotes and separated "
                 "with pipes)", "mime", None, True)
    p.add_avalue("-p", "--path", "path of the directory from which to check "
                 "the files for MIME type mismatches (recursive)", "path",
                 None, True)

    # Depending arguments
    if main.file_util():
        # In case the both the 'file' utility and 'libmagic' are installed on
        # the system, the preferred method must be given. If the utility is
        # missing, 'libmagic' is the only supported method and is being used
        # explicitly and the '--method' argument is disabled (does not exist).
        p.add_predef(None, "--method", "method to get the MIME type",
                     "method", ["file", "magic"], True)

    # Optional arguments
    p.add_switch("-v", "--verbose", "print detailed output",
                 "verbose", True, False)
    p.add_switch(None, "--version", "print the version number and exit", None,
                 True, False)

    if len(sys.argv) == 1:
        p.error("At least one required argument is missing.")
    elif ("-h" in sys.argv) or ("--help" in sys.argv):
        p.print_help()
        sys.exit(0)
    elif "--version" in sys.argv:
        print(common.get_version())
        sys.exit(0)

    args = p.parse_args()
    try:
        use_magic = True
        if main.file_util():
            if args.method == "file":
                use_magic = False
        main.get_mime_types(args.path, args.extension, args.mime, use_magic,
                            args.verbose)
    except Exception as e:
        p.error(e)


if __name__ == "__main__":
    main()

# EOF
