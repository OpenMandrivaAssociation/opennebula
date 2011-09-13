#
# spec file for package opennebula (Version 2.2.1)
#
# Copyright (c) 2010 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:          opennebula
Version:       2.2.1
Release:       19.1
License:       Apache License version 2.0
Summary:       Elastic Utility Computing Architecture
URL:           http://www.opennebula.org
Group:         Productivity/Networking/System
Source0:       %{name}-%{version}.tar.bz2
Source1:       sunstone.init
Patch:         openneb_64bitlib.patch
Patch1:        openneb_creatPIDdir.patch
Patch2:        openneb_LSBhead.patch
Patch3:        openneb_xmlrpcTest.patch
Patch4:        openneb_constCorrectPool.patch
BuildRequires: post-build-checks
BuildRequires: gcc-c++
BuildRequires: libcurl-devel
BuildRequires: libxml2-devel    
BuildRequires: libxmlrpc-c-devel    >= 1.06
BuildRequires: libopenssl-devel     >= 0.9
BuildRequires: openssh
BuildRequires: pkg-config
BuildRequires: pwgen
BuildRequires: ruby                 >= 1.8.6
BuildRequires: scons                >= 0.97
BuildRequires: sqlite3-devel        >= 3.5.2
BuildRequires: xmlrpc-c             >= 1.06
Requires:      openssl              >= 0.9
Requires:      ruby                 >= 1.8.6
Requires:      rubygem-libxml-ruby
Requires:      openssh
Requires:      pwgen
Requires:      sqlite3              >= 3.5.2
Requires:      rubygem-nokogiri
Requires:      rubygem-sqlite3
Requires:      xmlrpc-c             >= 1.06
Recommends:    nfs-kernel-server
Recommends:    ypserv
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root

%description
OpenNebula.org is an open-source project aimed at building the industry
standard open source cloud computing tool to manage the complexity and
heterogeneity of distributed data center infrastructures.

The OpenNebula.org Project is maintained and driven by the community. The
OpenNebula.org community has thousands of users, contributors, and supporters,
who interact through various online email lists, blogs and innovative projects
to support each other. 

%package devel
Summary:  Development files for %{name}
Group:    Development/Libraries/Other
Requires: %{name} = %{version}

%description devel
The %{name} devel package contains man pages and examples.

%package sunstone
Summary: Browser based UI to administer an OpenNebulaCloud
Group:   Productivity/Networking/System
Requires: %{name} = %{version}
Requires: rubygem-json
Requires: rubygem-sinatra
Requires: rubygem-thin

%description sunstone
sunstone if the web base UI to manage a deployed OpenNebula Cloud

%prep
%setup -q
%patch
%patch1
%patch2
%patch3
%patch4

%build
scons sqlite_db=/usr xmlrpc=/usr

%install
export DESTDIR=%{buildroot}
install.sh
# Move the initscript
%{__mkdir} %{buildroot}/etc/init.d
%{__mv} %{buildroot}%{_bindir}/one %{buildroot}/etc/init.d
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/sunstone
#%{__mv} %{buildroot}%{_bindir}/sunstone-server %{buildroot}/etc/init.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE README
%config %{_sysconfdir}/one
%{_datadir}/one/hooks/*
%{_bindir}/econe*
%{_bindir}/o*
%{_bindir}/mm_sched
/usr/lib/one/mads/*
/usr/lib/one/remotes/*
/usr/lib/one/ruby/*
/usr/lib/one/tm_commands/*
/var/lib/one/*
/etc/init.d/one
%dir /usr/lib/one
%dir /usr/lib/one/mads
%dir /usr/lib/one/remotes
%dir /usr/lib/one/ruby
%dir /usr/lib/one/tm_commands
%dir /var/lib/one
%dir %{_datadir}/one
%dir %{_datadir}/one/hooks


%files devel
%defattr(-,root,root)
%{_mandir}/man8/*
%{_datadir}/one/examples/*
%dir %{_datadir}/one/examples

%files sunstone
%defattr(-,root,root,-)
/usr/lib/one/sunstone/*
/etc/init.d/sunstone
%{_bindir}/sunstone-server
%dir /usr/lib/one/sunstone


%pre
# cloud administrator setup
if ! getent passwd oneadmin &> /dev/null ; then
  echo "Creating oneadmin user"
  /usr/sbin/groupadd cloud
  ONEPWD=$(/usr/bin/pwgen 40 1)
  /usr/sbin/useradd -m -c "OpenNebula Cloud Admin" -d /var/lib/one -g cloud -p $ONEPWD oneadmin
fi

%post
if [ ! -d /var/lib/one/.ssh ] ; then
  %{__mkdir} /var/lib/one/.ssh
fi
# Setup the ssh infrastructure for the cloud
if [ ! -f /var/lib/one/.ssh/id_rsa ]; then
    /usr/bin/ssh-keygen -q -t rsa -f /var/lib/one/.ssh/id_rsa -N ''
fi
/bin/cp /var/lib/one/.ssh/id_rsa.pub /var/lib/one/.ssh/authorized_keys
echo "Host *" >> /var/lib/one/.ssh/config
echo "    StrictHostKeyChecking no" >> /var/lib/one/.ssh/config
# set the ownership of the management scripts
/bin/chown -R oneadmin:cloud /var/lib/one
if [ ! -d /var/log/one ]; then
  %{__mkdir} /var/log/one
fi
if [ ! -d /var/lock/one ]; then
  %{__mkdir} /var/lock/one
fi
/bin/chown -R oneadmin:cloud /var/log/one
/bin/chown -R oneadmin:cloud /var/lock/one

