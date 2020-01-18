PKGNAME=pykickstart
SPECFILE=$(PKGNAME).spec
VERSION=$(shell awk '/Version:/ { print $$2 }' $(SPECFILE))
RELEASE=$(shell awk '/Release:/ { print $$2 }' $(SPECFILE) | sed -e 's|%.*$$||g')
RC_RELEASE ?= $(shell date -u +0.1.%Y%m%d%H%M%S)
TAG=r$(VERSION)-$(RELEASE)

ZANATA_PULL_ARGS = --transdir ./po/
ZANATA_PUSH_ARGS = --srcdir ./po/ --push-type source --force

MANDIR=/usr/share/man
PREFIX=/usr

TESTSUITE:=tests/baseclass.py

MOCKCHROOT ?= fedora-21-x86_64

all:
	$(MAKE) -C po

po-pull:
	rpm -qa | grep zanata 2>/dev/null | grep -q client 2>/dev/null &>/dev/null || ( echo "need to run: yum install /usr/bin/zanata"; exit 1 )
	zanata pull $(ZANATA_PULL_ARGS)

po-empty:
	for lingua in $$(gawk 'match($$0, /locale>(.*)<\/locale/, ary) {print ary[1]}' ./zanata.xml) ; do \
		[ -f ./po/$$lingua.po ] || \
		msginit -i ./po/$(PKGNAME).pot -o ./po/$$lingua.po --no-translator || \
		exit 1 ; \
	done

docs:
	curl -A "programmers-guide" -o docs/programmers-guide "https://fedoraproject.org/w/index.php?title=PykickstartIntro&action=raw"

check:
	@echo "*** Running pylint to verify source ***"
	PYTHONPATH=. pylint tools/* pykickstart/*.py pykickstart/*/*.py --msg-template='{msg_id}:{line:3d},{column}: {obj}: {msg}' --rcfile=/dev/null -r n --disable=C,R --dummy-variables-rgx=_ --disable=deprecated-lambda,bad-builtin,star-args,protected-access,arguments-differ,fixme,global-statement,broad-except

test:
	@echo "*** Running unittests ***"
	PYTHONPATH=. python $(TESTSUITE) -v

coverage:
	@which coverage || (echo "*** Please install python-coverage ***"; exit 2)
	@echo "*** Running unittests with coverage ***"
	PYTHONPATH=. coverage run $(TESTSUITE) -v
	PYTHONPATH=. coverage report --show-missing --include='pykickstart/*'

clean:
	-rm *.tar.gz pykickstart/*.pyc pykickstart/*/*.pyc tests/*.pyc tests/*/*.pyc docs/programmers-guide
	$(MAKE) -C po clean
	python setup.py -q clean --all

install:
	python setup.py install --root=$(DESTDIR)
	$(MAKE) -C po install

tag:
	git tag -a -m "Tag as $(TAG)" -f $(TAG)
	@echo "Tagged as $(TAG)"

archive: tag docs
	git archive --format=tar --prefix=$(PKGNAME)-$(VERSION)/ $(TAG) > $(PKGNAME)-$(VERSION).tar
	mkdir -p $(PKGNAME)-$(VERSION)
	cp -r po $(PKGNAME)-$(VERSION)/po/
	mkdir -p $(PKGNAME)-$(VERSION)/docs/
	cp docs/kickstart-docs.rst $(PKGNAME)-$(VERSION)/docs/
	cp docs/programmers-guide $(PKGNAME)-$(VERSION)/docs/
	tar -rf $(PKGNAME)-$(VERSION).tar $(PKGNAME)-$(VERSION)
	gzip -9 $(PKGNAME)-$(VERSION).tar
	rm -rf $(PKGNAME)-$(VERSION)
	git checkout -- po/$(PKGNAME).pot
	@echo "The archive is in $(PKGNAME)-$(VERSION).tar.gz"

