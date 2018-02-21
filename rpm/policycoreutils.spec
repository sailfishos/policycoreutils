# based on work by The Fedora Project (2017)
# Copyright (c) 1998, 1999, 2000 Thai Open Source Software Center Ltd
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

%global libauditver     2.1.3-4
%global libsepolver     2.7-3
%global libsemanagever  2.7-5
%global libselinuxver   2.7-6
%global sepolgenver     2.7

%global generatorsdir %{_prefix}/lib/systemd/system-generators
%define python3_sitearch /%{_libdir}/python3.?/site-packages
%define python3_sitelib /%{_libdir}/python3.?/site-packages

Summary: SELinux policy core utilities
Name:    policycoreutils
Version: 2.7
Release: 10%{?dist}
License: GPLv2
Group:   System Environment/Base
Source: %{name}-%{version}.tar.bz2
URL:     https://github.com/SELinuxProject
Source15: selinux-autorelabel
Source16: selinux-autorelabel.service
Source17: selinux-autorelabel-mark.service
Source18: selinux-autorelabel.target
Source19: selinux-autorelabel-generator.sh
Patch0: systemd_unitdir.patch
Obsoletes: policycoreutils < 2.0.61-2
#Conflicts: filesystem < 3, selinux-policy-base < 3.13.1-138
# initscripts < 9.66 shipped fedora-autorelabel services which are renamed to selinux-relabel
#Conflicts: initscripts < 9.66
Provides: /sbin/fixfiles
Provides: /sbin/restorecon

BuildRequires: pam-devel libcap-ng-devel libsepol-static >= %{libsepolver} libsemanage-static >= %{libsemanagever} libselinux-devel >= %{libselinuxver}  libcap-devel audit-libs-devel >=  %{libauditver} gettext
BuildRequires: dbus-devel dbus-glib-devel
BuildRequires: python3-devel
BuildRequires: systemd
# we don't build python2 modules, but make clean expects python2 (could be patched out though)
BuildRequires: python
Requires: util-linux grep gawk diffutils rpm sed
Requires: libsepol >= %{libsepolver} coreutils libselinux-utils >=  %{libselinuxver}

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

policycoreutils contains the policy core utilities that are required
for basic operation of a SELinux system.  These utilities include
load_policy to load policies, setfiles to label filesystems, newrole
to switch roles.

%prep
%setup -q -n %{name}-%{version}/upstream
%patch0 -p 1

%build
make -C policycoreutils LSPP_PRIV=y SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" CFLAGS="%{optflags} -fPIE" LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now" SEMODULE_PATH="/usr/sbin" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C python SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" CFLAGS="%{optflags} -fPIE" LDFLAGS="-pie -Wl,-z,relro" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C dbus SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" CFLAGS="%{optflags} -fPIE" LDFLAGS="-pie -Wl,-z,relro" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C semodule-utils SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" CFLAGS="%{optflags} -fPIE" LDFLAGS="-pie -Wl,-z,relro" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C restorecond SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" CFLAGS="%{optflags} -fPIE" LDFLAGS="-pie -Wl,-z,relro" LIBSEPOLA="%{_libdir}/libsepol.a" all

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man5
mkdir -p %{buildroot}%{_mandir}/man8
%{__mkdir} -p %{buildroot}/%{_usr}/share/doc/%{name}/

make -C policycoreutils LSPP_PRIV=y  DESTDIR="%{buildroot}" SBINDIR="%{buildroot}%{_sbindir}" LIBDIR="%{buildroot}%{_libdir}" SEMODULE_PATH="/usr/sbin" LIBSEPOLA="%{_libdir}/libsepol.a" install

make -C python PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{buildroot}%{_sbindir}" LIBDIR="%{buildroot}%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install

make -C dbus PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{buildroot}%{_sbindir}" LIBDIR="%{buildroot}%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install

make -C semodule-utils PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{buildroot}%{_sbindir}" LIBDIR="%{buildroot}%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install

make -C restorecond PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{buildroot}%{_sbindir}" LIBDIR="%{buildroot}%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install


# Systemd
rm -rf %{buildroot}/%{_sysconfdir}/rc.d/init.d/restorecond

rm -f %{buildroot}/usr/share/man/man8/open_init_pty.8
rm -f %{buildroot}/usr/sbin/open_init_pty
rm -f %{buildroot}/usr/sbin/run_init
rm -f %{buildroot}/etc/pam.d/run_init*
rm -f %{buildroot}/usr/share/man/man8/sepolicy-gui.8*
rm -f %{buildroot}/usr/share/man/man8/run_init.8*
rm -f %{buildroot}/usr/lib/python3.4/site-packages/sepolicy/sepolicy.glade
rm -f %{buildroot}/usr/lib/python3.4/site-packages/sepolicy/gui.py

