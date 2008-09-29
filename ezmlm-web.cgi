#!/usr/bin/perl 
#===========================================================================
# ezmlm-web.cgi - version 3.3
# $Id$
# 
# This file is part of ezmlm-web.
#
# All user configuration happens in the config file ``ezmlmwebrc''
# POD documentation is at the end of this file
#
# Copyright (C) 1999-2000, Guy Antony Halse, All Rights Reserved.
# Copyright (C) 2005-2008, Lars Kruse, All Rights Reserved.
#
# ezmlm-web is distributed under a BSD-style license.  Please refer to
# the copyright file included with the release for details.
# ==========================================================================

package ezmlm_web;

# Modules to include
use strict;
use Getopt::Std;
use ClearSilver;
use Mail::Ezmlm;
use File::Copy;
use File::Path;
use DB_File;
use CGI;
use IO::File;
use POSIX;
use English;
use MIME::QuotedPrint;

# optional modules - they will be loaded later if they are available
#Encode
#Mail::Ezmlm::GpgEzmlm
#Mail::Ezmlm::GpgKeyRing
#Mail::Address OR Email::Address


my $mail_address_package;
# we can use either the Mail::Address or the Email::Address module
# "Mail::Address" was used exclusively until ezmlm-web v3.2, thus it is proven
# to work with ezmlm-web
# the downside of Mail::Address is, that it is not available in the debian
# distribution
if (&safely_import_module("Mail::Address")) {
	$mail_address_package = "Mail::Address";
} elsif (&safely_import_module("Email::Address")) {
	$mail_address_package = "Email::Address";
} else {
	die "Failed to import the Mail::Address and the Email::Address module.\n" .
		"At least one of these modules is required for ezmlm-web.\n";
}

# the Encode module is optional - we do not break if it is absent
my $ENCODE_SUPPORT = 1;
unless (&safely_import_module("Encode")) {
	$ENCODE_SUPPORT = 0;
	warn "Encoding module is not available - charset conversion will fail!";
}



################## some preparations at the beginning ##################

# drop privileges (necessary for calling gpg)
# this should not do any other harm
$UID = $EUID;
$GID = $EGID;

my $VERSION;
$VERSION = '3.3';

my $q = new CGI;
$q->import_names('Q');
use vars qw[$opt_c $opt_d $opt_C];
getopts('cd:C:');

# Suid stuff requires a secure path.
# The following three lines are taken from "man perlrun"
$ENV{PATH} = '/bin';
$ENV{SHELL} = '/bin/sh' if exists $ENV{SHELL};
delete @ENV{qw(IFS CDPATH ENV BASH_ENV)};

# We run suid so we can't use $ENV{'HOME'} and $ENV{'USER'} to determine the
# user. :( Don't alter this line unless you are _sure_ you have to.
my @tmp = getpwuid($>); use vars qw[$USER]; $USER=$tmp[0];

# defined by our environment - see above
use vars qw[$HOME_DIR]; $HOME_DIR=$tmp[7];

# use strict is a good thing++

# some configuration settings
use vars qw[$DEFAULT_OPTIONS $UNSAFE_RM $ALIAS_USER $LIST_DIR];
use vars qw[$QMAIL_BASE $PRETTY_NAMES $DOTQMAIL_DIR];
use vars qw[$FILE_UPLOAD $WEBUSERS_FILE $MAIL_DOMAIN $HTML_TITLE];
use vars qw[$TEMPLATE_DIR $LANGUAGE_DIR $HTML_LANGUAGE];
use vars qw[$HTML_CSS_COMMON $HTML_CSS_COLOR];
use vars qw[$MAIL_ADDRESS_PREFIX @HTML_LINKS];
use vars qw[@INTERFACE_OPTIONS_BLACKLIST];
# default interface template (basic/normal/expert)
use vars qw[$DEFAULT_INTERFACE_TYPE];
# some settings for encrypted mailing lists
use vars qw[$ENCRYPTION_SUPPORT $GPG_KEYRING_DEFAULT_LOCATION];
# settings for multi-domain setups
use vars qw[%DOMAINS $CURRENT_DOMAIN];
# cached data
use vars qw[%CACHED_DATA];
# available features
use vars qw[%FEATURES];

# some deprecated configuration settings - they have to be registered
# otherwise old configuration files would break
use vars qw[$HTML_CSS_FILE];	# replaced by HTML_CSS_COMMON since v3.2


# "pagedata" contains the hdf tree for clearsilver
# "pagename" refers to the template file that should be used
# "ui_template" is one of "basic", "normal" and "expert"
use vars qw[$pagedata $pagename];
use vars qw[$error $customError $warning $customWarning $success];
use vars qw[$ui_template $LOGIN_NAME];

# Get user configuration stuff
my $config_file;
if (defined($opt_C)) {
   $opt_C =~ /^([-\w.\/]+)$/;	# security check by ooyama
   $config_file = $1; # Command Line
} elsif (-e "$HOME_DIR/.ezmlmwebrc") {
   $config_file = "$HOME_DIR/.ezmlmwebrc"; # User
} elsif (-e "/etc/ezmlm-web/ezmlmwebrc") {
   $config_file = "/etc/ezmlm-web/ezmlmwebrc"; # System (new style - since v2.2)
} elsif (-e "/etc/ezmlm/ezmlmwebrc") {
   $config_file = "/etc/ezmlm/ezmlmwebrc"; # System (old style - up to v2.1)
} else {
   &fatal_error("Unable to find config file");
}
unless (my $return = do $config_file) {
	if ($@) {
		&fatal_error("Failed to parse the config file ($config_file): $@");
	} elsif (!defined $return) {
		&fatal_error("Failed to read the config file ($config_file): $!");
	} else {
		# the last statement of the config file return False -> this is ok
	}
}


####### validate configuration and apply some default settings ##########

# do we support encrypted mailing lists an keyring management?
$ENCRYPTION_SUPPORT = 0 unless defined($ENCRYPTION_SUPPORT);
if ($ENCRYPTION_SUPPORT) {
	$FEATURES{GPGEZMLM} = (0==0)
		if (&safely_import_module("Mail::Ezmlm::GpgEzmlm"));
	$FEATURES{GPGKEYRING} = (0==0)
		if (&safely_import_module("Mail::Ezmlm::GpgKeyRing"));
	# did we load any modules?
	if (scalar keys %FEATURES == 0) {
		warn "WARNING: all of the supported encryption modules "
				. "(Mail::Ezmlm::GpgEzmlm and Mail::Ezmlm::GpgKeyRing) failed "
				. "to load. Encryption support is disabled.";
		$ENCRYPTION_SUPPORT = 0;
	}
}

# Allow suid wrapper to override default list directory ...
if (defined($opt_d)) {
   $LIST_DIR = $1 if ($opt_d =~ /^([-\@\w.\/]+)$/);
}

# check required configuration settings
&fatal_error("Configuration setting 'LIST_DIR' not specified!")
	unless (defined($LIST_DIR));
&fatal_error("Configuration setting 'LANGUAGE_DIR' not specified!")
	unless (defined($LANGUAGE_DIR));
&fatal_error("Configuration setting 'TEMPLATE_DIR' not specified!")
	unless (defined($TEMPLATE_DIR));

# If WEBUSERS_FILE is not defined in ezmlmwebrc (as before version 2.2),
# then use former default value for compatibility
$WEBUSERS_FILE = $LIST_DIR . '/webusers' unless (defined($WEBUSERS_FILE));

# check for non-default dotqmail directory
$DOTQMAIL_DIR = $HOME_DIR unless defined($DOTQMAIL_DIR);

# check default options for new mailing lists
$DEFAULT_OPTIONS = 'aBDFGHiJkLMNOpQRSTUWx' unless defined($DEFAULT_OPTIONS);

# check default language
$HTML_LANGUAGE = 'en' unless defined($HTML_LANGUAGE);

# check stylesheet
# HTML_CSS_FILE was replaced by HTML_CSS_COMMON in v3.2
unless (defined($HTML_CSS_COMMON)) {
	# HTML_CSS_COMMON is undefined - we will check the deprecated setting first
	if (defined($HTML_CSS_FILE)) {
		# ok - we fall back to the deprecated setting
		$HTML_CSS_COMMON = $HTML_CSS_FILE;
	} else {
		# nothing is defined - we use the default value
		$HTML_CSS_COMMON = '/ezmlm-web/default.css';
	}
}

# CSS color scheme
$HTML_CSS_COLOR = '/ezmlm-web/color-red-blue.css'
	unless defined($HTML_CSS_COLOR);

# check template directory
$TEMPLATE_DIR = 'template' unless defined($TEMPLATE_DIR);

# check QMAIL_BASE
$QMAIL_BASE = '/var/qmail/control' unless defined($QMAIL_BASE);

# check UNSAFE_RM
$UNSAFE_RM = 0 unless defined($UNSAFE_RM);

# check PRETTY_NAMES
$PRETTY_NAMES = 0 unless defined($PRETTY_NAMES);

# check FILE_UPLOAD
$FILE_UPLOAD = 1 unless defined($FILE_UPLOAD);

# check ALIAS_USER
$ALIAS_USER = 'alias' unless defined($ALIAS_USER);

# check HTML_TITLE
$HTML_TITLE = '' unless defined($HTML_TITLE);

# check HTML_LINKS
@HTML_LINKS = () unless defined(@HTML_LINKS);

# check DEFAULT_INTERFACE_TYPE
$DEFAULT_INTERFACE_TYPE = 'normal' unless defined($DEFAULT_INTERFACE_TYPE);

# check possible blacklist of interface options (since v3.3)
@INTERFACE_OPTIONS_BLACKLIST = () unless defined(@INTERFACE_OPTIONS_BLACKLIST);

# check the configured detault location of gnupg keyrings
$GPG_KEYRING_DEFAULT_LOCATION = ".gnupg"
	unless defined($GPG_KEYRING_DEFAULT_LOCATION);

# determine MAIL_DOMAIN
unless (defined($MAIL_DOMAIN) && ($MAIL_DOMAIN ne '')) {
	if ((-e "$QMAIL_BASE/virtualdomains")
			&& open(VD, "<$QMAIL_BASE/virtualdomains")) {
		# Work out if this user has a virtual host and set input accordingly ...
		while(<VD>) {
			last if (($MAIL_DOMAIN) = /(.+?):$USER/);
		}
		close VD;
	}
	# use 'defaultdomain' or 'me' if no matching virtualdomain was found
	if (defined($MAIL_DOMAIN) && ($MAIL_DOMAIN ne '')) {
		# the prefix is empty for virtual domains
		$MAIL_ADDRESS_PREFIX = "" unless (defined($MAIL_ADDRESS_PREFIX));
	} else {
		# Work out default domain name from qmail (for David Summers)
		if (open(GETHOST, "<$QMAIL_BASE/defaultdomain")
				|| open(GETHOST, "<$QMAIL_BASE/me")) {
			chomp($MAIL_DOMAIN = <GETHOST>);
			close GETHOST;
		} else {
			&fatal_error("Unable to read $QMAIL_BASE/me: $!");
		}
	}
}

# check MAIL_ADDRESS_PREFIX
unless (defined($MAIL_ADDRESS_PREFIX)) {
	if ($USER eq $ALIAS_USER) {
		$MAIL_ADDRESS_PREFIX = "";
	} else {
		$MAIL_ADDRESS_PREFIX = "$USER-"
	}
}

# get the current login name advertised to the webserver (if it is defined)
$LOGIN_NAME = lc($ENV{'REMOTE_USER'});


###################### process a request ########################

# Untaint form input ...
&untaint;

my $pagedata = &init_hdf();
my $list;
my $action;

$action = defined($q->param('action'))
	? $q->param('action')
	: '';

