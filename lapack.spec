# lapack
%define	major	3
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}
%define	docname	%{name}-doc

# blas
%define	libblas %mklibname blas %{major}
%define	devblas %mklibname blas -d
%define	docblas blas-doc

Summary:	LAPACK libraries for linear algebra
Name:		lapack
Version:	3.4.2
Release:	7
License:	BSD-like
Group:		Sciences/Mathematics
Url:		http://www.netlib.org/lapack/
Source0:	http://www.netlib.org/lapack/%{name}-%{version}.tgz
Source1:	http://www.netlib.org/lapack/lapackqref.ps
Source2:	http://www.netlib.org/blas/blasqr.ps
Source3:	http://www.netlib.org/lapack/manpages.tgz
Patch2:		lapack-3.4.2-cmake-sover.patch
Patch3:		lapack-3.4.2-lib64.patch

BuildRequires:	cmake
BuildRequires:	gcc-gfortran

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

%description -n	%{devname}
This package contains the headers and development libraries
necessary to develop or compile applications using lapack.

%package -n	%{docname}
Summary:	Documentation for LAPACK
Group:		Sciences/Mathematics

%description -n %{docname}
Man pages / documentation for LAPACK.

%package -n	%{libblas}
Summary:	The BLAS (Basic Linear Algebra Subprograms) library
Group:		Sciences/Mathematics
Provides:	libblas = %{version}-%{release}

%description -n	%{libblas}
BLAS (Basic Linear Algebra Subprograms) is a standard library which
provides a number of basic algorithms for numerical algebra. Man
pages for blas are available in the blas-man package.

%package -n	%{devblas}
Summary:	BLAS development libraries
Group:		Sciences/Mathematics
Requires:	%{libblas} = %{version}-%{release}
Provides:	blas-devel = %{version}-%{release}

%description -n	%{devblas}
BLAS development libraries for applications that link statically.

%package -n	%{docblas}
Summary:	Documentation for BLAS
Group:		Sciences/Mathematics

%description -n	%{docblas}
Man pages / documentation for BLAS.

%prep
%setup -q -a3
%apply_patches

cp %{SOURCE1} lapackqref.ps
cp %{SOURCE2} blasqr.ps

rm -f manpages/blas/man/manl/{csrot.l,lsame.l,xerbla.l,xerbla_array.l,zdrot.l}

%build
%cmake \
	-DBUILD_STATIC_LIBS=ON \
	-DBUILD_SHARED_LIBS=OFF \
	-DBUILD_TESTING=OFF \
	-DCMAKE_Fortran_COMPILER_FORCED=ON \
	-DCMAKE_SHARED_LINKER_FLAGS=-lgfortran
%make
cd ..

%cmake \
	-DBUILD_STATIC_LIBS=OFF \
	-DBUILD_SHARED_LIBS=ON \
	-DBUILD_TESTING=OFF \
	-DCMAKE_Fortran_COMPILER_FORCED=ON \
	-DCMAKE_SHARED_LINKER_FLAGS=-lgfortran
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
%{_libdir}/liblapack.a
%{_libdir}/pkgconfig/lapack.pc
%{_libdir}/cmake/lapack-%{version}/lapack-*.cmake

%files -n %{docname} -f lapack-man-pages
%doc README lapackqref.ps

%files -n %{libblas}
%{_libdir}/libblas.so.%{major}*

%files -n %{devblas}
%{_libdir}/libblas.so
%{_libdir}/libblas.a
%{_libdir}/pkgconfig/blas.pc

%files -n %{docblas} -f blas-man-pages
%doc blasqr.ps

