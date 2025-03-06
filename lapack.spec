%global optflags %{optflags} -O3

# lapack
%define major 3
%define lapack_libname %mklibname %{name}
%define lapack_devname %mklibname %{name} -d
%define lapack_staticdevname %mklibname %{name} -s -d
%define lapack_oldlibname %mklibname %{name} 3
%define lapack_olddevname %mklibname %{name} 3 -d
%define lapack_docname %{name}-doc

# blas
%define blas_libname %mklibname blas
%define blas_devname %mklibname blas -d
%define blas_staticdevname %mklibname blas -s -d
%define blas_oldlibname %mklibname blas 3
%define blas_olddevname %mklibname blas 3 -d
%define blas_docname %{blas_libname}-doc

%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
%global arch64 1
%else
%global arch64 0
%endif

Summary:	LAPACK Libraries for Linear Algebra
Name:		lapack
Version:	3.12.1
Release:	1
License:	BSD-3-Clause-Open-MPI
Group:		Sciences/Mathematics
Url:		https://www.netlib.org/lapack/
Source0:	https://github.com/Reference-LAPACK/lapack/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	https://www.netlib.org/lapack/lapackqref.ps
Source2:	https://www.netlib.org/blas/blasqr.ps
# NOTE	In OMLx the LAPACK/BLAS doc/man pages are generated from source since v3.12.1,
# NOTE	therefore we have no need for the Source3 unversioned manpages tarball.
# NOTE	Keeping Source3 linked here meantime in-case upstream changes doc generation situation.
#Source3:	https://www.netlib.org/lapack/manpages.tgz

# Patches for 3.12.1 due to upstream release issues and bugs affecting successful compilation.
# Patch0:	https://github.com/Reference-LAPACK/lapack/pull/1093
Patch0:		https://github.com/Reference-LAPACK/lapack/pull/1093/commits/3aa877584bcc96e1a0ee37742628946c56afc15f.patch
# Patch1:	https://github.com/Reference-LAPACK/lapack/pull/1094
Patch1:		https://github.com/Reference-LAPACK/lapack/pull/1094/commits/f5103fc3b42fcff40e70b1fa4b5567df01dae9bc.patch
# Patch2:	https://github.com/Reference-LAPACK/lapack/pull/1095
Patch2:		https://github.com/Reference-LAPACK/lapack/pull/1095/commits/3e242fc8d5d38f0425c6018fe88abf31e1a9e80f.patch
# Patch3:	updates for doxygen 1.12
Patch3:		https://github.com/Reference-LAPACK/lapack/pull/1096/commits/31cd658cbd944e57aebd510725833f512b05c259.patch
# Patch4|5|6:	Fix line reflow in some of the deprecated sources (3/3)
#				https://github.com/Reference-LAPACK/lapack/pull/1099
Patch4:		https://github.com/Reference-LAPACK/lapack/pull/1099/commits/304fa305e85190c934e78eae75c7b092fcfd54c1.patch
Patch5:		https://github.com/Reference-LAPACK/lapack/pull/1099/commits/bc0c38f247f90f815a93f6ca0829004120745da4.patch
Patch6:		https://github.com/Reference-LAPACK/lapack/pull/1099/commits/3c209c6bdf524869d18d00119aeae4962740c3b3.patch
# Patch7:	Update Source code to fix issue with links in Doxygen
#			https://github.com/Reference-LAPACK/lapack/pull/1101/
Patch7:		https://github.com/Reference-LAPACK/lapack/pull/1101/commits/59f136760fb5cc62e9377c5d9103785037b7c660.patch
# Patch8:	Fix the testsuite of xGEMMTR
#			https://github.com/Reference-LAPACK/lapack/pull/1107
Patch8:		https://github.com/Reference-LAPACK/lapack/pull/1107/commits/4c637b83298e7b0777478194e1bc37d3af171504.patch

# Patch9:	Tweak CMakeLists & Makefile to strip source code from html generation output, reduce stub bloat & drop call graphs.
# NOTE	The use of the Makefile over CMakeLists is to enable man page and html doc generation as a build step.
# NOTE	Upstream's CMakeLists do not successfully complete these tasks, we fall back to using upstreams Makefile doc
# NOTE	and html tasks instead as they work successfully.
Patch9:		lapack-3.12.1-cmake-doxygen.patch