# get the list object
if (defined($q->param('list'))) {
	$list = get_list_object($q->param('list'));
} else {
	$list = undef;
}

# This is where we decide what to do, depending on the form state and the
# user's chosen course of action ...
# TODO: unify all these "is list param set?" checks ...
if (defined($action) && ($action eq 'show_mime_examples')) {
	&output_mime_examples();
	exit 0;
} elsif (%DOMAINS && (!defined($CURRENT_DOMAIN) || ($CURRENT_DOMAIN eq '')
		|| ($action eq 'domain_select'))) {
	# domain support is enabled, but no domain is selected
	$pagename = 'domain_select';
	# undef the currently selected domain
	undef $CURRENT_DOMAIN;
} elsif (!&check_permission_for_action()) {
	$pagename = 'list_select';
	$error = 'Forbidden';
} elsif ($action eq '' || $action eq 'list_select') {
	# Default action. Present a list of available lists to the user ...
	$pagename = 'list_select';
} elsif ($action eq 'show_page') {
	$pagename = $q->param('pagename');
	unless (-e "$TEMPLATE_DIR/$pagename.cs") {
		$pagename = 'list_select';
		$error = 'UnknownAction';
	}
} elsif ($action eq 'subscribers') {
	# display list (or part list) subscribers
	if ($list) {
		$pagename = 'subscribers';
	} else {
		$pagename = 'list_select';
		$error = 'ParameterMissing';
	}
} elsif ($action eq 'address_del') {
	# Delete a subscriber ...
	if ($list) {
		$success = 'DeleteAddress' if (&delete_address($list));
		$pagename = 'subscribers';
	} else {
		$error = 'ParameterMissing';
		$pagename = 'list_select';
	}
} elsif ($action eq 'address_add') {
	# Add a subscriber ...
	# no selected addresses -> no error
	if ($list) {
		$success = 'AddAddress' if (&add_address($list));
		$pagename = 'subscribers';
	} else {
		$error = 'ParameterMissing';
		$pagename = 'list_select';
	}
} elsif ($action eq 'download_subscribers') {
	# requesting a text file of all subscribers
	if ($list) {
		&download_subscribers($list);
		# just in case we return (something bad happened)
		$pagename = 'subscribers';
	} else {
		$pagename = 'list_select';
		$error = 'ParameterMissing';
	}
} elsif ($action eq 'subscribe_log') {
	if ($list) {
		&set_pagedata_subscription_log($list);
		$pagename = 'show_subscription_log';
	} else {
		$pagename = 'list_select';
		$error = 'ParameterMissing';
	}
} elsif ($action eq 'list_delete_ask') {
	# Confirm list removal
	if ($list) {
		$pagename = 'list_delete';
	} else {
		$pagename = 'list_select';
		$error = 'ParameterMissing';
	}
} elsif ($action eq 'list_delete_do') {
	# User really wants to delete a list ...
	if ($list) {
		$success = 'DeleteList' if (&delete_list($list));
		$list = undef;
	} else {
		$error = 'ParameterMissing';
	}
	$pagename = 'list_select';
} elsif ($action eq 'list_create_ask') {
	# User wants to create a list ...
	$pagename = 'list_create';
} elsif ($action eq 'list_create_do') {
	# create the new list
	# Message if list creation is unsuccessful ...
	if (defined($q->param('new_list'))) {
		if ($list = &create_list($q->param('new_list'))) {
			$success = 'CreateList';
			$pagename = 'subscribers';
		} else {
			$pagename = 'list_create';
		}
	} else {
		$error = 'ParameterMissing';
	}
} elsif (($action eq 'config_ask') || ($action eq 'config_do')) {
	# User wants to see/change the configuration ...
	my $subset = $q->param('config_subset');
	if ($list && ($subset ne '')) {
		if ($subset =~ m/^RESERVED-([\w_-]*)$/) {
			$pagename = $1
		} elsif (($subset =~ /^[\w]*$/)
				&& (-e "$TEMPLATE_DIR/config_$subset" . ".cs")) {
			$pagename = 'config_' . $subset;
		} else {
			$pagename = '';
		}
		if ($pagename ne '') {
			$success = 'UpdateConfig'
					if (($action eq 'config_do') && &update_config($list));
		} else {
			$error = 'UnknownConfigPage';
			warn "missing config page: $subset";
			$pagename = 'list_select';
		}
	} else {
		$error = 'ParameterMissing';
		$pagename = 'list_select';
	}
} elsif ($FEATURES{GPGEZMLM} && ($action eq 'gpgezmlm_convert_ask')) {
	$pagename = 'gpgezmlm_convert';
} elsif ($FEATURES{GPGEZMLM} && ($action eq 'gpgezmlm_convert_enable')) {
	if (ref($list) && $list->isa("Mail::Ezmlm::GpgEzmlm")) {
		$pagename = 'gpgezmlm_convert';
		$warning = 'GpgEzmlmConvertAlreadyEnabled';
	} else {
		my $enc_list = Mail::Ezmlm::GpgEzmlm->convert_to_encrypted($list->thislist());
		if ($enc_list) {
			$list = $enc_list;
			# if the keyring already contains a secret key, then we do not
			# need to generate a new one
			my $keyring = get_keyring($list);
			my @secret_keys = $keyring->get_secret_keys();
			if ($#secret_keys >= 0) {
				$pagename = 'gnupg_secret';
			} else {
				$pagename = 'gnupg_generate_key';
			}
			$success = 'GpgEzmlmConvertEnable';
		} else {
			$pagename = 'gpgezmlm_convert';
			$warning = 'GpgEzmlmConvertEnable';
		}
	}
} elsif ($FEATURES{GPGEZMLM} && ($action eq 'gpgezmlm_convert_disable')) {
	if ($list && $list->isa("Mail::Ezmlm::GpgEzmlm")) {
		if ($list->convert_to_plaintext()) {
			$list = $_;
			$pagename = 'gpgezmlm_convert';
			$success = 'GpgEzmlmConvertDisable';
		} else {
			$pagename = 'gpgezmlm_convert';
			$warning = 'GpgEzmlmConvertDisable';
		}
	} else {
		$pagename = 'gpgezmlm_convert';
		$warning = 'GpgEzmlmConvertAlreadyDisabled';
	}
} elsif ($FEATURES{GPGKEYRING} && (($action eq 'gnupg_ask') ||
		($action eq 'gnupg_do'))) {
	# User wants to manage keys (only for encrypted mailing lists)
	my $subset = $q->param('gnupg_subset');
	if ($list && is_list_encrypted($list) && ($subset ne '')) {
		if (($subset =~ /^[\w]*$/)
				&& (-e "$TEMPLATE_DIR/gnupg_$subset" . ".cs")) {
			if ($action eq 'gnupg_do') {
				$success = 'UpdateGnupg' if (&manage_gnupg_keys($list));
			} else {
				# warnings are defined in the respective subs
				$pagename = 'gnupg_' . $subset;
			}
		} else {
			$error = 'UnknownGnupgPage';
			warn "missing gnupg page: $subset";
			$pagename = 'list_select';
		}
	} else {
		$error = 'ParameterMissing';
		$pagename = 'list_select';
	}
} elsif ($FEATURES{GPGKEYRING} && ($action eq 'gnupg_export')) {
	if ($list && is_list_encrypted($list)
			&& defined($q->param('gnupg_keyid'))) {
		if (&gnupg_export_key($list, $q->param('gnupg_keyid'))) {
			# the key was printed to stdout - we can exit now
			# TODO: this should be something like "skip_output" instead
			exit 0;
		} else {
			$warning = 'GnupgExportKey';
			# pagename is quite random here ...
			$pagename = 'gnupg_public';
		}
	} else {
		$error = 'ParameterMissing';
		$pagename = 'list_select';
	}
} elsif ($action eq 'textfiles') {
	# Edit DIR/text ...
	if ($list) {
		$pagename = 'textfiles';
	} else {
		$error = 'ParameterMissing';
		$pagename = 'list_select';
	}
} elsif ($action eq 'textfile_edit') {
	# edit the content of a text file
	if ($list && defined($q->param('file'))) {
		if (!&check_filename($q->param('file'))) {
			$error = 'InvalidFileName';
			$pagename = 'textfiles';
		} else {
			$pagename = 'textfile_edit';
		}
	} else {
		$error = 'ParameterMissing';
		$pagename = 'list_select';
	}
} elsif ($action eq 'textfile_save') {   
	# User wants to save a new version of something in DIR/text ...
	if ($list && defined($q->param('file')) && defined($q->param('content'))) {
		if (!&check_filename($q->param('file'))) {
			$error = 'InvalidFileName';
			$pagename = 'textfiles';
		} elsif (&save_text($list)) {
			$pagename = 'textfiles';
			$success = 'SaveFile';
		} else {
			$warning = 'SaveFile';
			$pagename = 'textfile_edit';
		}
	} else {
		$error = 'ParameterMissing';
		if ($list) {
			$pagename = 'textfiles';
		} else {
			$pagename = 'list_select';
		}
	}
} elsif ($action eq 'textfile_reset') {   
	# User wants to remove a customized text file (idx >= 5) ...
	if ($list && defined($q->param('file'))) {
		if (!&check_filename($q->param('file'))) {
			$error = 'InvalidFileName';
			$pagename = 'textfiles';
		} elsif (Mail::Ezmlm->get_version() < 5) {
			$warning = 'RequiresIDX5';
			$pagename = 'textfile_edit';
		} elsif ($list->is_text_default($q->param('file'))) {
			$warning = 'ResetFileIsDefault';
			$pagename = 'textfile_edit';
		} elsif ($list->reset_text($q->param('file'))) {
			$success = 'ResetFile';
			$pagename = 'textfiles';
		} else {
			$warning = 'ResetFile';
			$pagename = 'textfile_edit';
		}
	} else {
		$error = 'ParameterMissing';
		if ($list) {
			$pagename = 'textfiles';
		} else {
			$pagename = 'list_select';
		}
	}
} else {
	$pagename = 'list_select';
	$error = 'UnknownAction';
}

# read the current state (after the changes are done)
&set_pagedata($list);

# set default action, if there is no list available and the user is
# allowed to create a new one
if (((!defined($action)) || ($action eq ''))
		&& ((%DOMAINS && defined($CURRENT_DOMAIN) and
				($CURRENT_DOMAIN ne '')) || (!%DOMAINS))
		&& (&webauth_create_allowed())
		&& ($pagedata->getValue('Data.Lists.0','') eq '')) {
	$pagename = 'list_create';
}

# Print page and exit :) ...
&output_page;
exit;


# =========================================================================

