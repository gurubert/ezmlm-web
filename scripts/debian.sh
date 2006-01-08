#!/bin/sh
#
#  Copyright (c) 02005 Lars Kruse <devel@sumpfralle.de>
#
#  License:  This script is distributed under the terms of 
#            the BSD license
#
# build a debian package
#

set -ue

######### some settings ###########
ROOT_DIR=$(dirname "$0")/..
ROOT_DIR=$(cd "$ROOT_DIR"; pwd)

BUILD_DIR=/tmp/ezmlm-web-build-$$

PACKAGE_DIR=$ROOT_DIR/../tags/packages
[ ! -e "$PACKAGE_DIR" ] && PACKAGE_DIR=$ROOT_DIR/../packages
[ ! -e "$PACKAGE_DIR" ] && echo "package dir not found" >&2 && exit 1

############# do it ###############

[ -e "$BUILD_DIR" ] && rm -rf "$BUILD_DIR"

ACTION=build
[ $# -gt 0 ] && ACTION=$1 && shift

case "$ACTION" in
	build )
		mkdir -p "$BUILD_DIR/usr/share/ezmlm-web"
		mkdir -p "$BUILD_DIR/usr/lib/ezmlm-web"
		mkdir -p "$BUILD_DIR/usr/bin"
		mkdir -p "$BUILD_DIR/usr/share/man/man1"
		mkdir -p "$BUILD_DIR/usr/share/doc/ezmlm-web/examples"
		mkdir -p "$BUILD_DIR/etc/ezmlm-web"
		mkdir -p "$BUILD_DIR/var/www"
		svn export "$ROOT_DIR/template" "$BUILD_DIR/usr/share/ezmlm-web/template" >/dev/null
		svn export "$ROOT_DIR/css" "$BUILD_DIR/usr/share/ezmlm-web/css" >/dev/null
		ln -s /usr/share/ezmlm-web/css/default.css "$BUILD_DIR/var/www/ezmlm-web.css"
		svn export "$ROOT_DIR/lang" "$BUILD_DIR/usr/share/ezmlm-web/lang" >/dev/null
		cp "$ROOT_DIR/ezmlm-web.cgi" "$BUILD_DIR/usr/lib/ezmlm-web/ezmlm-web.pl"
		cp "$ROOT_DIR/debian-related/index.c" "$BUILD_DIR/usr/share/ezmlm-web"
		cp "$ROOT_DIR/htaccess.sample" "$BUILD_DIR/usr/share/doc/ezmlm-web/examples"
		cp "$ROOT_DIR/webusers.sample" "$BUILD_DIR/usr/share/doc/ezmlm-web/examples"
		sed 's#/usr/local/#/usr/#g' "$ROOT_DIR/ezmlmwebrc" | tee "$BUILD_DIR/usr/share/doc/ezmlm-web/examples/ezmlmwebrc" >"$BUILD_DIR/etc/ezmlm-web/ezmlmwebrc"
		cp "$ROOT_DIR/README" "$BUILD_DIR/usr/share/doc/ezmlm-web"
		cp "$ROOT_DIR/TODO" "$BUILD_DIR/usr/share/doc/ezmlm-web"
		cp "$ROOT_DIR/UPGRADING" "$BUILD_DIR/usr/share/doc/ezmlm-web"
		cp "$ROOT_DIR/copyright" "$BUILD_DIR/usr/share/doc/ezmlm-web"
		cp "$ROOT_DIR/debian-related/README.Debian" "$BUILD_DIR/usr/share/doc/ezmlm-web"
		cp "$ROOT_DIR/debian-related/ezmlm-web-make-suid" "$BUILD_DIR/usr/bin"
		gzip --best -c "$ROOT_DIR/changelog" \
			>"$BUILD_DIR/usr/share/doc/ezmlm-web/changelog.gz"
		gzip --best -c "$ROOT_DIR/debian-related/changelog.Debian" \
			>"$BUILD_DIR/usr/share/doc/ezmlm-web/changelog.Debian.gz"
		gzip --best -c "$ROOT_DIR/debian-related/man/ezmlm-web-make-suid.1" \
			>"$BUILD_DIR/usr/share/man/man1/ezmlm-web-make-suid.1.gz"
		svn export "$ROOT_DIR/debian-related/DEBIAN" "$BUILD_DIR/DEBIAN" >/dev/null
		fakeroot dpkg-deb --build "$BUILD_DIR" "$PACKAGE_DIR"
		rm -rf "$BUILD_DIR"
		;;
	check )
		PACKAGE_FILE=$(find "$PACKAGE_DIR" -type f -name "ezmlm-web*" | grep "\.deb$" | sort -n | tail -1)
		if [ -z "$PACKAGE_FILE" ]
			then	echo "no debian package found in $PACKAGE_DIR"
			else	lintian "$PACKAGE_FILE"
		  fi
		;;
	* )
		echo "Syntax: $(basename $0) [ build | check | help ]"
		echo
		;;
  esac

