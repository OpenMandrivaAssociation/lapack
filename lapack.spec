#lapack
%define major 3
%define minor 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

# blas
%define libblasname %mklibname blas %{major}
%define develblasname %mklibname blas -d

Summary:	LAPACK libraries for linear algebra
Name:		lapack
Version:	%{major}.%{minor}
Release:	%mkrel 3
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
Obsoletes:	%{name} < 3.1.1
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
Obsoletes:	%{_lib}lapack3.2
Obsoletes:	%{_lib}lapack3.1

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
Requires:	blas-devel = %{version}-%{release}

%description -n	%{develname}
This package contains the headers and development libraries
necessary to develop or compile applications using lapack.

%package -n %{libblasname}
Summary:	The BLAS (Basic Linear Algebra Subprograms) library
Group:		Sciences/Mathematics
Obsoletes:	%{mklibname blas 1.1}
Obsoletes:	%{_lib}blas3.2
Obsoletes:	%{_lib}blas3.1

%description -n %{libblasname}
BLAS (Basic Linear Algebra Subprograms) is a standard library which
provides a number of basic algorithms for numerical algebra. Man
pages for blas are available in the blas-man package.

%package -n %{develblasname}
Summary:	BLAS development libraries
Group:		Sciences/Mathematics
Requires:	%{libblasname} = %{version}-%{release}
Provides:	blas-devel = %{version}-%{release}
Provides:	libblas-devel = %{version}-%{release}
Obsoletes:	%{mklibname blas 1.1 -d} < 3.1.1
Requires:	gcc-gfortran

%description -n %{develblasname}
BLAS development libraries for applications that link statically.

%prep
%setup -q
%patch0 -p1

# take care of soname
cp -f %{SOURCE1} .
cp -f %{SOURCE2} .
sed -i -e 's/LIBMAJOR/%{major}/g' Makefile.*
sed -i -e 's/LIBSONAME/%{version}/g' Makefile.*

cp -f INSTALL/make.inc.gfortran make.inc
cp -f Makefile.lapack SRC/Makefile
cp -f Makefile.blas BLAS/SRC/Makefile

%build
export FC=gfortran
export CFLAGS="%{optflags} -funroll-all-loops -ffloat-store"
export FFLAGS=$CFLAGS

# Build BLAS
pushd BLAS/SRC
FFLAGS="$FFLAGS" %make dcabs1.o
FFLAGS="$FFLAGS" CFLAGS="$CFLAGS" %make static
cp libblas.a ${RPM_BUILD_DIR}/%{name}-%{version}/
%make clean
FFLAGS="$FFLAGS -Os -fPIC" %make dcabs1.o
FFLAGS="$FFLAGS -fPIC" CFLAGS="$CFLAGS -fPIC" %make shared
cp libblas.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/
popd

ln -s libblas.so.%{version} libblas.so

# Some files don't like -O2, but -Os is fine
RPM_OPT_SIZE_FLAGS=$(echo $RPM_OPT_FLAGS | sed 's|-O2|-Os|')

# Build the static dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
%make NOOPT="$CFLAGS -Os" OPTS="$CFLAGS"
popd

# Build the static lapack library
pushd SRC
%make FFLAGS="$FFLAGS" CFLAGS="$CFLAGS" static
cp liblapack.a ${RPM_BUILD_DIR}/%{name}-%{version}/
popd

# Build the shared dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
%make clean
%make NOOPT="$CFLAGS -Os -fPIC" OPTS="$CFLAGS -fPIC"
popd

# Build the shared lapack library
pushd SRC
%make clean
%make FFLAGS="$FFLAGS -fPIC" CFLAGS="$CFLAGS -fPIC" shared
cp liblapack.so.%{version} ${RPM_BUILD_DIR}/%{name}-%{version}/
popd

# Buuld the static with pic dlamch, dsecnd, lsame, second, slamch bits
pushd INSTALL
%make clean
%make NOOPT="$CFLAGS -Os -fPIC" OPTS="$CFLAGS -fPIC"
popd

# Build the static with pic lapack library
pushd SRC
%make clean
%make FFLAGS="$CFLAGS -fPIC" CFLAGS="$CFLAGS -fPIC" static
cp liblapack.a ${RPM_BUILD_DIR}/%{name}-%{version}/liblapack_pic.a
popd

cp %{SOURCE3} lapackqref.ps
cp %{SOURCE4} blasqr.ps

%install
rm -fr %{buildroot}


mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_mandir}/man3

for f in liblapack.so.%{version} libblas.so.%{version} libblas.a liblapack.a liblapack_pic.a; do
  cp -f $f %{buildroot}%{_libdir}/$f
done

pushd %{buildroot}%{_libdir}
ln -sf liblapack.so.%{version} liblapack.so
ln -sf liblapack.so.%{version} liblapack.so.3
#ln -sf liblapack.so.3.2 liblapack.so.3.2
ln -sf libblas.so.%{version} libblas.so
ln -sf libblas.so.%{version} libblas.so.3
#ln -sf libblas.so.3.2 libblas.so.3.2
popd

#for file in manpages/man/manl/*; do
#    install -m 644 $file %{buildroot}%{_mandir}/man3/`basename $file .l`.3
#done

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
%{_libdir}/liblapack.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/liblapack.so
%{_libdir}/liblapack*.a
#%{_mandir}/man3/*

%files -n %{libblasname}
%defattr(-,root,root)
%doc blasqr.ps
%{_libdir}/libblas.so.%{major}*

%files -n %{develblasname}
%defattr(-,root,root,-)
%{_libdir}/libblas.so
%{_libdir}/libblas*.a
