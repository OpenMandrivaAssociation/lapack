# lapack
%define major 3
%define minor 3.1
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}
%define docname	%{name}-doc

# blas
%define libblasname %mklibname blas %{major}
%define develblasname %mklibname blas -d
%define docblasname blas-doc

Summary:	LAPACK libraries for linear algebra
Name:		lapack
Version:	%{major}.%{minor}
Release:	%mkrel 2
License:	BSD-like
Group:		Sciences/Mathematics
URL:		http://www.netlib.org/lapack/
Source0:	http://www.netlib.org/lapack/%{name}-%{version}.tgz
Source1:	http://www.netlib.org/lapack/lapackqref.ps
Source2:	http://www.netlib.org/blas/blasqr.ps
Source3:	http://www.netlib.org/lapack/manpages.tgz
Patch2:		lapack-3.3.1-cmake-sover.patch
Patch3:		lapack-3.3.1-lib64.patch
BuildRequires:	gcc-gfortran
BuildRequires:	cmake
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

%package -n %{docname}
Summary:	Documentation for LAPACK
Group:		Sciences/Mathematics

%description -n %{docname}
Man pages / documentation for LAPACK.

%package -n %{libblasname}
Summary:	The BLAS (Basic Linear Algebra Subprograms) library
Group:		Sciences/Mathematics
Provides:	libblas = %{version}-%{release}
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

%package -n %{docblasname}
Summary:	Documentation for BLAS
Group:		Sciences/Mathematics

%description -n %{docblasname}
Man pages / documentation for BLAS.

%prep
%setup -q -a3
%patch2 -p1 -b .sover
%patch3 -p0 -b .lib64

cp %{SOURCE1} lapackqref.ps
cp %{SOURCE2} blasqr.ps

rm -f manpages/blas/man/manl/{csrot.l,lsame.l,xerbla.l,xerbla_array.l,zdrot.l}

%build
export CFLAGS="%{optflags} -fPIC"
export FFLAGS="%{optflags} -fPIC"
%cmake -DBUILD_STATIC_LIBS=ON -DBUILD_SHARED_LIBS=OFF -DBUILD_TESTING=OFF
%make
cd ..

%cmake -DBUILD_STATIC_LIBS=OFF -DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=OFF
%make

%install
rm -fr %{buildroot}
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
%{_libdir}/liblapack.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/liblapack.so
%{_libdir}/liblapack*.a
%{_libdir}/pkgconfig/lapack.pc
%{_libdir}/cmake/lapack-%{version}/lapack-*.cmake

%files -n %{docname} -f lapack-man-pages
%doc README lapackqref.ps

%files -n %{libblasname}
%defattr(-,root,root)
%{_libdir}/libblas.so.%{major}*

%files -n %{develblasname}
%defattr(-,root,root,-)
%{_libdir}/libblas.so
%{_libdir}/libblas*.a
%{_libdir}/pkgconfig/blas.pc

%files -n %{docblasname} -f blas-man-pages
%doc blasqr.ps
