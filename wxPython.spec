%define pyver %(python -c 'import sys ; print sys.version[:3]')

%define buildflags WXPORT=gtk2 UNICODE=1

Name:           wxPython
Version:        2.4.2.4
Release:        0.fdr.2.1
Epoch:          0
Summary:        wxPython is a GUI toolkit for the Python programming language.

Group:          Development/Languages
License:        LGPL
URL:            http://www.wxpython.org/
Source0:        http://dl.sf.net/wxpython/wxPythonSrc-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  wxGTK2-devel >= 0:2.4.2, pkgconfig
BuildRequires:	zlib-devel, libpng-devel, libjpeg-devel, libtiff-devel
BuildRequires:	python-devel, wxGTK2-gl
Requires:       %{_libdir}/python%{pyver}

%description
wxPython is a GUI toolkit for the Python programming language. It allows 
Python programmers to create programs with a robust, highly functional
graphical user interface, simply and easily. It is implemented as a Python 
extension module (native code) that wraps the popular wxWindows cross 
platform GUI library, which is written in C++.

%prep
%setup -q -n %{name}Src-%{version}

%build
# just build the wxPython part, not all of wxWindows which we already have
# in fedora...
cd wxPython
python setup.py %{buildflags} build

# this doesn't get built automatically, resulting in bogus libwx_gtk2-2.3.so.0
# dependency for the package
cd demo/dllwidget
make clean
make

%install
rm -rf $RPM_BUILD_ROOT
cd wxPython
python setup.py %{buildflags} install --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc wxPython/docs wxPython/demo wxPython/licence/ wxPython/samples 
%{_bindir}/*
%{_libdir}/python%{pyver}/site-packages/wxPython
%{_libdir}/python%{pyver}/site-packages/wx

%changelog
* Thu Nov 20 2003 Panu Matilainen <pmatilai@welho.com> 0:2.4.2.4-0.fdr.2
- add missing buildrequires: python-devel, wxGTK2-gl

* Sun Nov 02 2003 Panu Matilainen <pmatilai@welho.com> 0:2.4.2.4-0.fdr.1
- Initial RPM release.
