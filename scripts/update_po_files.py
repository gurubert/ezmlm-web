#!/usr/bin/env python
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


LANGUAGE_FILE = 'language.hdf'
## name of the main domain and prefix for all plugin domains
GETTEXT_DOMAIN = 'ezmlm-web'
## set the msgstrs for this language to the value of the respective msgids
DEFAULT_LANG = 'en'
LANG_DIR = 'intl'
## mail adress for translation bugs
MAIL_ADDRESS = 'devel@sumpfralle.de'
## the complete list of languages wastes a lot of space - for now we use only a few
#ALL_LANGUAGES = "af aka am ar bn ca cs da de el en es et eu fa fi fr fur gl he hi hr hu hy is it ja ka kg ko ku lt lv mr ms mt nb ne nl nn ns pa pl pt ru sl sr st sv tr uk ve vi xh".split(" ")
ALL_LANGUAGES = "cs da de en es fi fr hu it ja nl pl pt ru sl sv".split(" ")

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


def process_language_file(hdf_file, po_dir, textDomain):
	## prepare hdf
	if not os.path.isfile(hdf_file) or not os.access(hdf_file, os.R_OK):
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
			for (key,value) in hdf_node.attrs():
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
					or new_prefix.endswith(".Link.Attr2.value.")):
				addPoItem(node)
			walk_hdf(new_prefix, node.child())
			node = node.next()
	walk_hdf("",hdf)
	pot.savefile(pot_file)
	p = translate.storage.po.pofile(pot_file)
	for ld in ALL_LANGUAGES:
		if not os.path.isdir(os.path.join(po_dir,ld)):
			os.mkdir(os.path.join(po_dir, ld))
		po_file = os.path.join(po_dir, ld, "%s.po" % textDomain)
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
		revert_if_unchanged(po_file)
		## make it writeable for pootle
		os.chmod(po_file, 0666)
		## compile po file
		mo_file = po_file[:-3] + '.mo'
		translate.tools.pocompile.convertmo(file(po_file), file(mo_file,'w'), file(pot_file))




# ----------------=-=-=- main -=-=-=-----------------------


if __name__ == "__main__":

	## the project directory is the parent of the directory of this script
	PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]),os.path.pardir))

	process_language_file(
			os.path.join(PROJECT_DIR, 'templates', LANGUAGE_FILE),
			os.path.join(PROJECT_DIR, LANG_DIR),
			GETTEXT_DOMAIN)

