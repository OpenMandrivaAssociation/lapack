%bcond deprecated	1
%bcond cblas		1
%bcond lapacke		1
%bcond static		1
%bcond static_pic	0
%bcond testing		0
%bcond xblas		0

# lapack
%define major 3
%define lapack_libname %mklibname %{name}
%define lapack_devname %mklibname %{name} -d
%define lapack_oldlibname %mklibname %{name} 3
%define lapack_olddevname %mklibname %{name} 3 -d
%define lapack_docname %{name}-doc

# blas
%define libblas %mklibname blas
%define blas_libname %mklibname blas
%define blas_devname %mklibname blas -d
%define blas_oldlibname %mklibname blas 3
%define blas_olddevname %mklibname blas 3 -d
%define blas_docname blas-doc

%global optflags %{optflags} -O3

%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
%global arch64 1
%else
%global arch64 0
%endif

Summary:	LAPACK libraries for linear algebra
Name:		lapack
Version:	3.12.1
Release:	1
License:	BSD-like
Group:		Sciences/Mathematics
Url:		https://www.netlib.org/lapack/
Source0:	https://github.com/Reference-LAPACK/lapack/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	https://www.netlib.org/lapack/lapackqref.ps
Source2:	https://www.netlib.org/blas/blasqr.ps
Source3:	https://www.netlib.org/lapack/manpages.tgz
# (upsream)
Patch100:	https://github.com/Reference-LAPACK/lapack/commit/3aa877584bcc96e1a0ee37742628946c56afc15f.patch
# (upsream)
# https://github.com/Reference-LAPACK/lapack/pull/1094/commits
Patch101:	https://github.com/Reference-LAPACK/lapack/commit/f5103fc3b42fcff40e70b1fa4b5567df01dae9bc.patch
# (upsream)
# https://github.com/Reference-LAPACK/lapack/pull/1099
Patch200:	https://github.com/Reference-LAPACK/lapack/pull/1099/commits/304fa305e85190c934e78eae75c7b092fcfd54c1.patch
Patch201:	https://github.com/Reference-LAPACK/lapack/pull/1099/commits/bc0c38f247f90f815a93f6ca0829004120745da4.patch
Patch202:	https://github.com/Reference-LAPACK/lapack/pull/1099/commits/3c209c6bdf524869d18d00119aeae4962740c3b3.patch
BuildRequires:	cmake ninja
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

#---------------------------------------------------------------------------

%package -n %{lapack_libname}
Summary:	LAPACK libraries for linear algebra
Group:		Sciences/Mathematics
Provides:	lib%{name} = %{version}-%{release}
Obsoletes:	%{lapack_oldlibname} < %{EVRD}

%description -n %{lapack_libname}
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

%files -n %{lapack_libname}
%license LICENSE
%{_libdir}/liblapack.so.%{major}*
%if %{with lapacke}
%{_libdir}/liblapacke.so.%{major}*
%{_libdir}/libtmglib.so.%{major}*
%endif
%if 0%{?arch64}
%{_libdir}/liblapack64.so.%{major}*
%if %{with lapacke}
%{_libdir}/liblapacke64.so.%{major}*
%{_libdir}/libtmglib64.so.%{major}*
%endif
%endif

#-----------------------------------------------------------------------

