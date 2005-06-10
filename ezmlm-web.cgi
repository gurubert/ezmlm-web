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
use Mail::Ezmlm;
use Mail::Address;
use DB_File;
use CGI;
use CGI::Carp qw(fatalsToBrowser set_message);

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
use vars qw[$HTML_CSS_FILE];

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
if(defined($Q::action) && $Q::action eq '[Web Archive]') {
   print $q->redirect(&ezmlmcgirc);
   exit;
}

# Print header on every page ...
print $q->header(-pragma=>'no-cache', '-cache-control'=>'no-cache', -expires=>'-1d', '-Content-Type'=>'text/html; charset=utf-8');
print $q->start_html(-style=>{'src'=>"$HTML_CSS_FILE"},-title=>$HTML_TITLE, -author=>'guy-ezmlm@rucus.ru.ac.za', -expires=>'-1d');
print $HTML_HEADER;

# check permissions
&check_permission_for_action == 0 || die 'Error: you are not allowed to do this!';

# This is where we decide what to do, depending on the form state and the
# users chosen course of action ...
unless (defined($q->param('state'))) {
   # Default action. Present a list of available lists to the user ...
   &select_list; 

} elsif ($Q::state eq 'select') {
   # User selects an action to perform on a list ...
   
   if ($Q::action eq "[$BUTTON{'create'}]") { # Create a new list ...
      &allow_create_list;
   } elsif (defined($Q::list)) {
      if ($Q::action eq "[$BUTTON{'edit'}]") { # Edit an existing list ...
         &display_list;
      } elsif ($Q::action eq "[$BUTTON{'delete'}]") { # Delete a list ...
         &confirm_delete;
      }
   } else {
      &select_list; # NOP - Blank input ...
   }
   
} elsif ($Q::state eq 'edit') {
   # User chooses to edit a list
   
   my($list); $list = $LIST_DIR . '/' . $q->param('list'); 
   if ($Q::action eq "[$BUTTON{'deleteaddress'}]") { # Delete a subscriber ...
      &delete_address($list);
      &display_list;
   
   } elsif ($Q::action eq "[$BUTTON{'addaddress'}]") { # Add a subscriber ...
      &add_address($list);
      &display_list;
   
   } elsif ($Q::action eq "[$BUTTON{'moderators'}]") { # Edit the moderators ...
      &part_subscribers('mod');

   } elsif ($Q::action eq "[$BUTTON{'denylist'}]") { # Edit the deny list ...
      &part_subscribers('deny');

   } elsif ($Q::action eq "[$BUTTON{'allowlist'}]") { # edit the allow list ...
      &part_subscribers('allow');   

   } elsif ($Q::action eq "[$BUTTON{'digestsubscribers'}]") { # Edit the digest subscribers ...
      &part_subscribers('digest');
      
   } elsif ($Q::action eq "[$BUTTON{'configuration'}]") { # Edit the config ...
      &list_config;

   } else { # Cancel - Return a screen ...
      &select_list;
   }

} elsif ($Q::state eq 'allow' || $Q::state eq 'mod' || $Q::state eq 'deny' || $q->param('state') eq 'digest') {
   # User edits moderators || deny || digest ...

   my($part); 
   # Which list directory are we using ...
   if($Q::state eq 'mod') {
      $part = 'mod'; 
   } elsif($Q::state eq 'deny' ) {
      $part = 'deny'; 
   } elsif($Q::state eq 'allow') {
      $part = 'allow';
   } else {
      $part = 'digest'; 
   }
   
   if ($Q::action eq "[$BUTTON{'deleteaddress'}]") { # Delete a subscriber ...
      &delete_address("$LIST_DIR/$Q::list", $part);
      &part_subscribers($part);

   } elsif ($Q::action eq "[$BUTTON{'addaddress'}]") { # Add a subscriber ...
      &add_address("$LIST_DIR/$Q::list", $part);
      &part_subscribers($part);

   } else { # Cancel - Return to the list ...
      &display_list;
   }

} elsif ($Q::state eq 'confirm_delete') {
   # User wants to delete a list ...
   
   &delete_list if($q->param('confirm') eq "[$BUTTON{'yes'}]"); # Do it ...
   $q->delete_all;
   &select_list;

} elsif ($Q::state eq 'create') {
   # User wants to create a list ...

   if ($Q::action eq "[$BUTTON{'createlist'}]") {
      if (&create_list) { # Return if list creation is unsuccessful ...
         &allow_create_list;
      } else {
         &select_list; # Else choose a list ...
      }
   
   } else { # Cancel ...
      &select_list;
   }
   
} elsif ($Q::state eq 'configuration') {
   # User updates configuration ...
   
   if ($Q::action eq "[$BUTTON{'updateconfiguration'}]") { # Save current settings ...
      &update_config;
      &display_list;
      
   } elsif ($Q::action eq "[$BUTTON{'edittexts'}]") { # Edit DIR/text ...
      &list_text;
   
   } else { # Cancel - Return to list editing screen ...
      &display_list;
   }

} elsif ($Q::state eq 'list_text') {
   # User wants to edit texts associated with the list ...
   
   if ($Q::action eq "[$BUTTON{'editfile'}]") {
      &edit_text;  
   } else {
      &list_config; # Cancel ...
   }

} elsif ($Q::state eq 'edit_text') {   
   # User wants to save a new version of something in DIR/text ...
   
   &save_text if ($Q::action eq "[$BUTTON{'savefile'}]");
   &list_text;
   
} else {
   print "<h1>$Q::action</h1><h2>$LANGUAGE{'nop'}</h2><hr>";
} 

