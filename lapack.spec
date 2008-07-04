#lapack
%define major 3.1
%define libname %mklibname %{name} %{major}
%define oldmajor 3.0
%define oldlibname %mklibname %{name} %{oldmajor}
%define develname %mklibname -d %{name}

# blas
%define libblasname %mklibname blas %{major}
%define develblasname %mklibname blas -d

Summary:	LAPACK libraries for linear algebra
Name:		lapack
Version:	3.1.1
Release:	%mkrel 2
License:	BSD-like
Group:		Sciences/Mathematics
URL:		http://www.netlib.org/lapack/
Source0:	http://www.netlib.org/lapack/%{name}-%{version}.tar.bz2
Source1:	Makefile.lapack
Source2:	Makefile.blas
Source3:	http://www.netlib.org/lapack/lapackqref.ps
Source4:	http://www.netlib.org/blas/blasqr.ps
Patch0:		lapack-3.1.1-make.inc.patch
BuildRequires:	gcc-gfortran
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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

%package -n %{libname}
Summary:	LAPACK libraries for linear algebra
Group:		Sciences/Mathematics
Provides:	lib%{name} = %{version}-%{release}
Obsoletes:	%{oldlibname}

%description -n %{libname}
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

%package -n %{develname}
Summary:	LAPACK static library
Group:		Sciences/Mathematics
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d %{name} %{oldmajor}
Obsoletes:	%mklibname -d %{name} %{major}

%description -n	%{develname}
This package contains the headers and development libraries
necessary to develop or compile applications using lapack.

%package -n %{libblasname}
Summary:	The BLAS (Basic Linear Algebra Subprograms) library
Group:		Sciences/Mathematics
Obsoletes:	%{mklibname blas 1.1} < 3.1.1
Provides:	%{mklibname blas 1.1}

%description -n %{libblasname}
BLAS (Basic Linear Algebra Subprograms) is a standard library which
provides a number of basic algorithms for numerical algebra. Man
pages for blas are available in the blas-man package.

%package -n %{develblasname}
Summary:	BLAS development libraries
Group:		Sciences/Mathematics
Requires:	%{libblasname} = %{version}-%{release}
Provides:	blas = %{version}-%{release}
Provides:	libblas = %{version}-%{release}
Obsoletes:	%{mklibname blas 1.1 -d} < 3.1.1
Provides:	%{mklibname blas 1.1 -d}

%description -n %{develblasname}
BLAS development libraries for applications that link statically.

%prep
%setup -q
%patch0 -p1

cp -f INSTALL/make.inc.gfortran make.inc
cp -f %{SOURCE1} SRC/Makefile
cp -f %{SOURCE2} BLAS/SRC/Makefile

%build
export FC=gfortran
export CFLAGS="%{optflags} -funroll-all-loops -ffloat-store"
export FFLAGS=$CFLAGS

# Build BLAS
pushd BLAS/SRC
FFLAGS="$FFLAGS" make dcabs1.o
FFLAGS="$FFLAGS" CFLAGS="$CFLAGS" make static
cp libblas.a ${RPM_BUILD_DIR}/%{name}-%{version}/
make clean
FFLAGS="$FFLAGS -Os -fPIC" make dcabs1.o
FFLAGS="$FFLAGS -fPIC" CFLAGS="$CFLAGS -fPIC" make shared
cp libblas.so.3.1.1 ${RPM_BUILD_DIR}/%{name}-%{version}/
popd

ln -s libblas.so.3.1.1 libblas.so

# Some files don't like -O2, but -Os is fine
RPM_OPT_SIZE_FLAGS=$(echo $RPM_OPT_FLAGS | sed 's|-O2|-Os|')

# Build the static dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
make NOOPT="$CFLAGS -Os" OPTS="$CFLAGS"
popd

# Build the static lapack library
pushd SRC
make FFLAGS="$FFLAGS" CFLAGS="$CFLAGS" static
cp liblapack.a ${RPM_BUILD_DIR}/%{name}-%{version}/
popd

# Build the shared dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
make clean
make NOOPT="$CFLAGS -Os -fPIC" OPTS="$CFLAGS -fPIC"
popd

# Build the shared lapack library
pushd SRC
make clean
make FFLAGS="$FFLAGS -fPIC" CFLAGS="$CFLAGS -fPIC" shared
cp liblapack.so.3.1.1 ${RPM_BUILD_DIR}/%{name}-%{version}/
popd

# Buuld the static with pic dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
make clean
make NOOPT="$CFLAGS -Os -fPIC" OPTS="$CFLAGS -fPIC"
popd

# Build the static with pic lapack library
pushd SRC
make clean
make FFLAGS="$CFLAGS -fPIC" CFLAGS="$CFLAGS -fPIC" static
cp liblapack.a ${RPM_BUILD_DIR}/%{name}-%{version}/liblapack_pic.a
popd

cp %{SOURCE3} lapackqref.ps
cp %{SOURCE4} blasqr.ps

%install
rm -fr %{buildroot}


mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_mandir}/man3

for f in liblapack.so.3.1.1 libblas.so.3.1.1 libblas.a liblapack.a liblapack_pic.a; do
  cp -f $f %{buildroot}%{_libdir}/$f
done

pushd %{buildroot}%{_libdir}
ln -sf liblapack.so.3.1.1 liblapack.so
ln -sf liblapack.so.3.1.1 liblapack.so.3
ln -sf liblapack.so.3.1.1 liblapack.so.3.1
ln -sf libblas.so.3.1.1 libblas.so
ln -sf libblas.so.3.1.1 libblas.so.3
ln -sf libblas.so.3.1.1 libblas.so.3.1
popd

for file in manpages/man/manl/*; do
    install -m 644 $file %{buildroot}%{_mandir}/man3/`basename $file .l`.3
done

%clean
%__rm -fr %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%doc README lapackqref.ps
%{_libdir}/liblapack.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/liblapack.so
%{_libdir}/liblapack*.a
%{_mandir}/man3/*


%files -n %{libblasname}
%defattr(-,root,root)
%doc blasqr.ps
%{_libdir}/libblas.so.*

%files -n %{develblasname}
%defattr(-,root,root,-)
%{_libdir}/libblas.so
%{_libdir}/libblas*.a
