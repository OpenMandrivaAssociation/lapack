%define name 		lapack
%define version 	3.0
%define release 	%mkrel 21
%define major 		3.0
%define libname_orig	lib%{name}
%define libname 	%mklibname %{name} %{major}
%define oldmajor 	3
%define oldlibname 	%mklibname %{name} %{oldmajor}

%if %{mdkversion} <= 1020
%define f77	g77
%define runtime	g2c
%else
%define f77	gfortran
%define runtime	gfortran
%endif

Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Summary: 	LAPACK libraries for linear algebra
License: 	BSD-like
Group:		Sciences/Mathematics
URL: 		http://www.netlib.org/lapack/
Source0: 	http://www.netlib.org/lapack/%{name}.tar.bz2
Source1: 	%{name}.makefile.bz2
Source2: 	http://www.netlib.org/lapack/manpages.tar.bz2
%if %{mdkversion} <= 1020
BuildRequires:	gcc-g77
%else
BuildRequires:	gcc-gfortran
%endif
BuildRequires:	blas-devel >= 0:1.1
BuildRoot: 	%{_tmppath}/%{name}-%{version}

%description
LAPACK (Linear Algebra PACKage) is a standard library for numerical
linear algebra.  LAPACK provides routines for solving systems of
simultaneous linear equations, least-squares solutions of linear
systems of equations, eigenvalue problems, and singular value
problems.  Associated matrix factorizations (LU, Cholesky, QR, SVD,
Schur, and generalized Schur) and related computations (i.e.,
reordering of Schur factorizations and estimating condition numbers)
are also included.  LAPACK can handle dense and banded matrices, but
not general sparse matrices.  Similar functionality is provided for
real and complex matrices in both single and double precision.  LAPACK
is coded in Fortran77.

The lapack package provides the dynamic libraries for LAPACK/BLAS.

%package -n	%{libname}
Summary: 	LAPACK libraries for linear algebra
Group:		Sciences/Mathematics
Provides:	lib%{name} = %{version}-%{release}
Obsoletes:	%{oldlibname}
Provides:	%{oldlibname}

%description -n %{libname}
LAPACK (Linear Algebra PACKage) is a standard library for numerical
linear algebra.  LAPACK provides routines for solving systems of
simultaneous linear equations, least-squares solutions of linear
systems of equations, eigenvalue problems, and singular value
problems.  Associated matrix factorizations (LU, Cholesky, QR, SVD,
Schur, and generalized Schur) and related computations (i.e.,
reordering of Schur factorizations and estimating condition numbers)
are also included.  LAPACK can handle dense and banded matrices, but
not general sparse matrices.  Similar functionality is provided for
real and complex matrices in both single and double precision.  LAPACK
is coded in Fortran77.

The lapack package provides the dynamic libraries for LAPACK.

%package -n	%{libname}-devel
Summary: 	LAPACK static library
Group:		Sciences/Mathematics
Requires: 	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides: 	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{oldlibname}-devel
Provides:	%{oldlibname}-devel

%description -n	%{libname}-devel
LAPACK (Linear Algebra PACKage) is a standard library for numerical
linear algebra.  LAPACK provides routines for solving systems of
simultaneous linear equations, least-squares solutions of linear
systems of equations, eigenvalue problems, and singular value
problems.  Associated matrix factorizations (LU, Cholesky, QR, SVD,
Schur, and generalized Schur) and related computations (i.e.,
reordering of Schur factorizations and estimating condition numbers)
are also included.  LAPACK can handle dense and banded matrices, but
not general sparse matrices.  Similar functionality is provided for
real and complex matrices in both single and double precision.  LAPACK
is coded in Fortran77.

This package contains the headers and development libraries
necessary to develop or compile applications.

%prep
%setup -q -n LAPACK
bzcat %{SOURCE1} > Makefile
%setup -q -D -T -a 2 -n LAPACK

%build
%make F77="%{f77}" \
      RUNTIME="%{runtime}" \
      CFLAGS="%optflags" \
      FFLAGS="%optflags -ffloat-store"

%install
rm -fr %{buildroot}
install -d -m 755 %{buildroot}%{_bindir} \
                  %{buildroot}%{_libdir} \
                  %{buildroot}%{_mandir}/man3

install -m 755 equivalence %{buildroot}%{_bindir}/
install -m 755 *.so.* %{buildroot}%{_libdir}
install -m 644 *.a %{buildroot}%{_libdir}
(cd %{buildroot}%{_libdir} && ln -s lib%{name}.so.%{major} lib%{name}.so)

for file in man/manl/*; do
    install -m 644 $file %{buildroot}%{_mandir}/man3/`basename $file .l`.3
done

%clean
rm -fr %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README 
%{_bindir}/*

%files -n %{libname}
%defattr(-,root,root)
%doc README 
%{_libdir}/liblapack.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/liblapack.so
%{_libdir}/liblapack.a
%{_mandir}/man3/*
