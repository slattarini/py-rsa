# -*- Makefile -*-
# Simple makefile for RSA personal project.
#
# This makefile is used mostly to run the testsuite of RSA.py, and to build
# the tarball for project distribution; in particular, note that there is
# no installation procedure for the RSA.py module.

.POSIX:
.SUFFIXES:

PACKAGE := py-rsa
VERSION := 0.5a
MAKEFILE := GNUmakefile

GZIP := gzip
GNUTAR := tar
XARGS := xargs
FIND := $(shell test -d .git && echo wcfind || echo find)
LATEXMK := latexmk

PDFLATEX_CMD = $(LATEXMK) </dev/null -pdf -nonstopmode

DIST_FILES := \
    README TODO $(MAKEFILE) \
    RSA.tex sty/*.sty \
    RSA-for-display.pdf RSA-for-print.pdf \
    RSA.py tests/*.py pytest.ini random.bytes

distdir = $(PACKAGE)-$(VERSION)

default: pdf-display
all: pdf-display pdf-print
.PHONY: default all

distdir:
	@set -u \
	  && rm -rf $(distdir) \
	  && mkdir $(distdir) \
	  && echo Creating temporary tarball... \
	  && $(GNUTAR) -cf dist.tmp $(DIST_FILES) \
	  && echo Populating dist directory... \
	  && (cd $(distdir) && $(GNUTAR) -xf ../dist.tmp) \
	  && rm -f dist.tmp
.PHONY: distdir

$(distdir).tar.gz: $(DIST_FILES) $(MAKEFILE)
	rm -f $@
	$(MAKE) distdir
	$(GNUTAR) czf $@-t $(distdir)
	rm -rf $(distdir)
	@echo && echo 'Archive details:' \
	  && ls -l $@-t | sed 's/^/  /' \
	  && $(GNUTAR) tzf $@-t | sort | sed 's/^/  /'
	@mv -f $@-t $@

dist: $(distdir).tar.gz
.PHONY: dist

# build the report in PDF format
RSA-for-display.pdf RSA-for-print.pdf: RSA.tex $(MAKEFILE)
	@rm -f $@
	@case $@ in \
	   *display*) build_dir=_texbuild_display uselinks=true ;; \
	     *print*) build_dir=_texbuild_print   uselinks=false;; \
	 esac; \
	 set -x -u -e \
	   && { test -d "$$build_dir" || mkdir "$$build_dir"; } \
	   && cd "$$build_dir" \
	   && echo "\uselinks$$uselinks" > RSA-ifuselinks.tex \
	   && TEXINPUTS=.:..:../sty:$${TEXINPUTS+":$$TEXINPUTS"} \
	        $(PDFLATEX_CMD) ../RSA.tex \
	   && cd .. \
	   && cp "$$build_dir"/RSA.pdf $@-t \
	   && chmod a-w $@-t && mv -f $@-t $@

pdf-display: RSA-for-display.pdf
pdf-print: RSA-for-print.pdf
.PHONY: pdf-display pdf-print

clean:
	$(FIND) . \( -name '*.tmp' -o -name '*.tmp[0-9]' \) -print | \
	   $(XARGS) rm -f
	$(FIND) . -name '*.tmpdir' -print | $(XARGS) rm -rf
	$(FIND) . -name '*.py[co]' -print | $(XARGS) rm -f
	rm -rf $(distdir) _texbuild_display _texbuild_print
	rm -f $(distdir).tar.gz
	rm -f RSA-for-display.pdf RSA-for-print.pdf
.PHONY: clean

test check:
	py.test $(PYTESTFLAGS)
.PHONY: test check

# vim: ft=make ts=4 sw=4 noet
