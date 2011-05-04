# lapack
%define major 3
%define minor 3.0
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
Patch0:		lapack-3.1.1-make.inc.patch
Patch1:		lapack-3.3.0-Makefile.patch
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
%setup -q
%patch0 -p1
%patch1 -p0

tar zxf %SOURCE3

cp -f INSTALL/make.inc.gfortran make.inc

# add Makefile entries for building static/shared libs
cat >> SRC/Makefile <<EOF

static: \$(ALLOBJ) \$(ALLXOBJ)
	\$(ARCH) \$(ARCHFLAGS) liblapack.a \$(ALLOBJ) \$(ALLXOBJ)
	\$(RANLIB) liblapack.a

shared: \$(ALLOBJ) \$(ALLXOBJ)
	cc \$(CFLAGS) -shared -Wl,-soname,liblapack.so.%{major} -o liblapack.so.%{version} \$(ALLOBJ) \$(ALLXOBJ) -L.. -lblas -lm -lgfortran -lc
EOF

cat >> BLAS/SRC/Makefile <<EOF

static: \$(ALLOBJ)
	\$(ARCH) \$(ARCHFLAGS) libblas.a \$(ALLOBJ)
	\$(RANLIB) libblas.a

shared: \$(ALLOBJ)
	cc \$(CFLAGS) -shared -Wl,-soname,libblas.so.%{major} -o libblas.so.%{version} \$(ALLOBJ) -lm -lgfortran -lc
EOF

%build
export FC=gfortran
export CFLAGS="%{optflags} -funroll-all-loops"
export FFLAGS=$CFLAGS

# Build BLAS
pushd BLAS/SRC
%make FFLAGS="$FFLAGS" OPTS="$FFLAGS" dcabs1.o
%make FFLAGS="$FFLAGS" CFLAGS="$CFLAGS" OPTS="$CFLAGS" static
cp libblas.a ${RPM_BUILD_DIR}/%{name}-%{version}/
%make clean
%make FFLAGS="$FFLAGS -Os -fPIC" OPTS="$FFLAGS -Os -fPIC" dcabs1.o
%make FFLAGS="$FFLAGS -fPIC" CFLAGS="$CFLAGS -fPIC" OPTS="$CFLAGS -fPIC" shared
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
%make FFLAGS="$FFLAGS" CFLAGS="$CFLAGS" NOOPT="$CFLAGS -Os" OPTS="$CFLAGS" static
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
%make FFLAGS="$FFLAGS -fPIC" CFLAGS="$CFLAGS -fPIC" NOOPT="$CFLAGS -Os -fPIC" OPTS="$CFLAGS -fPIC" shared
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
%make FFLAGS="$CFLAGS -fPIC" CFLAGS="$CFLAGS -fPIC" NOOPT="$CFLAGS -Os -fPIC" OPTS="$CFLAGS -fPIC" static
cp liblapack.a ${RPM_BUILD_DIR}/%{name}-%{version}/liblapack_pic.a
popd

cp %{SOURCE1} lapackqref.ps
cp %{SOURCE2} blasqr.ps

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
ln -sf libblas.so.%{version} libblas.so
ln -sf libblas.so.%{version} libblas.so.3
popd

touch lapack-man-pages
for file in lapack-3.2.0/manpages/man/manl/*; do
    install -m 644 $file %{buildroot}%{_mandir}/man3/`basename $file .l`.3
    echo %{_mandir}/man3/`basename $file .l`.3.xz >> lapack-man-pages
done
touch blas-man-pages
for file in lapack-3.2.0/manpages/blas/man/manl/*; do
    install -m 644 $file %{buildroot}%{_mandir}/man3/`basename $file .l`.3
    echo %{_mandir}/man3/`basename $file .l`.3.xz >> blas-man-pages
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

%files -n %{docname} -f lapack-man-pages
%doc README lapackqref.ps

%files -n %{libblasname}
%defattr(-,root,root)
%{_libdir}/libblas.so.%{major}*

%files -n %{develblasname}
%defattr(-,root,root,-)
%{_libdir}/libblas.so
%{_libdir}/libblas*.a

%files -n %{docblasname} -f blas-man-pages
%doc blasqr.ps
