# language-specific definitions for ezmlm-web
# in english

# The meanings of the various ezmlm-make command line switches. The default
# ones match the ezmlm-idx 0.4 default ezmlmrc ... Alter them to suit your
# own ezmlmrc. Removing options from this list makes them unavailable
# through ezmlm-web - this could be useful for things like -w

%EZMLM_LABELS = (
#   option => ['Short Name', 
#              'Long Help Description'],

      a => ['Archived', 
            'Ezmlm will archive new messages'],
      b => ['Block archive', 
            'Only moderators are allowed to access the archive'],
#     c => config. This is implicity called, so is not defined here
      d => ['Digest',
            'Set up a digest list to disseminate digest of the list messages'], 
#     e => edit. Also implicity called, so not defined here
      f => ['Prefix',
            'Outgoing subject will be prefixed with the list name'],
      g => ['Guard Archive',
            'Archive access requests from unrecognized SENDERs will be rejected'],
      h => ['Help subscription',
            'Subscriptions do not require confirmation'],
      i => ['Indexed',
            'Indexed for WWW archive access'],
      j => ['Jump off',
            'Unsubscribe does not require  confirmation'],
      k => ['Kill',
            'Posts from addresses in dir/deny/ are rejected'], 
      l => ['Subscriber List',
            'Remote administrators can request a subscriber list'],
      m => ['Message Moderation',
            'All incoming messages are moderated'],
      n => ['Text Editing', 
            'Allow remote administrators to edit files in dir/text/'],
      o => ['Others  rejected', 
            'Posts from addresses other than moderators are rejected'],
      p => ['Public',
            'List will respond to administrative requests and archive retrieval'],
      q => ['Service Request Address',
            'Process commands sent in the subject to local-request@host'],
      r => ['Remote Admin',
            'Enable remote adminstration of the list'],
      s => ['Subscription Moderation',
            'Subscriptions to the main list and digest will be moderated'],
      t => ['Trailer',
            'Add a trailer to outgoing messages'], 
      u => ['User Posts Only',
            'Posts from unrecognized SENDER addresses will be rejected'], 
#     v => version. I doubt you will really need this ;-)
      w => ['Remove Warn',
            'Remove the ezmlm-warn(1) invocations from the list setup. It is assumed that ezmlm-warn(1) is run by other means'],
      x => ['Extra',
            'Strip certain mimetypes, etc'],
#     y => not used
#     z => not used

# These all take an extra argument, which is the default value to use

      0 => ['Sublist', 
            'Make the list a sublist of list mainlist@host',
            'mainlist@host'],   
#     1 => not used
#     2 => not used
      3 => ['From Address',
            'Replace the &quot;From:&quot; header of the message with &quot;From: fromarg&quot;',
            'fromarg'],
      4 => ['Digest Options',
            'Switches for ezmlm-tstdig(1)',
            '-t24 -m30 -k64'],
      5 => ['List Owner',
            'The email address of the list owner', 
            ''],
      6 => ['SQL Database',
            'SQL database connect information. Requires SQL support',
            'host:port:user:password:datab:table'],
      7 => ['Message Moderation Path',
            'Make /path the path to the database for message moderators, if the list is set up for message moderation',
            '/some/full/path'],
      8 => ['Subscription Moderation Path',
            'Make /path the path to the database for message moderators, if the list is set up for message moderation',
            '/some/full/path'],
      9 => ['Remote Admin Path',
            'Make /path the path to the database for message moderators, if the list is set up for message moderation',
            '/some/full/path']

);

# This list defines most of the context sensitive help in ezmlm-web. What
# isn't defined here is the options, which are defined above ... You can
# alter these if you feel something else would make more sense to your users
# Just be careful of what can fit on a screen!

%HELPER = (

   # These should be self explainitory
   addaddress       => 'You may enter any RFC822 compliant email address here, including the comment part. For example; J Random User <jru@on.web.za>',
   addaddressfile   => 'or you may enter the filename of a plain text file containing multiple RFC822 email addresses, one per line',
   moderator        => 'Moderators: people who control who may subscribe or post to a list',
   deny             => 'Deny: A list of addresses that are _never_ allowed to mail the list',
   allow            => 'Allow: A list of address that are allowed to mail the list even if the configuration otherwise restricts it',
   digest           => 'Digest: People who will recieve a digest of all messages on the list',
   webarch          => 'View the web based archive of this list',
   config           => 'This lets you alter the way the list is set up',
   listname         => 'This is the name of the list as displayed on the Select Lists screen. It is also the name of the subdirectory that contains the list',
   listadd          => 'This is the email address of the list. Note that the defaults come from your qmail config. You should just update the local part (before the @)',
   webusers         => 'NB! At this stage, any users specified here must exist. User creation may be added in future versions',
   prefix           => 'Text to add to the subject line of all outgoing messages',
   headerremove     => 'This is a list of headers to remove from all outgoing mail',
   headeradd        => 'This is a list of headers to add to all outging mail',
   mimeremove       => 'All messages whose Content-Type matches these mime types will be bounced back to sender',
   allowedit        => 'Comma separated list of usernames, or <CODE>ALL</CODE> (all valid users)',
   mysqlcreate      => 'This will create the necessary MySQL tables if the list configuration above requires it'

);

