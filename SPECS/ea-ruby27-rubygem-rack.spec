# Defining the package namespace
%global ns_name ea
%global ns_dir /opt/cpanel
%global pkg ruby27
%global gem_name rack

%global ruby_version %(/opt/cpanel/ea-ruby27/root/usr/bin/ruby -e 'puts %RUBY_VERSION')

# Force Software Collections on
%global _scl_prefix %{ns_dir}
%global scl %{ns_name}-%{pkg}
# HACK: OBS Doesn't support macros in BuildRequires statements, so we have
#       to hard-code it here.
# https://en.opensuse.org/openSUSE:Specfile_guidelines#BuildRequires
%global scl_prefix %{scl}-
%{?scl:%scl_package rubygem-%{gem_name}}

# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
%define release_prefix 3

Name:           %{?scl_prefix}rubygem-%{gem_name}
Summary:        Common API for connecting web frameworks, web servers and layers of software
Version:        2.2.3
Release:        %{release_prefix}%{?dist}.cpanel
Group:          Development/Languages
# lib/rack/backports/uri/* are taken from Ruby which is (Ruby or BSD)
License:        MIT and (Ruby or BSD)
URL:            http://rubyforge.org/projects/%{gem_name}/
Source0:        %{gem_name}-%{version}.gem
Requires:       %{?scl_prefix}ruby(rubygems)
Requires:       %{?scl_prefix}ruby(release)
%{?scl:Requires:%scl_runtime}

BuildRequires:  %{?scl_prefix}ruby
BuildRequires:  %{?scl_prefix}rubygems-devel
BuildRequires:  scl-utils
BuildRequires:  scl-utils-build
%{?scl:BuildRequires: %{scl}-runtime}

BuildArch:      noarch
Provides:       %{?scl_prefix}rubygem(%{gem_name}) = %{version}
Provides:       bundled(okjson) = 20130206

%description
Rack provides a common API for connecting web frameworks,
web servers and layers of software in between

%prep
%setup -q -c -T
%{?scl:scl enable %{scl} - << \EOF} \
%gem_install -n %{SOURCE0} \
%{?scl:EOF}

%build

%install
rm -rf %{buildroot}

%global gemsbase opt/cpanel/ea-ruby27/root/usr/share/gems
%global gemsdir  %{gemsbase}/gems
%global gemsrack %{gemsdir}/rack-%{version}

mkdir -p %{buildroot}/%{gemsrack}
mkdir -p %{buildroot}/%{gemsbase}/specifications
mkdir -p %{buildroot}/%{gemsbase}/doc/rack-%{version}

cp -ar ./%{gemsbase}/doc/rack-%{version}/* %{buildroot}/%{gemsbase}/doc/rack-%{version}
cp -ar ./%{gemsdir}/rack-%{version}/* %{buildroot}/%{gemsrack}
cp -a  ./%{gemsbase}/specifications/rack-%{version}.gemspec %{buildroot}/%{gemsbase}/specifications/rack-%{version}.gemspec

mkdir -p %{buildroot}%{_bindir}
cp -pa %{buildroot}/%{gemsrack}/bin/* \
        %{buildroot}%{_bindir}/

# Fix anything executable that does not have a shebang
for file in `find %{buildroot}/%{gemsrack} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}/%{gemsrack} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

%clean
rm -rf %{buildroot}

%files
%dir /%{gemsrack}
%doc /%{gemsbase}/doc
%doc /%{gemsrack}/CHANGELOG.md
%doc /%{gemsrack}/Rakefile
%doc /%{gemsrack}/README.rdoc
%doc /%{gemsrack}/SPEC.rdoc
%doc /%{gemsrack}/example
%doc /%{gemsrack}/MIT-LICENSE
%doc /%{gemsrack}/contrib
%doc /%{gemsrack}/CONTRIBUTING.md
/%{gemsrack}
/%{gemsbase}/specifications
%{_bindir}/rackup

%changelog
* Thu Jul 29 2021 Travis Holloway <t.holloway@cpanel.net> - 2.2.3-3
- EA-10007: ea-ruby27 was updated from v2.7.3 to v2.7.4

* Tue Jun 29 2021 Julian Brown <julian.brown@cpanel.net> - 2.2.3-2
- ZC-9033: provide reliable way to get the ruby_version

* Mon Mar 01 2021 Cory McIntire <cory@cpanel.net> - 2.2.3-2
- EA-9609: Update global_version for ea-ruby27 v2.7.2

* Tue Sep 08 2020 Julian Brown <julian.browny@cpanel.net> - 2.2.3-1
- ZC-7510: initial rubygem rack for Ruby2.7