sub init_hdf {
	# initialize the data for clearsilver

	my $hdf = ClearSilver::HDF->new();
 
	&fatal_error("Language data dir ($LANGUAGE_DIR) not found!")
		unless (-e $LANGUAGE_DIR);
	$hdf->setValue("LanguageDir", "$LANGUAGE_DIR/");

	&fatal_error("Template dir ($TEMPLATE_DIR) not found!")
		unless (-e $TEMPLATE_DIR);
	$hdf->setValue("TemplateDir", "$TEMPLATE_DIR/");

	# easy/normal/expert
	my $one_template;
	my @all_templates = &get_available_interfaces();
	if (defined($q->param('template'))) {
		foreach $one_template (@all_templates) {
			$ui_template = $q->param('template')
				if ($q->param('template') eq $one_template);
		}
	}
	$ui_template = $DEFAULT_INTERFACE_TYPE unless defined($ui_template);
	$hdf->setValue("Config.UI.LinkAttrs.template", $ui_template);


	# retrieve available interface sets and add them to the dataset
	my %interfaces = &get_available_interfaces();
	my $interface;
	foreach $interface (keys %interfaces) {
		$hdf->setValue("Config.UI.Interfaces.$interface",
				$interfaces{$interface});
	}

	# retrieve available languages and add them to the dataset
	my %languages = &get_available_interface_languages();
	my $lang;
	foreach $lang (sort keys %languages) {
		$hdf->setValue("Config.UI.Languages.$lang", $languages{$lang});
	}

	$hdf = &load_interface_language($hdf);

	$hdf->setValue("ScriptName", $ENV{SCRIPT_NAME})
			if (defined($ENV{SCRIPT_NAME}));
	$hdf->setValue("Stylesheet.0", "$HTML_CSS_COMMON");
	$hdf->setValue("Stylesheet.1", "$HTML_CSS_COLOR");
	$hdf->setValue("Config.PageTitle", "$HTML_TITLE");

	my $i;
	for $i (0 .. $#HTML_LINKS) {
		$hdf->setValue("Config.PageLinks.$i.name", $HTML_LINKS[$i]{name});
		$hdf->setValue("Config.PageLinks.$i.url", $HTML_LINKS[$i]{url});
		$i++;
	}

	# support for encryption?
	$hdf->setValue("Config.Features.GpgEzmlm", 1) if ($FEATURES{GPGEZMLM});
	$hdf->setValue("Config.Features.GpgKeyRing", 1) if ($FEATURES{GPGKEYRING});

	# enable some features that are only available for specific versions
	# of ezmlm-idx
	if (Mail::Ezmlm->get_version() >= 5.1) {
		$hdf->setValue("Config.Features.KeepFiles", 1);
	}
	if (Mail::Ezmlm->get_version() >= 5) {
		$hdf->setValue("Config.Features.LanguageSelect", 1);
		$hdf->setValue("Config.Features.CharsetSelect", 1);
		$hdf->setValue("Config.Features.CopyLines", 1);
	}

	$hdf->setValue("Config.Version.ezmlm_web", "$VERSION");

	return $hdf;
}

# =========================================================================

sub output_page {
	# Print the page

	my $ui_template_file = "$TEMPLATE_DIR/ui/${ui_template}.hdf";
	&fatal_error("UI template file ($ui_template_file) not found")
		unless (-e $ui_template_file);
	$pagedata->readFile($ui_template_file);

	$pagedata->setValue('Data.Success', "$success") if (defined($success));
	$pagedata->setValue('Data.Error', "$error") if (defined($error));
	$pagedata->setValue('Data.Warning', "$warning") if (defined($warning));
	$pagedata->setValue('Data.customError', "$customError")
			if (defined($customError));
	$pagedata->setValue('Data.customWarning', "$customWarning")
			if (defined($customWarning));

	$pagedata->setValue('Data.Action', "$pagename");

	my $pagefile = $TEMPLATE_DIR . "/main.cs";
	&fatal_error("main template ($pagefile) not found!")
			unless (-e "$pagefile");
	&fatal_error("sub template ($TEMPLATE_DIR/$pagename.cs) not found!")
			unless (-e "$TEMPLATE_DIR/$pagename.cs");

	# print http header
	print "Content-Type: text/html; charset=utf-8\n\n";

	my $cs = ClearSilver::CS->new($pagedata);

	$cs->parseFile($pagefile);

	my $output;
	if ($output = $cs->render()) {
		print $output;
	} else {
		&fatal_error($cs->displayError());
	}
}

# ---------------------------------------------------------------------------

# create the list object - also check for encryption and other modules
sub get_list_object {
	my $listname = shift;
	my ($list, @module_order, $one_module);

	@module_order = ();

	# gpg-ezmlm
	push(@module_order, "Mail::Ezmlm::GpgEzmlm")
		if ($FEATURES{GPGEZMLM});

	# default
	push(@module_order, "Mail::Ezmlm");

	for $one_module (@module_order) {
		$list = $one_module->new("$LIST_DIR/$listname");
		# invalid lists are undef
		return $list if defined($list);
	}

	return undef;
}

# ---------------------------------------------------------------------------

sub load_interface_language {

	my ($data) = @_;
	my $config_language;

	# load default language (configured or 'en') first
	# this will serve as a fallback
	#
	# we do not have to load 'en' separately as a fallback, because partly
	# translated language files always include the English default for all
	# missing strings
	if (&check_interface_language($HTML_LANGUAGE)) {
		$config_language = "$HTML_LANGUAGE";
	} else {
		$config_language = 'en';
	}
	$data->readFile("$LANGUAGE_DIR/$config_language" . ".hdf");

	# check for preferred browser language
	my $prefLang = &get_browser_language();
	# take it, if a supported browser language was found
	$config_language = $prefLang unless ($prefLang eq '');

	######### temporary language setting? ############
	# the default language can be overriden by the language selection form
	if ($q->param('web_lang')) {
		my $weblang = $q->param('web_lang');
		if (&check_interface_language($weblang)) {
			# load the data
			$config_language = "$weblang";
		} else {
			# no valid language was selected - so you may ignore it
			$warning = 'InvalidLanguage';
		}
	}

	# add the setting to every link
	$data->setValue('Config.UI.LinkAttrs.web_lang', "$config_language");

	# import the configured resp. the temporarily selected language
	$data->readFile("$LANGUAGE_DIR/$config_language" . ".hdf");

	return $data;
}

# ---------------------------------------------------------------------------