# Print HTML footer and exit :) ...
print $HTML_FOOTER, $q->end_html;
exit;

# =========================================================================

sub select_list {
   # List all mailing lists (sub directories) in the list directory.
   # Allow the user to choose a course of action; either editing an existing
   # list, creating a new one, or deleting an old one.

   my (@lists, @files, $i, $scrollsize);

   # Read the list directory for mailing lists.
   opendir DIR, $LIST_DIR || die "Unable to read $LIST_DIR: $!";
   @files = grep !/^\./, readdir DIR; 
   closedir DIR;

   # Check that they actually are lists ...
   foreach $i (0 .. $#files) {
      if (-e "$LIST_DIR/$files[$i]/lock") {
         $lists[$#lists + 1] = $files[$i] if (&webauth($files[$i]) == 0);
      }
   }

   # Keep selection box a resonable size - suggested by Sebastian Andersson 
   $scrollsize = 25 if(($scrollsize = $#lists + 1) > 25);

   # Begin of content
   print '<div id="main" class="container">';

   # Print a form
   $q->delete_all;
   print $q->startform;
   print $q->hidden(-name=>'state', -default=>'select');

   print '<div class="list">';
   print $q->scrolling_list(-name=>'list', -size=>$scrollsize, -values=>\@lists) if defined(@lists);
   print '</div>';	# end of main_mainlinglists_list
 
   print '<div class="info">', $LANGUAGE{'chooselistinfo'}, '</div>';		# explanation of options

   print '<div class="add_remove">';
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'create'}]"), '</span>' if (&webauth_create_allowed == 0);
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'edit'}]"), '</span>' if(defined(@lists));
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'delete'}]"), '</span>' if(defined(@lists));
   print '</div>';	# end of main_buttons
   print $q->endform;

   print '</div>';	# end of content
}

# ------------------------------------------------------------------------

sub confirm_delete {
   # Make sure that the user really does want to delete the list!

   # Begin of content
   print '<div id="delete" class="container">';

   # Print a form ...
   $q->delete('state');
   print $q->startform;
   print $q->hidden(-name=>'state', -default=>'confirm_delete');
   print $q->hidden(-name=>'list', -default=>$q->param('list'));

   print '<div class="title">';
   print '<h2>', $LANGUAGE{'confirmdelete'}, ' ', $q->param('list'), '</h2>';
   print '</div>';	# end of delete->title

   print '<div class="question">';
   print '<span class="button">', $q->submit(-name=>'confirm', -value=>"[$BUTTON{'no'}]"), '</span>';
   print '<span class="button">', $q->submit(-name=>'confirm', -value=>"[$BUTTON{'yes'}]"), '</span>';
   print '</div>';	# end of delete->question

   print '</div>';	# enf of delete
}