BuildRequires:	cmake ninja make
BuildRequires:	gcc-gfortran
BuildRequires:	lib64absl-devel >= 20250127.0
BuildRequires:	doxygen
Requires:	%{blas_libname} = %{version}-%{release}

%global _description_lapack %{expand:
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
}

%global _description_blas %{expand:
BLAS (Basic Linear Algebra Subprograms) is a standard library which
provides a number of basic algorithms for numerical algebra.
}

%description	%_description_lapack

####################################
# lapack-lib
%package	-n	%{lapack_libname}
Summary:	LAPACK Libraries for Linear Algebra
Group:		Sciences/Mathematics
Provides:	%{blas_libname} = %{version}-%{release}
Suggests:	%{lapack_docname} = %{version}-%{release}
Obsoletes:	%{lapack_oldlibname} < %{EVRD}

%description	-n %{lapack_libname} %_description_lapack
%if 0%{?arch64}
Includes 64bit and 64bit INDEX Libraries both
with and without symbol name suffixes
%endif

####################################
# lapack-devel
%package	-n %{lapack_devname}
Summary:	LAPACK Development Libraries
Group:		Sciences/Mathematics
Requires:	%{lapack_libname}%{_isa} = %{version}-%{release}
Requires:	%{blas_devname}%{_isa} = %{version}-%{release}
Suggests:	%{lapack_docname} = %{version}-%{release}
Obsoletes:	%{lapack_olddevname} < %{EVRD}

%description -n %{lapack_devname}
LAPACK Development Libraries (shared).

####################################
# lapack-static-devel
%package	-n %{lapack_staticdevname}
Summary:	LAPACK Static Libraries
Group:		Sciences/Mathematics
Requires:	%{lapack_devname}%{?_isa} = %{version}-%{release}

%description	-n %{lapack_staticdevname}
LAPACK Static Libraries.

####################################
# lapack-doc
%package	-n %{lapack_docname}
Summary:	LAPACK and LBAS Documentation
Group:		Sciences/Mathematics
BuildArch:	noarch
Provides:	%{lapack_docname} = %{version}-%{release}
Obsoletes:	%{name}-doc < %{EVRD}

%description	-n %{lapack_docname}
Documentation html and man pages for LAPACK and BLAS.

####################################
# blas-lib
%package	-n %{blas_libname}
Summary:	The Basic Linear Algebra Subprograms Library
Group:		Sciences/Mathematics
Provides:	%{blas_libname} = %{version}-%{release}
Suggests:	%{lapack_docname} = %{version}-%{release}
Obsoletes:	%{blas_oldlibname} < %{EVRD}

%description	-n %{blas_libname} %_description_blas
%if 0%{?arch64}
Includes 64bit and 64bit INDEX Libraries both
with and without symbol name suffixes
%endif

####################################
# blas-devel
%package	-n %{blas_devname}
Summary:	BLAS Development Libraries
Group:		Sciences/Mathematics
Requires:	%{blas_libname}%{_isa} = %{version}-%{release}
Requires:	gcc-gfortran
Obsoletes:	%{blas_olddevname} < %{EVRD}

%description	-n %{blas_devname}
BLAS Development Libraries (shared).

####################################
# blas-static-devel
%package	-n %{blas_staticdevname}
Summary:	BLAS Static Libraries
Group:		Sciences/Mathematics
Requires:	%{blas_devname}%{_isa} = %{version}-%{release}

%description -n %{blas_staticdevname}
BLAS Static Libraries.


