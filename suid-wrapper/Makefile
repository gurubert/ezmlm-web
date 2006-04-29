# Makefile to compile the binary suid-wrapper for ezmlm-web
#
# REALINSTALLBIN should be defined in the higher level Makefile

.PHONY: build clean

build:
	$(NOECHO) echo "#define EZMLM_WEB_CGI \"$(REALINSTALLBIN)/ezmlm-web.cgi\"" >index.h
	$(CC) -o index.cgi index.c
	sed -i 's#^EZMLM_WEB_SUID_WRAPPER=.*$$#EZMLM_WEB_SUID_WRAPPER=$(REALINSTALLBIN)/ezmlm-web.wrapper#' ezmlm-web-make-suid

clean:
	-rm index.cgi
	$(NOECHO) echo "#define EZMLM_WEB_CGI \"/usr/bin/ezmlm-web.cgi\"" >index.h

