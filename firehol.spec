# TODO
# - pldize initscript
# - unbash initscript
# - recheck deps
Summary:	A powerful yet easy to use iptables frontend
Name:		firehol
Version:	1.273
Release:	0.1
License:	GPL v2+
Group:		Applications/Networking
Source0:	http://downloads.sourceforge.net/firehol/%{name}-%{version}.tar.bz2
# Source0-md5:	cbbe1ba21cf44955827d5c906a55aa21
Patch0:		pld.patch
URL:		http://firehol.sourceforge.net
BuildRequires:	rpmbuild(macros) >= 1.228
Requires:	bash >= 2.04
Requires:	fileutils >= 4.0.36
Requires:	gawk >= 3.0
Requires:	grep >= 2.4.2
Requires:	iproute2 >= 2.2.4
Requires:	iptables >= 1.2.4
Requires:	kernel >= 2.4
Requires:	less
Requires:	modutils >= 2.4.13
Requires:	net-tools >= 1.57
Requires:	sed >= 3.02
Requires:	sh-utils >= 2.0
Requires:	textutils >= 2.0.11
Requires:	util-linux >= 2.11
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FireHOL is a generic firewall generator, meaning that you can design
any kind of local or routing stateful packet filtering firewalls with
ease. Install FireHOL if you want an easy way to configure stateful
packet filtering firewalls on Linux hosts and routers.

FireHOL uses an extremely simple but powerful way to define firewall
rules which it turns into complete stateful iptables firewalls.

You can run FireHOL with the 'helpme' argument, to get a configuration
file for the system run, which you can modify according to your needs.
The default configuration file will allow only client traffic on all
interfaces.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -D -p firehol.sh $RPM_BUILD_ROOT%{_initrddir}/firehol
install -D -p examples/client-all.conf $RPM_BUILD_ROOT%{_sysconfdir}/firehol/firehol.conf

# Install man files
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,5}
install -p man/*.1 $RPM_BUILD_ROOT/%{_mandir}/man1
install -p man/*.5 $RPM_BUILD_ROOT/%{_mandir}/man5

# Executables
install -d $RPM_BUILD_ROOT%{_libdir}/firehol
install -p *.sh $RPM_BUILD_ROOT%{_libdir}/firehol

# Install runtime directories
install -d $RPM_BUILD_ROOT%{_sysconfdir}/firehol/services
install -d $RPM_BUILD_ROOT%{_localstatedir}/spool/firehol

%post
/sbin/chkconfig --add firehol
%service firehol restart

%preun
if [ "$1" = 0 ]; then
	%service firehol stop
	/sbin/chkconfig --del firehol
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO ChangeLog WhatIsNew examples doc
%dir %{_sysconfdir}/firehol
%config(noreplace) %{_sysconfdir}/firehol/firehol.conf
%attr(754,root,root) /etc/rc.d/init.d/firehol
%{_libdir}/firehol
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_sysconfdir}/firehol/services
%{_localstatedir}/spool/firehol