# ------------------------------------------------------------------------

sub display_list {
   # Show a list of subscribers to the user ...

   my ($i, $list, $listaddress, $moderated, @subscribers, $scrollsize);
   
   # Work out the address of this list ...
   $list = new Mail::Ezmlm("$LIST_DIR/$Q::list");
   $listaddress = &this_listaddress;

   
   # Get a list of subscribers from ezmlm ...
   @subscribers = $list->subscribers;
   
   # Keep selection box a resonable size - suggested by Sebastian Andersson 
   $scrollsize = 25 if(($scrollsize = $#subscribers + 1) > 25);

   # Print out a form of options ...
   $q->delete('state');                     

   # Begin of content
   print '<div id="edit" class="container">';

   print '<div class="title">';
   print "<h2>$LANGUAGE{'subscribersto'} $Q::list</h2>";
   print "<h3>($listaddress)</h3>";
   print '<hr>';
   print '</div>';	# end of edit->title

   print $q->start_multipart_form;
   print $q->hidden(-name=>'state', -default=>'edit');
   print $q->hidden(-name=>'list', -default=>$Q::list);

   print '<div class="list">';
   print $q->scrolling_list(-name=>'delsubscriber', -size=>$scrollsize, -values=>\@subscribers, -labels=>&pretty_names, -multiple=>'true') if defined(@subscribers);
   print '</div>';	# end of edit->list
   
   print '<div class="add_remove">';
   print '<p>', ($#subscribers + 1), ' ', $LANGUAGE{'subscribers'}, '</p>' if defined(@subscribers);
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'deleteaddress'}]"), '</span>' if defined(@subscribers);
   print '<span class="formfield">', $q->textfield(-name=>'addsubscriber', -size=>'40'), ' <img src="', $HELP_ICON_URL, '" title="', $HELPER{'addaddress'}, '"></span>';
   print '<span class="formfield">', $q->filefield(-name=>'addfile', -size=>20, -maxlength=>100), ' <img src="', $HELP_ICON_URL, '" title="', $HELPER{'addaddressfile'}, '"></span>' if ($FILE_UPLOAD);
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'addaddress'}]"), '</span>';
   print '</div>';	# end of edit->add_remove

   print '<div class="options">';
   print '<h3>', $LANGUAGE{'additionalparts'}, ':</h3>' if($list->ismodpost || $list->ismodsub || $list->isremote || $list->isdeny || $list->isallow || $list->isdigest);
   print '<p>';
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'moderators'}]"), '<img src="', $HELP_ICON_URL, '" title="', $HELPER{'moderator'}, '"> </span>' if ($list->ismodpost || $list->ismodsub || $list->isremote);
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'denylist'}]"), '<img src="', $HELP_ICON_URL, '" title="', $HELPER{'deny'}, '"> </span>' if ($list->isdeny);
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'allowlist'}]"), '<img src="', $HELP_ICON_URL, '" title="', $HELPER{'allow'}, '"> </span>' if ($list->isallow);
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'digestsubscribers'}]"), '<img src="', $HELP_ICON_URL, '" title="', $HELPER{'digest'}, '"> </span>' if ($list->isdigest);
   print '</p><p>';
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'webarchive'}]"), '<img src="', $HELP_ICON_URL, '" title="', $HELPER{'webarch'}, '">  </span>' if(&ezmlmcgirc);
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'configuration'}]"), '<img src="', $HELP_ICON_URL, '" title="', $HELPER{'config'}, '"> </span>';
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'selectlist'}]"), '</span>';
   print '</p>';
   print '</div>';	# end of edit->options
   print $q->endform; 

   print '</div>';	# end of edit

}

# ------------------------------------------------------------------------

