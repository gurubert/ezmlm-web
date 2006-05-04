# Makefile to compile the binary suid-wrapper for ezmlm-web
#
# REALINSTALLBIN should be defined in the higher level Makefile

.PHONY: build clean

build:
	$(NOECHO) echo "#define EZMLM_WEB_CGI \"$(REALINSTALLBIN)/ezmlm-web.cgi\"" >index.h
	$(CC) -o index.cgi index.c
	sed 's#^EZMLM_WEB_SUID_WRAPPER=.*$$#EZMLM_WEB_SUID_WRAPPER=$(REALINSTALLBIN)/ezmlm-web.wrapper#' ezmlm-web-make-suid >ezmlm-web-make-suid.configured

clean:
	-rm index.cgi ezmlm-web-make-suid.configured
	$(NOECHO) echo "#define EZMLM_WEB_CGI \"/usr/bin/ezmlm-web.cgi\"" >index.h

