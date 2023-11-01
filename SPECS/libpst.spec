%global python2_sybpackage 0

Summary:            Utilities to convert Outlook .pst files to other formats
Name:               libpst
Version:            0.6.71
Release:            8%{?dist}
License:            GPLv2+
Source:             http://www.five-ten-sg.com/%{name}/packages/%{name}-%{version}.tar.gz
URL:                http://www.five-ten-sg.com/%{name}/
Requires:           libgsf
Requires:           %{name}-libs = %{version}-%{release}
BuildRequires:      libtool
BuildRequires:      gd-devel zlib-devel boost-devel libgsf-devel

%if %{python2_sybpackage}
BuildRequires:      python2-devel
%endif

%description
The Libpst utilities include readpst which can convert email messages
to both mbox and MH mailbox formats, pst2ldif which can convert the
contacts to .ldif format for import into ldap databases, and pst2dii
which can convert email messages to the DII load file format used by
Summation.


%package libs
Summary:            Shared library used by the pst utilities

%description libs
The libpst-libs package contains the shared library used by the pst
utilities.


%if %{python2_sybpackage}

%package -n python2-libpst
%{?python_provide:%python_provide python2-libpst}
# Remove before F30
Provides: %{name}-python2 = %{version}-%{release}
Provides: %{name}-python2%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python2 < %{version}-%{release}
Summary:            Python bindings for libpst
Requires:           %{name}-libs = %{version}-%{release}

%description -n python2-libpst
The libpst-python package allows you to use the libpst shared object
from python code.

%endif

%package devel
Summary:            Library links and header files for libpst application development
Requires:           pkgconfig
Requires:           %{name}-libs = %{version}-%{release}

%description devel
The libpst-devel package contains the library links and header files
you'll need to develop applications using the libpst shared library.
You do not need to install it if you just want to use the libpst
utilities.


%package devel-doc
Summary:            Documentation for libpst.so for libpst application development
Requires:           %{name}-doc = %{version}-%{release}

%description devel-doc
The libpst-devel-doc package contains the doxygen generated
documentation for the libpst.so shared library.


%package doc
Summary:            Documentation for the pst utilities in html format

%description doc
The libpst-doc package contains the html documentation for the pst
utilities.  You do not need to install it if you just want to use the
libpst utilities.



%prep
%setup -q


%build
autoreconf -v -f -i
%configure \
%if %{python2_sybpackage}
	--enable-python \
%else
	--disable-python \
%endif
	--enable-libpst-shared
%make_build


%install
%make_install
rm $RPM_BUILD_ROOT%{_libdir}/libpst.la
rm $RPM_BUILD_ROOT%{_libdir}/libpst.a
mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/doc/%{name}


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*


%files libs
%{_libdir}/libpst.so.*
%doc COPYING


%if %{python2_sybpackage}