sub delete_list {
   # Delete a list ...

   # Fixes a bug from the previous version ... when the .qmail file has a
   # different name to the list. We use outlocal to handle vhosts ...
   my ($list, $listaddress, $listadd); 
   $list = new Mail::Ezmlm("$LIST_DIR/$Q::list");
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

      use File::Copy;

      my ($oldfile); $oldfile = "$LIST_DIR/$Q::list";
      my ($newfile); $newfile = "$LIST_DIR/.$Q::list"; 
      move($oldfile, $newfile) or die "Unable to rename list: $!";
      mkdir "$HOME_DIR/deleted.qmail", 0700 if(!-e "$HOME_DIR/deleted.qmail");

      opendir(DIR, "$HOME_DIR") or die "Unable to get directory listing: $!";
      my @files = map { "$HOME_DIR/$1" if m{^(\.qmail.+)$} } grep { /^\.qmail-$listaddress/ } readdir DIR;
      closedir DIR;
      foreach (@files) {
         unless (move($_, "$HOME_DIR/deleted.qmail/")) {
            die "Unable to move .qmail files: $!"; 
         }
      }
      warn "List '$oldfile' moved (deleted)";   
   } else {
      # This, however, does DELETE the list. I don't like the idea, but I was
      # asked to include support for it so ...
      if (!rmtree("$LIST_DIR/$Q::list")) {
         die "Unable to delete list: $!";
      }
      opendir(DIR, "$HOME_DIR") or die "Unable to get directory listing: $!";
      my @files = map { "$HOME_DIR/$1" if m{^(\.qmail.+)$} } grep { /^\.qmail-$listaddress/ } readdir DIR;
      closedir DIR;
      if (unlink(@files) <= 0) {
         die "Unable to delete .qmail files: $!";
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
         if ($param =~ /^([#-\@\w\.\/\[\]\:\n\r\>\< ]+)$/) {
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
   if ($Q::state eq 'create') {
	$ret = &webauth_create_allowed();
   } elsif (defined($Q::list)) {
	$ret = &webauth($Q::list);
   } else {
	$ret = 0;
   }
   return $ret;

}

# ------------------------------------------------------------------------

sub add_address {
   # Add an address to a list ..

   my ($address, $list, @addresses, $count); my ($listname, $part) = @_;
   $list = new Mail::Ezmlm($listname);

   if (($q->param('addfile')) && ($FILE_UPLOAD)) {

      # Sanity check
      die "File upload must be of type text/*" unless($q->uploadInfo($q->param('addfile'))->{'Content-Type'} =~ m{^text/});

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
   
   foreach $address (@addresses) {

      my($add) = Mail::Address->parse($address);
      if(defined($add->name()) && $PRETTY_NAMES) {
         my(%pretty);
         tie %pretty, "DB_File", "$LIST_DIR/$Q::list/webnames";
         $pretty{$add->address()} = $add->name();
         untie %pretty;
      }
   
      if ($list->sub($add->address(), $part) != 1) {
         die "Unable to subscribe to list: $!";
      }
      $count++;
   }

   $q->delete('addsubscriber');
}

# ------------------------------------------------------------------------

sub delete_address {
   # Delete an address from a list ...

   my ($list, @address); my($listname, $part) = @_;
   $list = new Mail::Ezmlm($listname);
   return if ($q->param('delsubscriber') eq '');

   @address = $q->param('delsubscriber');

   if ($list->unsub(@address, $part) != 1) {
      die "Unable to unsubscribe from list $list: $!";
   }
   
   if($PRETTY_NAMES) {
      my(%pretty, $add);
      tie %pretty, "DB_File", "$LIST_DIR/$Q::list/webnames";
      foreach $add (@address) {
         delete $pretty{$add};
      }
      untie %pretty;
   }

   $q->delete('delsubscriber');
}

# ------------------------------------------------------------------------

sub part_subscribers {
   my($part) = @_;
   # Deal with list parts ....

   my ($i, $list, $listaddress, @subscribers, $moderated, $scrollsize, $type);
   
   # Work out the address of this list ...
   $list = new Mail::Ezmlm("$LIST_DIR/$Q::list");
   $listaddress = &this_listaddress;

   if($part eq 'mod') {
      # Lets know what is moderated :)
      
      # do we store things in different directories?
      my $config = $list->getconfig;
      my($postpath) = $config =~ m{7\s*'([^']+)'};
      my($subpath) = $config =~ m{8\s*'([^']+)'};
      my($remotepath) = $config =~ m{9\s*'([^']+)'};
      
      my($divclass);

      $divclass = ($postpath)? 'warning' : 'ok';
      $moderated .= "<p class=\"$divclass\">[$LANGUAGE{'posting'}]" if ($list->ismodpost);
      $moderated .= '<img src="' . $HELP_ICON_URL . '" title="Posting Moderators are stored in a non-standard location (' . $postpath . '). You will have to edit them manually.">' if ($postpath);
      $moderated .= '</p>' if ($list->ismodpost);

      $divclass = ($subpath)? 'warning' : 'ok';
      $moderated .= "<p class=\"$divclass\">[$LANGUAGE{'subscription'}]" if($list->ismodsub);
      $moderated .= '<img src="' . $HELP_ICON_URL . '" title="Subscriber Moderators are stored in a non-standard location (' . $subpath . '). You will have to edit them manually">' if ($subpath);
      $moderated .= '</p>' if ($list->ismodsub);

      $divclass = ($remotepath)? 'warning' : 'ok';
      $moderated .= "<p class=\"$divclass\">[$LANGUAGE{'remoteadmin'}]" if($list->isremote);
      $moderated .= '<img src="' . $HELP_ICON_URL . '" title="Remote Administrators are stored in a non-standard location (' . $remotepath . '). You will have to edit them manually">' if ($remotepath);
      $moderated .= '</p> if ($list->isremote)';
     
   }

   # What type of sublist is this?
   ($type) = $Q::action =~ m/^\[(.+)\]$/;

   # Get a list of moderators from ezmlm ...
   @subscribers = $list->subscribers($part);

   # Keep selection box a resonable size - suggested by Sebastian Andersson 
   $scrollsize = 25 if(($scrollsize = $#subscribers + 1) > 25);

   # Begin of content
   print '<div id="parts" class="container">';
   
   # Print out a form of options ...
   $q->delete('state');                     

   print '<div class="title">';
   print "<h2>$type $LANGUAGE{'for'} $listaddress</h2>";
   print '<hr>';
   print '</div>';	# end of parts_title

   print '<div class="info">', "$moderated", '</div>' if(defined($moderated));

   print $q->start_multipart_form;
   print $q->hidden(-name=>'state', -default=>$part);
   print $q->hidden(-name=>'list', -default=>$Q::list), "\n";

   print '<div class="list">', $q->scrolling_list(-name=>'delsubscriber', -size=>$scrollsize, -values=>\@subscribers, -multiple=>'true', -labels=>&pretty_names), '</div>' if defined(@subscribers);

   print '<div class="add_remove">';
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'deleteaddress'}]"), '</span>' if defined(@subscribers);
   print '<span class="formfield">', $q->textfield(-name=>'addsubscriber', -size=>'40'), ' <img src="', $HELP_ICON_URL, '" title="', $HELPER{'addaddress'}, '"></span>';
   print '<span class="formfield">', $q->filefield(-name=>'addfile', -size=>20, -maxlength=>100), ' <img src="', $HELP_ICON_URL, '" title="', $HELPER{'addaddressfile'}, '"></span>' if ($FILE_UPLOAD);
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'addaddress'}]"), '</span>';
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'subscribers'}]"), '</span>';
   print '</div>';	# end of parts_subscribers_actions

   print $q->endform;          

   print '</div>';	# end of parts

}

