# *MIMEfield* <img src="https://raw.githubusercontent.com/urbanware-org/mimefield/main/mimefield.png" alt="MIMEfield logo" height="128px" width="128px" align="right"/>

**Table of contents**
*   [Definition](#definition)
*   [Details](#details)
*   [Usage](#usage)
*   [Requirements](#requirements)
*   [Contact](#contact)
*   [Useless facts](#useless-facts)

----

## Definition

The *MIMEfield* project is a simple tool to determine if the extension of a file matches with the expected MIME type.

[Top](#mimefield-)

## Details

In case your operating system identifies files by their extension rather than MIME type, there are problems opening them with the corresponding program. This is the usual behavior of *Windows*.

For example when saving an *OpenDocument* file (`.odt`) with the extension `.zip` (weird and unlike example, but explains it pretty good), double-clicking the file would open the archive tool instead of the corresponding text editor (e.g. *OpenOffice* or *LibreOffice*).

The *MIMEfield* project consists of two components.

With the `mime-get.py` script you can get the MIME type of a file. For example, if you want to know which MIME type a file has. Thus,
it can be determined which MIME type is the corresponding one for that file extension.

The `mime-detect.py` script checks all files in a path recursively to check if the files with the given extension match the corresponding MIME type.

[Top](#mimefield-)

## Usage

### MIME determination script

For example, you want to get the information, which MIME type the file `/tmp/somefile.odt` has:

```bash
./mime-get.py -p '/tmp/somefile.odt'
```

The script should return one of the following MIME types, depending on the method used.

There are two methods available to get the MIME information.

#### Using the `file` utility

If not explicitly changed via `--use-magic` command-line argument, *MIMEfield* will read out the MIME information using the `file` utility, which is included in all *Linux* and *Unix*-like operating systems by default. In case it is missing, *MIMEfield* uses the *libmagic* file type identification library instead as fallback.

```
application/vnd.oasis.opendocument.text
```

#### Using the *libmagic* library

The `file` utility mentioned above does not exist on *Windows* operating systems, so *MIMEfield* will directly use the *libmagic* library there.

```
OpenDocument Text
```

### MIME mismatch detection script

Let's assume you want to check the path `/tmp/documents` for files that have the extension `.odt` but the wrong MIME type.

This can be done as follows:

```bash
./mime-detect.py -p '/tmp/documents' -e 'odt' -m 'OpenDocument' -v
```

You can also give multiple MIME type strings, separated with pipes (`|`):

```bash
./mime-detect.py -p '/tmp/documents' -e 'odt' -m 'OpenDocument Text|opendocument.text' -v
```

The given directory will always be processed recursively.

When using the verbose argument (`-v` or `--verbose`) as in the examples above, the script will return all files with MIME mismatches.

In any case the script will return exit code `0` if there are no mismatches and `1` otherwise.

[Top](#mimefield-)

## Requirements

### *Python* framework

In order to run the latest version of *MIMEfield*, the *Python* 3.x framework (version 3.2 or higher is recommended) must be installed on the system.

If you need a version for the *Python* 2.x framework for whatever reason, you can try refactoring the syntax from *Python* 3.x to version 2.x using the *[3to2](https://pypi.python.org/pypi/3to2)* tool.

However, there is no guarantee that this works properly or at all.

### Packages

Furthermore, you need the *libmagic* file type identification library. Details can be found [here](https://pypi.org/project/python-magic).

[Top](#mimefield-)

## Contact

Any suggestions, questions, bugs to report or feedback to give?

You can contact me by sending an email to [dev@urbanware.org](mailto:dev@urbanware.org) or by opening a *GitHub* issue (which I would prefer if you have a *GitHub* account).

[Top](#mimefield-)

## Useless facts

*   The project name *MIMEfield* is an allusion to "mine field".

[Top](#mimefield-)
