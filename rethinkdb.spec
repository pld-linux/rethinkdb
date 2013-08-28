Summary:	RethinkDB - the database for solid drives
Name:		rethinkdb
Version:	1.8.1
Release:	0.1
License:	AGPL
Group:		Development/Tools
Source0:	https://github.com/rethinkdb/rethinkdb/archive/v%{version}.tar.gz
# Source0-md5:	466aaf278ae9cf9a57f126c34f068118
URL:		http://www.rethinkdb.com/
BuildRequires:	bash
BuildRequires:	boost-devel >= 1.40
BuildRequires:	git-core
BuildRequires:	libstdc++-devel
BuildRequires:	m4
BuildRequires:	nodejs-devel
BuildRequires:	npm
BuildRequires:	openssl-devel
BuildRequires:	protobuf-devel
BuildRequires:	python-PyYAML
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
BuildRequires:	v8-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RethinkDB is an open-source distributed database. It has an intuitive
query language, automatically parallelized queries, and simple
administration.

%prep
%setup -q

%{__sed} -i -e '1s,^#!.*python,#!%{__python},' scripts/backup/*.py

%build
CXX="%{__cxx}"
if [ "$CXX" != "${CXX#ccache }" ]; then
	ccache=--ccache
	CXX=${CXX#ccache }
fi

# NOTE: not autoconf based configure
./configure \
	CXX="$CXX" \
	CXXFLAGS="%{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags}" \
	--prefix %{_prefix} \
	--sysconfdir %{_sysconfdir} \
	--localstatedir %{_localstatedir} \
	--without-tcmalloc \
	$ccache \
	%{nil}

%{__make} \
	VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	init_dir=/etc/rc.d/init.d \
	STRIP_ON_INSTALL=0 \
	DESTDIR=$RPM_BUILD_ROOT

# omit the .py suffix, invoke tools directly without shell wrapper
for a in $RPM_BUILD_ROOT%{_bindir}/rethinkdb-*.py; do
	f=${a%.py}
	mv -f $a $f
done

%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/etc/bash_completion.d/rethinkdb.bash
%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}/copyright

%clean
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/rethinkdb/instances.d

%files
%defattr(644,root,root,755)
%doc README.md COPYRIGHT NOTES DEPENDENCIES
%dir %{_sysconfdir}/rethinkdb
%dir %{_sysconfdir}/rethinkdb/instances.d
%{_sysconfdir}/rethinkdb/default.conf.sample
%attr(754,root,root) /etc/rc.d/init.d/rethinkdb
%attr(755,root,root) %{_bindir}/rethinkdb
%attr(755,root,root) %{_bindir}/rethinkdb-dump
%attr(755,root,root) %{_bindir}/rethinkdb-export
%attr(755,root,root) %{_bindir}/rethinkdb-import
%attr(755,root,root) %{_bindir}/rethinkdb-restore
%{_mandir}/man1/rethinkdb.1*

/etc/bash_completion.d/rethinkdb.bash

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/web

%dir /var/lib/rethinkdb
%dir /var/lib/rethinkdb/instances.d