# ------------------------------------------------------------------------

sub allow_create_list {
   # Let the user select options for list creation ...
   
   my($username, $hostname, %labels, $j);
   
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

   print '<div id="create" class="container">';

   # Print a form of options ...
   $q->delete_all;

   print '<div class="title">';
   print '<h2>', $LANGUAGE{'createnew'}, '</h2>';
   print '<hr>';
   print '</div>';	# end of create->title

   print $q->startform;
   print $q->hidden(-name=>'state', -value=>'create');

   print '<div class="input">';
   print '<span class="formfield">', $LANGUAGE{'listname'}, ': ', $q->textfield(-name=>'list', -size=>'20'), ' <img src="', $HELP_ICON_URL, '" title="', $HELPER{'listname'}, '"></span>';
   print '<span class="formfield">', $LANGUAGE{'listaddress'}, ': ', $q->textfield(-name=>'inlocal', -default=>$username, -size=>'10');
   print ' @ ', $q->textfield(-name=>'inhost', -default=>$hostname, -size=>'30'), ' <img src="', $HELP_ICON_URL, '" title="', $HELPER{'listadd'}, '"></span>';
   
   print '<span class="formfield">', $LANGUAGE{'listoptions'}, ':</span>';
   &display_options($DEFAULT_OPTIONS);

   # Allow creation of mysql table if the module allows it
   if($Mail::Ezmlm::MYSQL_BASE) {
	print '<span class="formfield">', $q->checkbox(-name=>'sql', -label=>$LANGUAGE{'mysqlcreate'}, -on=>1);
	print ' <img src="', $HELP_ICON_URL, '" title="', $HELPER{'mysqlcreate'}, '"></span>';
   }
   
   if(-e "$WEBUSERS_FILE") {
	print '<span class="formfield">', $LANGUAGE{'allowedtoedit'}, ': '; 
	print $q->textfield(-name=>'webusers', -value=>$ENV{'REMOTE_USER'}||'ALL', -size=>'30');
	print ' <img src="', $HELP_ICON_URL, '" title="', $HELPER{'webusers'}, '"></span>';
	print '<span class="help">', $HELPER{'allowedit'}, '</span>';
   }
   print '</div>';	# end of create->input
   
   print '<div class="question">';
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'createlist'}]"), '</span>';
   print '<span class="button">', $q->reset(-value=>"[$BUTTON{'resetform'}]"), '</span>';
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'cancel'}]"), '</span>';
   print '</div>';	# end of create->question
   print $q->endform;  

   print '</div>';	# end of create
   
}

