#
%bcond_with	doc	# build documentation
#
Summary:	Linux bootloader for Power Macintosh "New World" computers
Summary(pl):	Bootloader dla komputerów Power Macintosh "New World"
Name:		yaboot
Version:	1.3.14
%define	_rc	rc1
Release:	0.%{_rc}.1
License:	GPL
Group:		Applications/System
Source0:	http://yaboot.ozlabs.org/snapshots/%{name}-%{version}%{_rc}.tar.gz
# Source0-md5:	d3ddbe0365db7b6af6e58054f60cf98a
Source1:	%{name}_functions.sh
Patch0:		%{name}-man.patch
Patch1:		%{name}-user.patch
Patch2:		%{name}-bash.patch
Patch3:		%{name}-crt0.patch
URL:		http://yaboot.ozlabs.org/
%if %{with doc}
BuildRequires:	debiandoc-sgml
BuildRequires:	opensp
%endif
BuildRequires:	sed >= 4.0
Requires:	bash >= 2.0
Requires:	hfsutils >= 3.2.0
Requires:	pmac-utils
Provides:	bootloader
Obsoletes:	quik
Obsoletes:	ybin
ExclusiveArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
yaboot is a bootloader for PowerPC machines which works on New World
ROM machines (Rev. A iMac and newer) and runs directly from Open
Firmware, eliminating the need for Mac OS.

%description -l pl
yaboot to bootloader dla maszyn PowerPC, który dzia³a na maszynach New
World ROM (rewizja A iMac oraz nowsze) oraz pracuje bezpo¶rednio z
Open Firmware, dziêki czemu nie trzeba stosowaæ Mac OS.

%prep
%setup -q -n %{name}-%{version}%{_rc}
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
sed -i '/VERSION=/s/=.*/=%{version}%{_rc}/' ybin/ybin

%build
%{__make} \
	CC="%{__cc}" \
	VERSION="%{version}%{_rc}"

%if %{with doc}
%{__make} -C doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	ROOT=$RPM_BUILD_ROOT \
	PREFIX=/ \
	MANDIR=%{_mandir} \
	VERSION="%{version}%{_rc}"

install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-boot
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-boot

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BUGS README THANKS TODO changelog doc/README.* doc/examples
%if %{with doc}
%doc doc/yaboot-howto.html
%endif
%attr(644,root,root) /etc/sysconfig/rc-boot/%{name}_functions.sh
%attr(755,root,root) /sbin/*
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%dir /lib/%{name}
%attr(755,root,root) /lib/%{name}/addnote
/lib/%{name}/*boot
%{_mandir}/man?/*
