# Version of ssh-askpass
%define aversion 1.2.0

# Do we want to disable building of x11-askpass? (1=yes 0=no)
%define no_x11_askpass 0

# Do we want to disable building of gnome-askpass? (1=yes 0=no)
%define no_gnome_askpass 0

# Reserve options to override askpass settings with:
# rpm -ba|--rebuild --define 'skip_xxx 1'
%{?skip_x11_askpass:%define no_x11_askpass 1}
%{?skip_gnome_askpass:%define no_gnome_askpass 1}

# Is this a build for the rescue CD (without PAM)? (1=yes 0=no)
%define rescue 0
%{?build_rescue:%define rescue 1}

# Is this a build for 6.x or earlier?
%define build6x 0
%{?build_6x:%define build6x 1}

# If this is 6.x, the default configuration has sysconfdir in /usr/etc.
%if %{build6x}
%define _sysconfdir /etc
%endif

Summary: OpenSSH free Secure Shell (SSH) implementation
Name: openssh
Version: 2.5.2p2
Release: 1.7.2
URL: http://www.openssh.com/portable.html
Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
%if ! %{no_x11_askpass}
Source1: http://www.jmknoble.cx/software/x11-ssh-askpass/x11-ssh-askpass-%{aversion}.tar.gz
%endif
Source2: openssh.init
Source3: gnome-ssh-askpass.sh
Source4: gnome-ssh-askpass.csh
Source5: openssh-closing.txt
Patch0: openssh-2.5.2p2-redhat.patch
Patch1: openssh-2.3.0p1-path.patch
Patch2: openssh-2.5.1p1-crypt.patch
Patch3: openssh-2.5.1p1-all.patch
Patch4: openssh-2.5.2p2-setcred.patch
Patch5: reinit.patch
Patch6: aes-compat.diff
Patch7: sftp-globfix.diff
Copyright: BSD
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
Obsoletes: ssh
PreReq: initscripts >= 5.20
BuildPreReq: perl, openssl-devel, tcp_wrappers
BuildPreReq: /bin/login, /usr/include/security/pam_appl.h
%if ! %{no_x11_askpass}
BuildPreReq: XFree86-devel
%endif
%if ! %{no_gnome_askpass}
BuildPreReq: gnome-libs-devel
%endif
Requires: openssl

%package clients
Summary: OpenSSH Secure Shell protocol clients
Requires: openssh = %{version}-%{release}
Group: Applications/Internet
Obsoletes: ssh-clients

%package server
Summary: OpenSSH Secure Shell protocol server (sshd)
Group: System Environment/Daemons
Obsoletes: ssh-server
PreReq: openssh = %{version}-%{release}, chkconfig >= 0.9
%if ! %{build6x}
Requires: /etc/pam.d/system-auth
%endif

%package askpass
Summary: OpenSSH X11 passphrase dialog
Group: Applications/Internet
Requires: openssh = %{version}-%{release}
Obsoletes: ssh-extras

%package askpass-gnome
Summary: OpenSSH GNOME passphrase dialog
Group: Applications/Internet
Requires: openssh = %{version}-%{release}
Obsoletes: ssh-extras

%description
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all 
patented algorithms to separate libraries (OpenSSL).

This package includes the core files necessary for both the OpenSSH
client and server.  To make this package useful, you should also
install openssh-clients, openssh-server, or both.

%description clients
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all 
patented algorithms to separate libraries (OpenSSL).

This package includes the clients necessary to make encrypted connections
to SSH servers.

%description server
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all 
patented algorithms to separate libraries (OpenSSL).

This package contains the secure shell daemon. The sshd is the server 
part of the secure shell protocol and allows ssh clients to connect to 
your host.

%description askpass
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all 
patented algorithms to separate libraries (OpenSSL).

This package contains Jim Knoble's <jmknoble@jmknoble.cx> X11 passphrase 
dialog.

%description askpass-gnome
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all 
patented algorithms to separate libraries (OpenSSL).

This package contains the GNOME passphrase dialog.

%prep

%if ! %{no_x11_askpass}
%setup -q -a 1
%else
%setup -q
%endif
%patch0 -p1 -b .redhat
%patch1 -p1 -b .path
%patch2 -p1 -b .crypt
%patch3 -p1 -b .all
%patch4 -p1 -b .setcred
%patch5 -p0 -b .reinit
%patch6 -p0 -b .aes-compat
%patch7 -p0 -b .sftp-globfix
autoheader
autoconf

%build
%configure \
	--sysconfdir=%{_sysconfdir}/ssh \
	--libexecdir=%{_libexecdir}/openssh \
	--with-tcp-wrappers \
	--with-ipv4-default \
	--with-rsh=/usr/bin/rsh \