sub get_browser_language {
	# look for preferred browser language setting
	# this code was adapted from Per Cederberg
	# http://www.percederberg.net/home/perl/select.perl
	# it returns an empty string, if no supported language was found

    my ($lang_main, $lang_sub, $lang_name, $one_lang, @langs, @res);
	my (@main_langs);

    # Use language preference settings
	if (defined($ENV{HTTP_ACCEPT_LANGUAGE})
			&& ($ENV{HTTP_ACCEPT_LANGUAGE} ne '')) {
		@langs = split(/,/, $ENV{HTTP_ACCEPT_LANGUAGE});
	} else {
		return "";
	}

	foreach $one_lang (@langs) {
		# get the first part of the language setting
		$one_lang =~ m/^([a-z]+)(_[A-Z]+)?/;
		$lang_main = defined($1) ? $1 : "";
		$lang_sub = defined($2) ? $2 : "";
		$lang_name = $lang_main . $lang_sub;
		# check, if it is available
		if (&check_interface_language($lang_name)) {
			$res[$#res+1] = $lang_name;
		} else {
			# remember the main languages of all non-supported regional
			# languages (only if the main language ist supported)
			$main_langs[$#main_langs+1] = $lang_main
				if (&check_interface_language($lang_main));
		}
	}

	# add the previously remembered main languages to the list of
	# preferred languages
	# useful, if someone configured 'de_AT' without the general 'de'
	$res[$#res+1] = $_ foreach (@main_langs);
	
    # if everything fails - return empty string
	$res[0] = "" if ($#res lt 0);
	return $res[0];
}

# ---------------------------------------------------------------------------

sub set_pagedata_domains {

	my ($domain_name);

	# multi-domain setup?
	if (defined($CURRENT_DOMAIN) && ($CURRENT_DOMAIN ne '')) {
		$pagedata->setValue("Config.UI.LinkAttrs.domain", $CURRENT_DOMAIN);
		$pagedata->setValue("Data.CurrentDomain", $CURRENT_DOMAIN);
		$pagedata->setValue("Data.CurrentDomain.Description",
				$DOMAINS{$CURRENT_DOMAIN}{name});
	}
	
	foreach $domain_name (keys %DOMAINS) {
		$pagedata->setValue("Data.Domains.$domain_name",
				$DOMAINS{$domain_name}{'name'});
	}
}

# ---------------------------------------------------------------------------

sub set_pagedata_list_of_lists {

	my (@files, $i, $num);

	# for a multi-domain setup there are no lists available if no domain
	# is selected
	return (0==0) if (%DOMAINS && 
			(!defined($CURRENT_DOMAIN) || ($CURRENT_DOMAIN eq '')));
	
	# undefined $LIST_DIR?
	return (0==0) if (!defined($LIST_DIR) || ($LIST_DIR eq ''));

	# Read the list directory for mailing lists.
	return (0==0) unless (opendir DIR, $LIST_DIR);

	@files = sort grep !/^\./, readdir DIR; 
	closedir DIR;

	$num = 0;
	# Check that they actually are lists and add good ones to pagedata ...
	foreach $i (0 .. $#files) {
		if ((-e "$LIST_DIR/$files[$i]/lock") && (&webauth($files[$i]))) {
			$pagedata->setValue("Data.Lists." . $num, "$files[$i]");
			$num++;
		}
	}
}

# ---------------------------------------------------------------------------

sub set_pagedata {
	my $list = shift;

	# read available list of lists
	&set_pagedata_list_of_lists();

	# multi domain support?
	&set_pagedata_domains() if (%DOMAINS);

	$pagedata->setValue("Data.LocalPrefix", $MAIL_ADDRESS_PREFIX);
	$pagedata->setValue("Data.HostName", $MAIL_DOMAIN);


	# modules
	# TODO: someone should test, if the mysql support works
	$pagedata->setValue("Data.Modules.mySQL",
			($Mail::Ezmlm::MYSQL_BASE)? 1 : 0);
   

	# permissions
	$pagedata->setValue("Data.Permissions.Create",
			(&webauth_create_allowed)? 1 : 0 );
	$pagedata->setValue("Data.Permissions.FileUpload", ($FILE_UPLOAD)? 1 : 0);


	# ezmlm-idx v5.0 stuff
	$pagedata->setValue('Data.areDefaultTextsAvailable', 
		(Mail::Ezmlm->get_version() >= 5)? 1 : 0);

	# get available languages for all lists
	# no results for ezmlm-idx < 5.0
	my $i = 0;
	my $item;
	foreach $item (sort Mail::Ezmlm->get_available_languages()) {
		$pagedata->setValue("Data.AvailableLanguages." . $i, $item);
		$i++;
	}


	# display webuser textfield?
	$pagedata->setValue("Data.WebUser.show", (-e "$WEBUSERS_FILE")? 1 : 0);
	# default username for webuser file
	$pagedata->setValue("Data.WebUser.UserName", $LOGIN_NAME || 'ALL');

	# list specific configuration - use defaults if no list is selected
	if ($list) {
		&set_pagedata4options($list, $list->getconfig);   
		&set_pagedata4list($list, &get_list_part());
	} else {
		&set_pagedata4options($list, $DEFAULT_OPTIONS);
	}

	# add module-specific pagedata
	if ($list) {
		if ($list->isa("Mail::Ezmlm::GpgEzmlm")) {
			set_pagedata_gpgezmlm($list);
		}
	}
}

# ---------------------------------------------------------------------------

sub set_pagedata4list {
	my $list = shift;
	my $part_type = shift;

	if (! -e $list->thislist() . "/lock" ) {
		$warning = 'ListDoesNotExist' if ($warning eq '');
		return (1==0);
	}

	$pagedata->setValue("Data.List.Name", get_listname($list));
	$pagedata->setValue("Data.List.Address", &get_listaddress($list));

	# set global or module-specific blacklist of list options
	&set_pagedata_options_blacklist($list);

	# do we support encryption? Show a possible keyring ...
	&set_pagedata_keyring($list) if ($FEATURES{GPGKEYRING});

	# is this a moderation/administration list?
	&set_pagedata4part_list($list, $part_type) if ($part_type ne '');

	&set_pagedata_subscribers($list, $part_type);
	&set_pagedata_misc_configfiles($list);
	&set_pagedata_textfiles($list);
	&set_pagedata_webusers($list);
	&set_pagedata_localization($list);

	return (0==0);
}

# ---------------------------------------------------------------------------

sub set_pagedata_options_blacklist {
	my $list = shift;
	my ($item, @list_blacklist);

	# check if the function "get_options_blacklist" exists for the list object
	eval {@list_blacklist = $list->get_options_blacklist();};
	# use an empty blacklist, if the member function was not defined
	@list_blacklist = () if ($@);

	foreach $item (@list_blacklist, @INTERFACE_OPTIONS_BLACKLIST) {
		$pagedata->setValue("Data.List.OptionsBlackList." . $item, $item);
	}
}

# ---------------------------------------------------------------------------

sub get_keyring {
	my $list = shift;

	my $keyring_location;

	if ($list->can("get_keyring_location")) {
		$keyring_location = $list->get_keyring_location();
	} elsif ($GPG_KEYRING_DEFAULT_LOCATION =~ m#^/#) {
		$keyring_location = $GPG_KEYRING_DEFAULT_LOCATION;
	} else {
		$keyring_location = $list->thislist()
				. "/$GPG_KEYRING_DEFAULT_LOCATION";
	}
	return Mail::Ezmlm::GpgKeyRing->new($keyring_location);
}

# ---------------------------------------------------------------------------

sub set_pagedata_keyring {
	my $list = shift;
	my ($keyring, @gpg_keys);

	$keyring = get_keyring($list);

	# return without error, if the keyring is empty
	return (0==0) unless (-r $keyring->get_location());

	# retrieve the currently available public keys
	@gpg_keys = $keyring->get_public_keys();
	for (my $i = 0; $i < @gpg_keys; $i++) {
		$pagedata->setValue("Data.List.gnupg_keys.public.$i.id",
				$gpg_keys[$i]{id});
		$pagedata->setValue("Data.List.gnupg_keys.public.$i.email",
				$gpg_keys[$i]{email});
		$pagedata->setValue("Data.List.gnupg_keys.public.$i.name",
				$gpg_keys[$i]{name});
		$pagedata->setValue("Data.List.gnupg_keys.public.$i.expires",
				$gpg_keys[$i]{expires});
	}

	# retrieve the currently available secret keys
	@gpg_keys = $keyring->get_secret_keys();
	for (my $i = 0; $i < @gpg_keys; $i++) {
		$pagedata->setValue("Data.List.gnupg_keys.secret.$i.id",
				$gpg_keys[$i]{id});
		$pagedata->setValue("Data.List.gnupg_keys.secret.$i.email",
				$gpg_keys[$i]{email});
		$pagedata->setValue("Data.List.gnupg_keys.secret.$i.name",
				$gpg_keys[$i]{name});
		$pagedata->setValue("Data.List.gnupg_keys.secret.$i.expires",
				$gpg_keys[$i]{expires});
	}
	# enable "keyring" feature in the interface
	$pagedata->setValue("Data.List.Features.GpgKeyRing", 1);
}

# ---------------------------------------------------------------------------

sub set_pagedata_gpgezmlm {
	# extract hdf-data for encrypted lists
	my $list = shift;
	my (%config, $item);

	$pagedata->setValue("Data.List.Features.GpgEzmlm", 1);
	
	# read the configuration
	%config = $list->getconfig();
	foreach $item (keys %config) {
		$pagedata->setValue("Data.List.Options.gpgezmlm_" . lc($item), $config{$item});
	}

}

# ---------------------------------------------------------------------------

sub set_pagedata_misc_configfiles {
	my $list = shift;
	my ($item);

	# Get the contents of some important files
	$item = $list->getpart('prefix');
	$item = '' unless defined($item);
	$pagedata->setValue("Data.List.Prefix", "$item");

	# check reply_to setting
	$item = $list->getpart('headeradd');
	$item = '' unless defined($item);
	$pagedata->setValue("Data.List.HeaderAdd", "$item");
	$pagedata->setValue("Data.List.Options.special_replytoself", 1)
		if (&is_reply_to_self("$item"));

	# 'headerremove' is ignored if 'headerkeep' exists (since ezmlm-idx v5)
	if ((Mail::Ezmlm->get_version() >= 5.1)
			&& (-e $list->thislist() . "/headerkeep")) {
		$item = $list->getpart('headerkeep');
		$pagedata->setValue("Data.List.HeaderKeep", "$item");
	} else {
		$item = $list->getpart('headerremove');
		$pagedata->setValue("Data.List.HeaderRemove", "$item");
	}
	
	# 'mimeremove' is ignored if 'mimekeep' exists (since ezmlm-idx v5)
	if ((Mail::Ezmlm->get_version() >= 5.1)
			&& (-e $list->thislist() . "/mimekeep")) {
		$item = $list->getpart('mimekeep');
		$item = '' unless defined($item);
		$pagedata->setValue("Data.List.MimeKeep", "$item");
	} else {
		$item = $list->getpart('mimeremove');
		$item = '' unless defined($item);
		$pagedata->setValue("Data.List.MimeRemove", "$item");
	}

	if (Mail::Ezmlm->get_version() >= 5) {
		$item = $list->getpart('copylines');
		$item = '' unless defined($item);
		$pagedata->setValue("Data.List.CopyLines", "$item");
	}

	$item = $list->getpart('mimereject');
	$item = '' unless defined($item);
	$pagedata->setValue("Data.List.MimeReject", "$item");
	$item = $list->get_text_content('trailer');
	$item = '' unless defined($item);
	$pagedata->setValue("Data.List.TrailingText", "$item");
	
	# read message size limits
	$item = $list->getpart('msgsize');
	$item = '' unless defined($item);
	$item =~ m/^\s*(\d*)\s*:\s*(\d*)\s*$/;
	$pagedata->setValue("Data.List.MsgSize.Max", "$1") if defined($1);
	$pagedata->setValue("Data.List.MsgSize.Min", "$2") if defined($2);
}

# ---------------------------------------------------------------------------

sub set_pagedata_subscribers {

	my ($list, $part_type) = @_;
	my ($i, $address, $addr_name, %pretty);

	$i = 0;
	tie %pretty, "DB_File", $list->thislist() . "/webnames" if ($PRETTY_NAMES);
	foreach $address (sort $list->subscribers($part_type)) {
		if ($address ne '') {
			$pagedata->setValue("Data.List.Subscribers." . $i . '.address',
					"$address");
			$addr_name = ($PRETTY_NAMES)? $pretty{$address} : '';
			$pagedata->setValue("Data.List.Subscribers." . $i . '.name',
					$addr_name) if (defined($addr_name));
		}
		$i++;
	}
	untie %pretty if ($PRETTY_NAMES);
}

# ---------------------------------------------------------------------------

sub set_pagedata_textfiles {
	# set the names of the textfiles of this list

	my $list = shift;
	my ($i, @files, $item);

	@files = sort $list->get_available_text_files();
	$i = 0;

	foreach $item (@files) {
		if ($list->is_text_default($item)) {
			$pagedata->setValue('Data.List.DefaultFiles.' . $i , "$item");
		} else {
			$pagedata->setValue('Data.List.CustomizedFiles.' . $i , "$item");
		}
		$i++;
	}

	# text file specified?
	if (defined($q->param('file')) && ($q->param('file') ne '')
			&& ($q->param('file') =~ m/^[\w-]*$/)) {
		my ($content);
		$content = $list->get_text_content($q->param('file'));
		# get character set of current list (ignore ":Q" prefix)
		my ($charset) = split(':',$list->get_charset());
		# use default for ezmlm-idx<5.0
		$charset = 'us-ascii' if ($charset eq '');
		my $content_utf8;
		eval { $content_utf8 = Encode::decode($charset, $content); };
		# use $content if conversion failed somehow
		if ($@) {
			$content_utf8 = $content;
			# no warning, if the encoding support is not available
			warn "Conversion failed for charset '$charset'"
					if ($ENCODE_SUPPORT);
		}
		$pagedata->setValue("Data.List.File.Name", $q->param('file'));
		$pagedata->setValue("Data.List.File.Content", "$content_utf8");
		$pagedata->setValue("Data.List.File.isDefault",
			$list->is_text_default($q->param('file')) ? 1 : 0);
	}
}

# ---------------------------------------------------------------------------

sub set_pagedata_localization {

	my $list = shift;
	my ($i, $item);

	# get available languages for this list
	# no result for ezmlm-idx < 5
	$i = 0;
	foreach $item (sort $list->get_available_languages()) {
		$pagedata->setValue("Data.List.AvailableLanguages." . $i, $item);
		$i++;
	}

	# charset of the list
	if (Mail::Ezmlm->get_version() >= 5) {
		my $charset = $list->get_charset();
		$charset =~ s/^#.*$//m;
		$pagedata->setValue('Data.List.CharSet', "$charset");
	}

	$pagedata->setValue('Data.List.Language', $list->get_lang());
}

# ---------------------------------------------------------------------------

sub set_pagedata_webusers {

	my $list = shift;
	my ($listname, $webusers);

	$listname = get_listname($list);

	# retrieve the users of the list by reading the webusers file
	if (open(WEBUSER, "<$WEBUSERS_FILE")) {
		while(<WEBUSER>) {
			# ok - this is very short:
			# $webusers becomes the matched group as soon as we find the
			# line of the list - and: no, we do not need "=~" instead of "="
			last if (($webusers) = m{^$listname\s*\:\s*(.+)$});
		}
		close WEBUSER;
	}
	# set default if there was no list definition
	$webusers ||= $LOGIN_NAME || 'ALL';

    $pagedata->setValue("Data.List.WebUsers", "$webusers");
}

# ---------------------------------------------------------------------------

sub set_pagedata4options {
	my $list = shift;
	my $options = shift;

	my($i, $key, $state, $value, $list_dir);

	$i = 0;
	$key = lc(substr($options, $i, 1));
	# parse the first part of the options string
	while ($key =~ m/\w/) {
		# scan the first part of the options string for lower case letters
		$state = ($options =~ /^\w*$key\w*\s*/);
		# set the lower case option
		$pagedata->setValue("Data.List.Options." . $key , ($state)? 1 : 0);
		# also set the reverse value - see cs macro "check_active_selection"
		$pagedata->setValue("Data.List.Options." . uc($key) , ($state)? 0 : 1);
		$i++;
		$key = lc(substr($options,$i,1));
	}

	# scan the config for settings
	for ($i=0; $i<=9; $i++) {
		unless (($i eq 1) || ($i eq 2)) {
			$state = ($options =~ /\s-$i (?:'(.+?)')/);
			# store the retrieved value (if possible)
			$value = $1;
			# reset "state" if the owner address starts with '/'
			$state = (0==1) if (($i == 5) && ($state) && ($value =~ m/^\//));
			unless ($state) {
				# set default values
				if ($i eq 0) {
					$value = 'mainlist@' . $MAIL_DOMAIN;
				} elsif ($i eq 3) {
					$value = 'from_address@domain.org';
				} elsif ($i eq 4) {
					$value = '-t24 -m30 -k64';
				} elsif ($i eq 5) {
					$value = 'owner_address@domain.org';
				} elsif ($i eq 6) {
					$value = 'host:port:user:password:database:table';
				} elsif (($i >= 7) && ($i <= 9)) {
					if (defined($list)) {
						$value = $list->thislist() . "/mod";
					} else {
						$value = "mod";
					}
				}
			}
			$pagedata->setValue("Data.List.Settings." . $i . ".value", $value);
			$pagedata->setValue("Data.List.Settings." . $i . ".state",
					$state ? 1 : 0);
		}
	}

	# the list dependent stuff follows - we can stop if no list is selected
	return unless (defined($list));

	$list_dir = $list->thislist();

	# the options "tpxmsr" are used to create a default value
	# if they are unset, the next ezmlm-make will remove the appropriate files
	# but: these files are used, if they exist - regardless of the flag
	# we will look for the files, if someone created them without ezmlm-make
	# this is easier for users, as the options now represent the current
	# behaviour of the list and not the configured flag value
	# this is especially necessary for "trailer", as this file can be created
	# via ezmlm-web without touching the flag
	$pagedata->setValue("Data.List.Options.t" , 1)
		if (-e "$list_dir/trailer");
	$pagedata->setValue("Data.List.Options.f" , 1)
		if (-e "$list_dir/prefix");
	$pagedata->setValue("Data.List.Options.m" , 1)
		if (-e "$list_dir/modpost");
	$pagedata->setValue("Data.List.Options.s" , 1)
		if (-e "$list_dir/modsub");
	$pagedata->setValue("Data.List.Options.r" , 1)
		if (-e "$list_dir/remote");
	# the option 'x' is always off, as we use it for resetting - this
	# should be easier to understand for users
	$pagedata->setValue("Data.List.Options.x" , 0);
}

# ---------------------------------------------------------------------------

sub download_subscribers {
	# return a list of subscribers of a list for download
	my $list = shift;

	my ($listname, $filename, $part_type);
	my (%pretty, $address, $address_name, @subscribers);

	$listname = get_listname($list);

	if (defined($q->param('part'))) {
		$part_type = $q->param('part');
		$filename = "mailinglist-$listname-$part_type.txt";
	} else {
		$filename = "mailinglist-$listname-subscribers.txt";
	}

	tie %pretty, "DB_File", $list->thislist() . "/webnames" if ($PRETTY_NAMES);
	foreach $address (sort $list->subscribers($part_type)) {
		if ($address ne '') {
			if ($PRETTY_NAMES) {
				$address_name = $pretty{$address};
				if ($address_name eq '') {
					push @subscribers, $address;
				} else {
					push @subscribers, "$address_name <$address>";
				}
			} else {
				push @subscribers, $address;
			}
		}
	}
	untie %pretty if ($PRETTY_NAMES);

	if ($#subscribers lt 0) {
		$warning = 'EmptyList';
		return (1==0);
	}

	print "Content-Type: text/plain\n";
	# suggest a download filename
	# (taken from http://www.bewley.net/perl/download.pl)
	print "Content-Disposition: attachment; filename=$filename\n";
	print "Content-Description: exported subscribers list of $listname\n\n";
	foreach $address (@subscribers) {
		print "$address\r\n";
	}
	exit;
}

# ---------------------------------------------------------------------------

sub check_filename {

	my $filename = shift;
	return ($filename =~ m/[^\w-]/) ? (1==0) : (0==0);
}

# ---------------------------------------------------------------------------

sub get_list_part {
	# return the name of the part list (deny, allow, mod, digest or '')

	if (defined($q->param('part'))) {
		$q->param('part') =~ m/^(allow|deny|digest|mod)$/;
		return $1;
	} else {
		return '';
	}
}

# ---------------------------------------------------------------------------

sub is_list_encrypted {
	my $list = shift;

	if ($list->isa("Mail::Ezmlm::GpgEzmlm")) {
		return (0==0);
	} else {
		return (0==1);
	}
}

# ---------------------------------------------------------------------------

sub get_dotqmail_files {
	my $list = shift;

	my (@files, $qmail_prefix);

	# get the location of the dotqmail files of the list
	# read 'dot' for idx v5
	$qmail_prefix = $list->getpart('dot');
	# untaint content (we trust in it)
	if ($qmail_prefix) {
		$qmail_prefix =~ m/^(.*)$/;
		$qmail_prefix = $1;
	}
	# read 'config' (line starts with "T") for idx v4
	unless ($qmail_prefix) {
		my $config = $list->getpart('config');
		$config =~ m/^T:(.*)$/m;
		$qmail_prefix = $1;
	}
	chomp($qmail_prefix);

	# return without result and print a warning, if no dotqmail files were found
	unless ($qmail_prefix) {
		warn "[ezmlm-web]: could not get the location of the dotqmail files of this list";
		return ();
	}

	# get list of existing files (remove empty entries)
	@files = grep {/./} map
			{ (-e "$qmail_prefix$_")? "$qmail_prefix$_" : undef  } (
					'',
					'-default',
					'-owner',
					'-return-default',
					'-reject-default',
					'-accept-default',
					'-confirm-default',
					'-discard-default',
					'-digest-owner',
					'-digest',
					'-digest-return-default');
	return @files;
}

# ---------------------------------------------------------------------------

# check if the input is a quoted string and decode it if necessary
# a quoted string could look like the following:
#	=?ISO-8859-1?Q?S=E9rgio?= <sergio@example.org>
# as a regex:
#	.*=\?ISO-[^\?]+\?Q\?.*\?=.*
sub decode_quoted_string {

	my ($input) = @_;
	my ($pre_text, $post_text, $charset, $encoded, $decoded);

	if ($input =~ m/^(.*)=\?(ISO-[^\?]+)\?Q\?(.*)\?=(.*)$/) {
		$pre_text = $1;
		$charset = $2;
		$encoded = $3;
		$post_text = $4;
		# decode the "quoted printable" encoding
		$decoded = decode_qp($encoded);
		# try to decode according to the given charset
		eval { $decoded = Encode::decode($charset, $decoded); };
		return $pre_text . $decoded . $post_text;
	} else {
		return $input;
	}
}

# ---------------------------------------------------------------------------

sub set_pagedata_subscription_log {
	
	my ($list) = @_;

	my ($log_file, $i, $line);
	my ($datetext, $epoch_seconds, $action, $action_details, $address);
	$log_file = $list->thislist() . "/Log";
	
	# break if there is no log_file
	return unless (-e "$log_file");

	unless (open LOG_FILE, "<$log_file") {
		warn "Failed to open log file: $log_file";
		$warning = 'LogFile';
		return (1==0);
	}

	$i = 0;
	while (<LOG_FILE>) {
		chomp;
		$line = $_;
		# a line of the log file could look like the following:
		#   748392136 +manual foo@bar.org Foo Bar <foo@bar.org>
		# for encoded sender names see "decode_quoted_string" above
		$line =~ m/^(\d+) ([+-])(\w*) ([^ ]*) ?(.*)$/;
		if (defined($5)) {
			$epoch_seconds = $1;
			$action = $2;
			$action_details = $3;
			$address = decode_quoted_string($5 ? $5 : $4);
			$datetext = localtime($epoch_seconds);
			# the date in gmt format - this should be sufficient
			$pagedata->setValue("Data.List.SubscribeLog.$i.date", $datetext);
			# the the action should be +/-
			$pagedata->setValue("Data.List.SubscribeLog.$i.action", $action);
			# manual, probe (removal) or auto (empty details)
			$pagedata->setValue("Data.List.SubscribeLog.$i.details",
					$action_details);
			$pagedata->setValue("Data.List.SubscribeLog.$i.address", $address);
			$i++;
		}
	}
	close LOG_FILE;
}

# ---------------------------------------------------------------------------

sub delete_list {
	# Delete a list ...
	my $list = shift;

	my $listname = get_listname($list);

	if ($UNSAFE_RM == 0) {
		# This doesn't actually delete anything ... It just moves them so that
		# they don't show up. That way they can always be recovered by a helpful
		# sysadmin should he/she be in the mood :)

		my $SAFE_DIR = "$LIST_DIR/_deleted_lists";
		mkdir "$SAFE_DIR", 0700 if (! -e "$SAFE_DIR");

		# look for an unused directory name
		my $i = 0;
		while (-e "$SAFE_DIR/$listname-$i") { $i++; }

		$SAFE_DIR .= "/$listname-$i";

		my @files = &get_dotqmail_files($list);

		# remove list directory
		my $oldfile = $list->thislist();
		unless (move($oldfile, $SAFE_DIR)) {
			$warning = 'SafeRemoveRenameDirFailed';
			return (1==0);
		}

		# remove dotqmail files
		foreach (@files) {
			unless (move($_, "$SAFE_DIR")) {
				$warning = 'SafeRemoveMoveDotQmailFailed';
				return (1==0); 
			}
		}

		warn "List '$oldfile' moved (deleted)";   
	} else {
		# This, however, does DELETE the list. I don't like the idea, but I was
		# asked to include support for it so ...
		my @files = &get_dotqmail_files($list);
		my $olddir = $list->thislist();
		if (unlink(@files) <= 0) {
			$warning = 'UnsafeRemoveDotQmailFailed';
			return (1==0);
		}
		unless (File::Path::rmtree("$LIST_DIR/$olddir")) {
			$warning = 'UnsafeRemoveListDirFailed';
			return (1==0);
		}
		warn "List '" . $list->thislist() . "' deleted";
	}
	return (0==0);
}

# ------------------------------------------------------------------------

sub untaint {
   # Go through all the CGI input and make sure it is not tainted. Log any
   # tainted data that we come accross ... See the perlsec(1) man page ...

   # maybe it was read from a file - so we should untaint it
   $MAIL_DOMAIN = $1 if $MAIL_DOMAIN =~ /^([\w\d\.-]+)$/;
   
   my (@params, $i, $param);
   @params = $q->param;
   
   foreach $i (0 .. $#params) {
      my(@values);
      next if ($params[$i] eq 'mailaddressfile');
      next if ($params[$i] eq 'gnupg_key_file');
      next if ($params[$i] eq 'content');
	  # the button description may contain non-ascii characters - skip check
	  next if ($params[$i] eq 'send');
      foreach $param ($q->param($params[$i])) {
         next if $param eq '';
         if ($param =~ /^([#-\@\w\.\/\[\]\:\n\r\>\< _"']+)$/) {
            push @values, $1;
         } else {
            warn "Tainted input in '$params[$i]': " . $q->param($params[$i]); 
         }
         $q->param(-name=>$params[$i], -values=>\@values);
      }
   } 

	# special stuff

	# check the list name
	if (defined($q->param('list'))) {
		# reset the 'list' input parameter, if it contains invalid characters
		if ($q->param('list') !~ m/^[\w\d\_\-\.\@]+$/) {
			$warning = 'InvalidListName' if ($warning eq '');
			$q->param(-name=>'list', -values=>'');
		}
	}
	
}

# ------------------------------------------------------------------------

sub check_permission_for_action {
	# test if the user is allowed to modify the choosen list or to create a
	# new one the user would still be allowed to fill out the create-form
	# (however he got there), but the final creation is omitted

	my $ret;
	if (defined($action) &&
			(($action eq 'list_create_ask' || $action eq 'list_create_do'))) {
		$ret = &webauth_create_allowed();
	} elsif (defined($q->param('list'))) {
		$ret = &webauth($q->param('list'));
	} else {
		$ret = (0==0);
	}
	return $ret;
}

# ------------------------------------------------------------------------

sub add_address {
	# Add an address to a list ..
	my $list = shift;

	my ($address, $part, @addresses, $fail_count, $success_count);
	$part = &get_list_part();

	$fail_count = 0;
	$success_count = 0;

	if (($q->param('mailaddressfile')) && ($FILE_UPLOAD)) {
		# Sanity check
		my $fileinfo = $q->uploadInfo($q->param('mailaddressfile'));
		my $filetype = $fileinfo->{'Content-Type'};
		unless ($filetype =~ m{^text/}i) {
			$warning = 'InvalidFileFormat';
			warn "[ezmlm-web] mime type of uploaded file rejected: $filetype";
			return (1==0);
		}

		# Handle file uploads of addresses
		my($fh) = $q->param('mailaddressfile');
		while (<$fh>) {
			next if (/^\s*$/ or /^#/); # blank, comments
			if ( /(\w[\w\.\!\#\$\%\&\'\`\*\+\-\/\=\?\^\{\|\}\~]*)@(\w[\-\w_\.]+)/) {
					chomp();
					push @addresses, "$_";
				} else {
				$fail_count++;
			}
		}
		# TODO: is CLOSE necessary?
	}
      
	# User typed in an address
	if ($q->param('mailaddress_add') ne '') {

		$address = $q->param('mailaddress_add');
		$address .= $MAIL_DOMAIN if ($q->param('mailaddress_add') =~ /\@$/);

		# untaint
		if ($address =~ m/(\w[\w\.\!\#\$\%\&\'\`\*\+\-\/\=\?\^\{\|\}\~]*)@(\w[\-\w_\.]+)/) {
			push @addresses, "$address";
		  } else {
			warn "invalid address to add: $address to $part";
			$warning = 'AddAddress';
			return (1==0);
		  }

	}
   
	my %pretty;
	my $add;
	tie %pretty, "DB_File", $list->thislist() . "/webnames" if ($PRETTY_NAMES);
	foreach $address (@addresses) {

		# call the "parse" function of either "Mail::Address" or "Email::Address"
		# based on the perl cookbook (chapter 12_14)
		# we have to disable 'strict refs' for the call
		no strict 'refs';
		($add) = ($mail_address_package . "::parse")->($mail_address_package, $address);
		use strict 'refs';
		if (($add->address() =~ m/^(\w[\w\.\!\#\$\%\&\'\`\*\+\-\/\=\?\^\{\|\}\~]*)@(\w[\-\w_\.]+)$/)
				&& !($list->issub($add->address(), $part))) {
			# it seems, that we cannot trust the return value of "$list->sub"
			$list->sub($add->address(), $part);
			if (defined($add->name()) && $PRETTY_NAMES) {
				$pretty{$add->address()} = $add->name();
			}
			$success_count++;
		} else {
			$fail_count++;
		}
	}
	untie %pretty if ($PRETTY_NAMES);
	if ($fail_count gt 0) {
		$warning = 'AddAddress';
		return (1==0);
	} elsif ($success_count eq 0) {
		# no subscribers - we report an error without issuing a warning
		return (1==0);
	} else {
		# no failures and at least one subscriber -> success
		return (0==0);
	}
}

# ------------------------------------------------------------------------

sub delete_address {
   # Delete an address from a list ...
   my $list = shift;

   my @address;
   my $part = &get_list_part();
   return (1==0) if ($q->param('mailaddress_del') eq '');

   @address = $q->param('mailaddress_del');

   if ($list->unsub(@address, $part) != 1) {
      $warning = 'DeleteAddress';
	  return (1==0);
   }
   
   if ($PRETTY_NAMES) {
      my(%pretty, $add);
      tie %pretty, "DB_File", $list->thislist() . "/webnames";
      foreach $add (@address) {
         delete $pretty{$add};
      }
      untie %pretty;
   }

}

# ------------------------------------------------------------------------

sub set_pagedata4part_list {
   # Deal with list parts ....

   my($list, $part) = @_;
   
   $pagedata->setValue("Data.List.PartType", "$part");

   if ($part eq 'mod') {
      # do we store things in different directories?
      my $config = $list->getconfig();
	  # empty values represent default settings - everything else is considered as evil :)
      my $postpath = $config =~ m{-7\s*'([^']+)'};
      my $subpath = $config =~ m{-8\s*'([^']+)'};
      my $remotepath = $config =~ m{-9\s*'([^']+)'};

      $pagedata->setValue("Data.List.hasCustomizedPostModPath", ($postpath ne '')? 1 : 0);
      $pagedata->setValue("Data.List.hasCustomizedSubModPath", ($subpath ne '')? 1 : 0);
      $pagedata->setValue("Data.List.hasCustomizedAdminPath", ($remotepath ne '')? 1 : 0);
   }
}

# ------------------------------------------------------------------------

sub create_list {
	# Create a list according to user selections ...
	my $listname = shift;
	my ($qmail, $options, $i);

	# Check if the list directory exists and create if necessary ...
	unless ((-e $LIST_DIR) || (mkdir $LIST_DIR, 0700)) {
		warn "Unable to create directory ($LIST_DIR): $!";
		$warning = 'ListDirAccessDenied';
		return undef;
	}

	# Some taint checking ...
	$qmail = $1 if $q->param('inlocal') =~ /(?:$MAIL_ADDRESS_PREFIX-)?([^\<\>\\\/\s]+)$/;
	# dots have to be turned into colons
	# see http://www.qmail.org/man/man5/dot-qmail.html
	$qmail =~ s/\./:/g;
	# dotqmail files may not contain uppercase letters
	$qmail = lc($qmail);
	# are there only valid characters?
	if ($listname !~ m/^[\w\d\_\-\.\@]+$/) {
		$warning = 'InvalidListName';
		return undef;
   	}

	# Sanity Checks ...
	if ($listname eq '') {
		$warning = 'EmptyListName';
		return undef;
   	}
	# the "magic" names are not allowed
	if (($listname =~ m/^ALL$/i) || ($listname =~ m/^ALLOW_CREATE$/i)) {
		$warning = 'ReservedListName';
		return undef;
   	}
	if ($qmail eq '') {
		$warning = 'InvalidLocalPart';
		return undef;
   	}
	if (-e "$LIST_DIR/$listname/lock") {
		$warning = 'ListNameAlreadyExists';
		return undef;
	}
	if (-e "$DOTQMAIL_DIR/.qmail-$qmail") {
		$warning = 'ListAddressAlreadyExists';
		return undef;
	}

	$options = &extract_options_from_params($listname);

	my($list) = new Mail::Ezmlm;

	unless ($list->make(-dir=>"$LIST_DIR/$listname",
				-qmail=>"$DOTQMAIL_DIR/.qmail-$qmail",
				-name=>$q->param('inlocal'),
				-host=>$q->param('inhost'),
				-switches=>$options,
				-user=>$USER)
	) {
		# fatal error
		$customError = "[ezmlm-make] " . $list->errmsg();
		return undef;
	}

	if (defined($q->param('list_language'))
			&& ($q->param('list_language') ne 'default')) {
		if (&check_list_language($list, $q->param('list_language'))) {
			$list->set_lang($q->param('list_language'));
		} else {
			$warning = 'InvalidListLanguage';
		}
	}
	
	# handle MySQL stuff
	if (defined($q->param('setting_state_6')) && $options =~ m/-6\s+/) {
		$customWarning = $list->errmsg() unless ($list->createsql());
	}
   
	if (defined($q->param('webusers'))) {
		# no error returned - just a warning
		$warning = 'WebUsersUpdate'
				unless (&update_webusers($listname, $q->param('webusers')));
	}

	return get_list_object($listname);
}

# ------------------------------------------------------------------------

sub extract_options_from_params {
	# Work out the command line options ...
	my $listname = shift;

	my ($options, $settings, $i);
	my ($old_options, $state, $old_key);

	# NOTE: we have to define _every_ (even unchanged) setting
	# as ezmlm-make removes any undefined value

	if (-e "$LIST_DIR/$listname") {
		# the list does already exist
		my $list = get_list_object($listname);
		$old_options = $list->getconfig();
	} else {
		# creating a new list
		$old_options = $DEFAULT_OPTIONS;
	}

	################ options ################
	$i = 0;
	$options = '';
	$old_key = substr($old_options,$i,1);
	# some special selections
	my @avail_selections = ('archive', 'subscribe', 'posting');
	# parse the first part of the options string
	while ($old_key =~ m/\w/) {
		# scan the first part of the options string for lower case letters
		if (lc($old_key) eq 'x') {
			# the 'x' setting does not really represent the mimeremove
			# ezmlm-idx is ugly: 'X' -> remove file / 'x' -> reset file to default
			if (-e "$LIST_DIR/$listname/mimeremove") {
				$options .= 'x';
				# we have to delete 'mimeremove' if the 'x' checkbox was activated
				# as ezmlm-make will only reset it, if the file does not exist
				unlink("$LIST_DIR/$listname/mimeremove")
					if (defined($q->param('option_x')));
			} else {
				$options .= 'X';
			}
		} elsif (defined($q->param('available_option_' . uc($old_key)))) {
			# inverted checkbox
			my $form_var_name = "option_" . uc($old_key);
			# this option was visible for the user
			if (defined($q->param($form_var_name))) {
				$options .= uc($old_key);
			} else {
				$options .= lc($old_key);
			}
		} elsif (defined($q->param('available_option_' . lc($old_key)))) {
			# non inverted checkbox
			my $form_var_name = "option_" . lc($old_key);
			# this option was visible for the user
			if (defined($q->param($form_var_name))) {
				$options .= lc($old_key);
			} else {
				$options .= uc($old_key);
			}
		} elsif (&is_option_in_selections(lc($old_key)))  {
			# enabled due to some special selection
			$options .= lc($old_key);
		} elsif (&is_option_in_selections(uc($old_key)))  {
			# disabled due to some special selection
			$options .= uc($old_key);
		} elsif ("cevz" =~ m/$old_key/i) {
			# ignore invalid settings (the output of "getconfig" is really weird!)
		} else {
			# import the previously set option
			$options .= $old_key;
		}
		$i++;
		$old_key = substr($old_options,$i,1);
	}


	############### settings ################
	for ($i=0; $i<=9; $i++) {
		if (defined($q->param('available_setting_' . $i))) {
			# this setting was visible for the user
			if (defined($q->param("setting_state_$i"))) {
				$options .= " -$i '" . $q->param("setting_value_$i") . "'";
			} else {
				if ($i != 5) {
					# everything except for the "owner" attribute:
					# do not set the value to an empty string, 
					# as ezmlm-idx 5.0 does not work correctly for this case
					# just skip this setting - this works for 0.4x and 5.0
					#$options .= " -$i ''";
				} else {
					# the "owner" attribute needs something special for reset:
					$options .= " -5 '$LIST_DIR/$listname/Mailbox'";
				}
			}
		} else {
			# import the previous setting
			$state = ($old_options =~ /\s-$i (?:'(.+?)')/);
			$options .= " -$i '$1'" if ($state);
		}
	}

	return $options;
}

# ------------------------------------------------------------------------

sub manage_gnupg_keys {
	# manage gnupg keys
	my $list = shift;

	my ($upload_file, $subset);

	$subset = $q->param('gnupg_subset');
	if (defined($q->param('gnupg_key_file'))) {
		$pagename = 'gnupg_public';
		return &gnupg_import_key($list, $q->param('gnupg_key_file'));
	} elsif (($subset eq 'public') || ($subset eq 'secret')) {
		$pagename = "gnupg_$subset";
		return &gnupg_remove_key($list);
	} elsif ($subset eq 'generate_key') {
		if (&gnupg_generate_key($list)) {
			$pagename = 'gnupg_secret';
			return (0==0);
		} else {
			$pagename = 'gnupg_generate_key';
			return (0==1);
		}
	} else {
		$error = 'UnknownAction';
		return (1==0);
	}
}

# ------------------------------------------------------------------------

sub gnupg_export_key {
	my $list = shift;
	my $keyid = shift;

	my $keyring = get_keyring($list);

	# get the name of the key (for the download filename)
	my @all_keys = $keyring->get_public_keys();
	my ($i, $key, $name);
	for ($i = 0; $i < @all_keys; $i++) {
		$name = $all_keys[$i]{name} if ($keyid eq $all_keys[$i]{id});
	}
	if ($name) {
		$name =~ s/\W+/_/g;
		$name .= '.asc';
	} else {
		$name = "public_key.asc";
	}
	
	my $key_armor;
	if ($key_armor = $keyring->export_key($keyid)) {
		print "Content-Type: text/plain\n";
		# suggest a download filename
		# (taken from http://www.bewley.net/perl/download.pl)
		print "Content-Disposition: attachment; filename=$name\n";
		print "Content-Description: exported key\n\n";
		print $key_armor;
		return (0==0);
	} else {
		return (0==1);
	}
}

# ------------------------------------------------------------------------

sub gnupg_import_key {

	my ($list, $upload_file) = @_;

	my $keyring = get_keyring($list);
	
	if ($upload_file) {
		# Sanity check
		my $fileinfo = $q->uploadInfo($upload_file);
		my $filetype = $fileinfo->{'Content-Type'};
		unless (($filetype =~ m{^text/}i)
				|| ($filetype eq 'application/pgp-encrypted')) {
			$warning = 'InvalidFileFormat';
			warn "[ezmlm-web] mime type of uploaded file rejected: $filetype";
			return (1==0);
		}

		# Handle key upload
		my @ascii_key = <$upload_file>;
		if ($keyring->import_key(join ('',@ascii_key))) {
			$success = 'GnupgKeyImport';
			return (0==0);
		} else {
			$error = 'GnupgKeyImport';
			return (0==1);
		}
	} else {
		$warning = 'GnupgNoKeyFile';
		return (1==0);
	}
}

# ------------------------------------------------------------------------

sub gnupg_generate_key {

	my $list = shift;
	my ($keyring, $key_name, $key_comment, $key_size, $key_expires);

	$keyring = get_keyring($list);

	if (defined($q->param('gnupg_keyname'))) {
		$key_name = $q->param('gnupg_keyname');
	} else {
		$key_name = get_listname($list);
	}

	if (defined($q->param('gnupg_keycomment'))) {
		$key_comment = $q->param('gnupg_keycomment');
	} else {
		$key_comment = "Mailing list";
	}

	if (defined($q->param('gnupg_keysize'))) {
		$key_size = $q->param('gnupg_keysize');
	} else {
		$key_size = 2048;
	}

	if (defined($q->param('gnupg_keyexpires'))) {
		$key_expires = $q->param('gnupg_keyexpires');
	} else {
		$key_expires = 0;
	}

	unless ($key_name) {
		$warning = 'GnupgNoName';
		return (0==1);
	}

	unless ($key_expires =~ m/^[0-9]+[wmy]?$/) {
		$warning = 'GnupgInvalidExpiration';
		return (1==0);
	}

	unless ($key_size =~ m/^[0-9]*$/) {
		$warning = 'GnupgInvalidKeySize';
		return (1==0);
	}

	if ($keyring->generate_private_key($key_name, $key_comment,
			&get_listaddress($list), $key_size, $key_expires)) {
		$pagename = 'gnupg_secret';
		return (0==0);
	} else {
		$error = 'GnupgGenerateKey';
		return (0==1);
	}
}

# ------------------------------------------------------------------------

sub gnupg_remove_key {

	my ($list) = @_;

	my $keyring = get_keyring($list);
	my $removed = 0;
	my $key_id;
	my @all_keys = grep /^gnupg_key_[0-9A-F]*$/, $q->param;

	foreach $key_id (@all_keys) {
		$key_id =~ /^gnupg_key_([0-9A-F]*)$/;
		$keyring->delete_key($1) && $removed++;
	}
	
	if ($removed == 0) {
		$error = 'GnupgDelKey';
		return (1==0);
	} elsif ($#all_keys > $removed) {
		$warning = 'GnupgDelKey';
		return (0==0);
	} else {
		return (0==0);
	}
}

# ------------------------------------------------------------------------

# save gpg-ezmlm settings
# This function should be called after all "common" list options are configured.
# Only encryption-settings are handled - the rest is ignored.
sub update_config_gpgezmlm {
	my $list = shift;
	
	my (%switches, $one_switch, $one_value, $key, @all_params, @blacklist);
	my ($forbidden_switch, $is_allowed);

	# which options are not allowed?
	@blacklist = ("gnupg_keyring_dir", );

	%switches = ();

	# retrieve the configuration settings from the CGI input
	@all_params = $q->param;
	foreach $one_switch (@all_params) {
		if ($one_switch =~ /^available_option_gpgezmlm_(\w*)$/) {
			$key = lc($1);
			# the gnupg directory setting may not be accessible via the web
			# interface, as this would expose the private keys of other lists
			# this would be VERY, VERY ugly!
			# Result: we use the blacklist above
			$is_allowed = (0==0);
			foreach $forbidden_switch (@blacklist) {
				$is_allowed = (0==1) if ($key eq $forbidden_switch);
			}
			if ($is_allowed) {
				$switches{$key} =
						defined($q->param('option_gpgezmlm_' . $key)) ? 1 : 0;
			}
		}
	}

	# Any changes? Otherwise just return. 
	# "scalar keys %..." calculates the length the length of a hash
	if (scalar keys %switches == 0) {
		return (0==0);
	} else {
		# update the configuration file
		if ($list->update(%switches)) {
			return (0==0);
		} else {
			return (1==0);
		}
	}
}

# ------------------------------------------------------------------------

# update the configuration of a list
# This calls the "common" list configuration update. Afterwards possible
# module-specific options are configured via "update_config_???".
sub update_config {
	my $list = shift;

	my $error = (1==0);

	$error = (0==0) unless (update_config_common($list));
	if ($list->isa("Mail::Ezmlm::GpgEzmlm")) {
		$error = (0==0) unless (update_config_gpgezmlm($list));
	}
	return (!$error);
}

# ------------------------------------------------------------------------

sub update_config_common {
	# Save the new user entered config ...
	my $list = shift;
   
	my ($options, @inlocal, @inhost, $old_msgsize);

	$options = &extract_options_from_params(get_listname($list));

	# save the settings, that are generally overwritten by ezmlm-make :(((
	# good candidates are: msgsize, inhost, inlocal and outhost
	# maybe there are some others?
	$old_msgsize = $list->getpart('msgsize');

	# Actually update the list ...
	unless ($list->update($options)) {
		$warning = 'UpdateConfig';
		return (1==0);
	}

	# update trailing text
	if (defined($q->param('trailing_text'))) {
		if (defined($q->param('option_t'))) {
			# TODO: the trailer _must_ be followed by a newline
			$list->set_text_content('trailer', $q->param('trailing_text'));
		} else {
			# ezmlm-make automatically removes this file
		}
	}

	# update prefix text
	if (defined($q->param('prefix'))) {
		if (defined($q->param('option_f'))) {
			$list->setpart('prefix', $q->param('prefix'))
		} else {
			# ezmlm-make automatically removes this file
		}
	}

	# update mimeremove/keep
	if (defined($q->param('mimefilter_action'))) {
		if ($q->param('mimefilter_action') eq "remove") {
			# the checkbox 'x' is only used for reset - so we may not write,
			# if a reset was requested
			$list->setpart('mimeremove', $q->param('mimefilter'))
				unless (defined($q->param('option_x')));
			# remove 'mimekeep' as it is dominating
			my $keep_file = $list->thislist() . "/mimekeep";
			unlink ($keep_file) if (-e $keep_file);
		} elsif ($q->param('mimefilter_action') eq "keep") {
			$list->setpart('mimekeep', $q->param('mimefilter'))
			# it is not necessary to remove 'mimeremove' - see above
		} else {
			warn "Invalid value for 'mimefilter_action': " 
					. ($q->param('mimefilter_action') =~ s/\W/_/g);
				}
	}

	# update mimereject - we do not care for 'x'
	$list->setpart('mimereject', $q->param('mimereject'))
		if (defined($q->param('mimereject')));

	# Update headeradd if this option is visible
	# afterwards we will care about a single 'options_special_replytoself'
	if (defined($q->param('headeradd'))
			|| defined($q->param('available_option_special_replytoself'))) {
		my $headers;
		if (defined($q->param('headeradd'))) {
			$headers = $q->param('headeradd');
		} else {
			$headers = $list->getpart('headeradd');
		}
		chomp($headers);
		if (defined($q->param('available_option_special_replytoself'))) {
			if (!defined($q->param('option_special_replytoself'))
					&& (&is_reply_to_self("$headers"))) {
				# remove the header line
				$headers =~ s/^Reply-To:\s+.*$//m;
			} elsif (defined($q->param('option_special_replytoself'))
					&& (!&is_reply_to_self("$headers"))) {
				# add the header line
				chomp($headers);
				$headers .= "\nReply-To: <#l#>@<#h#>";
			}
		}
		$list->setpart('headeradd', "$headers");
	}

	# update headerremove/keep
	if (defined($q->param('headerfilter_action'))) {
		if ($q->param('headerfilter_action') eq "remove") {
			$list->setpart('headerremove', $q->param('headerfilter'));
			# remove 'headerkeep' as it is dominating
			my $keep_file = $list->thislist() . "/headerkeep";
			unlink ($keep_file) if (-e $keep_file);
		} elsif ($q->param('headerfilter_action') eq "keep") {
			$list->setpart('headerkeep', $q->param('headerfilter'))
			# it is not necessary to remove 'headerremove' - see above
		} else {
			warn "Invalid value for 'headerfilter_action': " 
					. ($q->param('headerfilter_action') =~ s/\W/_/g);
		}
	}

	# 'copylines' setting (since ezmlm-idx v5)
	if (defined($q->param('copylines'))) {
		my $copylines;
		$copylines = (defined($q->param('copylines'))) ?
			$q->param('copylines') : 0;
		if (defined($q->param('copylines_enabled')) && ($copylines)) {
			$list->setpart('copylines', "$copylines");
		} else {
			my $copyfile = $list->thislist() . "/copylines";
			unlink ($copyfile) if (-e $copyfile);
		}
	}

	# 'msgsize' setting
	if (defined($q->param('msgsize_max_value'))
			&& defined($q->param('msgsize_min_value'))) {
		my ($minsize, $maxsize);
		$maxsize = (defined($q->param('msgsize_max_state'))) ?
			$q->param('msgsize_max_value') : 0;
		$minsize = (defined($q->param('msgsize_min_state'))) ?
			$q->param('msgsize_min_value') : 0;
		$list->setpart('msgsize', "$maxsize:$minsize");
	} else {
		# restore the original value, as ezmlm-make always overrides these values :(((
		$list->setpart('msgsize', "$old_msgsize");
	}

	# update charset
	# only if it is different from the previous value and the language was NOT changed
	# otherwise it could overwrite the default of a new selected language
	# this has to be done before updating the language
	if (defined($q->param('list_charset'))) {
		if ((defined($q->param('list_language')))
				&& ($q->param('list_language') ne $list->get_lang())
				&& ($list->get_charset() eq $q->param('list_charset'))) {
			$list->set_charset('');
		} else {
			$list->set_charset($q->param('list_charset'));
		}
	}
	
	# update language
	# this _must_ happen after set_charset to avoid accidently overriding
	# the default charset
	if (defined($q->param('list_language'))) {
		if (&check_list_language($list, $q->param('list_language'))) {
			$list->set_lang($q->param('list_language'));
		} else {
			$warning = 'InvalidListLanguage';
		}
	}

	# change webuser setting
	if (defined($q->param('webusers'))) {
		$warning = 'WebUsersUpdate'
				unless (&update_webusers(get_listname($list),
						$q->param('webusers')));
	}

	return (0==0);
}

# ------------------------------------------------------------------------

sub is_reply_to_self {
	# check if the header lines of the list contain a reply-to-self line
	
	my ($header_lines) = @_;
	return (0==0) if ($header_lines =~ m/^Reply-To:\s+<#l#>@<#h#>/m);
	return (1==0);
}

# ------------------------------------------------------------------------

sub is_option_in_selections {
	# check if the given 'key' is defined in any of the special selection
	# form fields ('archive', 'subscribe', 'posting'). Case for key matters!

	my $key = shift;
	my @avail_selections = ('archive', 'subscribe', 'posting');
	my $one_selection;

	foreach $one_selection (@avail_selections) {
		my $form_name = "selection_$one_selection";
		return (0==0) if (defined($q->param($form_name))
				&& ($q->param($form_name) =~ m/$key/));
	}
	return (1==0);
}

# ------------------------------------------------------------------------

sub update_webusers {
	# replace existing webusers-line or add a new one
	my $listname = shift;
	my $webusers_input = shift;

	my ($temp_file, $fh, $matched, @admins, $admin);

	# Back up web users file
	# generate a temporary filename (as suggested by the Perl Cookbook)
	do { $temp_file = POSIX::tmpnam() }
	    until $fh = IO::File->new($temp_file, O_RDWR|O_CREAT|O_EXCL);
	close $fh; 
	unless (open(TMP, ">$temp_file")) {
		warn "could not open a temporary file";
		return (1==0);
	}
	open(WU, "<$WEBUSERS_FILE");
	while(<WU>) { print TMP; }
	close WU; close TMP;

	$matched = 0;
	# remove any insecure characters (e.g. a line break :))
	$webusers_input =~ s/[^\w,_\.\-\@]/ /gs;

	# replace commas by space and reduce multiple space
	# strip leading and trailing whitespace
	$webusers_input =~ s/,/ /g;
	$webusers_input =~ s/^\s+//;
	$webusers_input =~ s/\s+$//;
	# reduce multiple whitespaces to a single space
	$webusers_input =~ s/\s+/ /g;
	# turn everything into lowercase (except for "ALL")
	@admins = ();
	foreach $admin (split(/ /, $webusers_input)) {
		$admin = lc($admin) unless ($admin eq 'ALL');
		push @admins, $admin;
	}
	# concatenate the lowercase usernames again
	$webusers_input = join(' ', @admins);

	# create the updated webusers file
	open(TMP, "<$temp_file");
	unless (open(WU, ">$WEBUSERS_FILE")) {
		warn "the webusers file ($WEBUSERS_FILE) is not writable";
		return (0==1);
	}
	while(<TMP>) {
		if ($_ =~ m/^$listname\s*:/i) {
			print WU $listname . ': ' . $webusers_input . "\n"
					if ($matched == 0);
			$matched = 1;
		} else {
			print WU $_;
		}
	}
	# append the line, if there was no matching line found before
	print WU $listname . ': ' . $webusers_input . "\n" if ($matched == 0);
	
	close TMP; close WU;
	unlink "$temp_file";
}

# ------------------------------------------------------------------------

sub output_mime_examples {
	# print an incomplete list of possible mime types (taken from ezmlm-idx 6.0)

	my $example_file = "$TEMPLATE_DIR/mime_type_examples.txt";
	print "Content-Type: text/plain\n\n";
	if (open(MTF, "<$example_file")) {
		while (<MTF>) {
			print $_;
		}
		close MTF;
	} else {
		warn "Failed to open the example file ($example_file): $!\n";
		print "Failed to open the example file ($example_file): $!\n";
	}
}

# ------------------------------------------------------------------------

sub get_listname {
	my $list = shift;
	my @list_dir = split "/", $list->thislist();
	return $list_dir[$#list_dir];
}

# ------------------------------------------------------------------------

sub get_listaddress {
   # Work out the address of this list ...
   my $list = shift;
   my $listaddress;

   chomp($listaddress = $list->getpart('outlocal'));
   $listaddress .= '@';
   chomp($listaddress .= $list->getpart('outhost'));
   return $listaddress;
}

# ------------------------------------------------------------------------

sub save_text {
	# Save new text in DIR/text ...
	my $list = shift;

	my ($content, $charset);

	$content = $q->param('content');
	$charset = split(':',$list->get_charset());
	$charset = 'us-ascii' if ($charset eq '');
	# untaint 'content' unconditionally
	$content =~ m/^(.*)$/;
	$content = $1;
	my $content_encoded;
	eval { $content_encoded = Encode::encode($charset, $content); };
	if ($@) {
		$content_encoded = $content;
		# no warning, if the encoding support is not available
		warn "Conversion failed for charset '$charset'" if ($ENCODE_SUPPORT);
	}
	unless ($list->set_text_content($q->param('file'), $content_encoded)) {
		$warning = 'SaveFile';
		return (1==0);
	}
	return (0==0);
}   

# ------------------------------------------------------------------------

sub webauth {
	my $listname = shift;
   
	# Check if webusers file exists - if not, then access is granted
	return (1==0) if (! -e "$WEBUSERS_FILE");

	# if there was no user authentication, then everything is allowed
	return (0==0) if (!$LOGIN_NAME);

	# Read authentication level from webusers file. Format of this file is
	# somewhat similar to the unix groups file
	unless (open (USERS, "<$WEBUSERS_FILE")) {
		warn "Unable to read webusers file ($WEBUSERS_FILE): $!";
		$warning = 'WebUsersRead';
		return (1==0);
	}

	# TODO: check, why "directly after creating a new list" this does not
	# work without the "m" switch for the regexp - very weird!
	# the same goes for webauth_create_allowed
	# maybe the creating action changed some file access defaults?
	while(<USERS>) {
		if (/^($listname|ALL):/im) {
			# the following line should be synchronized with the
			# webauth_create_allowed sub
			if (/^[^:]*:(|.*[\s,])($LOGIN_NAME|ALL)(,|\s|$)/m) {
				close USERS;
				return (0==0);
			}
		}   
	}
	close USERS;
	return (1==0);
}

# ---------------------------------------------------------------------------

sub webauth_create_allowed {

	# for a multi-domain setup we disallow list creation until a domain
	# is selected
	return (1==0) if (%DOMAINS && 
			(!defined($CURRENT_DOMAIN) || ($CURRENT_DOMAIN eq '')));

	# Check if we were called with the deprecated
	# argument "-c" (allow to create lists)
	return (0==0) if (defined($opt_c));

	# if there was no user authentication, then everything is allowed
	return (0==0) if (!$LOGIN_NAME);

	# Check if webusers file exists - if not, then access is granted
	return (1==0) if (! -e "$WEBUSERS_FILE");

	# Read create-permission from webusers file.
	# the special listname "ALLOW_CREATE" controls, who is allowed to do it
	unless (open (USERS, "<$WEBUSERS_FILE")) {
		warn "Unable to read webusers file ($WEBUSERS_FILE): $!";
		$warning = 'WebUsersRead';
		return (1==0);
	}

	while(<USERS>) {
		if (/^ALLOW_CREATE:/im) {
			# the following line should be synchronized with the webauth sub
			if (/[:\s,]($LOGIN_NAME|ALL)(,|\s|$)/m) {
				close USERS;
				return (0==0);
			}
		}   
	}
	close USERS;
	return (1==0);
}

# ---------------------------------------------------------------------------

sub get_available_interface_languages {

	my (%languages, @files, $file);

	%languages = ();

	# already cached? otherwise we have to retrieve the data first
	if (exists($CACHED_DATA{'interface_languages'})) {
		# we only store a reference to the languages hash
		%languages = %{$CACHED_DATA{'interface_languages'}};
	} else {

		opendir(DIR, $LANGUAGE_DIR)
			or &fatal_error ("Language directory ($LANGUAGE_DIR) "
					. "is not accessible!");
		@files = sort grep { /.*\.hdf$/ } readdir(DIR);
		close(DIR);

		foreach $file (@files) {
			my $hdf = ClearSilver::HDF->new();
			$hdf->readFile("$LANGUAGE_DIR/$file");
			substr($file, -4) = "";
			my $lang_name = $hdf->getValue("Lang.Name", "$file");
			$languages{$file} = $lang_name;
		}

		$CACHED_DATA{'interface_languages'} = \%languages;
	}

	return %languages;
}

# ---------------------------------------------------------------------------

sub get_available_interfaces {

	my (%interfaces, @files, $file);

	# already cached? otherwise we have to retrieve the data first
	if (exists($CACHED_DATA{'interfaces'})) {
		# we only store a reference to the interfaces hash
		%interfaces = %{$CACHED_DATA{'interfaces'}};
	} else {
		opendir(DIR, "$TEMPLATE_DIR/ui")
			or &fatal_error ("Interface directory ($TEMPLATE_DIR/ui)"
					. "is not accessible!");
		@files = sort grep { /.*\.hdf$/ } readdir(DIR);
		close(DIR);

		foreach $file (@files) {
			substr($file, -4) = "";
			$interfaces{$file} = $file;
		}
		$CACHED_DATA{'interfaces'} = \%interfaces;
	}

	return %interfaces;
}

# ---------------------------------------------------------------------------

sub check_interface_language {

	my ($language) = @_;
	my %languages = &get_available_interface_languages();
	return defined($languages{$language});
}

# ---------------------------------------------------------------------------

sub check_list_language {

	my ($list, $lang) = @_;
	my $found = 0;
	my $item;
	foreach $item ($list->get_available_languages()) {
		$found++ if ($item eq $q->param('list_language'));
	}
	return ($found > 0);
}

# ---------------------------------------------------------------------------

sub safely_import_module {
	# import a module if it exists
	# otherwise False is returned

	my ($mod_name) = @_;
	eval "use $mod_name";
	if ($@) {
		# we do not need the warning message
		# warn "Failed to load module '$mod_name': $@";
		return (1==0);
	} else {
		return (0==0);
	}
}

# ---------------------------------------------------------------------------

sub fatal_error() {

	my $text = shift;

	print "Content-Type: text/html; charset=utf-8\n\n";
	print "<html><head>\n";
	print "<title>ezmlm-web</title></head>\n";
	print "<body><h1>a fatal error occoured!</h1>\n";
	print "<p><strong><big>$text</big></strong></p>\n";
	print "<p>check the error log of your web server for details</p>\n";
	print "</body></html>\n";
	die "$text";
}

# ------------------------------------------------------------------------
# End of ezmlm-web.cgi
# ------------------------------------------------------------------------
__END__

=head1 NAME

ezmlm-web - A web configuration interface to ezmlm mailing lists

=head1 SYNOPSIS

ezmlm-web [B<-c>] [B<-C> E<lt>F<config file>E<gt>] [B<-d> E<lt>F<list directory>E<gt>]

=head1 DESCRIPTION

=over 4

=item B<-C>

Specify an alternate configuration file given as F<config file>
If not specified, ezmlm-web checks first in the users home directory, then the
current directory (filename: .ezmlmwebrc) and then F</etc/ezmlm-web/ezmlmwebrc>.

=item B<-d>

Specify an alternate directory where lists live. This is now
depreciated in favour of using a custom ezmlmwebrc, but is left for backward
compatibility.

=back

=head1 SUID WRAPPER

Create a suid binary wrapper for every (virtual) mailing list account:

	ezmlm-web-make-suid john ~john/public_html/cgi-bin/ezmlm-web

=head1 DOCUMENTATION/CONFIGURATION

Please refer to the example ezmlmwebrc which is well commented, and
to the README file in this distribution.

=head1 ENCRYPTED MAILING LISTS

Please refer to README.gnupg for details on how to manage encrypted
mailing lists with ezmlm-web.

=head1 FILES

=over

=item F<./.ezmlmwebrc>

=item F<~/.ezmlmwebrc>

=item F</etc/ezmlm-web/ezmlmwebrc>

=back

=head1 AUTHORS

=over

=item Guy Antony Halse <guy-ezmlm@rucus.ru.ac.za>

=item Lars Kruse <devel@sumpfralle.de>

=back

=head1 BUGS

None known yet. Please report bugs to the author.

=head1 S<SEE ALSO>
 
L<ezmlm-web-make-suid(1)>, L<ezmlm(5)>, L<ezmlm-cgi(1)>, L<Mail::Ezmlm(3)>

=over

=item L<https://systemausfall.org/toolforge/ezmlm-web/>

=item L<http://rucus.ru.ac.za/~guy/ezmlm/>

=item L<http://www.ezmlm.org/>

=item L<http://www.qmail.org/>

=back