%package -n %{lapack_devname}
Summary:	LAPACK static library
Group:		Sciences/Mathematics
Requires:	%{lapack_libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{lapack_olddevname} < %{EVRD}

%description -n %{lapack_devname}
This package contains the headers and development libraries
necessary to develop or compile applications using lapack.

%files -n %{lapack_devname}
%license LICENSE
%{_includedir}/lapack*.h
%{_libdir}/liblapack.so
%if %{with static}
%{_libdir}/liblapack.a
%endif
%{_libdir}/pkgconfig/lapack.pc
%{_libdir}/cmake/lapack-%{version}/lapack-*.cmake
%if %{with lapacke}
%{_libdir}/liblapacke.so
%{_libdir}/libtmglib.so
%if %{with static}
%{_libdir}/libtmglib.a
%{_libdir}/liblapacke.a
%endif
%{_libdir}/pkgconfig/lapacke.pc
%{_libdir}/cmake/lapacke-%{version}/lapacke-*.cmake
%endif
%if 0%{?arch64}
%{_libdir}/liblapack64.so
%if %{with static}
%{_libdir}/liblapack64.a
%endif
%{_libdir}/pkgconfig/lapack64.pc
%{_libdir}/cmake/lapack64-%{version}/lapack64-*.cmake
%if %{with lapacke}
%{_libdir}/liblapacke64.so
%{_libdir}/libtmglib64.so
%if %{with static}
%{_libdir}/libtmglib64.a
%{_libdir}/liblapacke64.a
%endif
%{_libdir}/pkgconfig/lapacke64.pc
%{_libdir}/cmake/lapacke64-%{version}/lapacke64-*.cmake
%endif
%endif

#---------------------------------------------------------------------------

%package -n %{lapack_docname}
Summary:	Documentation for LAPACK
Group:		Sciences/Mathematics

%description -n %{lapack_docname}
Man pages / documentation for LAPACK.

%files -n %{lapack_docname} -f lapack-man-pages
%license LICENSE
%doc README.md lapackqref.ps

#---------------------------------------------------------------------------

%package -n %{blas_libname}
Summary:	The BLAS (Basic Linear Algebra Subprograms) library
Group:		Sciences/Mathematics
Provides:	libblas = %{version}-%{release}
Obsoletes:	%{blas_oldlibname} < %{EVRD}

%description -n %{blas_libname}
BLAS (Basic Linear Algebra Subprograms) is a standard library which
provides a number of basic algorithms for numerical algebra. Man
pages for blas are available in the blas-man package.

%files -n %{blas_libname}
%license LICENSE
%{_libdir}/libblas.so.%{major}*
%if %{with cblas}
%{_libdir}/libcblas.so.%{major}*
%endif
%if 0%{?arch64}
%{_libdir}/libblas64.so.%{major}*
%if %{with cblas}
%{_libdir}/libcblas64.so.%{major}*
%endif
%endif

#---------------------------------------------------------------------------

%package -n %{blas_devname}
Summary:	BLAS development libraries
Group:		Sciences/Mathematics
Requires:	%{blas_libname} = %{version}-%{release}
Provides:	blas-devel = %{version}-%{release}
Obsoletes:	%{blas_olddevname} < %{EVRD}

%description -n %{blas_devname}
BLAS development libraries for applications that link statically.

%files -n %{blas_devname}
%license LICENSE
%{_libdir}/libblas.so
%if %{with static}
%{_libdir}/libblas.a
%endif
%{_libdir}/pkgconfig/blas.pc

%if %{with cblas}
%{_includedir}/cblas*.h
%{_libdir}/libcblas.so
%if %{with static}
%{_libdir}/libcblas.a
%endif
%{_libdir}/pkgconfig/cblas.pc
%{_libdir}/cmake/cblas-%{version}/cblas-*.cmake
%endif

%if 0%{?arch64}
%{_libdir}/libblas64.so
%if %{with static}
%{_libdir}/libblas64.a
%endif
%{_libdir}/pkgconfig/blas64.pc

%if %{with cblas}
%{_libdir}/libcblas64.so
%if %{with static}
%{_libdir}/libcblas64.a
%endif
%{_libdir}/pkgconfig/cblas64.pc
%{_libdir}/cmake/cblas64*-%{version}/cblas64-*.cmake
%endif
%endif

#---------------------------------------------------------------------------

%package -n %{blas_docname}
Summary:	Documentation for BLAS
Group:		Sciences/Mathematics

%description -n %{blas_docname}
Man pages / documentation for BLAS.

%files -n %{blas_docname} -f blas-man-pages
%license LICENSE
%doc blasqr.ps

#---------------------------------------------------------------------------

%prep
%autosetup -p1 -a3
cp %{SOURCE1} lapackqref.ps
cp %{SOURCE2} blasqr.ps

# purge apple stuff
rm -rf man/man3/.*.3

%build
%global optflags %{optflags} -fno-optimize-sibling-calls
export CC=gcc
export CXX=g++
export FC=gfortran
export default_optflags=" -g %{optflags}"

cp -a CMakeLists.txt CMakeLists.txt.orig
for d in {SHARED%{?with_static:,STATIC}%{?with_static_pic:,STATIC_PIC}}%{?arch64:{,64}}
do
	cp -a CMakeLists.txt.orig CMakeLists.txt.$d

	if [[ "$d" =~ "STATIC_PIC" ]]; then
		STATIC=ON
		SHARED=OFF
		%global optflags ${default_optflags} -fPIC

		# change lib names
		sed -i \
			-e 's,set(BLASLIB "blas"),set(BLASLIB "blas_pic"),g' \
			-e 's,set(CBLASLIB "cblas"),set(CBLASLIB "cblas_pic"),g' \
			-e 's,set(LAPACKLIB "lapack"),set(LAPACKLIB "lapack_pic"),g' \
			-e 's,set(LAPACKELIB "lapacke"),set(LAPACKELIB "lapacke_pic"),g' \
			-e 's,set(TMGLIB "tmglib"),set(TMGLIB "tmglib_pic"),g' \
			-e 's,set(BLASLIB "blas64"),set(BLASLIB "blas_pic64"),g' \
			-e 's,set(CBLASLIB "cblas64"),set(CBLASLIB "cblas_pic64"),g' \
			-e 's,set(LAPACKLIB "lapack64"),set(LAPACKLIB "lapack_pic64"),g' \
			-e 's,set(LAPACKELIB "lapacke64"),set(LAPACKELIB "lapacke_pic64"),g' \
			-e 's,set(TMGLIB "tmglib64"),set(TMGLIB "tmglib_pic64"),g' \
			CMakeLists.txt.$d
	elif [[ "$d" =~ "STATIC" ]]; then
		STATIC=ON
		SHARED=OFF
		%global optflags ${default_optflags}
	else
		STATIC=OFF
		SHARED=ON
		%global optflags ${default_optflags}
	fi
	[[ "$d" =~ "64" ]] && INDEX64=ON || INDEX64=OFF

	ln -fs CMakeLists.txt.$d CMakeLists.txt
	%cmake -Wno-dev \
		-DCMAKE_Fortran_FLAGS:STRING="$FFLAGS -frecursive" \
		-DBUILD_STATIC_LIBS:BOOL=$STATIC \
		-DBUILD_SHARED_LIBS:BOOL=$SHARED \
		-DBUILD_DEPRECATED:BOOL=%{?with_deprecated:ON}%{?!with_deprecated:OFF} \
		-DLAPACKE:BOOL=%{?with_lapacke:ON}%{?!with_lapacke:OFF} \
		-DLAPACKE_WITH_TMG:BOOL=%{?with_lapacke:ON}%{?!with_lapacke:OFF} \
		-DCBLAS:BOOL=%{?with_cblas:ON}%{?!with_cblas:OFF} \
		-DUSE_XBLAS:BOOL=%{?with_xblas:ON}%{?!with_xblas:OFF} \
		-DBUILD_INDEX64:BOOL=$INDEX64 \
		-DBUILD_TESTING:BOOL=%{?with_testing:ON}%{?!with_testing:OFF} \
		-GNinja
	%ninja_build

	cd ..
	mv %_vpath_builddir %_vpath_builddir-$d
done

%install
for d in {SHARED%{?with_static:,STATIC}%{?with_static_pic:,STATIC_PIC}}%{?arch64:{,64}}
do
	ln -fs %_vpath_builddir-$d build
	ln -fs CMakeLists.txt.$d CMakeLists.txt
	%ninja_install -C build
	rm build
done

# man
install -dpm 0755 %{buildroot}%{_mandir}/man3

# Blas manpages
mkdir -p blas/man/man3
cd man/man3/
mv caxpy.f.3 caxpy.3 ccopy.f.3 ccopy.3 cdotc.f.3 cdotc.3 cdotu.f.3 cdotu.3 cgbmv.f.3 cgbmv.3 \
cgemm.f.3 cgemm.3 cgemv.f.3 cgemv.3 cgerc.f.3 cgerc.3 cgeru.f.3 cgeru.3 chbmv.f.3 chbmv.3 \
chemm.f.3 chemm.3 chemv.f.3 chemv.3 cher.f.3 cher.3 cher2.f.3 cher2.3 cher2k.f.3 cher2k.3 \
cherk.f.3 cherk.3 chpmv.f.3 chpmv.3 chpr.f.3 chpr.3 chpr2.f.3 chpr2.3 \
cscal.f.3 cscal.3 csrot.f.3 csrot.3 csscal.f.3 csscal.3 cswap.f.3 cswap.3 csymm.f.3 \
csymm.3 csyr2k.f.3 csyr2k.3 csyrk.f.3 csyrk.3 ctbmv.f.3 ctbmv.3 ctbsv.f.3 ctbsv.3 ctpmv.f.3 \
ctpmv.3 ctpsv.f.3 ctpsv.3 ctrmm.f.3 ctrmm.3 ctrmv.f.3 ctrmv.3 ctrsm.f.3 ctrsm.3 ctrsv.f.3 \
ctrsv.3 dasum.f.3 dasum.3 daxpy.f.3 daxpy.3 dcabs1.f.3 dcabs1.3 dcopy.f.3 dcopy.3 ddot.f.3 \
ddot.3 dgbmv.f.3 dgbmv.3 dgemm.f.3 dgemm.3 dgemv.f.3 dgemv.3 dger.f.3 dger.3 \
drot.f.3 drot.3 drotm.f.3 drotm.3 drotmg.f.3 drotmg.3 dsbmv.f.3 \
dsbmv.3 dscal.f.3 dscal.3 dsdot.f.3 dsdot.3 dspmv.f.3 dspmv.3 dspr.f.3 dspr.3 dspr2.f.3 \
dspr2.3 dswap.f.3 dswap.3 dsymm.f.3 dsymm.3 dsymv.f.3 dsymv.3 dsyr.f.3 dsyr.3 dsyr2.f.3 \
dsyr2.3 dsyr2k.f.3 dsyr2k.3 dsyrk.f.3 dsyrk.3 dtbmv.f.3 dtbmv.3 dtbsv.f.3 dtbsv.3 dtpmv.f.3 \
dtpmv.3 dtpsv.f.3 dtpsv.3 dtrmm.f.3 dtrmm.3 dtrmv.f.3 dtrmv.3 dtrsm.f.3 dtrsm.3 dtrsv.f.3 \
dtrsv.3 dzasum.f.3 dzasum.3 icamax.f.3 icamax.3 idamax.f.3 idamax.3 \
isamax.f.3 isamax.3 izamax.f.3 izamax.3 lsame.3 sasum.f.3 sasum.3 saxpy.f.3 saxpy.3 \
scabs1.f.3 scabs1.3 scasum.f.3 scasum.3 scopy.f.3 scopy.3 sdot.f.3 sdot.3 \
sdsdot.f.3 sdsdot.3 sgbmv.f.3 sgbmv.3 sgemm.f.3 sgemm.3 sgemv.f.3 sgemv.3 sger.f.3 sger.3 \
srot.f.3 srot.3 srotm.f.3 srotm.3 srotmg.f.3 srotmg.3 \
ssbmv.f.3 ssbmv.3 sscal.f.3 sscal.3 sspmv.f.3 sspmv.3 sspr.f.3 sspr.3 sspr2.f.3 sspr2.3 \
sswap.f.3 sswap.3 ssymm.f.3 ssymm.3 ssymv.f.3 ssymv.3 ssyr.f.3 ssyr.3 ssyr2.f.3 ssyr2.3 \
ssyr2k.f.3 ssyr2k.3 ssyrk.f.3 ssyrk.3 stbmv.f.3 stbmv.3 stbsv.f.3 stbsv.3 stpmv.f.3 stpmv.3 \
stpsv.f.3 stpsv.3 strmm.f.3 strmm.3 strmv.f.3 strmv.3 strsm.f.3 strsm.3 strsv.f.3 strsv.3 \
xerbla.3 xerbla_array.3 zaxpy.f.3 zaxpy.3 zcopy.f.3 zcopy.3 \
zdotc.f.3 zdotc.3 zdotu.f.3 zdotu.3 zdrot.f.3 zdrot.3 zdscal.f.3 zdscal.3 zgbmv.f.3 zgbmv.3 \
zgemm.f.3 zgemm.3 zgemv.f.3 zgemv.3 zgerc.f.3 zgerc.3 zgeru.f.3 zgeru.3 zhbmv.f.3 zhbmv.3 \
zhemm.f.3 zhemm.3 zhemv.f.3 zhemv.3 zher.f.3 zher.3 zher2.f.3 zher2.3 zher2k.f.3 zher2k.3 \
zherk.f.3 zherk.3 zhpmv.f.3 zhpmv.3 zhpr.f.3 zhpr.3 zhpr2.f.3 zhpr2.3 \
zscal.f.3 zscal.3 zswap.f.3 zswap.3 zsymm.f.3 zsymm.3 zsyr2k.f.3 zsyr2k.3 zsyrk.f.3 zsyrk.3 \
ztbmv.f.3 ztbmv.3 ztbsv.f.3 ztbsv.3 ztpmv.f.3 ztpmv.3 ztpsv.f.3 ztpsv.3 ztrmm.f.3 ztrmm.3 \
ztrmv.f.3 ztrmv.3 ztrsm.f.3 ztrsm.3 ztrsv.f.3 ztrsv.3 ../../blas/man/man3
cd ../..

find blas/man/man3 -type f -printf "%{_mandir}/man3/%f*\n" > blas-man-pages

# remove weird man pages
cd man/man3
rm -rf _Users_julie*
cd -

find man/man3 -type f -printf "%{_mandir}/man3/%f*\n" > lapack-man-pages

cp -f blas/man/man3/* %{buildroot}%{_mandir}/man3
cp -f man/man3/* %{buildroot}%{_mandir}/man3

%check
%if %{with testing}
for d in {SHARED%{?with_static:,STATIC}%{?with_static_pic:,STATIC_PIC}}%{?arch64:{,64}}
do
	ln -fs %_vpath_builddir-$d build
	pushd build
	ctest
	popd 1>/dev/null
	rm build
done
%endif

