#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# MIMEfield - MIME type mismatch detection tool
# MIME determination script
# Copyright (C) 2021 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/mimefield
# GitLab: https://gitlab.com/urbanware-org/mimefield
#

import magic
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

    p.set_description("Determine MIME type from file.")
    # p.set_epilog("Further information and usage examples can be found "
    #             "inside the documentation file for this script.")

    # Required arguments
    p.add_avalue("-p", "--path", "path of file to determine the files from",
                 "path", None, True)

    # Optional arguments

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
        print(main.get_mime_type(args.path))
    except FileNotFoundError as e:
        p.error(e)
    except PermissionError as e:
        p.error(e)
    except Exception as e:
        p.error(e)


if __name__ == "__main__":
    main()

# EOF
