%define rname   rake

Summary:    Simple ruby build program with capabilities similar to make
Name:       ruby-%{rname}
Version:    0.8.7
Release:    %mkrel 4
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


%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.8.7-4mdv2011.0
+ Revision: 669460
- mass rebuild

* Thu Nov 04 2010 Rémy Clouard <shikamaru@mandriva.org> 0.8.7-3mdv2011.0
+ Revision: 593325
- Install rake as a gem to allow other gems requiring it
- move gem install to %%install
- move files to %%{ruby_gemdir} (needed for spork)

* Fri Sep 17 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.8.7-2mdv2011.0
+ Revision: 579221
- rebuild with automatic provides/requires

* Tue Feb 02 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.8.7-1mdv2010.1
+ Revision: 499443
- new release: 0.8.8
- perform some cosmetics

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.8.3-2mdv2010.0
+ Revision: 426965
- rebuild

* Sun Feb 01 2009 Funda Wang <fwang@mandriva.org> 0.8.3-1mdv2009.1
+ Revision: 336111
- New version 0.8.3

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.8.1-2mdv2009.0
+ Revision: 225338
- rebuild

* Mon Jan 14 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0.8.1-1mdv2008.1
+ Revision: 151230
- new version

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Apr 22 2007 Pascal Terjan <pterjan@mandriva.org> 0.7.3-1mdv2008.0
+ Revision: 16720
- 0.7.3

* Sat Apr 21 2007 Pascal Terjan <pterjan@mandriva.org> 0.7.1-2mdv2008.0
+ Revision: 16671
- ri is now in ri/ and not ri/ri/
- Use Development/Ruby group


* Fri Jul 28 2006 Olivier Blin <blino@mandriva.com> 0.7.1-1mdv2007.0
- 0.7.1

* Mon Feb 13 2006 Pascal Terjan <pterjan@mandriva.org> 0.7.0-2mdk
- use gem
- use system ruby macros

* Thu Feb 09 2006 Pascal Terjan <pterjan@mandriva.org> 0.7.0-1mdk
- 0.7.0

* Tue Sep 06 2005 Pascal Terjan <pterjan@mandriva.org> 0.6.0-1mdk
- 0.6.0
- mkrel

* Mon Jul 11 2005 Pascal Terjan <pterjan@mandriva.org> 0.5.4-1mdk
- first release

