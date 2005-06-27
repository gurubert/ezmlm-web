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

# Modules to include
use strict;
use Getopt::Std;
use ClearSilver;
use Mail::Ezmlm;
use Mail::Address;
use File::Copy;
use DB_File;
use CGI;

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
my @tmp = getpwuid($>); my $USER=$tmp[0]; 

# use strict is a good thing++

use vars qw[$HOME_DIR]; $HOME_DIR=$tmp[7];
use vars qw[$DEFAULT_OPTIONS %EZMLM_LABELS $UNSAFE_RM $ALIAS_USER $LIST_DIR];
use vars qw[$QMAIL_BASE $EZMLM_CGI_RC $EZMLM_CGI_URL $HTML_BGCOLOR $PRETTY_NAMES];
use vars qw[%HELPER $HELP_ICON_URL $HTML_HEADER $HTML_FOOTER $HTML_TEXT $HTML_LINK];
use vars qw[%BUTTON %LANGUAGE $HTML_VLINK $HTML_TITLE $FILE_UPLOAD $WEBUSERS_FILE];
use vars qw[$HTML_CSS_FILE $TEMPLATE_DIR $LANGUAGE_DIR];

# pagedata contains the hdf tree for clearsilver
# pagename refers to the template file that should be used
use vars qw[$pagedata $pagename];

