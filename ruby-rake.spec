%define rname   rake

Summary:    Simple ruby build program with capabilities similar to make
Name:       ruby-%{rname}
Version:    0.8.7
Release:    %mkrel 3
License:    MIT
Group:      Development/Ruby
URL:        http://rake.rubyforge.org/
Source0:    http://gems.rubyforge.org/gems/%{rname}-%{version}.gem
BuildRoot:  %{_tmppath}/%{name}-buildroot
BuildArch:  noarch
BuildRequires: ruby-RubyGems
Provides:   rubygem(%{rname}) = %{version}

%description
This package contains Rake, a simple ruby build program with capabilities
similar to make.

Rake has the following features:
 * Rakefiles (rake's version of Makefiles) are completely defined in
   standard Ruby syntax. No XML files to edit. No quirky Makefile syntax to
   worry about (is that a tab or a space?)
 * Users can specify tasks with prerequisites.
 * Rake supports rule patterns to sythesize implicit tasks.
 * Rake is lightweight. It can be distributed with other projects as a single
   file. Projects that depend upon rake do not require that rake be installed
   on target systems.

%prep

%build

%install
rm -rf %buildroot
gem install --local --install-dir %{buildroot}%{ruby_gemdir} \
            --force --rdoc %{SOURCE0}

# Move executable to bindir
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{ruby_gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{ruby_gemdir}/bin
chmod a+x %{buildroot}%{ruby_gemdir}/gems/%{rname}-%{version}/bin/rake

# Move manpage to mandir
mkdir -p %{buildroot}%{_mandir}/man1/
gzip -dc %{buildroot}%{ruby_gemdir}/gems/%{rname}-%{version}/doc/rake.1.gz > %{buildroot}%{_mandir}/man1/rake.1
rm %{buildroot}%{ruby_gemdir}/gems/%{rname}-%{version}/doc/rake.1.gz

# Fix shebang and permissions
for f in `find %buildroot%{ruby_gemdir}/gems/%{rname}-%{version} -type f`
do
  if head -n1 "$f" | grep '^#!' >/dev/null;
  then
    sed -i 's|/usr/local/bin|/usr/bin|' "$f"
    chmod 0755 "$f"
  else
    chmod 0644 "$f"
  fi
done

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%{_bindir}/rake
%{_mandir}/man1/%{rname}.1.*
%dir %{ruby_gemdir}/gems/%{rname}-%{version}/
%{ruby_gemdir}/gems/%{rname}-%{version}/bin/
%{ruby_gemdir}/gems/%{rname}-%{version}/lib/
%{ruby_gemdir}/gems/%{rname}-%{version}/test/
%{ruby_gemdir}/gems/%{rname}-%{version}/install.rb
%doc %{ruby_gemdir}/doc/%{rname}-%{version}
%doc %{ruby_gemdir}/gems/%{rname}-%{version}/Rakefile
%doc %{ruby_gemdir}/gems/%{rname}-%{version}/README
%doc %{ruby_gemdir}/gems/%{rname}-%{version}/MIT-LICENSE
%doc %{ruby_gemdir}/gems/%{rname}-%{version}/TODO
%doc %{ruby_gemdir}/gems/%{rname}-%{version}/CHANGES
%doc %{ruby_gemdir}/gems/%{rname}-%{version}/doc/
%{ruby_gemdir}/cache/%{rname}-%{version}.gem
%{ruby_gemdir}/specifications/%{rname}-%{version}.gemspec
