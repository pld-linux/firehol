# TODO
# - pldize initscript
# - unbash initscript
# - recheck deps
# - update configure not to require tools at build time
Summary:	Simple and powerful firewall and traffic shaping languages
Name:		firehol
Version:	3.0.1
Release:	0.1
License:	GPL v2+
Group:		Applications/Networking
Source0:	https://firehol.org/download/firehol/releases/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	afee409b698ad0707340112ff0e811b2
Source1:	%{name}.service
Source2:	fireqos.service
URL:		https://firehol.org/
BuildRequires:	hostname
BuildRequires:	iprange >= 1.0.2
BuildRequires:	tar >= 1:1.22
BuildRequires:	wget
BuildRequires:	xz
Requires(post,preun):	/sbin/chkconfig
Requires:	coreutils
Requires:	gawk >= 3.0
Requires:	grep >= 2.4.2
Requires:	gzip
Requires:	hostname
Requires:	iproute2 >= 2.2.4
Requires:	ipset
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
# grep -E 'AX_NEED_PROG|AX_CHECK_PROG' configure.ac |sort -u|sed -rne 's/.+\(\[([^]]+)\], \[([^]]+)\].+/echo \1=`PATH=$PATH:\/usr\/sbin which \2` \\\\/p'|sh
%configure \
	BASH_SHELL_PATH=/bin/bash \
	BRIDGE=/sbin/bridge \
	CAT=/bin/cat \
	CHMOD=/bin/chmod \
	CHOWN=/bin/chown \
	CP=/bin/cp \
	CURL=/usr/bin/curl \
	CUT=/usr/bin/cut \
	DATE=/bin/date \
	DIFF=/usr/bin/diff \
	DIRNAME=/usr/bin/dirname \
	ENV=/usr/bin/env \
	EXPR=/usr/bin/expr \
	FIND=/usr/bin/find \
	FLOCK=/usr/bin/flock \
	FOLD=/usr/bin/fold \
	FUNZIP=/usr/bin/funzip \
	GAWK=/usr/bin/gawk \
	GIT=/usr/bin/git \
	HEAD=/usr/bin/head \
	HOSTNAMECMD=/bin/hostname \
	IP6TABLES=/usr/sbin/ip6tables \
	IP6TABLES_RESTORE=/usr/sbin/ip6tables-restore \
	IP6TABLES_SAVE=/usr/sbin/ip6tables-save \
	IP=/sbin/ip \
	IPRANGE=/usr/bin/iprange \
	IPSET=/usr/sbin/ipset \
	IPTABLES=/usr/sbin/iptables \
	IPTABLES_RESTORE=/usr/sbin/iptables-restore \
	IPTABLES_SAVE=/usr/sbin/iptables-save \
	LN=/bin/ln \
	LOGGER=/usr/bin/logger \
	LS=/bin/ls \
	LSMOD=/sbin/lsmod \
	MKDIR=/bin/mkdir \
	MKTEMP=/bin/mktemp \
	MODPROBE=/sbin/insmod \
	MODPROBE=/sbin/modprobe \
	MORE=/bin/more \
	MV=/bin/mv \
	NEATO=/usr/bin/neato \
	PING6=/usr/bin/ping6 \
	PING=/usr/bin/ping \
	RENICE=/usr/bin/renice \
	RM=/bin/rm \
	RMMOD=/sbin/rmmod \
	SCREEN=/usr/bin/screen \
	SEQ=/usr/bin/seq \
	SH=/bin/sh \
	SLEEP=/bin/sleep \
	SORT=/bin/sort \
	SS=/sbin/ss \
	STTY=/bin/stty \
	SYSCTL=/sbin/sysctl \
	TAIL=/usr/bin/tail \
	TAR=/bin/tar \
	TC=/sbin/tc \
	TCPDUMP=/usr/sbin/tcpdump \
	TOUCH=/bin/touch \
	TPUT=/usr/bin/tput \
	TR=/usr/bin/tr \
	TRACEROUTE=/usr/bin/traceroute \
	UNAME=/bin/uname \
	UNIQ=/usr/bin/uniq \
	UNZIP=/usr/bin/unzip \
	WC=/usr/bin/wc \
	WGET=/usr/bin/wget \
	WHOIS=/usr/bin/whois \
	ZCAT=/bin/zcat \
	%{nil}

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
%doc README THANKS examples
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