# Get user configuration stuff
if(defined($opt_C)) {
   require "$opt_C"; # Command Line
} elsif(-e "$HOME_DIR/.ezmlmwebrc") {
   require "$HOME_DIR/.ezmlmwebrc"; # User
} elsif(-e "/etc/ezmlm/ezmlmwebrc") {
   require "/etc/ezmlm/ezmlmwebrc"; # System
} elsif(-e "./ezmlmwebrc") {
   require "./ezmlmwebrc"; # Install
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

# Work out default domain name from qmail (for David Summers)
my($DEFAULT_HOST);
open (GETHOST, "<$QMAIL_BASE/me") || open (GETHOST, "<$QMAIL_BASE/defaultdomain") || die "Unable to read $QMAIL_BASE/me: $!";
chomp($DEFAULT_HOST = <GETHOST>);
close GETHOST;

# Untaint form input ...
&untaint;

# redirect must come before headers are printed
if(defined($q->param('action')) && $q->param('action') eq 'web_archive') {
   print $q->redirect(&ezmlmcgirc);
   exit;
}

my $pagedata = load_hdf();

# check permissions
&check_permission_for_action == 0 || &error_die($pagedata->getValue("Lang.ErrorMessages.Forbidden", "Error: you are not allowed to do this!"));

&set_pagedata();

my $action = $q->param('action');

# This is where we decide what to do, depending on the form state and the
# users chosen course of action ...
if ($action eq '' || $action eq 'select_list') {
	# Default action. Present a list of available lists to the user ...
	$pagename = 'select_list';
} elsif ($action eq 'create_list') {
	# Create a new list ...
	$pagename = 'create_list';
} elsif ($action eq 'list_subscribers') {
	# display list (or part list) subscribers
	&error_die("no list selected") unless (defined($q->param('list')));
	$pagename = 'list_subscribers';
} elsif ($action eq 'delete_address') {
	# Delete a subscriber ...
	&delete_address();
	$pagename = 'list_subscribers';
} elsif ($action eq 'add_address') {
	# Add a subscriber ...
	&add_address();
	$pagename = 'list_subscribers';
} elsif ($action eq 'list_config') {
	# Edit the config ...
	$pagename = 'list_config';
} elsif ($action eq 'list_delete_ask') {
	# Confirm list removal
	$pagename = 'confirm_delete';
} elsif ($action eq 'list_delete_do') {
	# User really wants to delete a list ...
	&delete_list if($q->param('confirm') eq 'yes'); # Do it ...
	$pagename = 'select_list';
} elsif ($action eq 'list_create_ask') {
	# User wants to create a list ...
         $pagename = 'create_list';
} elsif ($action eq 'create_list_do') {
	# create the new list
	if (&create_list) {
		# Return if list creation is unsuccessful ...
		$pagename = 'create_list';
	} else {
		# Else choose a list ...
		$pagename = 'select_list';
	}
} elsif ($action eq 'list_config_ask') {
	# User updates configuration ...
	$pagename = 'list_config';
} elsif ($action eq 'list_config_do') {
	# Save current settings ...
	&update_config;
	$pagename = 'list_subscribers';
} elsif ($action eq 'list_textfiles') {
	# Edit DIR/text ...
	$pagename = 'list_textfiles';
} elsif ($action eq 'edit_file_ask') {
	$pagename = 'edit_text';
} elsif ($action eq 'edit_text_do') {   
	# User wants to save a new version of something in DIR/text ...
	&save_text();
	$pagename = 'list_textfiles';
} else {
	&error_die('unknown_action');
}

# Print page and exit :) ...
&output_page;
exit;


# =========================================================================

sub load_hdf {
	# initialize the data for clearsilver
	my $hdf = ClearSilver::HDF->new();

	# TODO: respect LANGUAGE_DIR and LANGUAGE
	$hdf->readFile($LANGUAGE_DIR . "/en.hdf");

	# TODO: check for existence
	$hdf->setValue("TemplateDir", "$TEMPLATE_DIR/");
	$hdf->setValue("LanguageDir", "$LANGUAGE_DIR/");
	$hdf->setValue("ScriptName", $ENV{'SCRIPT_NAME'});
	$hdf->setValue("Stylesheet", "$HTML_CSS_FILE");
	$hdf->setValue("HelpIconURL", "$HELP_ICON_URL");

	return $hdf;
}


sub output_page {
	# Print the page

	&error_die("invalid action - ask the administrator for help") if ($pagename eq '');

	my $pagefile = $TEMPLATE_DIR . "/" . $pagename . ".cs";
	die "template ($pagefile) not found!" unless (-e "$pagefile");

	# print http header
	print "Content-Type: text/html\n\n";

	my $cs = ClearSilver::CS->new($pagedata);
	$cs->parseFile($TEMPLATE_DIR . '/macros.cs');
	$cs->parseFile($TEMPLATE_DIR . '/header.cs');
	$cs->parseFile($TEMPLATE_DIR . '/' . $pagename . '.cs');
	$cs->parseFile($TEMPLATE_DIR . '/footer.cs');

	print $cs->render();
}


sub set_pagedata()
{
   my (@lists, @files, $i, $item);

   # Read the list directory for mailing lists.
   opendir DIR, $LIST_DIR || &error_die($pagedata->getValue("Lang.ErrorMessages.ListDirAccessDenied", "Unable to read") . " $LIST_DIR");
   @files = grep !/^\./, readdir DIR; 
   closedir DIR;

   # Check that they actually are lists and add good ones to pagedata ...
   my $num = 0;
   foreach $i (0 .. $#files) {
      if ((-e "$LIST_DIR/$files[$i]/lock") && (&webauth($files[$i]) == 0)) {
         $num++;
         $pagedata->setValue("Data.Lists." . $num, "$files[$i]");
      }
   }
   $pagedata->setValue("Data.ListsCount", "$num");


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
   $pagedata->setValue("Data.Modules.mySQL", ($Mail::Ezmlm::MYSQL_BASE)? 1 : 0);
   

   # permissions
   $pagedata->setValue("Data.Permissions.Create", (&webauth_create_allowed == 0)? 1 : 0 );
   $pagedata->setValue("Data.Permissions.FileUpload", ($FILE_UPLOAD)? 1 : 0);


   # display webuser textfield?
   $pagedata->setValue("Data.WebUser.show", (-e "$WEBUSERS_FILE")? 1 : 0);
   # default username for webuser file
   $pagedata->setValue("Data.WebUser.UserName", $ENV{'REMOTE_USER'}||'ALL');
}


sub set_pagedata4list
{
	my $part_type = shift;
	my ($list, $listname);
	my ($i, $item, @files);

	$listname = $q->param('list');
	
	# Work out the address of this list ...
	$list = new Mail::Ezmlm("$LIST_DIR/$listname");

	$pagedata->setValue("Data.List.Name", "$listname");
	$pagedata->setValue("Data.List.Address", &this_listaddress);
	&set_pagedata4part_list($part_type) if ($part_type ne '');

	$i = 0;
	my $item;
	# TODO: use "pretty" output style for visible mail address
	foreach $item ($list->subscribers($part_type)) {
		$pagedata->setValue("Data.List.Subscribers." . $i, "$item");
		$i++;
	}
	$pagedata->setValue("Data.List.SubscribersCount", "$i");

	$pagedata->setValue("Data.ConfigAvail.Extras", 1) if($list->ismodpost || $list->ismodsub || $list->isremote || $list->isdeny || $list->isallow || $list->isdigest);
	$pagedata->setValue("Data.ConfigAvail.Moderation", 1) if ($list->ismodpost || $list->ismodsub || $list->isremote);
	$pagedata->setValue("Data.ConfigAvail.DenyList", 1) if ($list->isdeny);
	$pagedata->setValue("Data.ConfigAvail.AllowList", 1) if ($list->isallow);
	$pagedata->setValue("Data.ConfigAvail.Digest", 1) if ($list->isdigest);
	$pagedata->setValue("Data.ConfigAvail.WebArchive", 1) if(&ezmlmcgirc);

	# Get the contents of the headeradd, headerremove, mimeremove and prefix files
	$pagedata->setValue("Data.List.Prefix", $list->getpart('prefix'));
	$item = $list->getpart('headeradd');
	$pagedata->setValue("Data.List.HeaderAdd", "$item");
	$item = $list->getpart('headerremove');
	$pagedata->setValue("Data.List.HeaderRemove", "$item");
	$item = $list->getpart('mimeremove');
	$pagedata->setValue("Data.List.MimeRemove", "$item");

	# TODO: this is definitely ugly - create a new sub!
	if(open(WEBUSER, "<$WEBUSERS_FILE")) {
	      my($webusers);
	      while(<WEBUSER>) {
		 last if (($webusers) = m{^$listname\s*\:\s*(.+)$});
	      }
	      close WEBUSER;
	      $webusers ||= $ENV{'REMOTE_USER'} || 'ALL';

	      $pagedata->setValue("Data.List.WebUsers", "$webusers");
	}

	# get the names of the textfiles of this list
	{
		my($listDir);
		$listDir = $LIST_DIR . '/' . $q->param('list');

		# Read the list directory for text ...
		opendir DIR, "$listDir/text" || &error_die($pagedata->getValue("Lang.ErrorMessages.TextDirAccessDenied","Unable to read DIR/text:") . " $listDir/text");
		@files = grep !/^\./, readdir DIR; 
		closedir DIR;

		# TODO: find a better way to set a list ...
		$i = 0;
		my $item;
		foreach $item (@files) {
			$pagedata->setValue("Data.Files." . $i, "$item");
			$i++;
		}
		$pagedata->setValue("Data.FilesCount", "$i");

		# text file specified?
		if ($q->param('file') ne '')
		{
			my ($content);
			$content = $list->getpart("text/" . $q->param('file'));
			$pagedata->setValue("Data.File.Name", $q->param('file'));
			$pagedata->setValue("Data.File.Content", "$content");
		}
	}
	&set_pagedata4options($list->getconfig);   
}

# ---------------------------------------------------------------------------

sub set_pagedata4options {
   my($opts) = shift;
   my($i, $j);
 
   # TODO: remove when migration to cs is done
   $j = 0;
   # convert EZMLM_LABELS to hdf-language values
   foreach $i (grep {/\D/} keys %EZMLM_LABELS) {
	$pagedata->setValue("Data.ListOptions." . $i . ".name", "$i");
	$pagedata->setValue("Data.ListOptions." . $i . ".short", "$EZMLM_LABELS{$i}[0]");
	$pagedata->setValue("Data.ListOptions." . $i . ".long", "$EZMLM_LABELS{$i}[1]");
	$pagedata->setValue("Data.ListOptions." . $i . ".state", ($opts =~ /^\w*$i\w*\s*/)? 1 : 0);
	$j++;
   }
   $pagedata->setValue("Data.ListOptionsCount", "$j");

   $j = 0;
   my $state;
   # convert EZMLM_LABELS to hdf-language values
   foreach $i (grep {/\d/} keys %EZMLM_LABELS) {
	$pagedata->setValue("Data.ListSettings." . $i . ".name", "$i");
	$pagedata->setValue("Data.ListSettings." . $i . ".short", "$EZMLM_LABELS{$i}[0]");
	$pagedata->setValue("Data.ListSettings." . $i . ".long", "$EZMLM_LABELS{$i}[1]");
	#$pagedata->setValue("Data.ListSettings." . $i . ".state", ($opts =~ /$i (?:'(.+?)')/)? 1 : 0);
	$state = ($opts =~ /$i (?:'(.+?)')/);
	$pagedata->setValue("Data.ListSettings." . $i . ".state", $state ? 1 : 0);
	$pagedata->setValue("Data.ListSettings." . $i . ".value", $state ? $1 : "$EZMLM_LABELS{$i}[2]");
	$j++;
   }
   $pagedata->setValue("Data.ListSettingsCount", "$j");
}

# ---------------------------------------------------------------------------

sub get_list_part
# return the name of the part list (deny, allow, mod, digest or '')
{
	return $q->param('part') if (defined($q->param('part')));

	my $action = $q->param('action');

	# moderators list?
	return 'mod' if ($action eq 'part_mod');

	# deny list?
	return 'deny' if ($action eq 'part_deny');

	# allow list?
	return 'allow' if ($action eq 'part_allow');

	# digest list?
	return 'digest' if ($action eq 'part_digest');
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
      # sysadmin should he be in the mood :)

      my ($oldfile); $oldfile = "$LIST_DIR/" . $q->param('list');
      my ($newfile); $newfile = "$LIST_DIR/." . $q->param('list'); 
      move($oldfile, $newfile) or error_die($pagedata->getValue("Lang.ErrorMessages.SafeRemoveRenameDirFailed","Unable to rename list:") . " ($oldfile -> $newfile)");
      mkdir "$HOME_DIR/deleted.qmail", 0700 if(!-e "$HOME_DIR/deleted.qmail");

      opendir(DIR, "$HOME_DIR") or &error_die($pagedata->getValue("Lang.ErrorMessages.DotQmailDirAccessDenied","Unable to get directory listing:") . " $HOME_DIR");
      my @files = map { "$HOME_DIR/$1" if m{^(\.qmail.+)$} } grep { /^\.qmail-$listaddress/ } readdir DIR;
      closedir DIR;
      foreach (@files) {
         unless (move($_, "$HOME_DIR/deleted.qmail/")) {
            &error_die($pagedata->getValue("Lang.ErrorMessages.SafeRemoveMoveDotQmailFailed", "Unable to move .qmail files:") . " ($_ -> $HOME_DIR/deleted.qmail)"); 
         }
      }
      warn "List '$oldfile' moved (deleted)";   
   } else {
      # This, however, does DELETE the list. I don't like the idea, but I was
      # asked to include support for it so ...
      if (!rmtree("$LIST_DIR/" . $q->param('list'))) {
         &error_die($pagedata->getValue("Lang.ErrorMessages.UnsafeRemoveListDirFailed", "Unable to delete list:"). " $LIST_DIR/" . $q->param('list'));
      }
      opendir(DIR, "$HOME_DIR") or die "Unable to get directory listing: $!";
      my @files = map { "$HOME_DIR/$1" if m{^(\.qmail.+)$} } grep { /^\.qmail-$listaddress/ } readdir DIR;
      closedir DIR;
      if (unlink(@files) <= 0) {
         &error_die($pagedata->getValue("Lang.ErrorMessages.UnsafeRemoveDotQmailFailed", "Unable to delete .qmail files:") . " $HOME_DIR");
      }
      warn "List '$list->thislist()' deleted";
   }   
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
      next if($params[$i] eq 'addfile');
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
   $q->import_names('Q');
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
	$ret = 0;
   }
   return $ret;
}

