#!/bin/bash

#
# MIMEfield - MIME type mismatch detection tool
# Simple testrun script
# Copyright (c) 2026 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/mimefield
# GitLab: https://gitlab.com/urbanware-org/mimefield
#

script_dir="$(dirname "$(readlink -f "$0")")"
mimefd_dir="$script_dir/.."
logfile="$script_dir/mime-detect-testrun.log"
logfile_temp="${logfile}.tmp"
exit_code=0

check_mime() {
    message=$1
    extension=$2
    mime=$3

    echo -e "\e[0m${message} (\e[93m*.$extension\e[0m) ... \c"
    $mimefd_dir/mime-detect.py -e "$extension" -t "$mime" \
                               -p "$path" --ignore-empty \
                               >> $logfile_temp
    if [ $? -eq 0 ]; then
        echo -e "\e[92mOK\e[0m"
    else
        echo -e "\e[91mMISMATCH\e[0m"
        cat $logfile_temp >> $logfile
        echo -e "\n" >> $logfile
        exit_code=2
    fi
    rm -f $logfile_temp
}

confirm() {
    while true; do
        echo -n "Do you wish to proceed (Y/N)? "
        read choice
        if [ "$choice" = "Y" ] || [ "$choice" = "y" ]; then
            proceed=1
            break
        elif [ "$choice" = "N" ] || [ "$choice" = "n" ]; then
            proceed=0
            break
        fi
    done
}

rm -f $logfile
rm -f $logfile_temp

echo
echo "This testrun script checks files with various extensions in the home" \
     "directory"
echo "for their MIME type and writes suspected mismatches into a log file."
echo
echo "It is not unusual for false positives to occur; these can vary" \
     "depending on"
echo "the system, environment and the method used to determine the MIME type."
echo
echo "Even though, MIMEfield only reads the information regarding the file" \
     "type and"
echo "does not modify the files in any way, you are using this script at" \
     "own risk."
echo
confirm
if [ $proceed -eq 0 ]; then
    echo
    exit
fi

# Multiple paths can be specified below, each of which should be written on a
# new line for better readability
pathlist="
    $HOME
"

for path in $pathlist; do
    echo
    echo -e "\e[0mPath:  \e[93m$path\e[0m"
    echo "Path:  $path" >> $logfile
    echo

    check_mime "    - Microsoft Word"             "doc"     "application/msword|opendoc|text/|Composite Document File"
    check_mime "    - Microsoft Word"             "docx"    "officedocument|opendoc|Microsoft OOXML"
    check_mime "    - Microsoft Excel"            "xls"     "application/vnd.ms-excel|officedocument|spread|Composite Document File"
    check_mime "    - Microsoft Excel"            "xlsx"    "officedocument|spread|Microsoft OOXML"
    check_mime "    - LibreOffice Writer"         "odt"     "application/vnd.oasis.opendocument.text|opendocument|word|application/zip|Zip|html"
    check_mime "    - LibreOffice Calc"           "ods"     "application/vnd.oasis.opendocument.spreadsheet|opendocument|excel"
    check_mime "    - Portable Document Format"   "pdf"     "application/pdf|pdf"
    check_mime "    - Extensible Markup Language" "xml"     "text/xml|text/plain|text/html|XML|HTML"
    check_mime "    - 7-Zip archives"             "7z"      "application/x-7z-compressed|7-zip"
    check_mime "    - Gzip archives"              "gz"      "application/gzip|gzip|application/zip|Zip|tar"
    check_mime "    - Bzip archives"              "bz2"     "application/bzip2|bzip"
    check_mime "    - Zip archives"               "zip"     "application/zip|Zip"
    check_mime "    - Tar archives"               "tar"     "application/x-tar|tar|zip|compress"
    check_mime "    - JPEG images"                "jpg"     "image/|JPG|JPEG"
    check_mime "    - JPEG images"                "jpeg"    "image/|JPG|JPEG"
    check_mime "    - Portable Network Graphics"  "png"     "image/|PNG"
    check_mime "    - Shell scripts"              "sh"      "text/plain|Unicode text|text/x-shellscript|text/x-file|magic text fragment|Bourne-Again shell script"
    check_mime "    - Python scripts"             "py"      "text/plain|Unicode text|text/x-script.python|Python|ini|C source|very short|x-tex|latex|html|xml|csv|application/javascript|JavaScript source"
    check_mime "    - PowerShell scripts"         "ps1"     "text/plain|Unicode text|text/x-script.python|Python|html|csv"
    check_mime "    - C# source code"             "cs"      "text/x-affix|affix definition for MySpell/Hunspell|text/plain|Unicode text|text/plain|Unicode text|text/x-c++|C++ source|C source"
    check_mime "    - SQL files"                  "sql"     "text/x-affix|affix definition for MySpell/Hunspell|text/plain|Unicode text|ASCII text|sql|csv|text/html|HTML document|xml"
    check_mime "    - SQLite files"               "sqlite"  "text/x-affix|affix definition for MySpell/Hunspell|text/plain|Unicode text|ASCII text|sql|csv|text/html|HTML document|xml"
    check_mime "    - Key files"                  "key"     "application/x-pem-file|ifoo PEM DSA private key|text/plain|Unicode text|ASCII text|sql|csv|text/html|HTML document|xml|registry|text/x-ssh-private-key|OpenSSH private key|text/x-ssl-private-key|PEM RSA private key"
    check_mime "    - Image files"                "img"     "filesystem|Linux|DOS/MBR boot sector"
    check_mime "    - ISO files"                  "iso"     "application/x-iso|CD-ROM"
done
echo

if [ $exit_code -eq 2 ]; then
    echo "Mismatches found, see 'mime-detect-testrun.log' for details."
else
    echo "No mismatches found." | tee -a $logfile
fi
echo

exit $exit_code

# EOF