%if %{rescue}
	--without-pam --with-md5-passwords
%else
	--with-pam
%endif

make

%if ! %{no_x11_askpass}
pushd x11-ssh-askpass-%{aversion}
xmkmf -a
make
popd
%endif

%if ! %{no_gnome_askpass}
pushd contrib
gcc $RPM_OPT_FLAGS `gnome-config --cflags gnome gnomeui` \
        gnome-ssh-askpass.c -o gnome-ssh-askpass \
        `gnome-config --libs gnome gnomeui`
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/openssh
make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/pam.d/
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_libexecdir}/openssh
%if ! %{build6x}
install -m644 contrib/redhat/sshd.pam-7.x $RPM_BUILD_ROOT/etc/pam.d/sshd
%else
install -m644 contrib/redhat/sshd.pam     $RPM_BUILD_ROOT/etc/pam.d/sshd
%endif
install -m755 $RPM_SOURCE_DIR/openssh.init $RPM_BUILD_ROOT/etc/rc.d/init.d/sshd

%if ! %{no_x11_askpass}
install -s x11-ssh-askpass-%{aversion}/x11-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/x11-ssh-askpass
ln -s x11-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/ssh-askpass
%endif

%if ! %{no_gnome_askpass}
install -s contrib/gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/gnome-ssh-askpass
%endif

install -d $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/

perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*

%clean
rm -rf $RPM_BUILD_ROOT

%triggerun server -- ssh-server
if [ "$1" != 0 -a -r /var/run/sshd.pid ] ; then
	touch /var/run/sshd.restart
fi

%triggerun server -- openssh-server < 2.5.0p1
# Count the number of HostKey and HostDsaKey statements we have.
gawk	'BEGIN {IGNORECASE=1}
	 /^hostkey/ || /^hostdsakey/ {sawhostkey = sawhostkey + 1}
	 END {exit sawhostkey}' /etc/ssh/sshd_config
# And if we only found one, we know the client was relying on the old default
# behavior, which loaded the the SSH2 DSA host key when HostDsaKey wasn't
# specified.  Now that HostKey is used for both SSH1 and SSH2 keys, specifying
# one nullifies the default, which would have loaded both.
if [ $? -eq 1 ] ; then
	echo HostKey /etc/ssh/ssh_host_rsa_key >> /etc/ssh/sshd_config
	echo HostKey /etc/ssh/ssh_host_dsa_key >> /etc/ssh/sshd_config
fi

%triggerpostun server -- ssh-server
if [ "$1" != 0 ] ; then
	/sbin/chkconfig --add sshd
	if test -f /var/run/sshd.restart ; then
		rm -f /var/run/sshd.restart
		/sbin/service sshd start > /dev/null 2>&1 || :
	fi
fi

%post server
/sbin/chkconfig --add sshd

%postun server
/sbin/service sshd condrestart > /dev/null 2>&1 || :

%preun server
if [ "$1" = 0 ]
then
	/sbin/service sshd stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del sshd
fi

%files
%defattr(-,root,root)
%doc CREDITS ChangeLog INSTALL LICENCE OVERVIEW README* RFC* TODO WARNING*
%attr(0755,root,root) %{_bindir}/scp
%attr(0644,root,root) %{_mandir}/man1/scp.1*
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/primes
%if ! %{rescue}
%attr(0755,root,root) %{_bindir}/ssh-keygen
%attr(0644,root,root) %{_mandir}/man1/ssh-keygen.1*
%attr(0755,root,root) %dir %{_libexecdir}/openssh
%endif

%files clients
%defattr(-,root,root)
%attr(4755,root,root) %{_bindir}/ssh
%attr(0644,root,root) %{_mandir}/man1/ssh.1*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%attr(-,root,root) %{_bindir}/slogin
%attr(-,root,root) %{_mandir}/man1/slogin.1*
%if ! %{rescue}
%attr(0755,root,root) %{_bindir}/ssh-agent
%attr(0755,root,root) %{_bindir}/ssh-add
%attr(0755,root,root) %{_bindir}/ssh-keyscan
%attr(0755,root,root) %{_bindir}/sftp
%attr(0644,root,root) %{_mandir}/man1/ssh-agent.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-add.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-keyscan.1*
%attr(0644,root,root) %{_mandir}/man1/sftp.1*
%endif

%if ! %{rescue}
%files server
%defattr(-,root,root)
%attr(0755,root,root) %{_sbindir}/sshd
%attr(0755,root,root) %{_libexecdir}/openssh/sftp-server
%attr(0644,root,root) %{_mandir}/man8/sshd.8*
%attr(0644,root,root) %{_mandir}/man8/sftp-server.8*
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%attr(0600,root,root) %config(noreplace) /etc/pam.d/sshd
%attr(0755,root,root) %config /etc/rc.d/init.d/sshd
%endif

