# TODO
# - pldize initscript
# - unbash initscript
# - recheck deps
Summary:	Simple and powerful firewall and traffic shaping languages
Name:		firehol
Version:	2.0.1
Release:	0.1
License:	GPL v2+
Group:		Applications/Networking
Source0:	http://firehol.org/download/firehol/releases/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	e2672c82b2b6012f9000c15c08c7dc89
Source1:	%{name}.service
Source2:	fireqos.service
URL:		http://firehol.org
BuildRequires:	hostname
BuildRequires:	iproute2
BuildRequires:	iptables
BuildRequires:	procps
BuildRequires:	systemd-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,preun):	/sbin/chkconfig
Requires:	coreutils
Requires:	gawk >= 3.0
Requires:	grep >= 2.4.2
Requires:	gzip
Requires:	hostname
Requires:	iproute2 >= 2.2.4
Requires:	iptables >= 1.2.4
Requires:	kmod
Requires:	less
Requires:	procps
Requires:	rc-scripts
Requires:	sed
Requires:	uname(release) >= 2.4
Requires:	util-linux >= 2.11
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

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# Hack for documentation without crufts.
rm -frv $RPM_BUILD_ROOT%{_docdir}
find examples/ -name "Makefile*" -delete -print

# Install systemd units.
install -d $RPM_BUILD_ROOT%{systemdunitdir}
cp -p %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}

# Install runtime directories.
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/services
install -d $RPM_BUILD_ROOT%{_localstatedir}/spool/firehol

# Ghost configurations.
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/firehol.conf \
      $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/fireqos.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add firehol
%service firehol restart
%systemd_post firehol.service
%systemd_post fireqos.service

%preun
if [ "$1" = 0 ]; then
	%service firehol stop
	/sbin/chkconfig --del firehol
fi
%systemd_preun firehol.service
%systemd_preun fireqos.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README THANKS examples
%doc doc/firehol/firehol-manual.{pdf,html}
%doc doc/fireqos/fireqos-manual.{pdf,html}
%dir %{_sysconfdir}/firehol
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/firehol.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/fireqos.conf
%{_sysconfdir}/%{name}/*.example
%dir %{_sysconfdir}/%{name}/services
%{_sysconfdir}/%{name}/services/*.example
%attr(755,root,root) %{_sbindir}/firehol
%attr(755,root,root) %{_sbindir}/fireqos
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{systemdunitdir}/firehol.service
%{systemdunitdir}/fireqos.service
%{_localstatedir}/spool/%{name}
