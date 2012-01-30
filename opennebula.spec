%define	unitdir /lib/systemd/system/


Name:          opennebula
Version:       3.2.1
Release:       1
License:       Apache License version 2.0
Summary:       Elastic Utility Computing Architecture
URL:           http://www.opennebula.org
Group:         System/Configuration/Networking
Source0:       %{name}-%{version}.tar.gz
Source1:       sunstone.init
Source2:       onedsetup
Source3:       one.service
Source4:       one_scheduler.service
Source5:       sunstone.service
Source6:       ozones.init
Source7:       ozones.service
Source8:       onetmpdirs
Patch0:        openneb_64bitlib.patch
Patch1:        nebula_linker.patch
BuildRequires: gcc-c++
BuildRequires: libcurl-devel
BuildRequires: libxml2-devel    
BuildRequires: libxmlrpc-c-devel    >= 1.06
BuildRequires: libopenssl-devel     >= 0.9
BuildRequires: openssh
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
Requires:      sqlite3-tools        >= 3.5.2
Requires:      rubygem-nokogiri
Requires:      rubygem-sqlite3
Requires:      xmlrpc-c             >= 1.06

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
Group:    Development/Ruby
Requires: %{name} = %{version}

%description devel
The %{name} devel package contains man pages and examples.

%package zones
Summary: Manage multy tenancy
Group:   System/Configuration/Networking
Requires: %{name} = %{version}
Requires: apache-base
Requires: rubygem-datamapper
Requires: rubygem-dm-sqlite-adapter
Requires: rubygem-json
Requires: rubygem-openssl-nonblock
Requires: rubygem-rack
Requires: rubygem-sequel
Requires: rubygem-sinatra
Requires: rubygem-thin

%description zones
The OpenNebula Zones (oZones) component allows for the centralized management
of multiple instances of OpenNebula (zones), managing in turn potentially
different administrative domains.

%package sunstone
Summary: Browser based UI to administer an OpenNebulaCloud
Group:   System/Configuration/Networking
Requires: %{name} = %{version}
Requires: rubygem-json
Requires: rubygem-sequel
Requires: rubygem-sinatra
Requires: rubygem-thin

%description sunstone
sunstone if the web base UI to manage a deployed OpenNebula Cloud

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
scons sqlite_db=/usr xmlrpc=/usr

%install
export DESTDIR=%{buildroot}

./install.sh

install -p -D -m 755 %{SOURCE2} %{buildroot}%{_sbindir}/onedsetup
install -p -D -m 755 %{SOURCE3} %{buildroot}%{unitdir}/one.service
install -p -D -m 755 %{SOURCE4} %{buildroot}%{unitdir}/one_scheduler.service
install -p -D -m 755 %{SOURCE5} %{buildroot}%{unitdir}/sunstone.service
install -p -D -m 755 %{SOURCE5} %{buildroot}%{unitdir}/ozones.service
install -p -D -m 755 %{SOURCE8} %{buildroot}%{_sysconfdir}/tmpdirs.d/30_One

%files
%doc LICENSE NOTICE
%config(noreplace) %{_sysconfdir}/one/acctd.conf
%config(noreplace) %{_sysconfdir}/one/auth
%config(noreplace) %{_sysconfdir}/one/cli
%config(noreplace) %{_sysconfdir}/one/defaultrc
%config(noreplace) %{_sysconfdir}/one/ec2query_templates
%config(noreplace) %{_sysconfdir}/one/econe.conf
%config(noreplace) %{_sysconfdir}/one/group.default
%config(noreplace) %{_sysconfdir}/one/hm
%config(noreplace) %{_sysconfdir}/one/im_ec2
%config(noreplace) %{_sysconfdir}/one/occi*
%config(noreplace) %{_sysconfdir}/one/oned.conf
%config(noreplace) %{_sysconfdir}/one/tm_*
%config(noreplace) %{_sysconfdir}/one/vmm_*
%config(noreplace) %{_sysconfdir}/tmpdirs.d/30_One
%dir	%{_sysconfdir}/one/image/
%config(noreplace) %{_sysconfdir}/one/image/fs.conf
%config(noreplace) %{_sysconfdir}/one/sched.conf
%config(noreplace) %{_sysconfdir}/one/vmwarerc

%{_bindir}/econe*
%{_bindir}/oc*
%{_bindir}/on*
%{_bindir}/mm_sched
%{_bindir}/tty_expect
/usr/lib/one/mads/*
/usr/lib/one/sh/scripts_common.sh
/usr/lib/one/ruby/*
/usr/lib/one/tm_commands/*
/var/lib/one/*
%{_sbindir}/onedsetup
%{unitdir}/one.service
%{unitdir}/one_scheduler.service
%dir %{_sysconfdir}/one
%dir /usr/lib/one
%dir /usr/lib/one/mads
%dir /usr/lib/one/ruby
%dir /usr/lib/one/sh
%dir /usr/lib/one/tm_commands
%dir /var/lib/one

%files devel
%doc README.md
%{_mandir}/man1/*
%{_datadir}/one/install_*
%{_datadir}/one/examples/*
%dir %{_datadir}/one
%dir %{_datadir}/one/examples

%files zones
%config(noreplace) %{_sysconfdir}/one/ozones-server.conf
/usr/lib/one/ozones/*
%{unitdir}/ozones.service
%{_bindir}/ozones-server
%dir /usr/lib/one/ozones

%files sunstone
%config(noreplace) %{_sysconfdir}/one/sunstone*
/usr/lib/one/sunstone/*
%{unitdir}/sunstone.service
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
