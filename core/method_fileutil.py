#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# MIMEfield - MIME type mismatch detection tool
# Detection core module via 'file' utility
# Copyright (c) 2026 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/mimefield
# GitLab: https://gitlab.com/urbanware-org/mimefield
#

import subprocess


def get_mime_type(file_path):
    proc = subprocess.Popen(['file', '--brief', '--mime-type', file_path],
                            stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    mtype = stdout.decode("utf-8").replace("\n", "")

    return mtype
