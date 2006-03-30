/* $Id$ */

#include <stdio.h>
#include <unistd.h>

/* C wrapper to allow ezmlm-web.cgi to run suid */
/* Copyright (C) 1999/2000, Guy Antony Halse, All Rights Reserved */
/* Copyright (C) 02005/02006, Lars Kruse, All Rights Reserved */
/* See the README file in this distribution for copyright information */

int main(void) {

	/* Set the (real) uid to the same value, as the effective uid.
	   This is necesary, as (the suid) gpg tries to run on behalf of www-data
	   instead of the presumed user.
	   I hope, that this will not break on non-linux systems ... */
	setreuid(getuid(), -1);
	
	/* Change this path to wherever you decided to put ezmlm-web.cgi */
	execv("/usr/local/bin/ezmlm-web.cgi", NULL); 

	/* Note that you could also use the following to allow a specific user
	   to store their mailing lists and configuration file in a different 
	   location. This overrides the default.
	  
	   ezmlm-web.cgi understands the following parameters:
		-C /path/to/config.file
		-d /path/to/list/directory

	  See README for the default values. */

      
	/* Look at the exec(3) man page if you don't understand how the arguments
	   list below works */
   
	/*
		char *switches[] = { "ezmlm-web.cgi", "-d", "/tmp/ezmlm-web-demo", NULL };
		execv("/usr/local/bin/ezmlm-web.cgi", switches);
	*/
   
   
}
