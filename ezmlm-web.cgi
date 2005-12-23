#!/usr/bin/perl 
#===========================================================================
# ezmlm-web.cgi - version 2.3 - 10/06/02005
#
# Copyright (C) 1999/2000, Guy Antony Halse, All Rights Reserved.
# Please send bug reports and comments to guy-ezmlm@rucus.ru.ac.za
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: 
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# Neither name Guy Antony Halse nor the names of any contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ``AS
# IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ==========================================================================
# All user configuration happens in the config file ``ezmlmwebrc''
# POD documentation is at the end of this file
# ==========================================================================

package ezmlm_web;

# Modules to include
use strict;
use Getopt::Std;
use ClearSilver;
use Mail::Ezmlm;
use Mail::Address;
use File::Copy;
use DB_File;
use CGI;
use IO::File;
use POSIX qw(tmpnam);
use Encode qw/ from_to /;	# add by ooyama for char convert

# These two are actually included later and are put here so we remember them.
#use File::Find if ($UNSAFE_RM == 1);
#use File::Copy if ($UNSAFE_RM == 0);


my $q = new CGI;
$q->import_names('Q');
use vars qw[$opt_c $opt_d $opt_C];
getopts('cd:C:');

# Suid stuff requires a secure path.
$ENV{'PATH'} = '/bin';

# We run suid so we can't use $ENV{'HOME'} and $ENV{'USER'} to determine the
# user. :( Don't alter this line unless you are _sure_ you have to.
my @tmp = getpwuid($>); use vars qw[$USER]; $USER=$tmp[0];

# use strict is a good thing++

use vars qw[$HOME_DIR]; $HOME_DIR=$tmp[7];
use vars qw[$DEFAULT_OPTIONS $UNSAFE_RM $ALIAS_USER $LIST_DIR];
use vars qw[$QMAIL_BASE $PRETTY_NAMES];
use vars qw[$FILE_UPLOAD $WEBUSERS_FILE $MAIL_DOMAIN $HTML_TITLE];
use vars qw[$HTML_CSS_FILE $TEMPLATE_DIR $LANGUAGE_DIR $HTML_LANGUAGE];

# set default TEXT_ENCODE
use vars qw[$TEXT_ENCODE]; $TEXT_ENCODE='us-ascii';	# by ooyama for multibyte convert support

# pagedata contains the hdf tree for clearsilver
# pagename refers to the template file that should be used
use vars qw[$DEFAULT_HOST];
use vars qw[$pagedata $pagename $error $customError $warning $customWarning $success];

# Get user configuration stuff
if(defined($opt_C)) {
   $opt_C =~ /^([-\w.\/]+)$/;	# security check by ooyama
   require "$1"; # Command Line
} elsif(-e "$HOME_DIR/.ezmlmwebrc") {
   require "$HOME_DIR/.ezmlmwebrc"; # User
} elsif(-e "./ezmlmwebrc") {
   require "./ezmlmwebrc"; # Install
} elsif(-e "/etc/ezmlm/ezmlmwebrc") {
   require "/etc/ezmlm/ezmlmwebrc"; # System
} else {
   die "Unable to read config file";
}

# Allow suid wrapper to over-ride default list directory ...
if(defined($opt_d)) {
   $LIST_DIR = $1 if ($opt_d =~ /^([-\@\w.\/]+)$/);
}

# If WEBUSERS_FILE is not defined in ezmlmwebrc (as before version 2.2), then use former default value for compatibility
if (!defined($WEBUSERS_FILE)) {
   $WEBUSERS_FILE = $LIST_DIR . '/webusers'
}

# check optional stylesheet
$HTML_CSS_FILE = '' unless defined($HTML_CSS_FILE);

# check template directory
$TEMPLATE_DIR = 'template' unless defined($TEMPLATE_DIR);

if (defined($MAIL_DOMAIN) && ($MAIL_DOMAIN ne '')) {
	$DEFAULT_HOST = $MAIL_DOMAIN;
} else {
	# Work out default domain name from qmail (for David Summers)
	open (GETHOST, "<$QMAIL_BASE/defaultdomain") || open (GETHOST, "<$QMAIL_BASE/me") || die "Unable to read $QMAIL_BASE/me: $!";
	chomp($DEFAULT_HOST = <GETHOST>);
	close GETHOST;
}


# Untaint form input ...
&untaint;

my $pagedata = load_hdf();
my $action = $q->param('action');

