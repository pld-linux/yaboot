Summary:	Linux bootloader for Power Macintosh "New World" computers
Summary(pl):	Bootloader dla komputer�w Power Macintosh "New World"
Name:		yaboot
Version:	1.3.13
Release:	2
License:	GPL
Group:		Applications/System
Source0:	http://penguinppc.org/projects/yaboot/%{name}-%{version}.tar.gz
# Source0-md5:	f12798d1b2063f21d07e0ae7f602ccaf
Source1:	%{name}_functions.sh
Patch0:		%{name}-man.patch
Patch1:		%{name}-user.patch
Patch2:		%{name}-bash.patch
Patch3:		%{name}-crt0.patch
URL:		http://penguinppc.org/projects/yaboot/
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
yaboot to bootloader dla maszyn PowerPC, kt�ry dzia�a na maszynach New
World ROM (rewizja A iMac oraz nowsze) oraz pracuje bezpo�rednio z
Open Firmware, dzi�ki czemu nie trzeba stosowa� Mac OS.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	ROOT=$RPM_BUILD_ROOT \
	PREFIX=/ \
	MANDIR=%{_mandir}

install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-boot
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-boot

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BUGS README THANKS TODO changelog doc/README.* doc/yaboot-howto.html
%attr(644,root,root) /etc/sysconfig/rc-boot/%{name}_functions.sh
%attr(755,root,root) /sbin/*
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%dir /lib/%{name}
%attr(755,root,root) /lib/%{name}/addnote
/lib/%{name}/*boot
%{_mandir}/man?/*