%if ! %{no_x11_askpass}
%files askpass
%defattr(-,root,root)
%doc x11-ssh-askpass-%{aversion}/README
%doc x11-ssh-askpass-%{aversion}/ChangeLog
%doc x11-ssh-askpass-%{aversion}/SshAskpass*.ad
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-askpass
%attr(0755,root,root) %{_libexecdir}/openssh/x11-ssh-askpass
%endif

%if ! %{no_gnome_askpass}
%files askpass-gnome
%defattr(-,root,root)
%attr(0755,root,root) %{_sysconfdir}/profile.d/gnome-ssh-askpass.*
%attr(0755,root,root) %{_libexecdir}/openssh/gnome-ssh-askpass
%endif

%changelog
* Fri Mar 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- add pam_limits back to the PAM configuration

* Wed Mar 28 2001 Nalin Dahyabhai <nalin@redhat.com>
- tweak the init script because 7.0's initscripts daemon() function
  isn't as smart as it should be

* Mon Mar 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- build for a 7.0 errata

* Fri Mar 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- make do_pam_setcred() smart enough to know when to establish creds and
  when to reinitialize them
- add in a couple of other fixes from Damien for inclusion in the errata

* Thu Mar 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.5.2p2
- call setcred() again after initgroups, because the "creds" could actually
  be group memberships

* Tue Mar 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.5.2p1 (includes endianness fixes in the rijndael implementation)
- don't enable challenge-response by default until we find a way to not
  have too many userauth requests (we may make up to six pubkey and up to
  three password attempts as it is)
- remove build dependency on rsh to match openssh.com's packages more closely