# This defines the captions of each of the buttons in ezmlm-web, and allows 
# you to configure them for your own language or taste. Since these are used
# by the switching algorithm it is important that every button has a unique
# caption - ie we can't have two 'Edit' buttons doing different things.

%BUTTON = (
   
   # These MUST all be unique!
   create                => 'Create',
   createlist            => 'Create List',
   edit                  => 'Edit',
   delete                => 'Delete',
   deleteaddress         => 'Delete Address',
   addaddress            => 'Add Address',
   moderators            => 'Moderators',
   denylist              => 'Deny List',
   allowlist             => 'Allow List',
   digestsubscribers     => 'Digest Subscribers',
   configuration         => 'Configuration',
   yes                   => 'Yes',
   no                    => 'No',
   updateconfiguration   => 'Update Configuration',
   edittexts             => 'Edit Texts',
   editfile              => 'Edit File',
   savefile              => 'Save File',
   webarchive            => 'Web Archive',
   selectlist            => 'Select List',
   subscribers           => 'Subscribers',
   cancel                => 'Cancel',
   resetform             => 'Reset Form',

);

# This defines the fixed text strings that are used in ezmlm-web. By editing
# these along with the button labels and help texts, you can convert ezmlm-web
# to another language :-) If anyone gets arround to doing complete templates
# for other languages I would appreciate a copy so that I can include it in
# future releases of ezmlm-web.

%LANGUAGE = (
   nop                   => 'Action not yet implemented',
   chooselistinfo        => "<UL><LI>Choose a mailing list from the selection box or click on [$BUTTON{'create'}].<LI>Click on the [$BUTTON{'edit'}] button if you want to edit the selected list.<LI>Click on the [$BUTTON{'delete'}] button if you want to delete the selected list.</UL>",
   confirmdelete         => 'Confirm deletion of', # list name
   subscribersto         => 'Subscribers to', # list name
   subscribers           => 'subscribers',
   additionalparts       => 'Additional list parts',
   posting               => 'Posting',
   subscription          => 'Subscription',
   remoteadmin           => 'Remote Admin',
   for                   => 'for', # as in; moderators for blahlist
   createnew             => 'Create a New List',
   listname              => 'List Name',
   listaddress           => 'List Address',
   listoptions           => 'List Options',
   allowedtoedit         => 'Users allowed to edit this list',
   editconfiguration     => 'Edit the List Configuration',
   prefix                => 'Subject prefex for outgoing messages',
   headerremove          => 'Headers to strip from all outgoing mail',
   headeradd             => 'Headers to add to all outgoing mail',
   mimeremove            =>   'Mime types to strip from all outgoing mail',
   edittextinfo          => "The box on the left contains a list of files available in the<BR>DIR/text directory. These files are sent out in response to specfic user request, or as part of all outgoing messages<P>To edit a file, select its name from the box. Then click on the [$BUTTON{'editfile'}] button.<P>Press [$BUTTON{'cancel'}] when you have finished editing.",
   editingfile           => 'Editing File',
   editfileinfo          => '<BIG><STRONG>ezmlm-manage</STRONG></BIG><BR><TT><STRONG>&lt;#l#&gt;</STRONG></TT> The list name<BR><TT><STRONG>&lt;#A#&gt;</STRONG></TT> The subscription address<BR><TT><STRONG>&lt;#R#&gt;</STRONG></TT> The address a subscriber must reply to<P><BIG><STRONG>ezmlm-store</STRONG></BIG><BR><TT><STRONG>&lt;#l#&gt;</STRONG></TT> The list name<BR><TT><STRONG>&lt;#A#&gt;</STRONG></TT> The acceptance address<BR><TT><STRONG>&lt;#R#&gt;</STRONG></TT> The rejection address</UL>',
   mysqlcreate           => 'Create the MySQL database tables if necessary',

);

#                      === Configuration file ends ===
