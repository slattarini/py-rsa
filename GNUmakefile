# -*- Makefile -*-
# Simple makefile for RSA personal project.
#
# This makefile is used mostly to run the testsuite of RSA.py, and to build
# the tarball for project distribution; in particular, note that there is
# no installation procedure for the RSA.py module.

.POSIX:
.SUFFIXES:

DISTNAME := RSA
MAKEFILE := GNUmakefile

GZIP := gzip
GNUTAR := tar
XARGS := xargs
FIND := $(shell test -d .git && echo wcfind || echo find)
PYTHON := python

DIST_FILES := README $(MAKEFILE) $(DISTNAME).py tests/*.py

default: all
all: # nothing yet
.PHONY: default all

# make gzipped tarball for distribution
$(DISTNAME).tar.gz: $(DIST_FILES) $(MAKEFILE)
	@set -u \
	  && rm -rf $@ _dist \
	  && mkdir _dist \
	  && echo Creating temporary tarball... \
	  && $(GNUTAR) -cf _dist/tmp.tar $(DIST_FILES) \
	  && echo Populating temporary dist directory... \
	  && cd _dist \
	  && mkdir $(DISTNAME) \
	  && cd $(DISTNAME) \
	  && $(GNUTAR) -xf ../tmp.tar \
	  && cd .. \
	  && rm -f tmp.tar \
	  && echo Creating real tarball... \
	  && $(GNUTAR) -cf $(DISTNAME).tar ./$(DISTNAME) \
	  && $(GZIP) $(DISTNAME).tar \
	  && cd .. \
	  && mv -f _dist/$@ $@ \
	  && rm -rf _dist \
	  && echo Done. \
	  && echo \
	  && echo 'Archive details:' \
	  && ls -l $@ | sed 's/^/  /' \
	  && tar tzf $@ | sort | sed 's/^/  /'

dist: $(DISTNAME).tar.gz
.PHONY: dist

clean:
	$(FIND) . \( -name '*.tmp' -o -name '*.tmp[0-9]' \) -print | \
	   $(XARGS) rm -f
	$(FIND) . -name '*.tmpdir' -print | $(XARGS) rm -rf
	$(FIND) . -name '*.py[co]' -print | $(XARGS) rm -f
	rm -rf _dist
	rm -f $(DISTNAME).tar.gz
.PHONY: clean

test check:
	py.test $(PYTESTFLAGS)
.PHONY: test check

# vim: ft=make ts=4 sw=4 noet