# ------------------------------------------------------------------------

sub add_address {
   # Add an address to a list ..

   my ($address, $list, $part, @addresses, $count);
   $list = new Mail::Ezmlm("$LIST_DIR/" . $q->param('list'));
   $part = &get_list_part();

   if (($q->param('addfile')) && ($FILE_UPLOAD)) {

      # Sanity check
      &error_die("File upload must be of type text/*") unless($q->uploadInfo($q->param('addfile'))->{'Content-Type'} =~ m{^text/});

      # Handle file uploads of addresses
      my($fh) = $q->param('addfile');
      return unless (defined($fh));
      while (<$fh>) {
	next if (/^\s*$/ or /^#/); # blank, comments
	next unless ( /(\w[\-\w_\.]*)@(\w[\-\w_\.]+)/ ); # email address ...
	chomp();
	push @addresses, "$_";
      }

   }
      
	# User typed in an address
	if ($q->param('addsubscriber') ne '') {

		$address = $q->param('addsubscriber');
		$address .= $DEFAULT_HOST if ($q->param('addsubscriber') =~ /\@$/);

		# untaint
		if ($address =~ /(\w[\-\w_\.]*)@(\w[\-\w_\.]+)/) {
			push @addresses, "$1\@$2";
		  } else {
			warn "this address ($address) is not valid!";
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
   
      if ($list->sub($add->address(), $part) != 1) {
         &error_die("Unable to subscribe to list: $!");
      }
      $count++;
   }

   $q->delete('addsubscriber');
}

# ------------------------------------------------------------------------

sub delete_address {
   # Delete an address from a list ...

   my ($list, @address);
   $list = new Mail::Ezmlm("$LIST_DIR/" . $q->param('list'));
   my $part = &get_list_part();
   return if ($q->param('delsubscriber') eq '');

   @address = $q->param('delsubscriber');

   if ($list->unsub(@address, $part) != 1) {
      &error_die("Unable to unsubscribe from list $list: $!");
   }
   
   if($PRETTY_NAMES) {
      my(%pretty, $add);
      tie %pretty, "DB_File", "$LIST_DIR/" . $q->param('list') . "/webnames";
      foreach $add (@address) {
         delete $pretty{$add};
      }
      untie %pretty;
   }

   $q->delete('delsubscriber');
}

# ------------------------------------------------------------------------

sub set_pagedata4part_list {
   my($part) = @_;
   # Deal with list parts ....

   my ($i, $list, $listaddress,);
   
   $pagename = "list_subscribers";
   
   # Work out the address of this list ...
   $list = new Mail::Ezmlm("$LIST_DIR/" . $q->param('list'));
   $listaddress = &this_listaddress();

   $pagedata->setValue("Data.List.PartType", "$part");

   if($part eq 'mod') {
      # Lets know what is moderated :)

      $pagedata->setValue("Data.isModerated",1);
      
      # do we store things in different directories?
      my $config = $list->getconfig;
      my($postpath) = $config =~ m{7\s*'([^']+)'};
      my($subpath) = $config =~ m{8\s*'([^']+)'};
      my($remotepath) = $config =~ m{9\s*'([^']+)'};
      
      $pagedata->setValue("Data.isPostMod", ($list->ismodpost)? 1 : 0);
      $pagedata->setValue("Data.PostModPathWarn", "$postpath");

      $pagedata->setValue("Data.isSubMod", ($list->ismodsub)? 1 : 0);
      $pagedata->setValue("Data.SubModPathWarn", "$subpath");

      $pagedata->setValue("Data.isRemote", ($list->isremote)? 1 : 0);
      $pagedata->setValue("Data.RemotePathWarn", "$remotepath");
   }
}

