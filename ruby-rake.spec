%define	rname	rake

Summary:	Simple ruby build program with capabilities similar to make
Name:		ruby-%{rname}
Version:	0.8.7
Release:	%mkrel 2
License:	MIT
Group:		Development/Ruby
URL:		http://rake.rubyforge.org/
Source0:	http://gems.rubyforge.org/gems/%{rname}-%{version}.gem
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildArch:	noarch
BuildRequires:	ruby-RubyGems

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
rm -rf %rname-%version
rm -rf tmp-%rname-%version
mkdir tmp-%rname-%version
gem install --ignore-dependencies %{SOURCE0} --no-rdoc --install-dir `pwd`/tmp-%rname-%version
mv tmp-%rname-%version/gems/%rname-%version .
mv tmp-%rname-%version/specifications/%rname-%version.gemspec %rname-%version/
rm -rf tmp-%rname-%version
%setup -T -D -n %rname-%version

%build
rdoc --ri --op ri --title "Rake -- Ruby Make" --main README --line-numbers lib doc/glossary.rdoc doc/proto_rake.rdoc doc/rational.rdoc doc/rakefile.rdoc doc/release_notes/rake-0.4.14.rdoc doc/release_notes/rake-0.5.3.rdoc doc/release_notes/rake-0.4.15.rdoc doc/release_notes/rake-0.6.0.rdoc doc/release_notes/rake-0.5.0.rdoc doc/release_notes/rake-0.5.4.rdoc doc/release_notes/rake-0.7.0.rdoc README CHANGES TODO
rdoc --op rdoc --title "Rake -- Ruby Make" --main README --line-numbers lib doc/glossary.rdoc doc/proto_rake.rdoc doc/rational.rdoc doc/rakefile.rdoc doc/release_notes/rake-0.4.14.rdoc doc/release_notes/rake-0.5.3.rdoc doc/release_notes/rake-0.4.15.rdoc doc/release_notes/rake-0.6.0.rdoc doc/release_notes/rake-0.5.0.rdoc doc/release_notes/rake-0.5.4.rdoc doc/release_notes/rake-0.7.0.rdoc README CHANGES TODO

%install
rm -rf %buildroot

DESTDIR=$RPM_BUILD_ROOT ruby install.rb --no-ri --tests

mkdir -p $RPM_BUILD_ROOT{%{ruby_ridir},%{ruby_gemdir}/specifications}
cp -a ri/{CompositePublisher,Rake,RakeFileUtils,SshDirPublisher,SshFilePublisher,SshFreshDirPublisher} $RPM_BUILD_ROOT%{ruby_ridir}
cp -a %rname-%version.gemspec $RPM_BUILD_ROOT%{ruby_gemdir}/specifications/

mkdir -p %buildroot%{_mandir}/man1
cp doc/*.1.gz %buildroot%{_mandir}/man1/

for f in `find %buildroot%{ruby_sitelibdir} -type f`
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
%attr(755,root,root) %{_bindir}/%{rname}
%{_mandir}/man1/*
%{ruby_sitelibdir}/*
%{ruby_ridir}/*
%{ruby_gemdir}/specifications/%rname-%version.gemspec
%doc CHANGES README TODO rdoc doc/example