%files -n python2-libpst
%{python2_sitearch}/_*.so
%exclude %{python2_sitearch}/*.a
%exclude %{python2_sitearch}/*.la

%endif


%files devel
%{_libdir}/libpst.so
%{_includedir}/%{name}-4/
%{_libdir}/pkgconfig/libpst.pc


%files devel-doc
%{_datadir}/doc/%{name}/devel/


%files doc
%dir %{_datadir}/doc/%{name}/
%{_datadir}/doc/%{name}/*.html
%{_datadir}/doc/%{name}/AUTHORS
%{_datadir}/doc/%{name}/COPYING
%{_datadir}/doc/%{name}/ChangeLog
%{_datadir}/doc/%{name}/NEWS
%{_datadir}/doc/%{name}/README


%changelog
* Mon Apr 09 2018 Milan Crha <mcrha@redhat.com> - 0.6.71-8
- Remove dependency on ImageMagick

* Wed Mar 28 2018 Milan Crha <mcrha@redhat.com> - 0.6.71-7
- Disable python2 subpackage

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.6.71-6
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.6.71-5
- Python 2 binary package renamed to python2-libpst
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.6.71-4
- Python 2 binary package renamed to python2-libpst
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.71-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Carl Byington <carl@five-ten-sg.com> 0.6.71-1
- fedora python naming scheme changes
- Zachary Travis - Add support for the OST 2013 format, and
  Content-Disposition filename key fix for outlook compatibility

* Thu Jul 20 2017 Kalev Lember <klember@redhat.com> - 0.6.70-3
- Rebuilt for Boost 1.64

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.6.70-2
- Rebuild due to bug in RPM (RHBZ #1468476)

* Wed Feb 08 2017 Carl Byington <carl@five-ten-sg.com> 0.6.70-1
- Jeffrey Morlan - pst_getID2 must not recurse into children

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 0.6.69-2
- Rebuilt for Boost 1.63

* Sat Oct 29 2016 Carl Byington <carl@five-ten-sg.com> 0.6.69-1
- fix bugs in code allowing folders containing multiple item types

* Mon Aug 29 2016 Carl Byington <carl@five-ten-sg.com> 0.6.68-1
- allow folders containing multiple item types, e.g. email and calendar
- better detection of valid internet headers

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.67-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jul 06 2016 Carl Byington <carl@five-ten-sg.com> 0.6.67-1
- Jeffrey Morlan - multiple bug fixes and an optimization

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.66-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.6.66-2
- Rebuilt for Boost 1.60

* Mon Dec 21 2015 Carl Byington <carl@five-ten-sg.com> 0.6.66-1
- Igor Stroh - Added Content-ID header support

* Fri Sep 11 2015 Carl Byington <carl@five-ten-sg.com> 0.6.65-1
- Jeffrey Morlan - fix multiple Content-Type headers
- Hans Liss - debug level output

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.6.64-6
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.64-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.6.64-4
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.64-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.6.64-2
- Rebuilt for GCC 5 C++11 ABI change

* Mon Mar 09 2015 Carl Byington <carl@five-ten-sg.com> 0.6.64-1
- fix line wrap on python provides_exclude_from
- fix unchecked errors found by cppcheck
- AJ Shankar fixes for attachment processing and body encodings
  that contain embedded null chars.

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 0.6.63-5
- Rebuild for boost 1.57.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.63-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.63-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 David Tardon <dtardon@redhat.com> - 0.6.63-2
- rebuild for boost 1.55.0

* Fri Dec 27 2013 Carl Byington <carl@five-ten-sg.com> 0.6.63-1
- Daniel Gryniewicz found buffer overrun in LIST_COPY_TIME

* Sun Sep 22 2013 Carl Byington <carl@five-ten-sg.com> 0.6.62-1
- 983596 - Old dependency filter breaks file coloring

* Tue Aug 06 2013 Carl Byington <carl@five-ten-sg.com> 0.6.61-1
- move documentation to unversioned directory

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.59-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 0.6.59-3
- Rebuild for boost 1.54.0

* Wed Jun 12 2013 Carl Byington <carl@five-ten-sg.com> 0.6.60-1
- patch from Dominique Leuenberger to add AC_USE_SYSTEM_EXTENSIONS
- add readpst -a option for attachment stripping

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 0.6.59-2
- rebuild for new GD 2.1.0

* Fri May 17 2013 Carl Byington <carl@five-ten-sg.com> 0.6.59-1
- add autoconf checking for libgsf

* Fri Mar 29 2013 Carl Byington <carl@five-ten-sg.com> 0.6.58-4
- add autoreconf for aarch64

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.6.58-3
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.6.58-2
- Rebuild for Boost-1.53.0

* Fri Dec 28 2012 Carl Byington <carl@five-ten-sg.com> - 0.6.58-1
- fix From quoting on embedded rfc/822 messages

* Wed Dec 26 2012 Carl Byington <carl@five-ten-sg.com> - 0.6.57-1
- bugzilla 852414, remove unnecessary dependencies

* Mon Dec 24 2012 Carl Byington <carl@five-ten-sg.com> - 0.6.56-1
- filter private provides from rpm
- merge -m .msg files code into main branch

* Thu Aug 09 2012 Carl Byington <carl@five-ten-sg.com> - 0.6.55-2
- rebuild for python

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.54-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 08 2012 Carl Byington <carl@five-ten-sg.com> - 0.6.55-1
- preserve bcc headers
- document -C switch to set default character set
- space after colon is not required in header fields

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.54-5
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.54-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 24 2011 Carl Byington <carl@five-ten-sg.com> - 0.6.54-3
- bump versions and prep for fedora build

* Wed Nov 30 2011 Petr Pisar <ppisar@redhat.com> - 0.6.53-3
- Rebuild against boost-1.48

* Mon Nov 14 2011 Carl Byington <carl@five-ten-sg.com> - 0.6.54-2
- failed to bump version number

* Fri Nov 04 2011 Carl Byington <carl@five-ten-sg.com> - 0.6.54-1
- embedded rfc822 messages might contain rtf encoded bodies

* Fri Sep 02 2011 Petr Pisar <ppisar@redhat.com> - 0.6.53-2
- Rebuild against boost-1.47

* Sun Jul 10 2011 Carl Byington <carl@five-ten-sg.com> - 0.6.53-1
- add Status: header in output
- allow fork for parallel processing of individual email folders
  in separate mode
- proper handling of --with-boost-python option

* Sun May 22 2011 Carl Byington <carl@five-ten-sg.com> - 0.6.52-1
- fix dangling freed pointer in embedded rfc822 message processing
- allow broken outlook internet header field - it sometimes contains
  fragments of the message body rather than headers

* Sun Apr 17 2011 Carl Byington <carl@five-ten-sg.com> - 0.6.51-1
- fix for buffer overrun; attachment size from the secondary
  list of mapi elements overwrote proper size from the primary
  list of mapi elements.
  fedora bugzilla 696263

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.49-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Thomas Spura <tomspur@fedoraproject.org> - 0.6.49-3
- rebuild for new boost

* Fri Dec 24 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.50-1
- rfc2047 and rfc2231 encoding for non-ascii headers and
  attachment filenames.

* Wed Sep 29 2010 jkeating - 0.6.49-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.49-1
- fix to ignore embedded objects that are not email messages
  fedora bugzilla 633498

* Thu Sep 02 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.48-1
- fix for broken internet headers from Outlook
- fix ax_python.m4 to look for python2.7
- use mboxrd from quoting for output formats with multiple messages per file
- use no from quoting for output formats with single message per file

* Sat Jul 31 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.47-6
- rebuild for python dependencies

* Mon Jul 26 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.47-4
- hack up configure so that it looks for python 2.7

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.47-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 07 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.47-2
- Subpackage Licensing, add COPYING to -libs.
- patches from Kenneth Berland for solaris

* Fri May 07 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.47-1
- patches from Kenneth Berland for solaris

* Thu Jan 21 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.46-1
- prefer libpthread over librt for finding sem_init function.

* Thu Jan 21 2010 Carl Byington <carl@five-ten-sg.com> - 0.6.45-2
- rebuild for new boost package

* Wed Nov 18 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.45-1
- patch from Hugo DesRosiers to export categories and notes into vcards.
- extend that patch to export categories into vcalendar appointments also.

* Sun Sep 20 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.44-1
- patch from Lee Ayres to add file name extensions in separate mode.
- allow mixed items types in a folder in separate mode.

* Sat Sep 12 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.43-1
- decode more of the pst format, some minor bug fixes
- add support for code pages 1200 and 1201.
- add readpst -t option to select output item types, which can
  now be used to process folders containing mixed item types.
- fix segfault with embedded appointments
- add readpst -u option for Thunderbird mode .size and .type files
- better detection of embedded rfc822 message attachments

* Thu Sep 03 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.42-1
- patch from Fridrich Strba to build with DJGPP DOS cross-compiler.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.41-1
- fix ax_python detection - should not use locate command
- checking for fedora versions is not needed

* Tue Jun 23 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.40-1
- fedora 11 has python2.6
- remove pdf version of the man pages

* Sun Jun 21 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.39-1
- fedora > 10 moved to boost-python-devel

* Sun Jun 21 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.38-1
- add python interface to the shared library.
- bump soname to version 4 for many changes to the interface.
- better decoding of recurrence data in appointments.
- remove readpstlog since debug log files are now plain text.
- add readpst -j option for parallel jobs for each folder.
- make nested mime multipart/alternative to hold the text/html parts.

* Fri Apr 17 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.37-1
- add pst_attach_to_mem() back into the shared library interface.
- fix memory leak caught by valgrind.

* Tue Apr 14 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.36-1
- build separate -doc and -devel-doc subpackages.
- other spec file cleanup

* Wed Apr 08 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.35-1
- properly add trailing mime boundary in all modes.
- build separate libpst, libpst-libs, libpst-devel rpms.

* Thu Mar 19 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.34-1
- avoid putting mixed item types into the same output folder.

* Tue Mar 17 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.33-1
- compensate for iconv conversion to utf-7 that produces strings that
  are not null terminated.
- don't produce empty attachment files in separate mode.

* Sat Mar 14 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.32-1
- fix ppc64 compile error

* Sat Mar 14 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.31-1
- bump version for fedora cvs tagging mistake

* Sat Mar 14 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.30-1
- track character set individually for each mapi element.
- remove charset option from pst2ldif since we get that from each
  object now.
- avoid emitting bogus empty email messages into contacts and
  calendar files.

* Tue Feb 24 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.29-1
- fix for 64bit on Fedora 11

* Tue Feb 24 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.28-1
- improve decoding of multipart/report and message/rfc822 mime types.
- improve character set handling.
- fix embedded rfc822 messages with attachments.

* Sat Feb 07 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.27-1
- fix for const correctness on Fedora 11

* Sat Feb 07 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.26-1
- patch from Fridrich Strba for building on mingw and general
- cleanup of autoconf files.
- add processing for pst files of type 0x0f.
- strip and regenerate all MIME headers to avoid duplicates.
- do a better job of making unique MIME boundaries.
- only use base64 coding when strictly necessary.

* Fri Jan 16 2009 Carl Byington <carl@five-ten-sg.com> - 0.6.25-1
- improve handling of content-type charset values in mime parts

* Thu Dec 11 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.24-1
- patch from Chris Eagle to build on cygwin

* Thu Dec 04 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.23-1
- bump version to avoid cvs tagging mistake in fedora

* Fri Nov 28 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.22-1
- patch from David Cuadrado to process emails with type PST_TYPE_OTHER
- base64_encode_multiple() may insert newline, needs larger malloc
- subject lines shorter than 2 bytes could segfault

* Tue Oct 21 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.21-1
- fix title bug with old schema in pst2ldif.
- also escape commas in distinguished names per rfc4514.

* Thu Oct 09 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.20-1
- add configure option --enable-dii=no to remove dependency on libgd.
- many fixes in pst2ldif by Robert Harris.
- add -D option to include deleted items, from Justin Greer
- fix from Justin Greer to add missing email headers
- fix from Justin Greer for my_stristr()
- fix for orphan children when building descriptor tree
- avoid writing uninitialized data to debug log file
- remove unreachable code
- create dummy top-of-folder descriptor if needed for corrupt pst files

* Sun Sep 14 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.19-1
- Fix base64 encoding that could create long lines.
- Initial work on a .so shared library from Bharath Acharya.

* Thu Aug 28 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.18-1
- Fixes for iconv on Mac from Justin Greer.

* Tue Aug 05 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.17-1
- More fixes for 32/64 bit portability on big endian ppc.

* Tue Aug 05 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.16-1
- Use inttypes.h for portable printing of 64 bit items.

* Wed Jul 30 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.15-1
- Patch from Robert Simpson for file handle leak in error case.
- Fix for missing length on lz decompression, bug found by Chris White.

* Sun Jun 15 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.14-1
- Fix my mistake in debian packaging.

* Fri Jun 13 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.13-1
- Patch from Robert Simpson for encryption type 2.

* Tue Jun 10 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.12-1
- Patch from Joachim Metz for debian packaging and
- fix for incorrect length on lz decompression

* Tue Jun 03 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.11-1
- Use ftello/fseeko to properly handle large files.
- Document and properly use datasize field in b5 blocks.
- Fix some MSVC compile issues and collect MSVC dependencies into one place.

* Thu May 29 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.10-1
- Patch from Robert Simpson for doubly-linked list code and arrays of unicode strings.

* Fri May 16 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.9
- Patch from Joachim Metz for 64 bit compile.
- Fix pst format documentation for 8 byte backpointers.

* Wed Mar 05 2008 Carl Byington <carl@five-ten-sg.com> - 0.6.8
- Initial version of pst2dii to convert to Summation dii load file format
- changes for Fedora packaging guidelines (#434727)

* Tue Jul 10 2007 Carl Byington <carl@five-ten-sg.com> - 0.5.5
- merge changes from Joe Nahmias version

* Sun Feb 19 2006 Carl Byington <carl@five-ten-sg.com> - 0.5.3
- initial spec file using autoconf and http://www.fedora.us/docs/rpm-packaging-guidelines.html

