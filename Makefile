.PHONY: clean build install all

all: uninstall clean build install

clean:
	rm build -rf

build: clean
	umask 0022 
	python setup.py build 
	umask 0022

install:
	sudo python setup.py install

uninstall:
	sudo rm -rf /etc/chord-finder /usr/lib/python2.7/site-packages/chordfinder /usr/bin/chord-finder.py

upload:
	./setup.py sdist upload

