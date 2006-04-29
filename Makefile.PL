# $Id$

use strict;
use ExtUtils::MakeMaker;
# See lib/ExtUtils/MakeMaker.pm for details of how to influence
# the contents of the Makefile that is written.
WriteMakefile(
	'NAME'		=> 'ezmlm-web',
	'AUTHOR'	=> 'Lars Kruse <devel@sumpfralle.de>',
	'VERSION_FROM'	=> 'ezmlm-web.cgi', # finds $VERSION
	'DISTNAME'		=> 'ezmlm-web',
	'PREREQ_PM'		=> {
			'Mail::Ezmlm' => 0.07,
			'Mail::Address'	=> 1.15,
			'CGI'	=> 2.6,
			'CGI::Carp'	=> 1.06,
			'DB_File'	=> 1.65,
			'Getopt::Std'	=> 1.0,
			'File::Find'	=> 0.0,
			'File::Copy'	=> 2.02,
			'File::Path'	=> 1.07,
			'Text::ParseWords'	=> 3.0 },
	'dist'		=> { COMPRESS => 'gzip', SUFFIX => 'gz' }
);

sub MY::postamble {
	my ($self, $datadir) = @_;
	my $SHAREDIR = "\$(DESTINSTALLSHARE)/$self->{NAME}";
	return <<ENDOFTEXT
# REALINSTALLBIN is introduced later depending on "site" or "vendor" installation
export REALINSTALLBIN
export NOECHO
export CC

real_install_bin_:	REALINSTALLBIN := \$(INSTALLSITEBIN)
real_install_bin_:	install_suid_wrapper install_cgi

real_install_bin_site:	REALINSTALLBIN := \$(INSTALLSITEBIN)
real_install_bin_site:	install_suid_wrapper install_cgi

real_install_bin_vendor:	REALINSTALLBIN := \$(INSTALLVENDORBIN)
real_install_bin_vendor:	install_suid_wrapper install_cgi

real_install_bin_perl:	REALINSTALLBIN := \$(INSTALLBIN)
real_install_bin_perl:	install_suid_wrapper install_cgi

real_build_bin_:	REALINSTALLBIN := \$(INSTALLSITEBIN)
real_build_bin_:	build_suid_wrapper

real_build_bin_site:	REALINSTALLBIN := \$(INSTALLSITEBIN)
real_build_bin_site:	build_suid_wrapper

real_build_bin_vendor:	REALINSTALLBIN := \$(INSTALLVENDORBIN)
real_build_bin_vendor:	build_suid_wrapper

real_build_bin_perl:	REALINSTALLBIN := \$(INSTALLBIN)
real_build_bin_perl:	build_suid_wrapper


subdirs:: real_build_bin_\$(INSTALLDIRS)

clean_subdirs: clean_suid_wrapper

build_suid_wrapper:
	\$(MAKE) -C suid-wrapper build

clean_suid_wrapper:
	\$(MAKE) -C suid-wrapper clean

make_real_bin:	real_install_bin_\$(INSTALLDIRS)
	\$(MKPATH) \$(DESTDIR)\$(REALINSTALLBIN)

install_cgi:	make_real_bin
	install -c -m 755 ezmlm-web.cgi \$(DESTDIR)\$(REALINSTALLBIN)/ezmlm-web.cgi

install_suid_wrapper:	build_suid_wrapper make_real_bin
	\$(NOECHO) echo "WARNING: \$(REALINSTALLBIN)"
	install -c -m 0755 suid-wrapper/index.cgi \$(DESTDIR)\$(REALINSTALLBIN)/ezmlm-web.wrapper
	install -c -m 0755 suid-wrapper/ezmlm-web-make-suid \$(DESTDIR)\$(REALINSTALLBIN)/

install::	real_install_bin_\$(INSTALLDIRS) install_share_\$(INSTALLDIRS)
install_share_site::	DESTINSTALLSHARE := \$(DESTDIR)\$(PREFIX)/local/share
install_share_site::	install_share
install_share_vendor::	DESTINSTALLSHARE := \$(DESTDIR)\$(PREFIX)/share
install_share_vendor::	install_share
install_share:
	install -d -m 0755 $SHAREDIR
	install -d -m 0755 $SHAREDIR/lang
	for file in share/lang/*.hdf ; \\
		do	install -c -m 0644 \$\$file $SHAREDIR/lang/ ; \\
	 done
	install -d -m 0755 $SHAREDIR/css
	for file in share/css/*.css ; \\
		do	install -c -m 0644 \$\$file $SHAREDIR/css/ ; \\
	 done
	install -d -m 0755 $SHAREDIR/template
	install -d -m 0755 $SHAREDIR/template/ui
	install -d -m 0755 $SHAREDIR/template/ui/default
	install -d -m 0755 $SHAREDIR/template/ui/gnupg
	install -d -m 0755 $SHAREDIR/template/config_options
	for file in share/template/*.cs ; \\
		do	install -c -m 0644 \$\$file $SHAREDIR/template/ ; \\
	 done
	for file in share/template/config_options/*.cs ; \\
		do	install -c -m 0644 \$\$file $SHAREDIR/template/config_options/ ; \\
	 done
	for file in share/template/ui/default/*.hdf ; \\
		do	install -c -m 0644 \$\$file $SHAREDIR/template/ui/default/ ; \\
	 done
	for file in share/template/ui/gnupg/*.hdf ; \\
		do	install -c -m 0644 \$\$file $SHAREDIR/template/ui/gnupg/ ; \\
	 done
ENDOFTEXT
}