# ------------------------------------------------------------------------

sub create_list {
   # Create a list acording to user selections ...

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
      print '<h1 class="warning">', "List '$listname' already exists :(</h1>";
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
      die 'List creation failed', $list->errmsg();
   }

   # handle MySQL stuff
   if($q->param('sql') && $options =~ m/-6\s+/) {
      unless($list->createsql()) {
         die 'SQL table creation failed: ', $list->errmsg(); 
      }
   }
   
   &update_webusers();

   return 0;
}

# ------------------------------------------------------------------------

sub list_config {
   # Allow user to alter the list configuration ...

   my ($list, $listaddress, $listname, $options);
   my ($headeradd, $headerremove, $mimeremove, $prefix, $j);
   
   # Store some variables before we delete them ...
   $list = new Mail::Ezmlm("$LIST_DIR/$Q::list");
   $listname = $q->param('list');
   $listaddress = &this_listaddress;

   # Begin of content
   print '<div id="config" class="container">';
    
   # Print a form of options ...
   $q->delete_all;

   print '<div class="title">';
   print '<h2>', $LANGUAGE{'editconfiguration'}, '</h2>';
   print '<hr>';
   print '</div>';	# end of config->title

   print $q->startform;
   print $q->hidden(-name=>'state', -value=>'configuration');
   print $q->hidden(-name=>'list', -value=>$listname);

   print '<div class="info">';
   print '<p>', $LANGUAGE{'listname'}, ": <em>$listname</em></p>";
   print '<p>', "$LANGUAGE{'listaddress'}: <em>$listaddress</em></p>";
   print '</div>';	# end of config->info

   print '<div class="input">';
   print '<h2>', $LANGUAGE{'listoptions'}, ':</h2>';

   # Print a list of options, selecting the ones that apply to this list ...
   &display_options($list->getconfig);

   # Get the contents of the headeradd, headerremove, mimeremove and prefix files
   $headeradd = $list->getpart('headeradd');
   $headerremove = $list->getpart('headerremove');
   $mimeremove = $list->getpart('mimeremove');
   $prefix = $list->getpart('prefix'); 

   print '<span class="formfield">', $LANGUAGE{'prefix'}, ': ', $q->textfield(-name=>'prefix', -default=>$prefix, -size=>12), ' <img src="', $HELP_ICON_URL, '" title="', $HELPER{'prefix'}, '"></span>' if defined($prefix);
   print '<p class="formfield">', $LANGUAGE{'headerremove'}, ': <img src="', $HELP_ICON_URL, '" title="', $HELPER{'headerremove'}, '"><br>', $q->textarea(-name=>'headerremove', -default=>$headerremove, -rows=>5, -columns=>70), '</span>';
   print '<span class="formfield">', $LANGUAGE{'headeradd'}, ': <img src="', $HELP_ICON_URL, '" title="', $HELPER{'headeradd'}, '"><br>', $q->textarea(-name=>'headeradd', -default=>$headeradd, -rows=>5, -columns=>70), '</div>';
   print '<span class="formfield">', $LANGUAGE{'mimeremove'}, ': <img src="', $HELP_ICON_URL, '" title="', $HELPER{'mimeremove'}, '"><br>', $q->textarea(-name=>'mimeremove', -default=>$mimeremove, -rows=>5, -columns=>70), '</span>' if defined($mimeremove);
   
   if(open(WEBUSER, "<$WEBUSERS_FILE")) {
      my($webusers);
      while(<WEBUSER>) {
         last if (($webusers) = m{^$listname\s*\:\s*(.+)$});
      }
      close WEBUSER;
      $webusers ||= $ENV{'REMOTE_USER'} || 'ALL';

      print '<span class="formfield">', $LANGUAGE{'allowedtoedit'}, ': ';
      print $q->textfield(-name=>'webusers', -value=>$webusers, -size=>'30');
      print ' <img src="', $HELP_ICON_URL, '" title="', $HELPER{'webusers'}, '"></span>',
      print '<span class="help">', $HELPER{'allowedit'}, '</span>';
      
   }
   print '</div>';	# end of config->input
   
   print '<div class="question">';
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'updateconfiguration'}]"), '</span>';
   print '<span class="button">', $q->reset(-value=>"[$BUTTON{'resetform'}]"), '</span>';
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'cancel'}]"), '</span>'; 
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'edittexts'}]"), '</span>';
   print '</div>';	# end of config->question
   
   print $q->endform;  

   print '</div>';	# end of config
}

