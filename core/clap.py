#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Clap - Command-line argument parser module
# Copyright (c) 2026 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/clap
# GitLab: https://gitlab.com/urbanware-org/clap
#

__version__ = "1.2.0"


try:
    import argparse
except ImportError as e:
    raise ImportError(
        "The module 'argparse' cannot be imported and 'optparse' is no "
        "longer supported") from e


def get_version():
    """
        Return the version of this module.
    """
    return __version__


class Parser():
    """
        Project independent command-line argument parser class.
    """

    def __init__(self):
        self.__arg_parser = argparse.ArgumentParser(add_help=False)
        self.__arg_grp_req = \
            self.__arg_parser.add_argument_group("required arguments")
        self.__arg_grp_opt = \
            self.__arg_parser.add_argument_group("optional arguments")

    def add_avalue(self, arg_short, arg_long, arg_help, arg_dest, arg_default,
                   arg_required):
        """
            Add an argument that expects a single user-defined value.
        """
        if arg_required:
            obj = self.__arg_grp_req
        else:
            obj = self.__arg_grp_opt

        if arg_default is not None:
            # Enclose the value with quotes in case it is not an integer
            if isinstance(arg_default, int):
                quotes = ""
            else:
                quotes = "'"

            if arg_help.strip().endswith(")"):
                arg_default = str(arg_default)
                arg_help = arg_help.rstrip(")")
                arg_help += f", default is {quotes}{arg_default}{quotes})"
            else:
                arg_help += f", default is {quotes}{arg_default}{quotes})"

        if arg_short is None:
            obj.add_argument(arg_long, help=arg_help, dest=arg_dest,
                             default=arg_default, required=arg_required)
        else:
            obj.add_argument(arg_short, arg_long, help=arg_help,
                             dest=arg_dest, default=arg_default,
                             required=arg_required)

    def add_predef(self, arg_short, arg_long, arg_help, arg_dest, arg_choices,
                   arg_required):
        """
            Add an argument that expects a certain predefined value.
        """
        if arg_required:
            obj = self.__arg_grp_req
        else:
            obj = self.__arg_grp_opt

        if arg_short is None:
            obj.add_argument(arg_long, help=arg_help, dest=arg_dest,
                             choices=arg_choices, required=arg_required)
        else:
            obj.add_argument(arg_short, arg_long, help=arg_help,
                             dest=arg_dest, choices=arg_choices,
                             required=arg_required)

    def add_switch(self, arg_short, arg_long, arg_help, arg_dest, arg_store,
                   arg_required):
        """
            Add an argument that does not expect anything, but returns a
            boolean value.
        """
        if arg_required:
            obj = self.__arg_grp_req
        else:
            obj = self.__arg_grp_opt

        if arg_store:
            arg_store = "store_true"
        else:
            arg_store = "store_false"

        if arg_short is None:
            obj.add_argument(arg_long, help=arg_help, dest=arg_dest,
                             action=arg_store, required=arg_required)
        else:
            obj.add_argument(arg_short, arg_long, help=arg_help,
                             dest=arg_dest, action=arg_store,
                             required=arg_required)

    def dependency(self, arg_name, arg_value, dependency):
        """
            Check the dependency of a command-line argument.
        """
        if dependency is not None:
            if arg_value is None or str(arg_value) == "":
                raise ValueError(
                    f"The '{arg_name}' argument depends on '{dependency}'.")

    def error(self, obj):
        """
            Raise an error and cause the argument parser to print the error
            message.
        """
        if isinstance(obj, str):
            obj = obj.strip()

        self.__arg_parser.error(obj)

    def parse_args(self):
        """
            Parse and return the command-line arguments.
        """
        return self.__arg_parser.parse_args()

    def print_help(self):
        """
            Print the usage, description, argument details and epilog.
        """
        self.__arg_parser.print_help()

    def set_description(self, string):
        """
            Set the description text.
        """
        self.__arg_parser.description = string.strip()

    def set_epilog(self, string):
        """
            Set the epilog text.
        """
        self.__arg_parser.epilog = string.strip()