local: docs po-pull
	@rm -rf $(PKGNAME)-$(VERSION).tar.gz
	@rm -rf /tmp/$(PKGNAME)-$(VERSION) /tmp/$(PKGNAME)
	@dir=$$PWD; cp -a $$dir /tmp/$(PKGNAME)-$(VERSION)
	@cd /tmp/$(PKGNAME)-$(VERSION) ; python setup.py -q sdist
	@cp /tmp/$(PKGNAME)-$(VERSION)/dist/$(PKGNAME)-$(VERSION).tar.gz .
	@rm -rf /tmp/$(PKGNAME)-$(VERSION)
	@echo "The archive is in $(PKGNAME)-$(VERSION).tar.gz"

rpmlog:
	@git log --pretty="format:- %s (%ae)" $(TAG).. |sed -e 's/@.*)/)/'
	@echo

bumpver: po-pull
	@NEWSUBVER=$$((`echo $(VERSION) |cut -d . -f 4` + 1)) ; \
	NEWVERSION=`echo $(VERSION).$$NEWSUBVER |cut -d . -f 1,2,3,5` ; \
	DATELINE="* `date "+%a %b %d %Y"` `git config user.name` <`git config user.email`> - $$NEWVERSION-1"  ; \
	cl=`grep -n %changelog $(SPECFILE) |cut -d : -f 1` ; \
	tail --lines=+$$(($$cl + 1)) $(SPECFILE) > speclog ; \
	(head -n $$cl $(SPECFILE) ; echo "$$DATELINE" ; make --quiet rpmlog 2>/dev/null ; echo ""; cat speclog) > $(SPECFILE).new ; \
	mv $(SPECFILE).new $(SPECFILE) ; rm -f speclog ; \
	sed -i "s/Version: $(VERSION)/Version: $$NEWVERSION/" $(SPECFILE) ; \
	sed -i "s/version='$(VERSION)'/version='$$NEWVERSION'/" setup.py ; \
	make -C po $(PKGNAME).pot ; \
	zanata push $(ZANATA_PUSH_ARGS)

scratch-bumpver: po-empty
	@NEWSUBVER=$$((`echo $(VERSION) |cut -d . -f 4` + 1)) ; \
	NEWVERSION=`echo $(VERSION).$$NEWSUBVER |cut -d . -f 1,2,3,5` ; \
	DATELINE="* `date "+%a %b %d %Y"` `git config user.name` <`git config user.email`> - $$NEWVERSION-$(RC_RELEASE)"  ; \
	cl=`grep -n %changelog $(SPECFILE) |cut -d : -f 1` ; \
	tail --lines=+$$(($$cl + 1)) $(SPECFILE) > speclog ; \
	(head -n $$cl $(SPECFILE) ; echo "$$DATELINE" ; make --quiet rpmlog 2>/dev/null ; echo ""; cat speclog) > $(SPECFILE).new ; \
	mv $(SPECFILE).new $(SPECFILE) ; rm -f speclog ; \
	sed -i "s/Version: $(VERSION)/Version: $$NEWVERSION/" $(SPECFILE) ; \
	sed -i "s/Release: $(RELEASE)/Release: $(RC_RELEASE)/" $(SPECFILE) ; \
	sed -i "s/version='$(VERSION)'/version='$$NEWVERSION'/" setup.py ; \
	make -C po $(PKGNAME).pot

scratch: docs po-empty
	@rm -rf $(PKGNAME)-$(VERSION).tar.gz
	@rm -rf /tmp/$(PKGNAME)-$(VERSION) /tmp/$(PKGNAME)
	@dir=$$PWD; cp -a $$dir /tmp/$(PKGNAME)-$(VERSION)
	@cd /tmp/$(PKGNAME)-$(VERSION) ; python setup.py -q sdist
	@cp /tmp/$(PKGNAME)-$(VERSION)/dist/$(PKGNAME)-$(VERSION).tar.gz .
	@rm -rf /tmp/$(PKGNAME)-$(VERSION)
	@echo "The archive is in $(PKGNAME)-$(VERSION).tar.gz"

rc-release: scratch-bumpver scratch
	mock -r $(MOCKCHROOT) --scrub all || exit 1
	mock -r $(MOCKCHROOT) --buildsrpm  --spec ./$(SPECFILE) --sources . --resultdir $(PWD) || exit 1
	mock -r $(MOCKCHROOT) --rebuild *src.rpm --resultdir $(PWD)  || exit 1

.PHONY: check clean install tag archive local docs