# ------------------------------------------------------------------------

sub create_list {
   # Create a list according to user selections ...

   # Check the list directory exists and create if necessary ...
   if(!-e $LIST_DIR) {
      die "Unable to create directory ($LIST_DIR): $!" unless mkdir $LIST_DIR, 0700;
   }
   
   my ($qmail, $listname, $options, $i);
   
   # Some taint checking ...
   $qmail = $1 if $q->param('inlocal') =~ /(?:$USER-)?([^\<\>\\\/\s]+)$/;
   $listname = $q->param('list'); $listname =~ s/ /_/g; # In case some git tries to put a space in the file name

   # Sanity Checks ...
   return 1 if ($listname eq '' || $qmail eq '');
   if(-e ("$LIST_DIR/$listname/lock") || -e ("$HOME_DIR/.qmail-$qmail")) {
      &error_die("Can't create list '$listname', as it already exists");
      return 1;
   }
  
   # Work out the command line options
   foreach $i (grep {/\D/} keys %EZMLM_LABELS) {
      if (defined($q->param($i))) {
         $options .= $i;
      } else {
         $options .= uc($i);
      }
   }

   foreach $i (grep {/\d/} keys %EZMLM_LABELS) {
      if (defined($q->param($i))) {
         $options .= " -$i '" . $q->param("$i-value") . "'";
      }
   }

   my($list) = new Mail::Ezmlm;

   unless ($list->make(-dir=>"$LIST_DIR/$listname",
               -qmail=>"$HOME_DIR/.qmail-$qmail",
               -name=>$q->param('inlocal'),
               -host=>$q->param('inhost'),
               -switches=>$options,
               -user=>$USER)
   ) {
      &error_die('List creation failed' , $list->errmsg());
   }

   # handle MySQL stuff
   if($q->param('sql') && $options =~ m/-6\s+/) {
      unless($list->createsql()) {
         error_die('SQL table creation failed: ' , $list->errmsg());
      }
   }
   
   &update_webusers();

   return 0;
}