# check permissions
unless (&check_permission_for_action) {
	$pagename = 'list_select';
	$error = 'Forbidden';
}
# This is where we decide what to do, depending on the form state and the
# users chosen course of action ...
# TODO: unify all these "is list param set?" checks ...
elsif ($action eq '' || $action eq 'list_select') {
	# Default action. Present a list of available lists to the user ...
	$pagename = 'list_select';
} elsif ($action eq 'subscribers') {
	# display list (or part list) subscribers
	if (defined($q->param('list'))) {
		$pagename = 'subscribers';
	} else {
		$pagename = 'list_select';
		$error = 'ParameterMissing';
	}
} elsif ($action eq 'address_del') {
	# Delete a subscriber ...
	if (defined($q->param('list'))) {
		$success = 'DeleteAddress' if (&delete_address());
		$pagename = 'subscribers';
	} else {
		$error = 'ParameterMissing';
		$pagename = 'list_select';
	}
} elsif ($action eq 'address_add') {
	# Add a subscriber ...
	# no selected addresses -> no error
	if (defined($q->param('list'))) {
		$success = 'AddAddress' if (&add_address());
		$pagename = 'subscribers';
	} else {
		$error = 'ParameterMissing';
		$pagename = 'list_select';
	}
} elsif ($action eq 'list_delete_ask') {
	# Confirm list removal
	if (defined($q->param('list'))) {
		$pagename = 'list_delete';
	} else {
		$pagename = 'list_select';
		$error = 'ParameterMissing';
	}
} elsif ($action eq 'list_delete_do') {
	# User really wants to delete a list ...
	warn "do it";
	if (defined($q->param('list'))) {
		$success = 'DeleteList' if (&delete_list());
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
	if (&create_list()) {
		$success = 'CreateList';
		$pagename = 'subscribers';
	} else {
		$pagename = 'list_create';
	}
} elsif (($action eq 'config_ask') || ($action eq 'config_do')) {
	# User wants to see/change the configuration ...
	my $subset = $q->param('config_subset');
	if (defined($q->param('list')) && ($subset ne '')
			&& ($subset =~ /^[\w]*$/) && (-e "$TEMPLATE_DIR/config_$subset" . ".cs")) {
		$success = 'UpdateConfig' if (($action eq 'config_do') && &update_config());
		$pagename = 'config_' . $subset;
	} else {
		$error = 'ParameterMissing';
		$pagename = 'list_select';
	}
} elsif ($action eq 'textfiles') {
	# Edit DIR/text ...
	if (defined($q->param('list'))) {
		$pagename = 'textfiles';
	} else {
		$error = 'ParameterMissing';
		$pagename = 'list_select';
	}
} elsif ($action eq 'textfile_edit') {
	# edit the content of a text file
	if (defined($q->param('list')) && defined($q->param('file'))) {
		if (! &check_filename($q->param('file'))) {
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
	if (defined($q->param('list')) && defined($q->param('file')) && defined($q->param('content'))) {
		if (! &check_filename($q->param('file'))) {
			$error = 'InvalidFileName';
			$pagename = 'textfiles';
		} elsif (&save_text()) {
			$pagename = 'textfiles';
			$success = 'SaveFile';
		} else {
			$warning = 'SaveFile';
			$pagename = 'textfile_edit';
		}
	} else {
		$error = 'ParameterMissing';
		if ($q->param('list')) {
			$pagename = 'textfiles';
		} else {
			$pagename = 'list_select';
		}
	}
} else {
	$pagename = 'list_select';
	$error = 'UnknownAction';
}

# read the current state
&set_pagedata();

# Print page and exit :) ...
&output_page;
exit;


# =========================================================================

sub load_hdf {
	# initialize the data for clearsilver
	my $hdf = ClearSilver::HDF->new();

	$hdf->readFile($LANGUAGE_DIR . '/' . $HTML_LANGUAGE . '.hdf');

	# TODO: check for existence
	$hdf->setValue("TemplateDir", "$TEMPLATE_DIR/");
	$hdf->setValue("LanguageDir", "$LANGUAGE_DIR/");
	$hdf->setValue("ScriptName", $ENV{'SCRIPT_NAME'});
	$hdf->setValue("Stylesheet", "$HTML_CSS_FILE");
	$hdf->setValue("Config.PageTitle", "$HTML_TITLE");

	return $hdf;
}


sub output_page {
	# Print the page

	$pagedata->setValue('Data.Success', "$success") if (defined($success));
	$pagedata->setValue('Data.Error', "$error") if (defined($error));
	$pagedata->setValue('Data.Warning', "$warning") if (defined($warning));
	$pagedata->setValue('Data.CustomError', "$customError") if (defined($customError));
	$pagedata->setValue('Data.CustomWarning', "$customWarning") if (defined($customWarning));

	$pagedata->setValue('Data.Action', "$pagename");

	my $pagefile = $TEMPLATE_DIR . "/main.cs";
	die "main template ($pagefile) not found!" unless (-e "$pagefile");
	die "sub template ($TEMPLATE_DIR/$pagename.cs) not found!" unless (-e "$TEMPLATE_DIR/$pagename.cs");

	# print http header
	print "Content-Type: text/html\n\n";

	my $cs = ClearSilver::CS->new($pagedata);

	$cs->parseFile($pagefile);

	print $cs->render();
}


sub set_pagedata()
{
   my (@lists, @files, $i, $item);

   # Read the list directory for mailing lists.
   unless (opendir DIR, $LIST_DIR) {
		$warning = 'ListDirAccessDenied';
		return (1==0);
	}

   @files = sort grep !/^\./, readdir DIR; 
   closedir DIR;

   # Check that they actually are lists and add good ones to pagedata ...
   my $num = 0;
   foreach $i (0 .. $#files) {
		if ((-e "$LIST_DIR/$files[$i]/lock") && (&webauth($files[$i]))) {
		$pagedata->setValue("Data.Lists." . $num, "$files[$i]");
		$num++;
      }
   }

   # list specific configuration
   if ($q->param('list') ne '' )
   {
   	&set_pagedata4list(&get_list_part());
   } else {
   	&set_pagedata4options($DEFAULT_OPTIONS);
   }


   # username and hostname
   my ($hostname, $username);
   # Work out if this user has a virtual host and set input accordingly ...
   if(-e "$QMAIL_BASE/virtualdomains") {
      open(VD, "<$QMAIL_BASE/virtualdomains") || warn "Can't read virtual domains file: $!";
      while(<VD>) {
	 last if(($hostname) = /(.+?):$USER/);
      }
      close VD;
   }
   
   if(!defined($hostname)) {
      $username = "$USER-" if ($USER ne $ALIAS_USER);
      $hostname = $DEFAULT_HOST;
   }

   $pagedata->setValue("Data.UserName", "$username");
   $pagedata->setValue("Data.HostName", "$hostname");


   # modules
   # TODO: someone should test, if the mysql support works
   $pagedata->setValue("Data.Modules.MySQL", ($Mail::Ezmlm::MYSQL_BASE)? 1 : 0);
   

   # permissions
   $pagedata->setValue("Data.Permissions.Create", (&webauth_create_allowed)? 1 : 0 );
   $pagedata->setValue("Data.Permissions.FileUpload", ($FILE_UPLOAD)? 1 : 0);


   # display webuser textfield?
   $pagedata->setValue("Data.WebUser.show", (-e "$WEBUSERS_FILE")? 1 : 0);
   # default username for webuser file
   $pagedata->setValue("Data.WebUser.UserName", $ENV{'REMOTE_USER'}||'ALL');
}


sub set_pagedata4list
{
	my $part_type = shift;
	my ($list, $listname, $webusers);
	my ($i, $item, @files);

	$listname = $q->param('list');
	
	if (! -e "$LIST_DIR/$listname/lock" ) {
		$warning = 'ListDoesNotExist' if ($warning eq '');
		return;
	}
	
	# Work out the address of this list ...
	$list = new Mail::Ezmlm("$LIST_DIR/$listname");

	$pagedata->setValue("Data.List.Name", "$listname");
	$pagedata->setValue("Data.List.Address", &this_listaddress);
	&set_pagedata4part_list($part_type) if ($part_type ne '');

	$i = 0;
	my $item;
	# TODO: use "pretty" output style for visible mail address
	foreach $item ($list->subscribers($part_type)) {
		$pagedata->setValue("Data.List.Subscribers." . $i, "$item") unless ($item eq '');
		$i++;
	}

	$pagedata->setValue("Data.List.hasDenyList", 1) if ($list->isdeny);
	$pagedata->setValue("Data.List.hasAllowList", 1) if ($list->isallow);
	$pagedata->setValue("Data.List.hasDigestList", 1) if ($list->isdigest);

	# Get the contents of some important files
	$item = $list->getpart('prefix');
	$pagedata->setValue("Data.List.Prefix", "$item");
	$item = $list->getpart('headeradd');
	$pagedata->setValue("Data.List.HeaderAdd", "$item");
	$item = $list->getpart('headerremove');
	$pagedata->setValue("Data.List.HeaderRemove", "$item");
	$item = $list->getpart('mimeremove');
	$pagedata->setValue("Data.List.MimeRemove", "$item");
	$item = $list->getpart('mimereject');
	$pagedata->setValue("Data.List.MimeReject", "$item");
	$item = $list->getpart('text/trailer');
	$pagedata->setValue("Data.List.TrailingText", "$item");
	
	# read message size limits
	$list->getpart('msgsize') =~ m/^\s*(\d+)\s*:\s*(\d+)\s*$/;
	$pagedata->setValue("Data.List.MsgSize.Max", "$1");
	$pagedata->setValue("Data.List.MsgSize.Min", "$2");

	# TODO: this is definitely ugly - create a new sub!
	if(open(WEBUSER, "<$WEBUSERS_FILE")) {
		while(<WEBUSER>) {
			last if (($webusers) = m{^$listname\s*\:\s*(.+)$});
		}
		close WEBUSER;
	}
	# set default if there was no list definition
	$webusers ||= $ENV{'REMOTE_USER'} || 'ALL';

    $pagedata->setValue("Data.List.WebUsers", "$webusers");

	# get the names of the textfiles of this list
	{
		my($listDir);
		$listDir = $LIST_DIR . '/' . $q->param('list');

		# Read the list directory for text ...
		if (opendir DIR, "$listDir/text") {
			@files = grep !/^\./, readdir DIR; 
			closedir DIR;
		} else {
			$warning = 'TextDirAccessDenied' if ($warning eq '')
		}

		$i = 0;
		my $item;
		foreach $item (@files) {
			$pagedata->setValue("Data.List.Files." . $i, "$item");
			$i++;
		}

		# text file specified?
		if ($q->param('file') ne '')
		{
			my ($content);
			$content = $list->getpart("text/" . $q->param('file'));
			from_to($content,$TEXT_ENCODE,'utf8');	# by ooyama for multibyte
			$pagedata->setValue("Data.List.File.Name", $q->param('file'));
			$pagedata->setValue("Data.List.File.Content", "$content");
		}
	}
	&set_pagedata4options($list->getconfig);   
}

# ---------------------------------------------------------------------------

sub set_pagedata4options {
	my($options) = shift;
	my($i, $key, $state, $value, $dir_of_list);

	$dir_of_list = $LIST_DIR . '/' . $q->param('list');

	$i = 0;
	$key = lc(substr($options,$i,1));
	# parse the first part of the options string
	while ($key =~ m/\w/) {
		# scan the first part of the options string for lower case letters
		$state = ($options =~ /^\w*$key\w*\s*/);
		$pagedata->setValue("Data.List.Options." . $key , ($state)? 1 : 0);
		$i++;
		$key = lc(substr($options,$i,1));
	}

	# the options "t", "p" and "x" are only used to create a default value
	# they have no meaning, so we should adapt them to reality
	$pagedata->setValue("Data.List.Options.t" , 1)
		if (-e "$dir_of_list/text/trailer");
	$pagedata->setValue("Data.List.Options.p" , 1)
		if (-e "$dir_of_list/prefix");
	$pagedata->setValue("Data.List.Options.x" , 1)
		if ((-e "$dir_of_list/mimeremove") || (-e "$dir_of_list/mimereject"));

	for ($i=0; $i<9; $i++) {
		unless (($i eq 1) || ($i eq 2)) {
			$state = ($options =~ /$i (?:'(.+?)')/);
			unless ($state) {
				if ($i eq 0) {
					$value = 'mainlist@' . $DEFAULT_HOST;
				} elsif ($i eq 3) {
					$value = 'from_address@domain.org';
				} elsif ($i eq 4) {
					$value = '-t24 -m30 -k64';
				} elsif ($i eq 5) {
					$value = 'owner_address@domain.org';
				} elsif ($i eq 6) {
					$value = 'host:port:user:password:database:table';
				} elsif ($i eq 7) {
					$value = "$dir_of_list/mod";
				} elsif ($i eq 8) {
					$value = "$dir_of_list/mod";
				}
			} else {
				# use the configured value (extracted by the pattern matching for 'state')
				$value = $1;
			}
			$pagedata->setValue("Data.List.Settings." . $i . ".value", $value);
			$pagedata->setValue("Data.List.Settings." . $i . ".state", $state ? 1 : 0);
		}
	}
}

# ---------------------------------------------------------------------------

sub check_filename()
{
	my $filename = shift;
	return ($filename =~ m/[^\w-]/) ? (1==0) : (0==0);
}

# ---------------------------------------------------------------------------

sub get_list_part
# return the name of the part list (deny, allow, mod, digest or '')
{
	$q->param('part') =~ m/^(allow|deny|digest|mod)$/;
	return $1;
}

# ---------------------------------------------------------------------------

sub delete_list {
	# Delete a list ...

	# Fixes a bug from the previous version ... when the .qmail file has a
	# different name to the list. We use outlocal to handle vhosts ...
	my ($list, $listaddress, $listadd); 
	$list = new Mail::Ezmlm("$LIST_DIR/" . $q->param('list'));
	if ($listadd = $list->getpart('outlocal')) {
		chomp($listadd);
	} else {
		$listadd = $q->param('list');
	}
	$listaddress = $1 if ($listadd =~ /-?(\w+)$/);

	if ($UNSAFE_RM == 0) {
		# This doesn't actually delete anything ... It just moves them so that
		# they don't show up. That way they can always be recovered by a helpful
		# sysadmin should he/she be in the mood :)

		my ($oldfile); $oldfile = "$LIST_DIR/" . $q->param('list');
		my ($newfile); $newfile = "$LIST_DIR/." . $q->param('list'); 
		unless (move($oldfile, $newfile)) {
			$warning = 'SafeRemoveRenameDirFailed';
			return (1==0);
		}
		mkdir "$HOME_DIR/deleted.qmail", 0700 if(!-e "$HOME_DIR/deleted.qmail");

		unless (opendir(DIR, "$HOME_DIR")) {
			$warning = 'DotQmailDirAccessDenied';
			return (1==0);
		}
		my @files = map { "$HOME_DIR/$1" if m{^(\.qmail.+)$} } grep { /^\.qmail-$listaddress/ } readdir DIR;
		closedir DIR;
		foreach (@files) {
			unless (move($_, "$HOME_DIR/deleted.qmail/")) {
				$warning = 'SafeRemoveMoveDotQmailFailed';
				return (1==0); 
			}
		}
		warn "List '$oldfile' moved (deleted)";   
	} else {
		# This, however, does DELETE the list. I don't like the idea, but I was
		# asked to include support for it so ...
		unless (rmtree("$LIST_DIR/" . $q->param('list'))) {
			$warning = 'UnsafeRemoveListDirFailed';
			return (1==0);
		}
		opendir(DIR, "$HOME_DIR") or die "Unable to get directory listing: $!";
		my @files = map { "$HOME_DIR/$1" if m{^(\.qmail.+)$} } grep { /^\.qmail-$listaddress/ } readdir DIR;
		closedir DIR;
		if (unlink(@files) <= 0) {
			$warning = 'UnsafeRemoveDotQmailFailed';
			return (1==0);
		}
		warn "List '$list->thislist()' deleted";
	}
	$q->param(-name=>'list', -values=>'');
}

# ------------------------------------------------------------------------
sub untaint {

   $DEFAULT_HOST = $1 if $DEFAULT_HOST =~ /^([\w\d\.-]+)$/;
   
   # Go through all the CGI input and make sure it is not tainted. Log any
   # tainted data that we come accross ... See the perlsec(1) man page ...

   my (@params, $i, $param);
   @params = $q->param;
   
   foreach $i (0 .. $#params) {
      my(@values);
      next if($params[$i] eq 'mailaddressfile');
      foreach $param ($q->param($params[$i])) {
         next if $param eq '';
         if ($param =~ /^([#-\@\w\.\/\[\]\:\n\r\>\< _]+)$/) {
            push @values, $1;
         } else {
            warn "Tainted input in '$params[$i]': " . $q->param($params[$i]); 
         }
         $q->param(-name=>$params[$i], -values=>\@values);
      }
   } 

	# special stuff

	# check the list name
	if (($q->param('list') =~ /[^\w-]/) && ($q->param('action') !~ /^list_create_(do|ask)$/)) {
		$warning = 'InvalidListName' if ($warning eq '');
		$q->param(-name=>'list', -values=>'');
	}
	
}

# ------------------------------------------------------------------------

sub check_permission_for_action {
   # test if the user is allowed to modify the choosen list or to create an new one
   # the user would still be allowed to fill out the create-form (however he got there),
   # but the final creation is omitted

   my $ret;
   if ($action eq 'list_create_ask' || $action eq 'list_create_do') {
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

	my ($address, $list, $part, @addresses, $count);
	$list = new Mail::Ezmlm("$LIST_DIR/" . $q->param('list'));
	$part = &get_list_part();


	if (($q->param('mailaddressfile')) && ($FILE_UPLOAD)) {
		# Sanity check
		my $fileinfo = $q->uploadInfo($q->param('mailaddressfile'));
		my $filetype = $fileinfo->{'Content-Type'};
		unless($filetype =~ m{^text/}) {
			$warning = 'InvalidFileFormat';
			return (1==0);
		}

		# Handle file uploads of addresses
		my($fh) = $q->param('mailaddressfile');
		while (<$fh>) {
			next if (/^\s*$/ or /^#/); # blank, comments
			next unless ( /(\w[\-\w_\.]*)@(\w[\-\w_\.]+)/ ); # email address ...
			chomp();
			push @addresses, "$_";
		}
	}
      
	# User typed in an address
	if ($q->param('mailaddress_add') ne '') {

		$address = $q->param('mailaddress_add');
		$address .= $DEFAULT_HOST if ($q->param('mailaddress_add') =~ /\@$/);

		# untaint
		if ($address =~ /(\w[\-\w_\.]*)@(\w[\-\w_\.]+)/) {
			push @addresses, "$1\@$2";
		  } else {
			warn "invalid address to add: $address to $part";
			$warning = 'AddAddress';
			return (1==0);
		  }

	}
   
   $count = 0;
   foreach $address (@addresses) {

      my($add) = Mail::Address->parse($address);
      if(defined($add->name()) && $PRETTY_NAMES) {
         my(%pretty);
         tie %pretty, "DB_File", "$LIST_DIR/" . $q->param('list') . "/webnames";
         $pretty{$add->address()} = $add->name();
         untie %pretty;
      }

		if ($list->issub($add->address(), $part)) {
			$warning = 'AddAddress';
		} else {
			$warning = 'AddAddress' unless ($list->sub($add->address(), $part));
		}
		$count++;
	}
}

# ------------------------------------------------------------------------

sub delete_address {
   # Delete an address from a list ...

   my ($list, @address);
   $list = new Mail::Ezmlm("$LIST_DIR/" . $q->param('list'));
   my $part = &get_list_part();
   return (1==0) if ($q->param('mailaddress_del') eq '');

   @address = $q->param('mailaddress_del');

   if ($list->unsub(@address, $part) != 1) {
      $warning = 'DeleteAddress';
	  return (1==0);
   }
   
   if($PRETTY_NAMES) {
      my(%pretty, $add);
      tie %pretty, "DB_File", "$LIST_DIR/" . $q->param('list') . "/webnames";
      foreach $add (@address) {
         delete $pretty{$add};
      }
      untie %pretty;
   }

}

# ------------------------------------------------------------------------

sub set_pagedata4part_list {
   my($part) = @_;
   # Deal with list parts ....

   my ($i, $list, $listaddress,);
   
   # Work out the address of this list ...
   $list = new Mail::Ezmlm("$LIST_DIR/" . $q->param('list'));
   $listaddress = &this_listaddress();

   $pagedata->setValue("Data.List.PartType", "$part");

   if($part eq 'mod') {
      # do we store things in different directories?
      my $config = $list->getconfig;
	  # empty values represent default settings - everything else is considered as evil :)
      my($postpath) = $config =~ m{7\s*'([^']+)'};
      my($subpath) = $config =~ m{8\s*'([^']+)'};
      my($remotepath) = $config =~ m{9\s*'([^']+)'};
      
      $pagedata->setValue("Data.List.hasPostMod", ($list->ismodpost)? 1 : 0);
      $pagedata->setValue("Data.List.PostModPath", "$postpath");

      $pagedata->setValue("Data.List.hasSubMod", ($list->ismodsub)? 1 : 0);
      $pagedata->setValue("Data.List.SubModPath", "$subpath");

      $pagedata->setValue("Data.List.hasRemoteAdmin", ($list->isremote)? 1 : 0);
      $pagedata->setValue("Data.List.RemoteAdminPath", "$remotepath");
   }
}

# ------------------------------------------------------------------------

sub create_list {
	# Create a list according to user selections ...

	# Check if the list directory exists and create if necessary ...
	unless ((-e $LIST_DIR) || (mkdir $LIST_DIR, 0700)) {
		warn "Unable to create directory ($LIST_DIR): $!";
		$error = 'ListDirUnavailable';
		return (1==0);
	}

	my ($qmail, $listname, $options, $i);

	# Some taint checking ...
	$qmail = $1 if $q->param('inlocal') =~ /(?:$USER-)?([^\<\>\\\/\s]+)$/;
	$listname = $q->param('list');
	if ($listname =~ m/[^\w\.-]/) {
		$warning = 'InvalidListName';
		return (1==0);
   	}

	# Sanity Checks ...
	if ($listname eq '') {
		$warning = 'EmptyListName';
		return (1==0);
   	}
	if (($listname =~ m/^ALL$/i) || ($listname =~ m/^ALLOW_CREATE$/i)) {
		$warning = 'ReservedListName';
		return (1==0);
   	}
	if ($qmail eq '') {
		$warning = 'InvalidLocalPart';
		return (1==0);
   	}
	if(-e ("$LIST_DIR/$listname/lock") || -e ("$HOME_DIR/.qmail-$qmail")) {
		$warning = 'ListAlreadyExists';
		return (1==0);
	}

	$options = &extract_options_from_params();

	my($list) = new Mail::Ezmlm;

	unless ($list->make(-dir=>"$LIST_DIR/$listname",
				-qmail=>"$HOME_DIR/.qmail-$qmail",
				-name=>$q->param('inlocal'),
				-host=>$q->param('inhost'),
				-switches=>$options,
				-user=>$USER)
	) {
		# fatal error
		$customWarning = $list->errmsg();
		return (1==0);
	}

	# handle MySQL stuff
	if(defined($q->param('setting_state_6')) && $options =~ m/-6\s+/) {
		$customWarning = $list->errmsg() unless($list->createsql());
	}
   
	# no error returned - just a warning
	$warning = 'WebUsersUpdate' unless (&update_webusers());

	return (0==0);
}

# ------------------------------------------------------------------------

sub extract_options_from_params()
{
	# Work out the command line options ...
	my ($options, $avail_options, $settings, $avail_settings, $i);
	my ($listname, $list, $old_options, $state, $old_key);

	# NOTE: we have to define _every_ (even unchanged) setting
	# as ezmlm-make removes any undefined value

	$listname = $q->param('list');
	$list = new Mail::Ezmlm("$LIST_DIR/$listname");
	$old_options = $list->getconfig();

	################ options ################
	$i = 0;
	$old_key = substr($old_options,$i,1);
	$avail_options = $q->param('options_available');
	# parse the first part of the options string
	while ($old_key =~ m/\w/) {
		# scan the first part of the options string for lower case letters
		if ($avail_options =~ m/$old_key/i) {
			my $form_var_name = "option_" . lc($old_key);
			# this option was visible for the user
			if (defined($q->param($form_var_name))) {
				$options .= lc($old_key);
			} else {
				$options .= uc($old_key);
			}
		} elsif ("cevz" =~ m/$old_key/i) {
			# ignore invalid settings (the output of "getconfig" is really weird!)
		} else {
			# import the previous set option
			$options .= $old_key;
		}
		$i++;
		$old_key = substr($old_options,$i,1);
	}


	############### settings ################
	$avail_settings = $q->param('settings_available');
	for ($i=0; $i<9; $i++) {
		if ($avail_settings =~ m/$i/) {
			# this setting was visible for the user
			$options .= " -$i '" . $q->param("setting_value_$i") . "'"
				if (defined($q->param("setting_state_$i")));
		} else {
			# import the previous setting
			$state = ($old_options =~ /$i (?:'(.+?)')/);
			$options .= " -$i '$1'" if ($state);
		}
	}

	return $options;
}

# ------------------------------------------------------------------------

sub update_config {
	# Save the new user entered config ...
   
	my ($list, $options, @inlocal, @inhost, $dir_of_list);
	my ($old_msgsize);

	$list = new Mail::Ezmlm("$LIST_DIR/" . $q->param('list'));
	$dir_of_list = $LIST_DIR . '/' . $q->param('list');

	$options = &extract_options_from_params();

	# save the settings, that are generally overwritten by ezmlm-make :(((
	# good candidates are: msgsize, inhost, inlocal and outhost
	# maybe there are some others?
	$old_msgsize = $list->getpart('msgsize');

	# Actually update the list ...
	unless($list->update($options)) {
		$warning = 'UpdateConfig';
		return (1==0);
	}

	# update trailing text
	# remove old one if the checkbox was not active
	if (defined($q->param('trailing_text'))) {
		if (defined($q->param('option_t'))) {
			$list->setpart('text/trailer', $q->param('trailing_text'));
		} else {
			unlink("$dir_of_list/text/trailer");
		}
	}

	# update prefix text
	# remove old one if the checkbox was not active
	if (defined($q->param('prefix'))) {
		if (defined($q->param('option_f'))) {
			$list->setpart('prefix', $q->param('prefix'))
		} else {
			unlink("$dir_of_list/prefix");
		}
	}

	# update mimeremove
	# remove old one if the checkbox was not active
	if (defined($q->param('mimeremove'))) {
		if (defined($q->param('option_x'))) {
			$list->setpart('mimeremove', $q->param('mimeremove'))
		} else {
			unlink("$dir_of_list/mimeremove");
		}
	}

	# update mimereject
	# remove old one if the checkbox was not active
	if (defined($q->param('mimereject'))) {
		if (defined($q->param('option_x'))) {
			$list->setpart('mimereject', $q->param('mimereject'))
		} else {
			unlink("$dir_of_list/mimereject");
		}
	}

	# Update headeradd and headerremove if these options were visible
	$list->setpart('headeradd', $q->param('headeradd'))
		if (defined($q->param('headeradd')));
	$list->setpart('headerremove', $q->param('headerremove'))
		if (defined($q->param('headerremove')));
	
	if (defined($q->param('msgsize_max_value')) && defined($q->param('msgsize_min_value'))) {
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
	
	unless (&update_webusers()) {
		$warning = 'WebUsersUpdate';
		return (1==0);
	}

	return (0==0);
}

# ------------------------------------------------------------------------

sub update_webusers {
	# replace existing webusers-line or add a new one

	# return if there is no webusers entry
	return (0==0) unless defined($q->param('webusers'));

	# Back up web users file
	my $temp_file;
	my $fh;
	# generate a temporary filename (as suggested by the Perl Cookbook)
	do { $temp_file = tmpnam() }
	    until $fh = IO::File->new($temp_file, O_RDWR|O_CREAT|O_EXCL);
	close $fh; 
	unless (open(TMP, ">$temp_file")) {
		warn "could not open a temporary file";
		return (1==0);;
	}
	open(WU, "<$WEBUSERS_FILE");
	while(<WU>) { print TMP; }
	close WU; close TMP;

	my $matched = 0;
	my $listname = $q->param('list');
	my $webusers_filtered = $q->param('webusers');
	# remove any insecure characters (e.g. a line break :))
	$webusers_filtered =~ s/[^\w_,-]/ /gs;
	open(TMP, "<$temp_file");
	unless (open(WU, ">$WEBUSERS_FILE")) {
		warn "the webusers file ($WEBUSERS_FILE) is not writable";
		return (0==1);
	}
	while(<TMP>) {
		if ($_ =~ m/^$listname\s*:/i) {
			print WU $listname . ': ' . $webusers_filtered . "\n" if ($matched == 0);
			$matched = 1;
		} else {
			print WU $_;
		}
	}
	# append the line, if there was no matching line found before
	print WU $listname . ': ' . $webusers_filtered . "\n" if ($matched == 0);
	
	close TMP; close WU;
	unlink "$temp_file";
}

# ------------------------------------------------------------------------

sub this_listaddress {
   # Work out the address of this list ... Used often so put in its own subroutine ...
   
   my ($list, $listaddress);
   $list = new Mail::Ezmlm("$LIST_DIR/" . $q->param('list'));
   chomp($listaddress = $list->getpart('outlocal'));
   $listaddress .= '@';
   chomp($listaddress .= $list->getpart('outhost'));
   return $listaddress;
}

# ------------------------------------------------------------------------

sub save_text {
   # Save new text in DIR/text ...

   my ($list) = new Mail::Ezmlm("$LIST_DIR/" . $q->param('list'));
   my ($content) = $q->param('content');
   # TODO: is "utf8" instead of "utf-8" correct?
   from_to($content,'utf8',$TEXT_ENCODE);	# by ooyama for multibyte
   unless ($list->setpart("text/" . $q->param('file'), $content)) {
		$warning = 'SaveFile';
		return (1==0);
   }
}   

# ------------------------------------------------------------------------

sub webauth {
	my $listname = shift;
   
	# Check if webusers file exists - if not, then access is granted
	return (0==0) if (! -e "$WEBUSERS_FILE");

	# if there was no user authentication, then everything is allowed
	return (0==0) if ($ENV{'REMOTE_USER'} eq '');

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
			# the following line should be synchronized with the webauth_create_allowed sub
			if (/^[^:]*:(|.*[\s,])($ENV{'REMOTE_USER'}|ALL)(,|\s|$)/m) {
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

	# Check if we were called with the deprecated argument "-c" (allow to create lists)
	return (0==0) if (defined($opt_c));

	# if there was no user authentication, then everything is allowed
	return (0==0) if ($ENV{'REMOTE_USER'} eq '');

	# Check if webusers file exists - if not, then access is granted
	return (0==0) if (! -e "$WEBUSERS_FILE");

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
			if (/[:\s,]($ENV{'REMOTE_USER'}|(ALL))(,|\s|$)/m) {
				close USERS;
				return (0==0);
			}
		}   
	}
	close USERS;
	return (1==0);
}

# ---------------------------------------------------------------------------

sub pretty_names {
   return undef unless($PRETTY_NAMES);
   my (%pretty, %prettymem);
   tie %pretty, "DB_File", "$LIST_DIR/" . $q->param('list') . '/webnames';
   %prettymem = %pretty;
   untie %pretty;   
   
   return \%prettymem;
}

# -------------------------------------------------------------------------
sub rmtree {
   # A subroutine to recursively delete a directory (like rm -f).
   # Based on the one in the perl cookbook :)
    
   use File::Find qw(finddepth);
   File::Find::finddepth sub {
         # assume that File::Find::name is secure since it only uses data we pass it
         my($name) = $File::Find::name =~ m{^(.+)$}; 
         
         if (!-l && -d _) {
            rmdir($name)  or warn "couldn't rmdir $name: $!";
         } else {
            unlink($name) or warn "couldn't unlink $name: $!";
         }
      }, @_;
      1;                                   
}

# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
# End of ezmlm-web.cgi v2.3
# ------------------------------------------------------------------------
__END__

=head1 NAME

ezmlm-web - A web configuration interface to ezmlm mailing lists

=head1 SYNOPSIS

ezmlm-web [B<-c>] [B<-C> E<lt>F<config file>E<gt>] [B<-d> E<lt>F<list directory>E<gt>]

=head1 DESCRIPTION

=over 4

=item B<-C> Specify an alternate configuration file given as F<config file>
If not specified, ezmlm-web checks first in the users home directory, then in
F</etc/ezmlm> and then the current directory

=item B<-d> Specify an alternate directory where lists live. This is now
depreciated in favour of using a custom ezmlmwebrc, but is left for backward
compatibility.

=back

=head1 SUID WRAPPER

C<#include stdio.h>

C<void main (void) {>
   C</* call ezmlm-web */>
   C<system("/path/to/ezmlm-web.cgi");>
C<}>


=head1 DOCUMENTATION/CONFIGURATION

   Please refer to the example ezmlmwebrc which is well commented, and
   to the README file in this distribution.

=head1 FILES

F<~/.ezmlmwebrc>
F</etc/ezmlm/ezmlmwebrc>
F<./ezmlmwebrc>

=head1 AUTHOR

 Guy Antony Halse <guy-ezmlm@rucus.ru.ac.za>
 Lars Kruse <ezmlm-web@sumpfralle.de>

=head1 BUGS

 None known yet. Please report bugs to the author.

=head1 S<SEE ALSO>
 
 ezmlm(5), ezmlm-cgi(1), Mail::Ezmlm(3)
   
 https://systemausfall.org/toolforge/ezmlm-web
 http://rucus.ru.ac.za/~guy/ezmlm/
 http://www.ezmlm.org/
 http://www.qmail.org/
