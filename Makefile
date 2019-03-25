none:
	echo "Nothing to make. Just run any of the start_<something>.py programs."

autopep8:
	autopep8 --ignore=E501,E401,E402,W291,W293,W391,E265,E266,E226 --aggressive --in-place -r src/

clean: 
	find . -name "*.pyc" -print0 | xargs -0 rm -f
	find . -name "__pycache__" -print0 | xargs -0 rm -rf
	find . -name "*~" -print0 | xargs -0 rm -f	

dist: GENERATE_VERSION
	rm -f "python-optimade-reference-implementations-$$(cat VERSION).tgz"

	( \
		THISDIR=$$(basename "$$PWD"); \
		cd ..; \
		tar -zcf "$$THISDIR/python-optimade-reference-implementations-$$(cat $$THISDIR/VERSION).tgz" \
                         "$$THISDIR/src" "$$THISDIR/README.md" "$$THISDIR/VERSION" "$$THISDIR/LICENSE.txt" \
		         --exclude=".*" --transform "flags=r;s|$$THISDIR|python-optimade-reference-implementations-$$(cat $$THISDIR/VERSION)|"\
	)

release:
	( \
		echo "Present release: $$(git describe --always)"; \
		echo "Enter new tag:"; \
		read tag; \
		git tag -s "$$tag" -m "Release $$tag"; \
		git git push -u origin "$$tag"
	)

tests: unittests2 unittests3

unittests:
	(cd tests; TEST_EXPECT_PYVER=ignore python all.py)

unittests2: link_python2
	echo "Running unittests with Python 2"
        # Avoid mkdir -p in case this is run not in the right directory. 
	(cd tests; TEST_EXPECT_PYVER=2 PATH="$$(pwd -P)/python_versions/ver2:$$PATH" python all.py)

unittests3: link_python3
	echo "Running unittests with Python 3"
	(cd tests; TEST_EXPECT_PYVER=3 PATH="$$(pwd -P)/python_versions/ver3:$$PATH" python all.py)	

pytest:
	(cd tests; TEST_EXPECT_PYVER=ignore py.test)

pytest2: link_python2
	echo "Running pytest with Python 2"
	(cd tests; TEST_EXPECT_PYVER=2 PATH="$$(pwd -P)/python_versions/ver2:$$PATH" py.test)

pytest3: link_python3
	echo "Running pytest with Python 3"
	(cd tests; TEST_EXPECT_PYVER=3 PATH="$$(pwd -P)/python_versions/ver3:$$PATH" py.test-3)	

#tox:
#	tox

link_python2:
	if [ ! -e tests/python_versions ]; then mkdir tests/python_versions; fi
	if [ ! -e tests/python_versions/ver2 ]; then mkdir tests/python_versions/ver2; fi
	if [ ! -e tests/python_versions/ver2/python ]; then ln -sf /usr/bin/python2 tests/python_versions/ver2/python; fi

link_python3:
	if [ ! -e tests/python_versions ]; then mkdir tests/python_versions; fi
	if [ ! -e tests/python_versions/ver3 ]; then mkdir tests/python_versions/ver3; fi
	if [ ! -e tests/python_versions/ver3/python ]; then ln -sf /usr/bin/python3 tests/python_versions/ver3/python; fi

# Make git describe version PEP 440 compliant
GENERATE_VERSION:
	git describe --always --dirty | sed 's/^v\(.*\)/\1/' | sed 's/-/.dev/' | sed 's/-/+/' | sed 's/-dirty/.d/' > VERSION

.PHONY: tox tests unittests unittests2 unittests3 pytest clean autopep8 dist GENERATE_VERSION
