%define name 		lapack
%define version 	3.1.1
%define release 	%mkrel 1
%define major 		3.1
%define libname 	%mklibname %{name} %{major}
%define oldmajor 	3.0
%define oldlibname 	%mklibname %{name} %{oldmajor}
%define develname	%mklibname -d %{name}

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

%package -n	%{develname}
Summary: 	LAPACK static library
Group:		Sciences/Mathematics
Requires: 	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d %{name} %{oldmajor}
Obsoletes:	%mklibname -d %{name} %{major}

%description -n	%{develname}
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
%setup -q
bzcat %{SOURCE1} > Makefile

# Make sure these are compiled:
%__cp -p INSTALL/dlamch.f SRC/
%__cp -p INSTALL/slamch.f SRC/
%__cp -p INSTALL/dsecnd_INT_ETIME.f SRC/dsecnd.f
%__cp -p INSTALL/second_INT_ETIME.f SRC/second.f

%build
%make F77="%{f77}" \
      RUNTIME="%{runtime}" \
      CFLAGS="%optflags" \
      FFLAGS="%optflags -ffloat-store"

%install
%__rm -fr %{buildroot}
%__install -d -m 755 %{buildroot}%{_bindir} \
                  %{buildroot}%{_libdir} \
                  %{buildroot}%{_mandir}/man3

%__install -m 755 *.so.* %{buildroot}%{_libdir}
%__install -m 644 *.a %{buildroot}%{_libdir}
(cd %{buildroot}%{_libdir} && ln -s lib%{name}.so.%{major} lib%{name}.so)

for file in manpages/man/manl/*; do
    %__install -m 644 $file %{buildroot}%{_mandir}/man3/`basename $file .l`.3
done

%clean
%__rm -fr %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%doc README COPYING
%{_libdir}/liblapack.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/liblapack.so
%{_libdir}/liblapack*.a
%{_mandir}/man3/*