# https://bugzilla.redhat.com/show_bug.cgi?id=1328825
mkdir   -m 755 -p %{buildroot}/%{_unitdir}/basic.target.wants/
mkdir   -m 755 -p %{buildroot}/%{generatorsdir}
install -m 644 -p %{SOURCE16} %{buildroot}/%{_unitdir}/
install -m 644 -p %{SOURCE17} %{buildroot}/%{_unitdir}/
install -m 644 -p %{SOURCE18} %{buildroot}/%{_unitdir}/
install -m 755 -p %{SOURCE19} %{buildroot}/%{generatorsdir}/
install -m 755 -p %{SOURCE15} %{buildroot}/%{_libexecdir}/selinux/
ln -s ../selinux-autorelabel-mark.service %{buildroot}/%{_unitdir}/basic.target.wants/

# change /usr/bin/python to %%{__python3} in policycoreutils-python3
find %{buildroot}%{python3_sitelib} %{buildroot}%{python3_sitearch} -type f | xargs \
    sed -i '1s%\(#! *\)/usr/bin/python\([^3].*\|\)$%\1%{__python3}\2%'

# change /usr/bin/python to %%{__python3} in python-utils
sed -i '1s%\(#! *\)/usr/bin/python\([^3].*\|\)$%\1%{__python3}\2%' \
    %{buildroot}%{_sbindir}/semanage \
    %{buildroot}%{_bindir}/chcat \
    %{buildroot}%{_bindir}/audit2allow \
    %{buildroot}%{_bindir}/audit2why \
    %{buildroot}%{_bindir}/sepolicy \
    %{buildroot}%{_bindir}/sepolgen{,-ifgen} \
    %nil

%find_lang %{name}

%package python-utils
Summary:    SELinux policy core python utilities
Requires:   policycoreutils-python3 = %{version}-%{release}
Obsoletes:  policycoreutils-python <= 2.4-4

%description python-utils
The policycoreutils-python-utils package contains the management tools use to manage
an SELinux environment.

%files python-utils
%{_sbindir}/semanage
%{_bindir}/chcat
%{_bindir}/audit2allow
%{_bindir}/audit2why
%{_mandir}/man1/audit2allow.1*
%{_bindir}/semodule_package
%{_mandir}/man8/semodule_package.8*
%{_mandir}/man1/audit2why.1*
%{_sysconfdir}/dbus-1/system.d/org.selinux.conf
%{_mandir}/man8/chcat.8*
%{_mandir}/man8/semanage*.8*
%{_datadir}/bash-completion/completions/semanage
%{_datadir}/bash-completion/completions/setsebool

%package dbus
Summary:    SELinux policy core DBUS api
Requires:   policycoreutils-python3 = %{version}-%{release}
Requires:   python3-slip-dbus

%description dbus
The policycoreutils-dbus package contains the management DBUS API use to manage
an SELinux environment.

%files dbus
%{_sysconfdir}/dbus-1/system.d/org.selinux.conf
%{_datadir}/dbus-1/system-services/org.selinux.service
%{_datadir}/polkit-1/actions/org.selinux.policy
%{_datadir}/system-config-selinux/selinux_server.py*

%package python3
Summary: SELinux policy core python3 interfaces
Group:   System Environment/Base
Requires:policycoreutils = %{version}-%{release}
Requires:libsemanage-python3 >= %{libsemanagever} libselinux-python3 libcgroup
Requires:audit-libs-python3 >=  %{libauditver}
Requires: python3-IPy
Requires: checkpolicy
Requires: setools-python3 >= 4.1.1

%description python3
The policycoreutils-python3 package contains the interfaces that can be used
by python 3 in an SELinux environment.