# ------------------------------------------------------------------------

sub update_config {
   # Save the new user entered config ...
   
   my ($list, $options, $i, @inlocal, @inhost);
   $list = new Mail::Ezmlm("$LIST_DIR/" . $q->param('list'));

   # Work out the command line options ...
   foreach $i (grep {/\D/} keys %EZMLM_LABELS) {
      if (defined($q->param($i))) {
         $options .= $i;
      } else {
         $options .= uc($i);
      }
   }

   foreach $i (grep {/\d/} keys %EZMLM_LABELS) {
      if (defined($q->param($i))) {
         $options .= " -$i '" . $q->param("$i-value") . "'";
      }
   }

   # Actually update the list ...
   unless($list->update($options)) {
      die "List update failed";
   }

   # Update headeradd, headerremove, mimeremove and prefix ...
   $list->setpart('headeradd', $q->param('headeradd'));
   $list->setpart('headerremove', $q->param('headerremove'));
   $list->setpart('mimeremove', $q->param('mimeremove')) if defined($q->param('mimeremove'));
   $list->setpart('prefix', $q->param('prefix')) if defined($q->param('prefix'));

   &update_webusers();
}

# ------------------------------------------------------------------------

sub update_webusers {
   # replace existing webusers-line or add a new one

   if($q->param('webusers')) {
      # Back up web users file
      open(TMP, ">/tmp/ezmlm-web.$$");
      open(WU, "<$WEBUSERS_FILE");
      while(<WU>) { print TMP; }
      close TMP; close WU;
      
      open(TMP, "</tmp/ezmlm-web.$$");
      open(WU, ">$WEBUSERS_FILE");
      while(<TMP>) {
		print WU unless (/^$Q::list\s*:/);
	}
	print WU $q->param('list') . ': ' . $q->param('webusers') . "\n";
      close TMP; close WU;
      unlink "/tmp/ezmlm-web.$$";
   }

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
   $list->setpart("text/" . $q->param('list'), $q->param('content'));
   
}   