# ------------------------------------------------------------------------

sub update_config {
   # Save the new user entered config ...
   
   my ($list, $options, $i, @inlocal, @inhost);
   $list = new Mail::Ezmlm("$LIST_DIR/$Q::list");

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

   if($Q::webusers) {
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
	print WU "$Q::list\: $Q::webusers\n";
      close TMP; close WU;
      unlink "/tmp/ezmlm-web.$$";
   }

}

# ------------------------------------------------------------------------

sub this_listaddress {
   # Work out the address of this list ... Used often so put in its own subroutine ...
   
   my ($list, $listaddress);
   $list = new Mail::Ezmlm("$LIST_DIR/$Q::list");
   chomp($listaddress = $list->getpart('outlocal'));
   $listaddress .= '@';
   chomp($listaddress .= $list->getpart('outhost'));
   return $listaddress;
}

# ------------------------------------------------------------------------

sub list_text {
   # Show a listing of what is in DIR/text ...
   
   my(@files, $list);
   $list = $LIST_DIR . '/' . $q->param('list');

   # Read the list directory for text ...
   opendir DIR, "$list/text" || die "Unable to read DIR/text: $!";
   @files = grep !/^\./, readdir DIR; 
   closedir DIR;

   # Begin of content
   print '<div id="textfiles" class="container">';

   # Print a form ...
   $q->delete('state');
   print $q->startform;
   print $q->hidden(-name=>'state', -default=>'list_text');
   print $q->hidden(-name=>'list', -default=>$q->param('list'));

   print '<div class="list">';
   print $q->scrolling_list(-name=>'file', -values=>\@files);
   print '</div>';	# end of textfiles->list

   print '<div class="info">';
   print $LANGUAGE{'edittextinfo'};
   print '</div>';	# end of textfiles->info

   print '<div class="question">';
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'editfile'}]"), '</span>';
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'cancel'}]"), '</span>';
   print '</div>';	# end of textfiles->question

   print $q->endform;

   print '</div>';
   
}

# ------------------------------------------------------------------------

