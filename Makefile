# Scripnix Makefile for various and sundry tasks.

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

README.rst: README.md
	sed '/## Commands/,$$d' README.md | sed '/^Useful Python3.*YMMV\.$$/d' >README.tmp
	pandoc -f markdown -t rst -o README.rst README.tmp
	rm -f README.tmp

README.md: README-prefix.md scripnix/__init__.py
	./build-readme.py

clean:
	rm -fr dist/
	rm -fr build/

build: clean README.rst
	./build-readme.py
	@$(MAKE)
	./setup.py sdist >/dev/null
	./setup.py bdist_wheel >/dev/null

bump:
	./setup.py test
	./bump-version.py
	@$(MAKE) build
	ls dist/*.whl | xargs -I{} twine register {}
	ls dist/*.whl | xargs -I{} twine upload {}
	ls dist/*.tar.gz | xargs -I{} twine upload {}
	@echo "Run git tag -a... with the bumped version."
	@echo "Push to GitHub with git push --followtags"
	@echo "Update homebrew formula version number and SHA."