# ------------------------------------------------------------------------

sub webauth {
   
   # Check if webusers file exists - if not, then access is granted
   return 0 if (! -e "$WEBUSERS_FILE");

   # Read authentication level from webusers file. Format of this file is
   # somewhat similar to the unix groups file
   my($listname) = @_;
   open (USERS, "<$WEBUSERS_FILE") || die "Unable to read webusers file ($WEBUSERS_FILE): $!";
   while(<USERS>) {
      if (/^($listname|ALL)\:/i) {
         if (/(\:\s*|,\s+)((?:$ENV{'REMOTE_USER'})|(?:ALL))\s*(,|$)/) {
            close USERS; return 0;
         }
      }   
   }
   close USERS;
   return 1;
}

# ---------------------------------------------------------------------------

sub webauth_create_allowed {

   # Check if we were called with the deprecated argument "-c" (allow to create lists)
   return 0 if (defined($opt_c));

   # Check if webusers file exists - if not, then access is granted
   return 0 if (! -e "$WEBUSERS_FILE");

   # Read create-permission from webusers file.
   # the special listname "ALLOW_CREATE" controls, who is allowed to do it
   open (USERS, "<$WEBUSERS_FILE") || die "Unable to read webusers file ($WEBUSERS_FILE): $!";
   while(<USERS>) {
      if (/^ALLOW_CREATE:/i) {
         if (/(\:\s*|,\s+)((?:$ENV{'REMOTE_USER'})|(?:ALL))\s*(,|$)/) {
            close USERS; return 0;
         }
      }   
   }
   close USERS;
   return 1;
}

# ---------------------------------------------------------------------------

sub ezmlmcgirc {
   my($listno);
   if(open(WWW, "<$EZMLM_CGI_RC")) {
      while(<WWW>) {
         last if (($listno) = m{(\d+)(\D)\d+\2$LIST_DIR/$Q::list\2});
      }
      close WWW;
      return "$EZMLM_CGI_URL/$listno" if(defined($listno));
   } return undef;

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

sub error_die {
	my $msg = shift;
	$pagedata->setValue("Data.ErrorMessage", "$msg");
	# TODO: besser waere eine Warnung in header.cs
	$pagename = 'error';
	&output_page;
	die $msg;
}
                                                                                                                 
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
