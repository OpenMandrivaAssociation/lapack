# lapack
%define	major	3
%define	minor	4.2
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}
%define	docname	%{name}-doc

# blas
%define	libblasname %mklibname blas %{major}
%define	develblasname %mklibname blas -d
%define	docblasname blas-doc

Summary:	LAPACK libraries for linear algebra
Name:		lapack
Version:	%{major}.%{minor}
Release:	1
License:	BSD-like
Group:		Sciences/Mathematics
URL:		http://www.netlib.org/lapack/
Source0:	http://www.netlib.org/lapack/%{name}-%{version}.tgz
Source1:	http://www.netlib.org/lapack/lapackqref.ps
Source2:	http://www.netlib.org/blas/blasqr.ps
Source3:	http://www.netlib.org/lapack/manpages.tgz
Patch2:		lapack-3.4.2-cmake-sover.patch
Patch3:		lapack-3.4.2-lib64.patch
BuildRequires:	gcc-gfortran
BuildRequires:	cmake
Obsoletes:	%{name} < 3.1.1

%description
LAPACK (Linear Algebra PACKage) is a standard library for numerical
linear algebra. LAPACK provides routines for solving systems of
simultaneous linear equations, least-squares solutions of linear
systems of equations, eigenvalue problems, and singular value
problems. Associated matrix factorizations (LU, Cholesky, QR, SVD,
Schur, and generalized Schur) and related computations (i.e.,
reordering of Schur factorizations and estimating condition numbers)
are also included. LAPACK can handle dense and banded matrices, but
not general sparse matrices. Similar functionality is provided for
real and complex matrices in both single and double precision. LAPACK
is coded in Fortran77 and built with gcc.

The lapack package provides the dynamic libraries for LAPACK/BLAS.

%package -n	%{libname}
Summary:	LAPACK libraries for linear algebra
Group:		Sciences/Mathematics
Provides:	lib%{name} = %{version}-%{release}
Obsoletes:	%{_lib}lapack3.2
Obsoletes:	%{_lib}lapack3.1

%description -n	%{libname}
LAPACK (Linear Algebra PACKage) is a standard library for numerical
linear algebra. LAPACK provides routines for solving systems of
simultaneous linear equations, least-squares solutions of linear
systems of equations, eigenvalue problems, and singular value
problems. Associated matrix factorizations (LU, Cholesky, QR, SVD,
Schur, and generalized Schur) and related computations (i.e.,
reordering of Schur factorizations and estimating condition numbers)
are also included. LAPACK can handle dense and banded matrices, but
not general sparse matrices. Similar functionality is provided for
real and complex matrices in both single and double precision. LAPACK
is coded in Fortran77 and built with gcc.

The lapack package provides the dynamic libraries for LAPACK/BLAS.

%package -n	%{devname}
Summary:	LAPACK static library
Group:		Sciences/Mathematics
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d %{name} %{major}
Requires:	blas-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the headers and development libraries
necessary to develop or compile applications using lapack.

%package -n	%{docname}
Summary:	Documentation for LAPACK
Group:		Sciences/Mathematics

%description -n %{docname}
Man pages / documentation for LAPACK.

%package -n	%{libblasname}
Summary:	The BLAS (Basic Linear Algebra Subprograms) library
Group:		Sciences/Mathematics
Provides:	libblas = %{version}-%{release}
Obsoletes:	%{mklibname blas 1.1}
Obsoletes:	%{_lib}blas3.2
Obsoletes:	%{_lib}blas3.1

%description -n	%{libblasname}
BLAS (Basic Linear Algebra Subprograms) is a standard library which
provides a number of basic algorithms for numerical algebra. Man
pages for blas are available in the blas-man package.

%package -n	%{develblasname}
Summary:	BLAS development libraries
Group:		Sciences/Mathematics
Requires:	%{libblasname} = %{version}-%{release}
Provides:	blas-devel = %{version}-%{release}
Provides:	libblas-devel = %{version}-%{release}
Obsoletes:	%{mklibname blas 1.1 -d} < 3.1.1
Requires:	gcc-gfortran

%description -n	%{develblasname}
BLAS development libraries for applications that link statically.

%package -n	%{docblasname}
Summary:	Documentation for BLAS
Group:		Sciences/Mathematics

%description -n	%{docblasname}
Man pages / documentation for BLAS.

%prep
%setup -q -a3
%patch2 -p1 -b .sover~
%patch3 -p1 -b .lib64~

cp %{SOURCE1} lapackqref.ps
cp %{SOURCE2} blasqr.ps

rm -f manpages/blas/man/manl/{csrot.l,lsame.l,xerbla.l,xerbla_array.l,zdrot.l}

%build
%cmake -DBUILD_STATIC_LIBS=ON -DBUILD_SHARED_LIBS=OFF -DBUILD_TESTING=OFF -DCMAKE_Fortran_COMPILER_FORCED=ON -DCMAKE_SHARED_LINKER_FLAGS=-lgfortran
%make
cd ..

