#include <stdio.h>

/* C wrapper to allow ezmlm-web.cgi to run suid */
/* Copyright (C) 1999/2000, Guy Antony Halse, All Rights Reserved */
/* See the README file in this distribution for copyright information */

int main(void) {
   /* Change this path to wherever you decided to put ezmlm-web.cgi */
   execv("/usr/lib/ezmlm-web/ezmlm-web.pl"); 
}
