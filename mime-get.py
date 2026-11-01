#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# MIMEfield - MIME type mismatch detection tool
# MIME determination script
# Copyright (c) 2022 by Ralf Kilian
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

    p.set_description("Determine MIME type from file.")
    p.set_epilog("Further information and usage examples can be found "
                 "inside the documentation file for this script.")

    # Required arguments
    p.add_avalue("-p", "--path", "path of file to determine the MIME type "
                 "from", "path", None, True)

    # Optional arguments
    p.add_predef("-m", "--method", "method to get the MIME type ('file' or "
                 "'magic', both by default)", "method", ["file", "magic"],
                 False)
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
    if not args.method:
        method = "both"
    else:
        method = args.method

    try:
        if not os.path.isfile(args.path):
            raise Exception("Path must be a file")
        print(main.get_mime_type(args.path, None, None, method))
    except Exception as e:
        p.error(e)


if __name__ == "__main__":
    main()

# EOF