* Sat Mar  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- remove dependency on openssl -- would need to be too precise

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Mon Feb 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- Revert the patch to move pam_open_session.
- Init script and spec file changes from Pekka Savola. (#28750)
- Patch sftp to recognize '-o protocol' arguments. (#29540)

* Thu Feb 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- Chuck the closing patch.
- Add a trigger to add host keys for protocol 2 to the config file, now that
  configuration file syntax requires us to specify it with HostKey if we
  specify any other HostKey values, which we do.

* Tue Feb 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- Redo patch to move pam_open_session after the server setuid()s to the user.
- Rework the nopam patch to use be picked up by autoconf.

* Mon Feb 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- Update for 2.5.1p1.
- Add init script mods from Pekka Savola.
- Tweak the init script to match the CVS contrib script more closely.
- Redo patch to ssh-add to try to adding both identity and id_dsa to also try
  adding id_rsa.

* Fri Feb 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- Update for 2.5.0p1.
- Use $RPM_OPT_FLAGS instead of -O when building gnome-ssh-askpass
- Resync with parts of Damien Miller's openssh.spec from CVS, including
  update of x11 askpass to 1.2.0.
- Only require openssl (don't prereq) because we generate keys in the init
  script now.

* Tue Feb 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- Don't open a PAM session until we've forked and become the user (#25690).
- Apply Andrew Bartlett's patch for letting pam_authenticate() know which
  host the user is attempting a login from.
- Resync with parts of Damien Miller's openssh.spec from CVS.
- Don't expose KbdInt responses in debug messages (from CVS).
- Detect and handle errors in rsa_{public,private}_decrypt (from CVS).

* Wed Feb  7 2001 Trond Eivind Glomsr)Bød <teg@redhat.com>
- i18n-tweak to initscript.

* Tue Jan 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- More gettextizing.
- Close all files after going into daemon mode (needs more testing).
- Extract patch from CVS to handle auth banners (in the client).
- Extract patch from CVS to handle compat weirdness.

* Fri Jan 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- Finish with the gettextizing.

* Thu Jan 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- Fix a bug in auth2-pam.c (#23877)
- Gettextize the init script.

* Wed Dec 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- Incorporate a switch for using PAM configs for 6.x, just in case.

* Tue Dec  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- Incorporate Bero's changes for a build specifically for rescue CDs.

* Wed Nov 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- Don't treat pam_setcred() failure as fatal unless pam_authenticate() has
  succeeded, to allow public-key authentication after a failure with "none"
  authentication.  (#21268)

* Tue Nov 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to x11-askpass 1.1.1. (#21301)
- Don't second-guess fixpaths, which causes paths to get fixed twice. (#21290)

* Mon Nov 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- Merge multiple PAM text messages into subsequent prompts when possible when
  doing keyboard-interactive authentication.

* Sun Nov 26 2000 Nalin Dahyabhai <nalin@redhat.com>
- Disable the built-in MD5 password support.  We're using PAM.
- Take a crack at doing keyboard-interactive authentication with PAM, and
  enable use of it in the default client configuration so that the client
  will try it when the server disallows password authentication.
- Build with debugging flags.  Build root policies strip all binaries anyway.

* Tue Nov 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- Use DESTDIR instead of %%makeinstall.
- Remove /usr/X11R6/bin from the path-fixing patch.

* Mon Nov 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- Add the primes file from the latest snapshot to the main package (#20884).
- Add the dev package to the prereq list (#19984).
- Remove the default path and mimic login's behavior in the server itself.

* Fri Nov 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- Resync with conditional options in Damien Miller's .spec file for an errata.
- Change libexecdir from %%{_libexecdir}/ssh to %%{_libexecdir}/openssh.

* Tue Nov  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to OpenSSH 2.3.0p1.
- Update to x11-askpass 1.1.0.
- Enable keyboard-interactive authentication.

* Mon Oct 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to ssh-askpass-x11 1.0.3.
- Change authentication related messages to be private (#19966).

* Tue Oct 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- Patch ssh-keygen to be able to list signatures for DSA public key files
  it generates.

* Thu Oct  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- Add BuildPreReq on /usr/include/security/pam_appl.h to be sure we always
  build PAM authentication in.
- Try setting SSH_ASKPASS if gnome-ssh-askpass is installed.
- Clean out no-longer-used patches.
- Patch ssh-add to try to add both identity and id_dsa, and to error only
  when neither exists.

* Mon Oct  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update x11-askpass to 1.0.2. (#17835)
- Add BuildPreReqs for /bin/login and /usr/bin/rsh so that configure will
  always find them in the right place. (#17909)
- Set the default path to be the same as the one supplied by /bin/login, but
  add /usr/X11R6/bin. (#17909)
- Try to handle obsoletion of ssh-server more cleanly.  Package names
  are different, but init script name isn't. (#17865)

* Wed Sep  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.2.0p1. (#17835)
- Tweak the init script to allow proper restarting. (#18023)

* Wed Aug 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 20000823 snapshot.
- Change subpackage requirements from %%{version} to %%{version}-%%{release}
- Back out the pipe patch.

* Mon Jul 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.1.1p4, which includes fixes for config file parsing problems.
- Move the init script back.
- Add Damien's quick fix for wackiness.

* Wed Jul 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.1.1p3, which includes fixes for X11 forwarding and strtok().

* Thu Jul  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- Move condrestart to server postun.
- Move key generation to init script.
- Actually use the right patch for moving the key generation to the init script.
- Clean up the init script a bit.

* Wed Jul  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- Fix X11 forwarding, from mail post by Chan Shih-Ping Richard.

* Sun Jul  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.1.1p2.
- Use of strtok() considered harmful.

* Sat Jul  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- Get the build root out of the man pages.

* Thu Jun 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- Add and use condrestart support in the init script.
- Add newer initscripts as a prereq.

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- Build in new environment (release 2)
- Move -clients subpackage to Applications/Internet group

* Fri Jun  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.2.1p1

* Sat Jun  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- Patch to build with neither RSA nor RSAref.
- Miscellaneous FHS-compliance tweaks.
- Fix for possibly-compressed man pages.

* Wed Mar 15 2000 Damien Miller <djm@ibs.com.au>
- Updated for new location
- Updated for new gnome-ssh-askpass build

* Sun Dec 26 1999 Damien Miller <djm@mindrot.org>
- Added Jim Knoble's <jmknoble@pobox.com> askpass

* Mon Nov 15 1999 Damien Miller <djm@mindrot.org>
- Split subpackages further based on patch from jim knoble <jmknoble@pobox.com>

* Sat Nov 13 1999 Damien Miller <djm@mindrot.org>
- Added 'Obsoletes' directives

* Tue Nov 09 1999 Damien Miller <djm@ibs.com.au>
- Use make install
- Subpackages

* Mon Nov 08 1999 Damien Miller <djm@ibs.com.au>
- Added links for slogin
- Fixed perms on manpages

* Sat Oct 30 1999 Damien Miller <djm@ibs.com.au>
- Renamed init script

* Fri Oct 29 1999 Damien Miller <djm@ibs.com.au>
- Back to old binary names

* Thu Oct 28 1999 Damien Miller <djm@ibs.com.au>
- Use autoconf
- New binary names

* Wed Oct 27 1999 Damien Miller <djm@ibs.com.au>
- Initial RPMification, based on Jan "Yenya" Kasprzak's <kas@fi.muni.cz> spec.
