#!/bin/sh
#
# this script symlinks all ezmlm-web po files to a language directory
# structure, as it is used by the pootle translation server
#
# all language files are chgrp'ed to the 'pootle' group and group write
# permissions are added
#
# call this script whenever you add _new_ languages to your translation server
#
# it is useful to be root while calling it - otherwise chgrp will fail
#
#
# Copyright 2007 Lars Kruse <devel@sumpfralle.de>
# 
# This file is part of ezmlm-web.
#
# ezmlm-web is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# ezmlm-web is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the ezmlm-web; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#


set -eu

test $# -ne 1 && echo "Usage: $(basename $0) TARGET_DIR" && exit 1

test ! -d "$1" && echo "target directory does not exist: '$1'" && exit 1

if test "$(id -u)" == 0
  then	is_root=1
  else	is_root=0
  	echo "$(basename $0) not running as root: the language files will not be writeable for pootle" >&2
	echo " run this script as root to change the permissions of the language files appropriately" >&2
 fi

DEST_GROUP=pootle
TARGETPATH=${1%/}
BASEPATH=$(cd $(dirname "$0")/..; pwd)

############# functions ###############

# symlink a language file and chgrp if possible
# Paramters: LANG_FILE LANGUAGE
process_language_file()
{
	test ! -d "${TARGETPATH}/$2" && mkdir -p "${TARGETPATH}/$2"
	ln -sfn "$1" "${TARGETPATH}/$2/" 
	if test "$is_root" == 1
	  then	chgrp "$DEST_GROUP" "$1" "$TARGETPATH/$2"
		chmod g+w "$1" "$TARGETPATH/$2"
	 fi
}


############# main #################


for language in $(ls ${BASEPATH}/intl/) ; do
	test ! -d "${BASEPATH}/intl/${language}" && continue
	echo "Processing $language ..."
	[ ! -d ${TARGETPATH}/${language} ] && mkdir -p ${TARGETPATH}/${language}
	## base translation
	find "${BASEPATH}/intl/${language}" -name \*.po | while read fname
	  do	process_language_file "$fname" "$language"
	 done
done

echo "Processing template files ..."
find ${BASEPATH}/intl -type f -name \*.pot | while read fname
  do	process_language_file "$fname" "template"
 done