####################################
%prep
%autosetup -p1
mkdir -p ./build/DOCS/
cp ./DOCS/* ./build/DOCS
# copy makefile and make.inc into build for manpage and html generation
cp Makefile ./build
cp make.inc.example ./build/make.inc


####################################
%build
%global optflags %{optflags} -fno-optimize-sibling-calls
export default_optflags="-g %{optflags}"
# hush the build log fortran f951 warning spam, substantially reduces log size
export FFLAGS="-fallow-argument-mismatch"
export CC=/usr/bin/gcc
export CXX=/usr/bin/g++
export FC=/usr/bin/gfortran

####################################
# Shared Regular Libraries, man page & html doc generation.
# NOTE	doc generation requires this build stage's files to generate from.
%global optflags ${default_optflags}
%cmake  -G Ninja -DCMAKE_SKIP_RPATH:BOOL=ON -DBUILD_DEPRECATED=ON \
		-DBUILD_SHARED_LIBS=ON -DLAPACKE=ON -DLAPACKE_WITH_TMG=ON -DCBLAS=ON
%ninja_build
make man
make html
cd ..
# move docs out to own directory to preserve for install stage
mkdir -p %_vpath_builddir-DOCS
cp -r %_vpath_builddir/DOCS/* %_vpath_builddir-DOCS
mkdir -p %_vpath_builddir-SHARED
mv %_vpath_builddir/* %_vpath_builddir-SHARED


####################################
# Static Regular Libraries
%global optflags ${default_optflags} -fPIC
%cmake -G Ninja -DBUILD_DEPRECATED=ON -DBUILD_SHARED_LIBS=OFF -DLAPACKE=ON \
		-DLAPACKE_WITH_TMG=ON -DCBLAS=ON
%ninja_build
cd ..
mv %_vpath_builddir %_vpath_builddir-STATIC


####################################
# 64bit INDEX Libraries
%if 0%{?arch64}
# BLAS Shared 64bit INDEX Libraries
%global optflags ${default_optflags}
%cmake -G Ninja -DCMAKE_SKIP_RPATH:BOOL=ON -DBUILD_DEPRECATED=ON \
		-DBUILD_SHARED_LIBS=ON -DBUILD_INDEX64=ON -DLAPACKE=OFF -DCBLAS=ON
%ninja_build
cd ..
mv %_vpath_builddir %_vpath_builddir-SHARED64

# BLAS Static 64 bit INDEX Libraries
%global optflags ${default_optflags} -fPIC
%cmake -G Ninja -DBUILD_DEPRECATED=ON -DBUILD_SHARED_LIBS=OFF \
		-DBUILD_INDEX64=ON -DLAPACKE=OFF -DCBLAS=ON
%ninja_build
cd ..
mv %_vpath_builddir %_vpath_builddir-STATIC64

# BLAS Shared 64bit INDEX SUFFIX Libraries
%global optflags ${default_optflags}
sed -i 's|64"|64_"|g' CMakeLists.txt
%cmake -G Ninja -DCMAKE_SKIP_RPATH:BOOL=ON -DBUILD_DEPRECATED=ON \
		-DBUILD_SHARED_LIBS=ON -DBUILD_INDEX64=ON -DLAPACKE=OFF -DCBLAS=ON
%ninja_build
cd ..
mv %_vpath_builddir %_vpath_builddir-SHARED64SUFFIX

# BLAS Static 64bit INDEX SUFFIX Libraries
%global optflags ${default_optflags} -fPIC
%cmake -G Ninja -DBUILD_DEPRECATED=ON -DBUILD_SHARED_LIBS=OFF \
		-DBUILD_INDEX64=ON -DLAPACKE=OFF -DCBLAS=ON
%ninja_build
cd ..
mv %_vpath_builddir %_vpath_builddir-STATIC64SUFFIX

# Undo the 64_ suffix
sed -i 's|64_"|64"|g' CMakeLists.txt
%endif

####################################
# LAPACK Static regular FPIC Libraries
%global optflags ${default_optflags} -fPIC
%cmake -G Ninja -DBUILD_DEPRECATED=ON -DBUILD_SHARED_LIBS=OFF -DLAPACKE=OFF
%ninja_build
cd ..
mv %_vpath_builddir %_vpath_builddir-STATICFPIC
mv %_vpath_builddir-STATICFPIC/lib/liblapack.a %_vpath_builddir-STATICFPIC/lib/liblapack_pic.a

####################################
%if 0%{?arch64}
# LAPACK Static 64bit INDEX FPIC Libraries
%global optflags ${default_optflags} -fPIC
%cmake -G Ninja -DBUILD_DEPRECATED=ON -DBUILD_SHARED_LIBS=OFF \
		-DBUILD_INDEX64=ON -DLAPACKE=OFF -DCBLAS=OFF
%ninja_build
cd ..
mv %_vpath_builddir %_vpath_builddir-STATIC64FPIC
mv %_vpath_builddir-STATIC64FPIC/lib/liblapack64.a %_vpath_builddir-STATIC64FPIC/lib/liblapack_pic64.a

# LAPACK Static 64bit INDEX suffixed FPIC Libraries
%global optflags ${default_optflags} -fPIC
sed -i 's|64"|64_"|g' CMakeLists.txt
%cmake -G Ninja -DBUILD_DEPRECATED=ON -DBUILD_SHARED_LIBS=OFF \
		-DBUILD_INDEX64=ON -DLAPACKE=OFF -DCBLAS=OFF
%ninja_build
cd ..
mv %_vpath_builddir %_vpath_builddir-STATIC64SUFFIXFPIC
mv %_vpath_builddir-STATIC64SUFFIXFPIC/lib/liblapack64_.a %_vpath_builddir-STATIC64SUFFIXFPIC/lib/liblapack_pic64_.a

# Undo the 64_ suffix
sed -i 's|64_"|64"|g' CMakeLists.txt
%endif

####################################
# copy source scripts, pdf file and CBLAS.md into build
cp -p %{SOURCE1} %_vpath_builddir-DOCS/lapackqref.ps
cp -p %{SOURCE2} %_vpath_builddir-DOCS/blasqr.ps
cp -p DOCS/lapacke.pdf %_vpath_builddir-DOCS/lapacke.pdf
cp -p DOCS/CBLAS.md %_vpath_builddir-DOCS/CBLAS.md


####################################
%install
%if 0%{?arch64}
for i in SHARED SHARED64 STATIC STATIC64; do
%else
for i in SHARED STATIC; do
%endif
	mv	%_vpath_builddir-$i %_vpath_builddir
	cd %_vpath_builddir
	%ninja_install
	cd ..
	mv %_vpath_builddir %_vpath_builddir-$i
done


%if 0%{?arch64}
sed -i 's|64"|64_"|g' CMakeLists.txt
for i in SHARED64SUFFIX STATIC64SUFFIX; do
	mv %_vpath_builddir-$i %_vpath_builddir
	cd %_vpath_builddir
	%ninja_install
	cd ..
	mv %_vpath_builddir %_vpath_builddir-$i
done
%endif

####################################
# install html and man directories
install -dpm 0755 %{buildroot}%{_docdir}/%{name}/html
install -dpm 0755 %{buildroot}%{_mandir}/man3
# move docs and ps files into docdir
cp -p README.md %{buildroot}%{_docdir}/%{name}
cp -p LICENSE %{buildroot}%{_docdir}/%{name}
mv %_vpath_builddir-DOCS/lapackqref.ps %{buildroot}%{_docdir}/%{name}
mv %_vpath_builddir-DOCS/blasqr.ps %{buildroot}%{_docdir}/%{name}
mv %_vpath_builddir-DOCS/lapacke.pdf %{buildroot}%{_docdir}/%{name}
mv %_vpath_builddir-DOCS/CBLAS.md %{buildroot}%{_docdir}/%{name}

# move html from builddir in to docdir
mv %_vpath_builddir-DOCS/html %{buildroot}%{_docdir}/%{name}

# remove junk manpages
rm %_vpath_builddir-DOCS/man/man3/_home*.3
rm %_vpath_builddir-DOCS/man/man3/__*_.3
# compress manpages & remove input files after compression: 41.8 MiB => 9.44 MiB
zstd -r --rm %_vpath_builddir-DOCS/man/man3
# move man pages from builddir in to mandir
mv %_vpath_builddir-DOCS/man/man3 %{buildroot}%{_mandir}
####################################

install -m0644 %_vpath_builddir-STATICFPIC/lib/liblapack_pic.a %{buildroot}%{_libdir}
%if 0%{?arch64}
install -m0644 %_vpath_builddir-STATIC64FPIC/lib/liblapack_pic64.a %{buildroot}%{_libdir}
install -m0644 %_vpath_builddir-STATIC64SUFFIXFPIC/lib/liblapack_pic64_.a %{buildroot}%{_libdir}

pushd %{buildroot}%{_libdir}
for name in blas cblas lapack; do
	for i in `readelf -Ws lib${name}64_.so.%{version} | awk '{print $8}' | grep -v GLIBC |grep -v GFORTRAN |grep -v "Name" `; do echo "$i" "64_$i"; done > ${name}-prefix.def.dirty
	sort -n ${name}-prefix.def.dirty | uniq > ${name}-prefix.def
	llvm-objcopy --redefine-syms ${name}-prefix.def lib${name}64_.so.%{version} lib${name}64_.so.%{version}.fixed
	rm -rf lib${name}64_.so.%{version}
	mv lib${name}64_.so.%{version}.fixed lib${name}64_.so.%{version}
done

for name in blas cblas lapack lapack_pic; do
	for i in `llvm-nm lib${name}64_.a |grep " T " | awk '{print $3}'`; do echo "$i" "64_$i"; done > ${name}-static-prefix.def.dirty
	sort -n ${name}-static-prefix.def.dirty | uniq > ${name}-static-prefix.def
	llvm-objcopy --redefine-syms ${name}-static-prefix.def lib${name}64_.a lib${name}64_.a.fixed
	rm -rf lib${name}64_.a
	mv lib${name}64_.a.fixed lib${name}64_.a
done
popd
# remove def build artifacts
rm -rf %{buildroot}%{_libdir}/*.def*
%endif


####################################
%files	-n %{lapack_libname}
%{_libdir}/liblapack.so.*
%{_libdir}/liblapacke.so.*
%{_libdir}/libtmglib.so.*
%if 0%{?arch64}
%{_libdir}/liblapack64.so.*
%{_libdir}/liblapack64_.so.*
%endif
%doc README.md
%doc LICENSE

%files -n %{lapack_docname}
%{_mandir}/man3/*.3*
%{_docdir}/%{name}/html
%{_docdir}/%{name}/README.md
%{_docdir}/%{name}/LICENSE
%{_docdir}/%{name}/lapacke.pdf
%{_docdir}/%{name}/CBLAS.md
%{_docdir}/%{name}/lapackqref.ps
%{_docdir}/%{name}/blasqr.ps

%files -n %{lapack_devname}
%{_includedir}/lapack*.h
%{_libdir}/liblapack.so
%{_libdir}/liblapacke.so
%{_libdir}/libtmglib.so
%{_libdir}/cmake/lapack-*
%{_libdir}/cmake/lapacke-*
%{_libdir}/pkgconfig/lapack.pc
%{_libdir}/pkgconfig/lapacke.pc
%if 0%{?arch64}
%{_libdir}/liblapack64.so
%{_libdir}/cmake/lapack64*
%{_libdir}/pkgconfig/lapack64.pc
%{_libdir}/liblapack64_.so
%{_libdir}/pkgconfig/lapack64_.pc
%endif

%files -n %{lapack_staticdevname}
%{_libdir}/liblapack.a
%{_libdir}/liblapack_pic.a
%{_libdir}/liblapacke.a
%{_libdir}/libtmglib.a
%if 0%{?arch64}
%{_libdir}/liblapack64.a
%{_libdir}/liblapack_pic64.a
%{_libdir}/liblapack64_.a
%{_libdir}/liblapack_pic64_.a
%endif

%files -n %{blas_libname}
%{_libdir}/libblas.so.*
%{_libdir}/libcblas.so.*
%if 0%{?arch64}
%doc README.md
%doc LICENSE
%{_libdir}/libblas64.so.*
%{_libdir}/libcblas64.so.*
%{_libdir}/libblas64_.so.*
%{_libdir}/libcblas64_.so.*
%endif

%files -n %{blas_devname}
%{_includedir}/cblas*.h
%{_libdir}/libblas.so
%{_libdir}/libcblas.so
%{_libdir}/cmake/cblas-*
%{_libdir}/pkgconfig/blas.pc
%{_libdir}/pkgconfig/cblas.pc
%if 0%{?arch64}
%{_libdir}/libblas64.so
%{_libdir}/libcblas64.so
%{_libdir}/cmake/cblas64*
%{_libdir}/pkgconfig/blas64.pc
%{_libdir}/pkgconfig/cblas64.pc
%{_libdir}/libblas64_.so
%{_libdir}/libcblas64_.so
%{_libdir}/pkgconfig/blas64_.pc
%{_libdir}/pkgconfig/cblas64_.pc
%endif

%files -n %{blas_staticdevname}
%{_libdir}/libblas.a
%{_libdir}/libcblas.a
%if 0%{?arch64}
%{_libdir}/libblas64.a
%{_libdir}/libcblas64.a
%{_libdir}/libblas64_.a
%{_libdir}/libcblas64_.a
%endif

