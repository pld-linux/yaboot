Summary:	Linux bootloader for Power Macintosh "New World" computers
Summary(pl):	Bootloader dla komputer�w Power Macintosh "New World"
Name:		yaboot
Version:	1.3.6
Release:	2
License:	GPL
Group:		Applications/System
Source0:	http://penguinppc.org/projects/yaboot/%{name}-%{version}.tar.gz
Patch0:		%{name}-man.patch
Patch1:		%{name}-user.patch
Patch2:		%{name}-bash.patch
Requires:	hfsutils >= 3.2.0
Requires:	bash >= 2.0
URL:		http://penguinppc.org/projects/yaboot/
ExclusiveArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	ybin

%description
yaboot is a bootloader for PowerPC machines which works on New World
ROM machines (Rev. A iMac and newer) and runs directly from Open
Firmware, eliminating the need for Mac OS.

%description -l pl
yaboot to bootloader dla maszyn PowerPC, kt�ry dziala na maszynach New
World ROM (rewizja A iMac oraz nowsze) oraz pracuje bezposrednio z
Open Firmware przez co nie trzeba stosowac Mac OS.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	ROOT=$RPM_BUILD_ROOT \
	PREFIX=/ \
	MANDIR=%{_mandir}

gzip -9nf BUGS README THANKS TODO changelog doc/README.* doc/examples/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz doc/*.gz doc/examples doc/yaboot-howto.html
%attr(755,root,root) /sbin/*
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%dir /lib/%{name}
%attr(755,root,root) /lib/%{name}/addnote
/lib/%{name}/*boot
%{_mandir}/man?/*
