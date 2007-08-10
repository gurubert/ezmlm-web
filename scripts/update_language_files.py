#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Copyright 2007 Lars Kruse <devel@sumpfralle.de>
# 
# This file is part of ezmlm-web.
#
# All available hdf language files are parsed for creating pot (po-template) files.
# All existing po-file are merged with these templates to remove obsolete msgids.
# Additionally every msgstr of the english original is set to the value of the
# respective msgid.
# All resulting po files are chmod'ed to 0666 - this is useful if you locally use
# services like pootle.
# If there were no changes besides the "POT-Creation-Date" header, then the file
# is reverted via svn to avoid unnecessary commits.
# 
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
# along with ezmlm-web; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#


import os
import sys
try:
	import translate.storage.po, translate.convert.pot2po, translate.tools.pocompile
except ImportError, errMsg:
	sys.stderr.write("Failed to import a python module of the 'translate' package!\n")
	sys.stderr.write("Please install the appropriate files - for debian just do 'apt-get install translate-toolkit'.\n")
	sys.stderr.write("\tOriginal error message: %s\n\n" % errMsg)
	sys.exit(1)
try:
	import neo_cgi, neo_util
except ImportError, errMsg:
	sys.stderr.write("Failed to import a python module of the 'clearsilver' package!\n")
	sys.stderr.write("Please install the appropriate files - for debian just do 'apt-get install python-clearsilver'.\n")
	sys.stderr.write("\tOriginal error message: %s\n\n" % errMsg)
	sys.exit(1)
try:
	import subprocess
except ImportError, errMsg:
	sys.stderr.write("Failed to import the python module 'subprocess'!\n")
	sys.stderr.write("Please install python v2.4 or higher.\n")
	sys.stderr.write("\tOriginal error message: %s\n\n" % errMsg)
	sys.exit(1)


HDF_DIR = 'lang'
## name of the main domain and prefix for all plugin domains
GETTEXT_DOMAIN = 'ezmlm-web'
## set the msgstrs for this language to the value of the respective msgids
DEFAULT_LANG = 'en'
PO_DIR = 'intl'
## mail adress for translation bugs
MAIL_ADDRESS = 'devel@sumpfralle.de'
## the complete list of languages wastes a lot of space - for now we use only a few
#ALL_LANGUAGES = "af aka am ar bn ca cs da de el en es et eu fa fi fr fur gl he hi hr hu hy is it ja ka kg ko ku lt lv mr ms mt nb ne nl nn ns pa pl pt ru sl sr st sv tr uk ve vi xh".split(" ")
ALL_LANGUAGES = "cs da de en es fi fr hu it ja nl pl pt pt_BR ru sl sv".split(" ")

## use subversion for reverting?
USE_SVN = True

LANGUAGE_NAMES = {
    "cs": 'Český',
    "da": 'Dansk',
    "de": 'Deutsch',
    "en": 'English',
    "es": 'Español',
    "fi": 'Suomi',
    "fr": 'Français',
    "hu": 'Magyar',
    "it": 'Italiano',
    "ja": '日本語',
    "nl": 'Nederlands',
    "pl": 'Polski',
    "pt": 'Português',
    "pt_BR": 'Português do Brasil',
    "ru": 'Русский',
    "sl": 'Slovensko',
    "sv": 'Svenska',
    };

# --------------=-=-=- functions -=-=-=--------------------

def revert_if_unchanged(po_file):
	try:
		proc = subprocess.Popen(
			shell = False,
			stdout = subprocess.PIPE,
			args = [ "svn", "diff", po_file ] )
	except OSError, err_msg:
		sys.stderr.write("Failed to execute subversion's diff: %s\n" % err_msg)
		return
	(stdout, stderr) = proc.communicate()
	if proc.returncode != 0:
		sys.stderr.write("Subversion returned an error: %d\n" % proc.returncode)
		return
	## no changes at all?
	if not stdout:
		return
	lines = [ l for l in stdout.splitlines()
			if ((l.find("POT-Creation-Date:") < 0 ) and \
					((l.startswith("+") and (not l.startswith("+++"))) or \
					(l.startswith("-") and (not l.startswith("---"))))) ]
	## were there relevant changes?
	if lines:
		return
	## revert to previous state
	proc = subprocess.Popen(
		shell = False,
		args = [ "svn", "revert", po_file ] )
	proc.wait()


