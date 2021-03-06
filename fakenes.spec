%define _legacy_common_support 1
%define beta beta3

Name:           fakenes
Version:        0.5.9
Release:        0.15.%{beta}%{?dist}
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
Patch4:         fakenes-0.5.9-beta3-allegro44-build.patch
Patch5:         fakenes-0.5.9-beta3-libm-build.patch
Patch6:         fakenes-0.5.9-beta3-gcc7.patch
BuildRequires:  allegro-devel alleggl-devel zlib-devel openal-devel
BuildRequires:  libGLU-devel freealut-devel desktop-file-utils
BuildRequires:  libicns-utils gcc-c++
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
%patch4 -p1 -z .allegro44-build
%patch5 -p1 -z .libm
%patch6 -p1 -z .gcc7
sed -i 's/\r//' docs/faq.html


%build
export CFLAGS="$RPM_OPT_FLAGS -ffast-math"
make cbuild
./cbuild --verbose
icns2png -x build/mac/FakeNES.icns
touch -r build/mac/FakeNES.icns FakeNES_128x128x32.png


%install
install -D -m 755 %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}
# below is the desktop file and icon stuff.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor dribble           \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps
install -p -m 644 FakeNES_128x128x32.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps/%{name}.png


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc docs/CHANGES docs/LICENSE docs/README docs/faq.html
%{_bindir}/%{name}
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png


%changelog
* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.5.9-0.15.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.5.9-0.14.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.5.9-0.13.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.5.9-0.12.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.5.9-0.11.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 28 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.5.9-0.10.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.5.9-0.9.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 19 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.5.9-0.8.beta3
- Fix build with gcc-7.x

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.5.9-0.7.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.5.9-0.6.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.5.9-0.5.beta3
- Mass rebuilt for Fedora 19 Features

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.5.9-0.4.beta3
- Rebuilt for c++ ABI breakage

* Sat Dec 10 2011 Hans de Goede <j.w.r.degoede@hhs.nl> - 0.5.9-0.3.beta3
- Fix building with allegro-4.4.x (rf#1969)
- Fix the broken icon

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
