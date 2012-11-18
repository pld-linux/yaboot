#
# Conditional build:
%bcond_without	doc	# build documentation
#
Summary:	Linux bootloader for Power Macintosh "New World" computers
Summary(pl.UTF-8):	Bootloader dla komputerów Power Macintosh "New World"
Name:		yaboot
Version:	1.3.17
Release:	0.1
License:	GPL v2+
Group:		Applications/System
Source0:	http://yaboot.ozlabs.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	f599f52d1887a86fd798252d2946f635
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
BuildRequires:	e2fsprogs-static
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

%description -l pl.UTF-8
yaboot to bootloader dla maszyn PowerPC, który działa na maszynach New
World ROM (rewizja A iMac oraz nowsze) oraz pracuje bezpośrednio z
Open Firmware, dzięki czemu nie trzeba stosować Mac OS.

%package -n rc-boot-yaboot
Summary:	yaboot support for rc-boot
Summary(pl.UTF-8):	Wsparcie yaboota dla rc-boot
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	rc-boot
Provides:	rc-boot-bootloader

%description -n rc-boot-yaboot
yaboot support for rc-boot.

%description -n rc-boot-yaboot -l pl.UTF-8
Wsparcie yaboota dla rc-boot.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__make} strip \
	CC="%{__cc}"

%if %{with doc}
%{__make} -C doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	ROOT=$RPM_BUILD_ROOT \
	PREFIX= \
	MANDIR=%{_mandir}

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
%attr(755,root,root) /sbin/mkofboot
%attr(755,root,root) /sbin/ofpath
%attr(755,root,root) /sbin/yabootconfig
%attr(755,root,root) /sbin/ybin
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%dir /lib/%{name}
%attr(755,root,root) /lib/%{name}/addnote
%attr(755,root,root) /lib/%{name}/ofboot
%attr(755,root,root) /lib/%{name}/yaboot
%{_mandir}/man5/yaboot.conf.5*
%{_mandir}/man8/bootstrap.8*
%{_mandir}/man8/mkofboot.8*
%{_mandir}/man8/ofpath.8*
%{_mandir}/man8/yaboot.8*
%{_mandir}/man8/yabootconfig.8*
%{_mandir}/man8/ybin.8*

%files -n rc-boot-yaboot
%defattr(644,root,root,755)
/etc/sysconfig/rc-boot/%{name}_functions.sh