def generate_po_files(hdf_file, po_dir, textDomain):
	## prepare hdf
	if ((not os.path.isfile(hdf_file)) or (not os.access(hdf_file, os.R_OK))):
		sys.stderr.write("Unable to read the hdf file: %s\n" % hdf_file)
		return
	if not os.path.isdir(po_dir):
		os.mkdir(po_dir)
	pot_file = os.path.join(po_dir, "%s.pot" % textDomain)
	hdf = neo_util.HDF()
	hdf.readFile(hdf_file)
	## update pot
	if not os.path.isfile(pot_file):
		sys.stdout.write("Creating: %s\n" % pot_file)
		pot = translate.storage.po.pofile(encoding="utf-8")
		pot.makeheader(pot_creation_date=True)
		pot.updateheader(add=True, Project_Id_Version='ezmlm-web 3.2', pot_creation_date=True, language_team='Lars Kruse <%s>' % MAIL_ADDRESS, Report_Msgid_Bugs_To=MAIL_ADDRESS, encoding='utf-8', Plural_Forms=['nplurals=2','plural=(n != 1)'])
		#TODO: somehow we need 'updateheaderplural'
	else:
		sys.stdout.write("Loading: %s\n" % pot_file)
		pot = translate.storage.po.pofile.parsefile(pot_file)
	## remove all msgids - we will add them later
	pot.units = []
	## add new entries
	def walk_hdf(prefix, node):
		def addPoItem(hdf_node):
			## ignore hdf values with a "LINK" attribute
			for (key, value) in hdf_node.attrs():
				if key == "LINK":
					return
			if not hdf_node.value():
				return
			item = pot.findunit(hdf_node.value())
			if not item:
				item = pot.addsourceunit(hdf_node.value())
				item.addlocation("%s%s" % (prefix, hdf_node.name()))
		while node:
			if node.name():
				new_prefix = prefix + node.name() + '.'
			else:
				new_prefix = prefix
			## as the attribute feature of clearsilver does not work yet, we
			## have to rely on magic names to prevent the translation of links
			if not (new_prefix.endswith(".Link.Rel.") \
					or new_prefix.endswith(".Link.Prot.") \
					or new_prefix.endswith(".Link.Abs.") \
					or new_prefix.endswith(".Link.Attr1.name.") \
					or new_prefix.endswith(".Link.Attr1.value.") \
					or new_prefix.endswith(".Link.Attr2.name.") \
					or new_prefix.endswith(".Link.Attr2.value.") \
					or new_prefix == "Lang.Name."):
				addPoItem(node)
			walk_hdf(new_prefix, node.child())
			node = node.next()
	walk_hdf("",hdf)
	pot.savefile(pot_file)
	# TODO: remove the following line?
	p = translate.storage.po.pofile(pot_file)
	for ld in ALL_LANGUAGES:
		if not os.path.isdir(os.path.join(po_dir,ld)):
			os.mkdir(os.path.join(po_dir, ld))
		if not os.path.isdir(os.path.join(po_dir,ld, 'LC_MESSAGES')):
			os.mkdir(os.path.join(po_dir, ld, 'LC_MESSAGES'))
		po_file = os.path.join(po_dir, ld, 'LC_MESSAGES', "%s.po" % textDomain)
		if not os.path.isfile(po_file):
			translate.convert.pot2po.convertpot(file(pot_file), file(po_file,'w'), None)
		else:
			po2_file = po_file + '.new'
			translate.convert.pot2po.convertpot(file(pot_file), file(po2_file,'w'), file(po_file))
			os.rename(po2_file, po_file)
		if ld == DEFAULT_LANG:
			## set every msgstr to the respective msgid
			po_data = translate.storage.po.pofile.parsefile(po_file)
			po_data.removeduplicates()
			po_data.removeblanks()
			for po_unit in po_data.units:
				po_unit.settarget(po_unit.getsource())
			po_data.savefile(po_file)
		else:
			po_content = translate.storage.po.pofile.parsefile(po_file)
			po_content.removeduplicates()
			po_content.removeblanks()
			po_content.savefile(po_file)
		if USE_SVN:
			revert_if_unchanged(po_file)
		## make it writeable for pootle
		os.chmod(po_file, 0666)
		## compile po file
		mo_file = po_file[:-3] + '.mo'
		translate.tools.pocompile.convertmo(file(po_file), file(mo_file,'w'), file(pot_file))


