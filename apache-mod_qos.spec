%define		mod_name	qos
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: Quality Of Service
Name:		apache-mod_%{mod_name}
Version:	11.1
Release:	1
License:	Apache
Group:		Networking/Daemons/HTTP
Source0:	https://downloads.sourceforge.net/project/mod-qos/mod_qos-%{version}.tar.gz
# Source0-md5:	286d2d2b2f5abae9ccc48fa58f17dda1
Source1:	%{name}.conf
URL:		http://opensource.adnovum.ch/mod_qos/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.0
BuildRequires:	libpng-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apacheconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d
%define		apachelibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)

%description
mod_qos is a quality of service module for the Apache Web Server. It
implements control mechanisms that can provide different priority to
different requests and controls server access based on available
resources.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
cd tools
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-pcre=%{_bindir} \
	--with-png=%{_bindir} \
	--with-ssl=%{_prefix}
%{__make}
cd ..

%{apxs} -c -o mod_qos.la apache2/mod_qos.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{apachelibdir},%{apacheconfdir}}

%{__make} -C tools install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{apachelibdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{apacheconfdir}/97_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/*mod_*.conf
%attr(755,root,root) %{apachelibdir}/*.so
%attr(755,root,root) %{_bindir}/qs*
