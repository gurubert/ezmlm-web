#!/bin/sh

set -eu

CGI_URL="http://localhost:81/ezmlm-web"
CASE_DIR="`dirname $0`/cases.d"
OUT_DIR="`dirname $0`/output"
CURL_OPTS="-s"

PARENT_URL=`dirname "$CGI_URL"`

[ ! -e "$OUT_DIR" ] && echo "Creating output directory $OUT_DIR" && mkdir -p "$OUT_DIR"

for a in $CASE_DIR/*.conf
	do	CASENAME=`basename "$a" | sed 's/\.conf$//'`
		echo -n "Processing case '$CASENAME' ..."
		curl --config "$a" $CURL_OPTS "$CGI_URL" | sed "s#href=\"#href=\"$PARENT_URL/#g" >"${OUT_DIR}/${CASENAME}.html"
		echo
  done