def generate_translated_hdf_files(orig_hdf_file, po_dir, hdf_dir, textdomain):
	for lang in ALL_LANGUAGES:
		if lang != DEFAULT_LANG:
			generate_translated_hdf_file(orig_hdf_file, po_dir, hdf_dir, textdomain, lang)

def generate_translated_hdf_file(orig_hdf_file, po_dir, hdf_dir, textdomain, language):
	import gettext
	## prepare original hdf
	if ((not os.path.isfile(orig_hdf_file)) or (not os.access(orig_hdf_file, os.R_OK))):
		sys.stderr.write("Unable to read the hdf file: %s\n" % orig_hdf_file)
		return
	hdf = neo_util.HDF()
	hdf.readFile(orig_hdf_file)
	## name of new hdf file
	new_hdf_file = os.path.join(hdf_dir, language + '.hdf')
	## create translation object
	translator = gettext.translation(
			textdomain,
			localedir=po_dir,
			languages=[language])
	## translate entries
	## count the number of translated items - so we can decide later, if we
	## want to create the language file
	def walk_hdf(prefix, node):
		translate_count = 0
		def addHdfItem(hdf_node):
			## ignore hdf values with a "LINK" attribute
			for (key, value) in hdf_node.attrs():
				if key == "LINK":
					return
			if not hdf_node.value():
				return
			translated = translator.gettext(hdf_node.value())
			if translated:
				hdf.setValue("%s%s" % (prefix, hdf_node.name()), translated)
				return True
			else:
				hdf.setValue("%s%s" % (prefix, hdf_node.name()), hdf_node.value())
				return False
		while node:
			if node.name():
				new_prefix = prefix + node.name() + '.'
			else:
				new_prefix = prefix
			## as the attribute feature of clearsilver does not work yet, we
			## have to rely on magic names to prevent the translation of links
			if (new_prefix.endswith(".Link.Rel.") \
					or new_prefix.endswith(".Link.Prot.") \
					or new_prefix.endswith(".Link.Abs.") \
					or new_prefix.endswith(".Link.Attr1.name.") \
					or new_prefix.endswith(".Link.Attr1.value.") \
					or new_prefix.endswith(".Link.Attr2.name.") \
					or new_prefix.endswith(".Link.Attr2.value.")):
				pass
			elif new_prefix == "Lang.Name.":
				# set the "Lang.Name" attribute properly
				# remove trailing dot
				new_prefix = new_prefix.strip(".")
				if language in LANGUAGE_NAMES:
					hdf.setValue(new_prefix, LANGUAGE_NAMES[language])
				else:
					hdf.setValue(new_prefix, language)
			else:
				if addHdfItem(node):
					translate_count += 1
			translate_count += walk_hdf(new_prefix, node.child())
			node = node.next()
		return translate_count
	translated_items_count = walk_hdf("", hdf)
	## if there was at least one valid translation, then we should write
	## the language file
	if translated_items_count > 0:
		print "Writing translation: %s" % language
		hdf.writeFile(new_hdf_file)
	else:
		print "Skipping empty translation: %s" % language
	


# ----------------=-=-=- main -=-=-=-----------------------


if __name__ == "__main__":

	## the project directory is the parent of the directory of this script
	PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]),os.path.pardir))

	## ignore subversion, if we are not called from within a working copy
	## very useful for the release script (make-tar.sh)
	if not os.path.isdir(os.path.join(PROJECT_DIR, ".svn")):
		USE_SVN = False

	generate_po_files(
			os.path.join(PROJECT_DIR, HDF_DIR, DEFAULT_LANG + '.hdf'),
			os.path.join(PROJECT_DIR, PO_DIR),
			GETTEXT_DOMAIN)

	generate_translated_hdf_files(
			os.path.join(PROJECT_DIR, HDF_DIR, DEFAULT_LANG + '.hdf'),
			os.path.join(PROJECT_DIR, PO_DIR),
			os.path.join(PROJECT_DIR, HDF_DIR),
			GETTEXT_DOMAIN)

