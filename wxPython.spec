%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define buildflags WXPORT=gtk2 UNICODE=1

Name:           wxPython
Version:        2.6.3.2
Release:        2%{?dist}

Summary:        GUI toolkit for the Python programming language

Group:          Development/Languages
License:        LGPL
URL:            http://www.wxpython.org/
Source0:        http://dl.sf.net/wxpython/wxPython-src-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  wxGTK-devel = 2.6.3, pkgconfig
BuildRequires:  zlib-devel, libpng-devel, libjpeg-devel, libtiff-devel
BuildRequires:  libGL-devel, libGLU-devel
BuildRequires:  python-devel, wxGTK-gl

# packages should depend on "wxPython", not "wxPythonGTK2", but in case
# one does, here's the provides for it.
Provides:       wxPythonGTK2 = %{version}-%{release}

%description
wxPython is a GUI toolkit for the Python programming language. It allows
Python programmers to create programs with a robust, highly functional
graphical user interface, simply and easily. It is implemented as a Python
extension module (native code) that wraps the popular wxWindows cross
platform GUI library, which is written in C++.

%package        devel
Group:          Development/Libraries
Summary:        Development files for wxPython add-on modules
Requires:       %{name} = %{version}-%{release}
Requires:       wxGTK-devel

%description devel
This package includes C++ header files and SWIG files needed for developing
add-on modules for wxPython. It is NOT needed for development of most
programs which use the wxPython toolkit.


%prep
%setup -q -n wxPython-src-%{version}


%build
# Just build the wxPython part, not all of wxWindows which we already have
# in Fedora
cd wxPython
# included distutils is not multilib aware; use normal
rm -rf distutils
python setup.py %{buildflags} build


%install
rm -rf $RPM_BUILD_ROOT
cd wxPython
python setup.py %{buildflags} install --root=$RPM_BUILD_ROOT

# this is a kludge....
%if "%{python_sitelib}" != "%{python_sitearch}"
mv $RPM_BUILD_ROOT%{python_sitelib}/wx.pth  $RPM_BUILD_ROOT%{python_sitearch}
mv $RPM_BUILD_ROOT%{python_sitelib}/wxversion.py* $RPM_BUILD_ROOT%{python_sitearch}
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc wxPython/docs wxPython/demo wxPython/licence/ wxPython/samples
%{_bindir}/*
%{python_sitearch}/wx.pth
%{python_sitearch}/wxversion.py*
%dir %{python_sitearch}/wx-2.6-gtk2-unicode/
%{python_sitearch}/wx-2.6-gtk2-unicode/wx
%{python_sitearch}/wx-2.6-gtk2-unicode/wxPython

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/wx-2.6/wx/wxPython
%{_includedir}/wx-2.6/wx/wxPython/*.h
%dir %{_includedir}/wx-2.6/wx/wxPython/i_files
%{_includedir}/wx-2.6/wx/wxPython/i_files/*.i
%{_includedir}/wx-2.6/wx/wxPython/i_files/*.py*
%{_includedir}/wx-2.6/wx/wxPython/i_files/*.swg


%changelog
* Mon Aug 28 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.2-2
- bump release for FC6 rebuild

* Thu Apr 13 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.2-1
- version 2.6.3.2
- move wxversion.py _into_ lib64. Apparently that's the right thing to do. :)
- upstream tarball no longer includes embedded.o (since I finally got around
  to pointing that out to the developers instead of just kludging it away.)
- buildrequires to just libGLU-devel instead of mesa-libGL-devel

* Fri Mar 31 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.0-4
- grr. bump relnumber.

* Fri Mar 31 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.0-3
- oh yeah -- wxversion.py not lib64.

* Fri Mar 31 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.0-2
- buildrequires mesa-libGLU-devel

* Thu Mar 30 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.0-1
- update to 2.6.3.0
- wxGTK and wxPython versions are inexorably linked; make BuildRequires
  be exact, rather than >=.
- make devel subpackage as per comment #7 in bug #163440.

* Thu Nov 24 2005 Matthew Miller <mattdm@mattdm.org> - 2.6.1.0-1
- update to 2.6.0.0
- merge in changes from current extras 2.4.x package
- Happy Thanksgiving
- build animate extention again -- works now.

* Thu Apr 28 2005 Matthew Miller <mattdm@bu.edu> - 2.6.0.0-bu45.1
- get rid of accidental binaries in source tarball -- they generates
  spurious dependencies and serve no purpose
- update to 2.6.0.0 and build for Velouria
- switch to Fedora Extras base spec file
- enable gtk2 and unicode and all the code stuff (as FE does)
- disable BUILD_ANIMATE extension from contrib -- doesn't build
- files are in a different location now -- adjust to that
- zap include files (needed only for building wxPython 3rd-party modules),
  because I don't think this is likely to be very useful. Other option
  would be to create a -devel package, but I think that'd be confusing.

* Tue Feb 08 2005 Thorsten Leemhuis <fedora at leemhuis dot info> 0:2.4.2.4-4
- remove included disutils - it is not multilib aware; this
  fixes build on x86_64

* Tue Jan 06 2004 Panu Matilainen <pmatilai@welho.com> 0:2.4.2.4-0.fdr.3
- rename package to wxPythonGTK2, provide wxPython (see bug 927)
- dont ship binaries in /usr/share

* Thu Nov 20 2003 Panu Matilainen <pmatilai@welho.com> 0:2.4.2.4-0.fdr.2
- add missing buildrequires: python-devel, wxGTK2-gl

* Sun Nov 02 2003 Panu Matilainen <pmatilai@welho.com> 0:2.4.2.4-0.fdr.1
- Initial RPM release.
~