sub edit_text {
   # Allow user to edit the contents of DIR/text ...

   my ($content);
   my($list) = new Mail::Ezmlm("$LIST_DIR/$Q::list");
   $content = $list->getpart("text/$Q::file");

   # Begin of content
   print '<div id="edittext" class="container">';

   # Print a form ...
   $q->delete('state');

   print '<div class="title">';
   print '<h2>', $LANGUAGE{'editingfile'}, ': ', $Q::file, '</h2>';
   print '</div>';	# end of edittext->title

   print $q->startform;
   print $q->hidden(-name=>'state', -default=>'edit_text');
   print $q->hidden(-name=>'list', -default=>$q->param('list'));
   print $q->hidden(-name=>'file', -default=>$q->param('file'));

   print '<div class="input">';
   print '<span class="formfield">', $q->textarea(-name=>'content', -default=>$content, -rows=>'25', -columns=>'72'), '</span>';
   print '</div>';	# end of edittext->input

   print '<id class="info">';
   print $LANGUAGE{'editfileinfo'};
   print '</div>';	# end of edittext->info

   print '<div class="question">';
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'savefile'}]"), '</span>';
   print '<span class="button">', $q->reset(-value=>"[$BUTTON{'resetform'}]"), '</span>';
   print '<span class="button">', $q->submit(-name=>'action', -value=>"[$BUTTON{'cancel'}]"), '</span>';
   print '</div>';	# end of edittext->question

   print $q->endform;

   print '</div>';	# end of edittext
}
   
# ------------------------------------------------------------------------

sub save_text {
   # Save new text in DIR/text ...

   my ($list) = new Mail::Ezmlm("$LIST_DIR/$Q::list");
   $list->setpart("text/$Q::file", $q->param('content'));
   
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

sub display_options {
   my($opts) = shift;
   my($i, $j);
 
   print "<!-- $opts -->";  
   print '<p>';
   foreach $i (grep {/\D/} keys %EZMLM_LABELS) {
      if ($opts =~ /^\w*$i\w*\s*/) {
         print '<span class="checkbox">', $q->checkbox(-name=>$i, -value=>$i, -label=>$EZMLM_LABELS{$i}[0], -on=>'1');
      } else {
         print '<span class="checkbox">', $q->checkbox(-name=>$i, -value=>$i, -label=>$EZMLM_LABELS{$i}[0]);
      }
      print '<img src="', $HELP_ICON_URL, '" border="0" title="', $EZMLM_LABELS{$i}[1] , '"></span>';
      print '</td>'; $j++;
      if ($j >= 3) {
         $j = 0; print '</p><p>';
      }
   }
   print '</p>';

   foreach $i (grep {/\d/} keys %EZMLM_LABELS) {
      print '<p>';
      if ($opts =~ /$i (?:'(.+?)')/) {
         print '<span class="checkbox">', $q->checkbox(-name=>$i, -value=>$i, -label=>$EZMLM_LABELS{$i}[0], -on=>'1');
      } else {
         print '<span class="checkbox">', $q->checkbox(-name=>$i, -value=>$i, -label=>$EZMLM_LABELS{$i}[0]);
      }
      print '<img src="', $HELP_ICON_URL, '" border="0" title="', $EZMLM_LABELS{$i}[1] , '"></span>';
      print '<span class="formfield">', $q->textfield(-name=>"$i-value", -value=>$1||$EZMLM_LABELS{$i}[2], -size=>30), '</span>';
      print '</p>';
   }
   
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
   tie %pretty, "DB_File", "$LIST_DIR/$Q::list/webnames";
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

BEGIN {
   sub handle_errors {
      my $msg = shift;
      print << "EOM";
         </div><div class="error">
         <h2>A fatal error has occoured</h2>
         <p>Something you did caused this script to bail out. The error
         message we got was</p>
         <p class="msg">$msg</p>
         <p>Please try what you were doing again, checking everything you entered.<br>
         If you still find yourself getting this error, please
         contact the <a href="mailto:webmaster\@$DEFAULT_HOST">site administrator</a>
         quoting the error message above.</p>
         </</div>
EOM

   }
   set_message(\&handle_errors);
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

=head1 BUGS

 None known yet. Please report bugs to the author.

=head1 S<SEE ALSO>
 
 ezmlm(5), ezmlm-cgi(1), Mail::Ezmlm(3)
   
 https://systemausfall.org/toolforge/ezmlm-web
 http://rucus.ru.ac.za/~guy/ezmlm/
 http://www.ezmlm.org/
 http://www.qmail.org/
