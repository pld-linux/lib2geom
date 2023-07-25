#
# Conditional build:
%bcond_without	python	# Python bindings
#
Summary:	2Geom - easy 2D graphics library
Summary(pl.UTF-8):	2Geom - łatwa biblioteka do grafiki 2D
Name:		lib2geom
Version:	1.2.2
Release:	2
License:	LGPL v2.1 or MPL v1.1
Group:		Libraries
#Source0Download: https://gitlab.com/inkscape/lib2geom/-/tags
Source0:	https://gitlab.com/inkscape/lib2geom/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	814eb0c98fe9ae1ddbd1a36a361b81d8
Patch0:		%{name}-pc.patch
Patch1:		%{name}-python-install.patch
URL:		https://gitlab.com/inkscape/lib2geom
BuildRequires:	boost-devel >= 1.60
%{?with_python:BuildRequires:	boost-python3-devel >= 1.60}
BuildRequires:	cairo-devel
BuildRequires:	cmake >= 3.12
BuildRequires:	double-conversion-devel
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gsl-devel
BuildRequires:	gtk+3-devel >= 3.0
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python3-Cython >= 0.16}
%{?with_python:BuildRequires:	python3-devel >= 1:3.2}
%{?with_python:BuildRequires:	python3-modules >= 1:3.2}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
2Geom is a C++ 2D geometry library geared towards robust processing of
computational geometry data associated with vector graphics. The
primary design consideration is ease of use and clarity. It is
dual-licensed under LGPL 2.1 and MPL 1.1.

%description -l pl.UTF-8
2Geom to biblioteka C++ do geometrii 2D, nakierowana głównie na bogate
przetwarzanie danych geometrii obliczeniowej, związanych z grafiką
wektorową. Główne założenia projektowe to łatwość użycia i
przejrzystość. Kod biblioteki jest na podwójnej licencji LGPL 2.1 i
MPL 1.1.

%package devel
Summary:	Header files for 2Geom library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki 2Geom
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel >= 1.60
Requires:	gsl-devel
Requires:	libstdc++-devel >= 6:7

%description devel
Header files for 2Geom library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki 2Geom.

%package -n python3-py2geom
Summary:	Python bindings for lib2geom
Summary(pl.UTF-8):	Wiązania Pythona do lib2geom
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-py2geom
Boost-based Python bindings for lib2geom.

%description -n python3-py2geom -l pl.UTF-8
Wiązania Pythona do lib2geom oparte na bibliotece Boost.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake .. \
	-D2GEOM_TESTING:BOOL=OFF \
	-D2GEOM_BUILD_SHARED=ON \
	%{?with_python:-DCYTHON_EXECUTABLE=/usr/bin/cython3} \
	%{?with_python:-D2GEOM_BOOST_PYTHON=ON} \
	%{?with_python:-D2GEOM_CYTHON_BINDINGS=ON} \
	-DCMAKE_SKIP_RPATH=ON \
	-DPYTHON3_SITEARCH_INSTALL_DIR=%{py3_sitedir}

%{__make}

%if %{with python}
# cy2geom code seems outdated
#%{__make} -C src/cython

%{__make} -C src/py2geom
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python}
%{__make} -C build/src/py2geom install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.md LICENSE.md NEWS.md README.md TODO.md
%attr(755,root,root) %{_libdir}/lib2geom.so.1.2.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib2geom.so
%{_includedir}/2geom-%{version}
%{_pkgconfigdir}/2geom.pc
%{_libdir}/cmake/2Geom

%if %{with python}
%files -n python3-py2geom
%defattr(644,root,root,755)
%dir %{py3_sitedir}/py2geom
%{py3_sitedir}/py2geom/__pycache__
%{py3_sitedir}/py2geom/__init__.py
%attr(755,root,root) %{py3_sitedir}/py2geom/_py2geom.so
%endif
