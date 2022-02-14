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

For example, when saving an *OpenDocument* file (`.odt`) with the extension `.zip` (weird and unlike example, but explains it pretty good), double-clicking the file would open the archive tool instead of the corresponding text editor (e.g. *OpenOffice* or *LibreOffice*).

The *MIMEfield* project determines the file type regardless of the file extension and checks files if the MIME type matches the extension.

It consists of two components:

*   With the `mime-get.py` script you can simply get the MIME type of a file
*   The `mime-detect.py` script checks all files with a given extension in a path recursively to check if the extension matches with the corresponding MIME type


[Top](#mimefield-)

## Usage

There are two methods available to get the MIME information:

*   The `file` utility (on *Unix*-like systems, only)
*   The *libmagic* module for *Python* (platform independent)

In case the both the `file` utility and *libmagic* are installed on the system both methods will be used. The preferred method can be also be given using the `--method` (or the short `-m`) argument.

As already mentioned above, the `file` utility is only available on *Unix*-like systems (such as *Linux* and *BSD*) so on *Windows* operating systems *libmagic* is the only supported method to read out the MIME information from a file.

### MIME determination script

The `mime-get.py` script simply determines and returns the MIME type of a file.

For example, you want to get the information which MIME type the included file `mimefield.png` has you can use the script as follows.

#### Using both methods

If no method was given explicitly, the script will use both methods.

```
./mime-get.py -p mimefield.png
```

The script would actually return `image/png|PNG image data|PNG image data`. Due to the fact, that `file` already returned what *libmagic* also does, the duplicate value is omitted. Due to this, only `image/png|PNG image data` is returned.

#### Using the `file` utility

If the method `file` is explicitly given

```
./mime-get.py -p mimefield.png -m file
```

the script will return `image/png|PNG image data`.

#### Using the *libmagic* library

If the method `magic` is explicitly given

```
./mime-get.py -p mimefield.png -m magic
```

the script will return `PNG image data`.

### MIME mismatch detection script

Let's assume you want to check the path `/tmp/documents` for files that have the extension `.odt` but the wrong MIME type.

The `mime-get.py` usually returns `application/vnd.oasis.opendocument.text|OpenDocument Text` when using both methods.

In this case, you can just give `opendocument` as type as MIME type string (case-insensitive), as both methods return that information.

```bash
./mime-detect.py -p '/tmp/documents' -e 'odt' -t 'opendocument'
```

You can also give multiple MIME type strings, separated with pipes (`|`), so it does not matter which method to read out the MIME information is used:

```bash
./mime-detect.py -p '/tmp/documents' -e 'odt' -t 'application/vnd.oasis|opendocument.text'
```

Furthermore, it is also possible to explicitly give the method used to detect the MIME type mismatches with:

```bash
./mime-detect.py -p '/tmp/documents' -e 'odt' -t 'application/vnd.oasis|opendocument.text' -m magic
```

The given directory will always be processed recursively and the script will return all files with mismatches if there are any.

In case there are no mismatches the script will return exit code `0` and `1` otherwise.

[Top](#mimefield-)

## Requirements

### *Python* framework

In order to run the latest version of *MIMEfield*, the *Python* 3.x framework (version 3.2 or higher is recommended) must be installed on the system.

If you need a version for the *Python* 2.x framework for whatever reason, you can try refactoring the syntax from *Python* 3.x to version 2.x using the *[3to2](https://pypi.python.org/pypi/3to2)* tool.

However, there is no guarantee that this works properly or at all.

### Packages

If you are running *Windows*, the *libmagic* file type identification library is mandatory. Details can be found [here](https://pypi.org/project/python-magic).

On *Unix*-like operating systems (such as *Linux* and *BSD*) the library is not required, but can be used as fallback.

[Top](#mimefield-)

## Contact

Any suggestions, questions, bugs to report or feedback to give?

You can contact me by sending an email to [dev@urbanware.org](mailto:dev@urbanware.org) or by opening a *GitHub* issue (which I would prefer if you have a *GitHub* account).

[Top](#mimefield-)

## Useless facts

*   The project name *MIMEfield* is an allusion to "mine field".

[Top](#mimefield-)