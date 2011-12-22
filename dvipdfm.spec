# This macros need to match what is in the texlive-texmf package. Here
# we define it in case it's not set.
%{!?_texmf_main: %define _texmf_main %{_datadir}/texmf}

Name:           dvipdfm
Version:        0.13.2d
Release:        41.1%{?dist}
Summary:        A DVI to PDF translator

Group:          Applications/Publishing
License:        GPLv2+
URL:            http://gaspra.kettering.edu/dvipdfm/
Source0:        http://gaspra.kettering.edu/dvipdfm/%{name}-%{version}.tar.gz

# The following sources are taken from the TeXLive 2007 modified version of dvipdfm
Source1:        dvipdft
Source2:        dvipdft.1
Source3:        ebb.1
Source4:        dvipdfm-config

# These two fix up security issues associated with predicatble temp files
Patch0:         dvipdfm-0.13.2d-security.patch
Patch1:         dvipdfm-0.13.2d-dvipdft-security.patch

# The following patch contains miscellaneous fixes taken from the TeXLive 2007 sources
Patch2:         dvipdfm-0.13.2d-texlive2007.patch

# This patch fixes a bug seen when handling dvi files with included postscript
# images.
# https://bugzilla.redhat.com/show_bug.cgi?id=453283
# https://bugzilla.redhat.com/show_bug.cgi?id=228078
Patch3:		dvipdfm-0.13.2d-pdfobj-fix.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  zlib-devel kpathsea-devel 
BuildRequires:  tex(tex)

Requires:       ghostscript tex(dvips) tex(tex)
Requires(post): /usr/bin/mktexlsr
Requires(postun): /usr/bin/mktexlsr

%description
DVIPDFM is a DVI to PDF translator developed by Mark A. Wicks.

%prep
%setup -q -n %{name}
rm dvipdft
mv config config.original
cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} .
mv dvipdfm-config config

%patch0 -p3 -b .security
%patch1 -p1 -b .dvipdft-security
%patch2 -p1 -b .texlive2007
%patch3 -p1 -b .pdfobj-fix

# Add extra man pages to Makefile.in to ensure they're installed
sed -i -e 's/manpages=dvipdfm.1/manpages=dvipdfm.1 dvipdft.1 ebb.1/' Makefile.in

# Ensure manpages are utf-8
for i in dvipdft.1 ebb.1 ; do
    iconv -f ISO-8859-1 -t UTF8 $i > $i.utf8 && touch -r $i $i.utf8 && mv $i.utf8 $i
done

%build
%configure
make %{?_smp_mflags}

pushd doc
tex dvipdfm
../dvipdfm dvipdfm
popd

%install
rm -rf $RPM_BUILD_ROOT

# Makefile doesn't respect DESTDIR, so we have to use this hack
%makeinstall INSTALL='install -p'

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/mktexlsr > /dev/null 2>&1 || :

%postun
/usr/bin/mktexlsr > /dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING Credits README NEWS  latex-support config.original
%doc doc/dvipdfm.dvi doc/dvipdfm.pdf
%{_bindir}/ebb
%{_bindir}/dvipdfm
%{_bindir}/dvipdft
%{_texmf_main}/dvipdfm/base
%{_texmf_main}/dvipdfm/config
%{_mandir}/man1/dvipdfm.1*
%{_mandir}/man1/dvipdft.1*
%{_mandir}/man1/ebb.1*

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.13.2d-41.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.2d-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.2d-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jun 28 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.13.2d-39
- Add dvipdfm-0.13.2d-pdfobj-fix.patch to fix BZ 453283 and 228078

* Sun Apr 27 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.13.2d-38
- Untabify spec file
- Ensure dvipdft is not executeable in SRPM
- Ensure man pages are UTF-8
- Fix comment about tex(tex) 

* Sat Apr 26 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.13.2d-37
- Fix comment about texlive-texmf [tex(tex)] BuildRequires
- Rename config file tp dvipdfm-config in SRPM
- Add INSTALL='install -p' to makeinstall
- Run mktexlsr on install

* Sun Apr 14 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.13.2d-36
- Fix URL
- Cherry pick changes made by TeXLive 2007
- Build dvi and pdf docs
- Add Requires for tex(tex)
- Add security fix patches for temp file creation

* Sat Mar  8 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.13.2d-35
- Initial separate package - formerly part of texlive

