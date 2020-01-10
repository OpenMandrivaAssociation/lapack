%define debug_package %{nil}

# lapack
%define	major	3
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}
%define	docname	%{name}-doc

# blas
%define	libblas %mklibname blas %{major}
%define	devblas %mklibname blas -d
%define	docblas blas-doc

%global optflags %{optflags} -O3

Summary:	LAPACK libraries for linear algebra
Name:		lapack
Version:	3.8.0
Release:	5
License:	BSD-like
Group:		Sciences/Mathematics
Url:		http://www.netlib.org/lapack/
Source0:	http://www.netlib.org/lapack/%{name}-%{version}.tar.gz
Source1:	http://www.netlib.org/lapack/lapackqref.ps
Source2:	http://www.netlib.org/blas/blasqr.ps
Source3:	http://www.netlib.org/lapack/manpages.tgz
#Patch0:		lapack-3.6.0-make.inc.patch

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
%autopatch -p1

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

# Blas manpages
mkdir -p blas/man/man3
cd man/man3/
mv caxpy.f.3 caxpy.3 ccopy.f.3 ccopy.3 cdotc.f.3 cdotc.3 cdotu.f.3 cdotu.3 cgbmv.f.3 cgbmv.3 \
cgemm.f.3 cgemm.3 cgemv.f.3 cgemv.3 cgerc.f.3 cgerc.3 cgeru.f.3 cgeru.3 chbmv.f.3 chbmv.3 \
chemm.f.3 chemm.3 chemv.f.3 chemv.3 cher.f.3 cher.3 cher2.f.3 cher2.3 cher2k.f.3 cher2k.3 \
cherk.f.3 cherk.3 chpmv.f.3 chpmv.3 chpr.f.3 chpr.3 chpr2.f.3 chpr2.3 crotg.f.3 crotg.3 \
cscal.f.3 cscal.3 csrot.f.3 csrot.3 csscal.f.3 csscal.3 cswap.f.3 cswap.3 csymm.f.3 \
csymm.3 csyr2k.f.3 csyr2k.3 csyrk.f.3 csyrk.3 ctbmv.f.3 ctbmv.3 ctbsv.f.3 ctbsv.3 ctpmv.f.3 \
ctpmv.3 ctpsv.f.3 ctpsv.3 ctrmm.f.3 ctrmm.3 ctrmv.f.3 ctrmv.3 ctrsm.f.3 ctrsm.3 ctrsv.f.3 \
ctrsv.3 dasum.f.3 dasum.3 daxpy.f.3 daxpy.3 dcabs1.f.3 dcabs1.3 dcopy.f.3 dcopy.3 ddot.f.3 \
ddot.3 dgbmv.f.3 dgbmv.3 dgemm.f.3 dgemm.3 dgemv.f.3 dgemv.3 dger.f.3 dger.3 dnrm2.f.3 \
dnrm2.3 drot.f.3 drot.3 drotg.f.3 drotg.3 drotm.f.3 drotm.3 drotmg.f.3 drotmg.3 dsbmv.f.3 \
dsbmv.3 dscal.f.3 dscal.3 dsdot.f.3 dsdot.3 dspmv.f.3 dspmv.3 dspr.f.3 dspr.3 dspr2.f.3 \
dspr2.3 dswap.f.3 dswap.3 dsymm.f.3 dsymm.3 dsymv.f.3 dsymv.3 dsyr.f.3 dsyr.3 dsyr2.f.3 \
dsyr2.3 dsyr2k.f.3 dsyr2k.3 dsyrk.f.3 dsyrk.3 dtbmv.f.3 dtbmv.3 dtbsv.f.3 dtbsv.3 dtpmv.f.3 \
dtpmv.3 dtpsv.f.3 dtpsv.3 dtrmm.f.3 dtrmm.3 dtrmv.f.3 dtrmv.3 dtrsm.f.3 dtrsm.3 dtrsv.f.3 \
dtrsv.3 dzasum.f.3 dzasum.3 dznrm2.f.3 dznrm2.3 icamax.f.3 icamax.3 idamax.f.3 idamax.3 \
isamax.f.3 isamax.3 izamax.f.3 izamax.3 lsame.3 sasum.f.3 sasum.3 saxpy.f.3 saxpy.3 \
scabs1.f.3 scabs1.3 scasum.f.3 scasum.3 scnrm2.f.3 scnrm2.3 scopy.f.3 scopy.3 sdot.f.3 sdot.3 \
sdsdot.f.3 sdsdot.3 sgbmv.f.3 sgbmv.3 sgemm.f.3 sgemm.3 sgemv.f.3 sgemv.3 sger.f.3 sger.3 \
snrm2.f.3 snrm2.3 srot.f.3 srot.3 srotg.f.3 srotg.3 srotm.f.3 srotm.3 srotmg.f.3 srotmg.3 \
ssbmv.f.3 ssbmv.3 sscal.f.3 sscal.3 sspmv.f.3 sspmv.3 sspr.f.3 sspr.3 sspr2.f.3 sspr2.3 \
sswap.f.3 sswap.3 ssymm.f.3 ssymm.3 ssymv.f.3 ssymv.3 ssyr.f.3 ssyr.3 ssyr2.f.3 ssyr2.3 \
ssyr2k.f.3 ssyr2k.3 ssyrk.f.3 ssyrk.3 stbmv.f.3 stbmv.3 stbsv.f.3 stbsv.3 stpmv.f.3 stpmv.3 \
stpsv.f.3 stpsv.3 strmm.f.3 strmm.3 strmv.f.3 strmv.3 strsm.f.3 strsm.3 strsv.f.3 strsv.3 \
xerbla.3 xerbla_array.3 zaxpy.f.3 zaxpy.3 zcopy.f.3 zcopy.3 \
zdotc.f.3 zdotc.3 zdotu.f.3 zdotu.3 zdrot.f.3 zdrot.3 zdscal.f.3 zdscal.3 zgbmv.f.3 zgbmv.3 \
zgemm.f.3 zgemm.3 zgemv.f.3 zgemv.3 zgerc.f.3 zgerc.3 zgeru.f.3 zgeru.3 zhbmv.f.3 zhbmv.3 \
zhemm.f.3 zhemm.3 zhemv.f.3 zhemv.3 zher.f.3 zher.3 zher2.f.3 zher2.3 zher2k.f.3 zher2k.3 \
zherk.f.3 zherk.3 zhpmv.f.3 zhpmv.3 zhpr.f.3 zhpr.3 zhpr2.f.3 zhpr2.3 zrotg.f.3 zrotg.3 \
zscal.f.3 zscal.3 zswap.f.3 zswap.3 zsymm.f.3 zsymm.3 zsyr2k.f.3 zsyr2k.3 zsyrk.f.3 zsyrk.3 \
ztbmv.f.3 ztbmv.3 ztbsv.f.3 ztbsv.3 ztpmv.f.3 ztpmv.3 ztpsv.f.3 ztpsv.3 ztrmm.f.3 ztrmm.3 \
ztrmv.f.3 ztrmv.3 ztrsm.f.3 ztrsm.3 ztrsv.f.3 ztrsv.3 ../../blas/man/man3
cd ../..

find blas/man/man3 -type f -printf "%{_mandir}/man3/%f*\n" > blas-man-pages

# remove weird man pages
pushd man/man3
rm -rf _Users_julie*
popd

find man/man3 -type f -printf "%{_mandir}/man3/%f*\n" > lapack-man-pages

cp -f blas/man/man3/* %{buildroot}%{_mandir}/man3
cp -f man/man3/* %{buildroot}%{_mandir}/man3

%files -n %{libname}
%{_libdir}/liblapack.so.%{major}*

%files -n %{devname}
%{_libdir}/liblapack.so
%{_libdir}/liblapack.a
%{_libdir}/pkgconfig/lapack.pc
%{_libdir}/cmake/lapack-%{version}/lapack-*.cmake

%files -n %{docname} -f lapack-man-pages
%doc lapackqref.ps

%files -n %{libblas}
%{_libdir}/libblas.so.%{major}*

%files -n %{devblas}
%{_libdir}/libblas.so
%{_libdir}/libblas.a
%{_libdir}/pkgconfig/blas.pc

%files -n %{docblas} -f blas-man-pages
%doc blasqr.ps