%cmake -DBUILD_STATIC_LIBS=OFF -DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=OFF -DCMAKE_Fortran_COMPILER_FORCED=ON -DCMAKE_SHARED_LINKER_FLAGS=-lgfortran
%make

%install
%makeinstall_std -C build

install -m0644 build/lib/*.a %{buildroot}%{_libdir}/

mkdir -p %{buildroot}%{_mandir}/man3
touch lapack-man-pages
for file in manpages/man/manl/*; do
    install -m 644 $file %{buildroot}%{_mandir}/man3/`basename $file .l`.3
    echo %{_mandir}/man3/`basename $file .l`.3%{_extension} >> lapack-man-pages
done
touch blas-man-pages
for file in manpages/blas/man/manl/*; do
    install -m 644 $file %{buildroot}%{_mandir}/man3/`basename $file .l`.3
    echo %{_mandir}/man3/`basename $file .l`.3%{_extension} >> blas-man-pages
done

%files -n %{libname}
%{_libdir}/liblapack.so.%{major}*

%files -n %{devname}
%{_libdir}/liblapack.so
%{_libdir}/liblapack*.a
%{_libdir}/pkgconfig/lapack.pc
%{_libdir}/cmake/lapack-%{version}/lapack-*.cmake

%files -n %{docname} -f lapack-man-pages
%doc README lapackqref.ps

%files -n %{libblasname}
%{_libdir}/libblas.so.%{major}*

%files -n %{develblasname}
%{_libdir}/libblas.so
%{_libdir}/libblas*.a
%{_libdir}/pkgconfig/blas.pc

%files -n %{docblasname} -f blas-man-pages
%doc blasqr.ps


%changelog
* Wed May 18 2011 Funda Wang <fwang@mandriva.org> 3.3.1-1mdv2011.0
+ Revision: 675970
- drop unused patches
- install cmake module sinto lib64 for x86_64 arch
- cleanup spec file
- br cmake
- new version 3.3.1

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 3.3.0-2
+ Revision: 666058
- mass rebuild

* Thu Mar 03 2011 Lev Givon <lev@mandriva.org> 3.3.0-1
+ Revision: 641509
- Update to 3.3.0.

* Sat Jul 17 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 3.2.2-1mdv2011.0
+ Revision: 554562
- update to new version 3.2.2

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 3.2.1-5mdv2010.1
+ Revision: 523160
- rebuilt for 2010.1

* Mon Sep 28 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.2.1-4mdv2010.0
+ Revision: 450732
- subpackages can't be noarch

* Sat Sep 26 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.2.1-3mdv2010.0
+ Revision: 449542
- rebuild for missing binaries

* Mon Sep 07 2009 Lev Givon <lev@mandriva.org> 3.2.1-2mdv2010.0
+ Revision: 432920
- Create packages for docs and man pages.

* Tue May 05 2009 Lev Givon <lev@mandriva.org> 3.2.1-1mdv2010.0
+ Revision: 372255
- Update to 3.2.1.

* Wed Apr 01 2009 Giuseppe Ghibò <ghibo@mandriva.com> 3.2-6mdv2009.1
+ Revision: 363103
- Don't use -ffloat-store workaround anymore (libblas will result 3 times faster).

* Wed Dec 03 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 3.2-5mdv2009.1
+ Revision: 309808
- add to provides libblas

* Thu Nov 27 2008 Lev Givon <lev@mandriva.org> 3.2-4mdv2009.1
+ Revision: 307237
- Fix missing obj problem by patching stock blas/lapack Makefiles
  instead of using custom Makefiles with their own obj lists.

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - handle nicely major, version and soname changes

* Tue Nov 25 2008 Funda Wang <fwang@mandriva.org> 3.2-2mdv2009.1
+ Revision: 306553
- fix libname

* Sun Nov 23 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 3.2-1mdv2009.1
+ Revision: 306102
- update to new version 3.2
- add requires on blas-devel for lapack-devel subpackage
- fix file list

* Fri Jul 04 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 3.1.1-3mdv2009.0
+ Revision: 231865
- correct provides for libblas
- obsolete old lapack package

* Fri Jul 04 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 3.1.1-2mdv2009.0
+ Revision: 231702
- fix group and remove dot in summary
- update to new version 3.1.1
- create subpackage for blas library
- use the Fedora's idea to build the package
- fix descriptions
- fix mixture of tabs and spaces
- spec file clean

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Nov 08 2007 Lev Givon <lev@mandriva.org> 3.1.1-1mdv2008.1
+ Revision: 106977
- Update to 3.1.1.

* Wed Oct 24 2007 Lev Givon <lev@mandriva.org> 3.0-24mdv2008.1
+ Revision: 101875
- Update spec file in light of new devel package naming policy.

* Tue Oct 16 2007 Lev Givon <lev@mandriva.org> 3.0-23mdv2008.1
+ Revision: 99434
- Fixed etime issue introduced by new gfortran version.
- Create liblapack_pic.a containing objects compiled with -fPIC
  (needed to build atlas).

* Tue Sep 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-21mdv2008.0
+ Revision: 89831
- rebuild

  + Funda Wang <fwang@mandriva.org>
    - Import lapack



* Sun Sep 10 2006 Emmanuel Andry <eandry@mandriva.org> 3.0-20mdv2007.0
- rebuild

* Mon May 22 2006 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-19mdk
- rebuild for new gfortran

* Thu May 04 2006 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-18mdk
- backportable before 2006.0

* Tue May 02 2006 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-17mdk
- rebuild with a stricter dependency on blas-devel package to use

* Fri Mar 03 2006 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-16mdk
- obsoletes previous release with old partial soname

* Thu Mar 02 2006 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-15mdk
- drop blas sources, and use external blas package  
- spec cleanup

* Fri Aug 12 2005 Austin Acton <austin@mandriva.org> 3.0-14mdk
- rebuild

* Wed Jul 20 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 3.0-13mdk
- * Mon Jul 18 2005 Lev Givon <lev@columbia.edu> 3.0-13mdk
 - build libblas using full BLAS source
 - change man page suffixes from .l to .3
- buildrequires gcc-fortran
- patch3 : use gfortran
- tests done in check section
- fix some lint

* Sat Apr 16 2005 Abel Cheung <deaddog@mandriva.org> 3.0-12mdk
- Use -O2 -ffloat-store to avoid gcc optimization error (#13298)

* Sat Aug 28 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 3.0-11mdk
- manpage path: s/manl/man3/

* Wed Jun 23 2004 Abel Cheung <deaddog@deaddog.org> 3.0-10mdk
- don't let liblapack own libblas.so.3
- program is not for development
- enable test by default (if it fails for some arch, please use ifarch)
- lower optimization, otherwise hang indefinitely when running testsuite
- fix shlib-with-non-pic-code, link lapack with shared blas library

* Wed Jan 14 2004 Lenny Cartier <lenny@mandrakesoft.com> 3.0-9mdk
- rebuild

* Fri Dec 20 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 3.0-8mdk
- split lippack and libblas
- split doc in separate package

* Wed Oct 02 2002 Lenny Cartier <lenny@mandrakesoft.com> 3.0-7mdk
- rebuild

* Tue Aug 6 2002 Antoine Ginies <aginies@mandrakesoft.com> 3.0-6mdk
- build with gcc 3.2
* Mon Jul 07 2002 Erwan Velu <erwan@mandrakesoft.com> 3.0-5mdk
- Rebuild
* Wed Oct 10 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.0-4mdk
- Patch0: Add all patches from the LAPACK site as of 2001-10-10
- Patch1: Makefile fixes for make testing (optional)
- Make rpmlint happy:
  - E: liblapack3-devel obsolete-not-provided lapack-devel

* Thu Aug 09 2001 Lenny Cartier <lenny@mandrakesoft.com> 3.0-3mdk
- rebuild

* Thu Apr 26 2001 Lenny Cartier <lenny@mandrakesoft.com> 3.0-2mdk
- fixes from Pierre-Michel THEVENY <pmt@mnhn.fr> :
	- update sources from netlib
	- add equivalence program
	- rebuilt on Mandrake 8.0 (rpm-4.0)

* Tue Jan 16 2001 Lenny Cartier <lenny@mandrakesoft.com> 3.0-1mdk
- now library policy compliant

* Thu Nov 16 2000 Lenny Cartier <lenny@mandrakesoft.com> 3.0-1mdk
- used srpm provided by Gerard Vermeulen <gvermeul@labs.polycnrs-gre.fr> :
	- Mandrake RPM guidelines
	- split out devel
	- built on Mandrake-7.2

* Sun Aug 20 2000 Gerard Vermeulen <gvermeul@labs.polycnrs-gre.fr> 3.0-6gv
- collapse lapack, blas, lapack-man and blas-man into lapack
- built on Mandrake-7.1

* Thu Jan 03 2000 Gerard Vermeulen <gvermeul@labs.polycnrs-gre.fr>
- built on Mandrake-6.1 by gcc-2.95.2
- zap backwards compatibility
  this will require recompilation of some other packages

* Mon Oct 25 1999 Gerard Vermeulen <gvermeul@labs.polycnrs-gre.fr>
- built on Mandrake-6.1 by gcc-2.95.1

* Fri Oct 08 1999 Gerard Vermeulen <gvermeul@labs.polycnrs-gre.fr>
- link 3.0 libraries also as 2.0.1, hoping for backwards compatibility

* Sun Oct 3 1999 Gerard Vermeulen <gvermeul@labs.polycnrs-gre.fr>
- BUG: the new LAPACK-3.0 routines were missing
- FIX: generate new fast Makefiles by a python program
- Redhat-6.0 and gcc-2.95.1

* Mon Aug 2 1999 Tim Powers <timp@redhat.com>
- updated to v3.0
- built for 6.1

* Mon Apr 12 1999 Michael Maher <mike@redhat.com>
- built package for 6.0

* Sat Oct 24 1998 Jeff Johnson <jbj@redhat.com>
- new description/summary text.

* Fri Jul 17 1998 Jeff Johnson <jbj@redhat.com>
- repackage for powertools.
