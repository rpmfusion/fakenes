%define beta beta3

Name:           fakenes
Version:        0.5.9
Release:        0.2.%{beta}%{?dist}
Summary:        Nintendo Entertainment System emulator
Group:          Amusements/Games
License:        Artistic
URL:            http://fakenes.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-%{beta}.tar.gz
Source1:        %{name}.desktop
Patch0:         fakenes-0.5.8-menu-exit.patch
Patch1:         fakenes-0.5.8-driver-switch.patch
Patch2:         fakenes-0.5.9-beta3-gcc43.patch
Patch3:         fakenes-0.5.9-beta3-openal-build.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  allegro-devel alleggl-devel zlib-devel openal-devel
BuildRequires:  libGLU-devel freealut-devel desktop-file-utils
Requires:       hicolor-icon-theme

%description
FakeNES is an Open Source NES emulator.  It uses the excellent Allegro
multimedia library for input, graphics, and sound effects/music across
various platforms.  It is written in 100% C, and was originally designed to
run on DOS and Microsoft Windows, but now features a POSIX build system as
well.  There are also official builds available for Mac OS X.


%prep
%setup -q -n %{name}-%{version}-%{beta}
%patch0 -p1 -z .menu
%patch1 -p1 -z .driver
%patch2 -p1 -z .gcc43
%patch3 -p1 -z .openal-build
sed -i 's/\r//' docs/faq.html


%build
export CFLAGS="$RPM_OPT_FLAGS -ffast-math"
make cbuild
./cbuild --verbose


%install
rm -rf $RPM_BUILD_ROOT
install -D -m 755 %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}
# below is the desktop file and icon stuff.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor dribble           \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
install -p -m 644 support/icon-32x32.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/%{name}.png


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%postun
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :


%files
%defattr(-, root, root)
%doc docs/CHANGES docs/LICENSE docs/README docs/faq.html
%{_bindir}/%{name}
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png


%changelog
* Mon Oct 03 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.5.9-0.2.beta3
- Rebuilt for liballeg

* Sun Oct 25 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.5.9-0.1.beta3
- New upstream release 0.5.9-beta3

* Sat Oct 24 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.5.8-9
- rebuild for new openal

* Sat Oct 10 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.5.8-8
- rebuilt

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.5.8-7
- rebuild for new F11 features

* Thu Jul 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.5.8-6
- Rebuild for buildsys cflags issue

* Thu Jul 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.5.8-5
- Release bump for rpmfusion

* Sat Mar 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.5.8-4%{?dist}
- Fixup .desktop file categories for games-menus usage

* Sat Aug 12 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.5.8-3%{?dist}
- Fix crash when using openAL sound and openAL couldn't open the audiodevice

* Fri Aug 11 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.5.8-2%{?dist}
- Fix emulator hanging when pressing ESC in the main menu without a rom loaded
- Fix emulator crashing when switching between normal and opengl video modes
- Use %%{_bindir} instead of /usr/bin in %%install

* Thu Aug  3 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.5.8-1%{?dist}
- Initial Fedora Extras package
