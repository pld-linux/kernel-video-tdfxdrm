#
# Conditional build:
# _without_dist_kernel          without distribution kernel
#
Summary:	TDFX DRM Driver
Summary(pl):	Sterownik DRM do kart 3Dfx
Name:		kernel-video-tdfxdrm
Version:	1.0
%define	_rel	10
Release:	%{_rel}@%{_kernel_ver_str}
License:	MIT
Group:		Base/Kernel
Source0:	tdfxdrm.tgz
%{!?_without_dist_kernel:BuildRequires:         kernel-headers < 2.4.0 }
BuildRequires:	%{kgcc_package}
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Obsoletes:	tdfxdrm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides a device driver to allow 3dfx hardware to work
in the direct rendering manager.

%description -l pl
Ten pakiet zawiera sterowniki kt�ry pozwala na u�ywanie sprz�tu 3dfx z
DRM (Direct Rendering Manager).

%package -n kernel-smp-video-tdfxdrm
Summary:	TDFX DRM Driver
Summary(pl):	Sterownik DRM do kart 3Dfx
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Obsoletes:	tdfxdrm

%description -n kernel-smp-video-tdfxdrm
This package provides a device driver for SMP to allow 3dfx hardware
to work in the direct rendering manager.

%description -n kernel-smp-video-tdfxdrm -l pl
Ten pakiet zawiera sterowniki kt�ry pozwala na u�ywanie sprz�tu 3dfx z
DRM (Direct Rendering Manager) w systemach SMP

%prep
%setup -q -c

%build
%{__make} -f Makefile.linux tdfx.o AGP=1 SMP=1 CC="%{kgcc} -DCONFIG_X86_LOCAL_APIC"
mv -f tdfx.o tdfx.o-smp
%{__make} -f Makefile.linux clean
%{__make} -f Makefile.linux tdfx.o AGP=1 CC="%{kgcc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

install tdfx.o-smp $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/tdfx.o
install tdfx.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/tdfx.o

%clean 
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a -F /boot/System.map-%{_kernel_ver} %{_kernel_ver}

%postun
/sbin/depmod -a -F /boot/System.map-%{_kernel_ver} %{_kernel_ver}

%post	-n kernel-smp-video-tdfxdrm
/sbin/depmod -a -F /boot/System.map-%{_kernel_ver}smp %{_kernel_ver}smp

%postun -n kernel-smp-video-tdfxdrm
/sbin/depmod -a -F /boot/System.map-%{_kernel_ver}smp %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc README.drm
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-video-tdfxdrm
%defattr(644,root,root,755)
%doc README.drm
/lib/modules/%{_kernel_ver}smp/misc/*
