# Scripnix Makefile for various and sundry tasks.

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

README.rst : README.md
	pandoc -f markdown -t rst -o README.rst README-prefix-a.md

README.md : README-prefix-a.md README-prefix-b.md scripnix/__init__.py
	./build-readme.py
