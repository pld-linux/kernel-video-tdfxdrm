
# conditional build
# _without_dist_kernel          without distribution kernel

%define		_kernel_ver	%(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		_kernel_ver_str	%(echo %{_kernel_ver} | sed s/-/_/g)
%define		_rel 3

Summary:	TDFX DRM Driver
Summary(pl):	Sterownik DRM do kart 3Dfx
Name:		kernel-video-tdfxdrm
Version:	1.0
Release:	%{_rel}@%{_kernel_ver_str}
License:	MIT
Group:		Base/Kernel
Source0:	tdfxdrm.tgz
%{!?_without_dist_kernel:BuildRequires:         kernel-headers < 2.4.0 }
PreReq:		/sbin/depmod
%{!?_without_dist_kernel:Requires:	kernel-up = %{_kernel_ver}}
Obsoletes:	tdfxdrm
Obsoletes:	kernel-smp-video-tdfxdrm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides a device driver to allow 3dfx hardware to work
in the direct rendering manager.

%description -l pl
Ten pakiet zawiera sterowniki który pozwala na u¿ywanie sprzêtu 3dfx z
DRM (Direct Rendering Manager).

%package -n kernel-smp-video-tdfxdrm
Summary:	TDFX DRM Driver
Summary(pl):	Sterownik DRM do kart 3Dfx
Release:	%{_rel}@%{_kernel_ver_str}
%{!?_without_dist_kernel:Requires:     kernel-smp = %{_kernel_ver}}
Obsoletes:	kernel-video-tdfxdrm
Obsoletes:	tdfxdrm
PreReq:		/sbin/depmod
Group:		Base/Kernel

%description -n kernel-smp-video-tdfxdrm
This package provides a device driver for SMP to allow 3dfx hardware
to work in the direct rendering manager.

%description -n kernel-smp-video-tdfxdrm -l pl
Ten pakiet zawiera sterowniki który pozwala na u¿ywanie sprzêtu 3dfx z
DRM (Direct Rendering Manager) w systemach SMP

%prep
%setup -q -c

%build
%{__make} -f Makefile.linux tdfx.o AGP=1 SMP=1 CC="kgcc -DCONFIG_X86_LOCAL_APIC"
mv tdfx.o tdfx.o-smp
%{__make} -f Makefile.linux clean
%{__make} -f Makefile.linux tdfx.o AGP=1 CC="kgcc"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/video
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/video
install tdfx.o-smp $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/video/tdfx.o
install tdfx.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/video/tdfx.o

gzip -9nf README.drm

%clean 
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%post -n kernel-smp-video-tdfxdrm
/sbin/depmod -a

%postun -n kernel-smp-video-tdfxdrm
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc *.gz
/lib/modules/%{_kernel_ver}/video/*

%files -n kernel-smp-video-tdfxdrm
%defattr(644,root,root,755)
%doc *.gz
/lib/modules/%{_kernel_ver}smp/video/*
