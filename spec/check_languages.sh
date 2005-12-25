#!/bin/sh
#
# compare the defined fields of a language file with the english translation
# 
# nice for finding unavailable definitions
#
# Parameter: LANGUAGE
#	(e.g. "de")
#

set -u

LANG_DIR=$(dirname $0)/../lang
DEFAULT_LANG=en
TMP_FILE1=/tmp/$(basename $0)-$$-1
TMP_FILE2=/tmp/$(basename $0)-$$-2

[ $# -ne 1 ] && echo -e "Syntax: $(basename $0) LANGUAGE\n" >&2 && exit 1

grep "=" "$LANG_DIR/${DEFAULT_LANG}.hdf" | grep -v "^[[:space:]]*#" | cut -f 1 -d "=" >"$TMP_FILE1"
grep "=" "$LANG_DIR/${1}.hdf" | grep -v "^[[:space:]]*#" | cut -f 1 -d "=" >"$TMP_FILE2"

diff -wu "$TMP_FILE1" "$TMP_FILE2"

rm "$TMP_FILE1" "$TMP_FILE2"