%files python3
%{python3_sitearch}/seobject.py*
%{python3_sitearch}/__pycache__
%{python3_sitearch}/sepolgen
%dir %{python3_sitelib}/sepolicy
%{python3_sitelib}/sepolicy/templates
%dir %{python3_sitelib}/sepolicy/help
%{python3_sitelib}/sepolicy/help/*
%{python3_sitelib}/sepolicy/__init__.py*
%{python3_sitelib}/sepolicy/booleans.py*
%{python3_sitelib}/sepolicy/communicate.py*
%{python3_sitelib}/sepolicy/generate.py*
%{python3_sitelib}/sepolicy/interface.py*
%{python3_sitelib}/sepolicy/manpage.py*
%{python3_sitelib}/sepolicy/network.py*
%{python3_sitelib}/sepolicy/transition.py*
%{python3_sitelib}/sepolicy/sedbus.py*
%{python3_sitelib}/sepolicy*.egg-info
%{python3_sitelib}/sepolicy/__pycache__

%package devel
Summary: SELinux policy core policy devel utilities
Group:   System Environment/Base
Requires: policycoreutils-python-utils = %{version}-%{release}
Requires: /usr/bin/make dnf
Requires: selinux-policy-devel

%description devel
The policycoreutils-devel package contains the management tools use to develop policy in an SELinux environment.

%files devel
%{_bindir}/sepolgen
%{_bindir}/sepolgen-ifgen
%{_bindir}/sepolgen-ifgen-attr-helper
%dir  /var/lib/sepolgen
/var/lib/sepolgen/perm_map
%{_bindir}/sepolicy
%{_mandir}/man8/sepolgen.8*
%{_mandir}/man8/sepolicy-booleans.8*
%{_mandir}/man8/sepolicy-generate.8*
%{_mandir}/man8/sepolicy-interface.8*
%{_mandir}/man8/sepolicy-network.8*
%{_mandir}/man8/sepolicy.8*
%{_mandir}/man8/sepolicy-communicate.8*
%{_mandir}/man8/sepolicy-manpage.8*
%{_mandir}/man8/sepolicy-transition.8*
%{_usr}/share/bash-completion/completions/sepolicy
%{_bindir}/semodule_expand
%{_bindir}/semodule_link
%{_bindir}/semodule_unpackage
%{_bindir}/semodule_deps
%{_mandir}/man8/semodule_expand.8*
%{_mandir}/man8/semodule_link.8*
%{_mandir}/man8/semodule_unpackage.8*
%{_mandir}/man8/semodule_deps.8*

%package newrole
Summary: The newrole application for RBAC/MLS
Group: System Environment/Base
Requires: policycoreutils = %{version}-%{release}

%description newrole
RBAC/MLS policy machines require newrole as a way of changing the role
or level of a logged in user.

%files newrole
%attr(0755,root,root) %caps(cap_dac_read_search,cap_setpcap,cap_audit_write,cap_sys_admin,cap_fowner,cap_chown,cap_dac_override=pe) %{_bindir}/newrole
%{_mandir}/man1/newrole.1.gz
%config(noreplace) %{_sysconfdir}/pam.d/newrole

%files -f %{name}.lang
%{_sbindir}/restorecon
%{_sbindir}/restorecon_xattr
%{_sbindir}/fixfiles
%{_sbindir}/setfiles
%{_sbindir}/load_policy
%{_sbindir}/genhomedircon
%{_sbindir}/setsebool
%{_sbindir}/semodule
%{_sbindir}/sestatus
%{_bindir}/secon
%{_libexecdir}/selinux/hll
%{_libexecdir}/selinux/selinux-autorelabel
%{_unitdir}/selinux-autorelabel-mark.service
%{_unitdir}/basic.target.wants/selinux-autorelabel-mark.service
%{_unitdir}/selinux-autorelabel.service
%{_unitdir}/selinux-autorelabel.target
%{generatorsdir}/selinux-autorelabel-generator.sh
%config(noreplace) %{_sysconfdir}/sestatus.conf
# selinux-policy Requires: policycoreutils, so we own this set of directories and our files within them
%{_mandir}/man5/selinux_config.5.gz
%{_mandir}/man5/sestatus.conf.5.gz
%{_mandir}/man8/fixfiles.8*
%{_mandir}/man8/load_policy.8*
%{_mandir}/man8/restorecon.8*
%{_mandir}/man8/restorecon_xattr.8*
%{_mandir}/man8/semodule.8*
%{_mandir}/man8/sestatus.8*
%{_mandir}/man8/setfiles.8*
%{_mandir}/man8/setsebool.8*
%{_mandir}/man1/secon.1*
%{_mandir}/man8/genhomedircon.8*
%doc policycoreutils/COPYING
%doc %{_usr}/share/doc/%{name}

%package restorecond
Summary: SELinux restorecond utilities
Group:   System Environment/Base
#BuildRequires: systemd-units

%description restorecond
The policycoreutils-restorecond package contains the restorecond service.

%files restorecond
%{_sbindir}/restorecond
%{_unitdir}/restorecond.service
%config(noreplace) %{_sysconfdir}/selinux/restorecond.conf
%config(noreplace) %{_sysconfdir}/selinux/restorecond_user.conf
%{_sysconfdir}/xdg/autostart/restorecond.desktop
%{_datadir}/dbus-1/services/org.selinux.Restorecond.service
%{_mandir}/man8/restorecond.8*
%doc policycoreutils/COPYING

%post restorecond
%systemd_post restorecond.service

%preun restorecond
%systemd_preun restorecond.service

%postun restorecond
%systemd_postun_with_restart restorecond.service
