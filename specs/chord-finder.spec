%define name chord-finder
%define version 1.0
%define unmangled_version 1.0
%define release 1

Summary: Simple guitar chord app
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Desktop/Applications
Prefix:		%{_prefix}
BuildArch:	noarch
Vendor:		robert pearce <robert.m.pearce@googlemail.com>
Url:		http://code.google.com/p/chord-finder/
Requires:	python
Requires:	wxPython
Requires:	sox
Source0:	%{name}-%{version}.tar.gz

%description
An application to display 6 string guitar chords

%prep
%setup -q

%install
mkdir -p ${RPM_BUILD_ROOT}/usr/bin/
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/chord-finder/
mkdir -p ${RPM_BUILD_ROOT}/usr/data/chord-finder/
cp chord-finder ${RPM_BUILD_ROOT}/usr/bin/
cp data/{welcomeChord.png,ChordData.csv,favicon.ico} ${RPM_BUILD_ROOT}/usr/data/chord-finder/
cp src/{__init__,ChordFinder,ChordData,Gui,DrawRootFinder,Palettes,DrawChord,Instruments}.py ${RPM_BUILD_ROOT}/usr/lib/chord-finder/

%clean
rm -rf $RPM_BUILD_ROOT

%post

%files
/usr/bin/chord-finder

/usr/data/chord-finder/ChordData.csv
/usr/data/chord-finder/favicon.ico
/usr/data/chord-finder/welcomeChord.png

/usr/lib/chord-finder/__init__.py
/usr/lib/chord-finder/ChordData.py
/usr/lib/chord-finder/ChordFinder.py
/usr/lib/chord-finder/Gui.py
/usr/lib/chord-finder/DrawRootFinder.py
/usr/lib/chord-finder/Palettes.py
/usr/lib/chord-finder/DrawChord.py
/usr/lib/chord-finder/Instruments.py
%defattr(-,root,root,-)

