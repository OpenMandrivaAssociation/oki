%define	name	oki
%define	version	0.1.6
%define	release %mkrel 1
%define summary Oki is a small platform game with monochrome graphics
%define group	Games/Arcade

Name:		%{name} 
Summary:	%{summary}
Version:	%{version} 
Release:	%{release} 
Source0:	%{name}-%{version}.tar.bz2
Patch0:		%{name}-default-conf.patch.bz2
URL:		http://free.of.pl/s/szatkus/oki/
Group:		%{group}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPL
BuildRequires:	SDL_image-devel SDL_mixer-devel SDL-devel

%description
Oki is a small platform game with monochrome graphics.

%prep
%setup -q
%patch0 -p0
# We don't have a "clock" command but the configure script tries to use one
mv ./configure ./configure_orig
sed -e s,'clock','date',g ./configure_orig > ./configure
chmod +x ./configure

%build
%configure
%make

%install
rm -rf $RPM_BUILD_ROOT
install -m755 %{name} -D $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/%{name}
install -m755 %{name}_me $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/
cp -a gfx/ $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/
cp -a maps/ $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/
cp -a snd/ $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/
rm -f $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/gfx/Makefile
rm -f $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/snd/Makefile
mkdir $RPM_BUILD_ROOT%{_gamesbindir}/
echo "#!/bin/sh
cd %{_gamesdatadir}/%{name}
./oki \$*" > $RPM_BUILD_ROOT%{_gamesbindir}/%{name}
echo "#!/bin/sh
cd %{_gamesdatadir}/%{name}
./oki_me \$*" > $RPM_BUILD_ROOT%{_gamesbindir}/%{name}_me
chmod +x $RPM_BUILD_ROOT%{_gamesbindir}/*
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}  $RPM_BUILD_ROOT%{_datadir}/applications
ln -s %{_gamesdatadir}/%{name}/gfx/oki40.png $RPM_BUILD_ROOT%{_iconsdir}/oki.png

cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{name}
Icon=oki
Categories=Game;ArcadeGame;
Name=Oki
Comment=Oki
EOF

cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}_me.desktop
[Desktop Entry]
Type=Application
Exec=%{name}_me
Icon=oki
Categories=Game;ArcadeGame;
Name=Oki map editor
Comment=Oki map editor
EOF

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean 
rm -rf $RPM_BUILD_ROOT 

%files 
%defattr(-,root,root)
%doc TODO README CHANGELOG
%{_gamesdatadir}/%{name}
%{_gamesbindir}/*
%{_iconsdir}/*
%{_datadir}/applications/mandriva-*.desktop

