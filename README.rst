Scripnix
========

|status| |buildstatus| |codecov| |pypiversion| |pyversions| |licence|

Replaces the old `Scripnix0 <https://github.com/yukondude/Scripnix0>`__
project which had grown crufty and was not macOS-friendly.

Motivation
----------

Scripnix was born during my Linux server admin days when I wanted all of
my aliases and scriplets to follow me from machine to machine. Packaging
everything together made installing and keeping up-to-date that much
easier. Writing it was also a bash scripting learning exercise, although
I soon grew to loathe space-containing-filenames and all of the quoting
that implied.

As I moved more to MacOS, the BSD version of most commands clashed with
the GNU/Linux versions that Scripnix assumed. Still wanting those handy
aliases and scriplets on MacOS, I resurrected Scripnix, but with many
more of the commands written in Python, and with Homebrew-supplied GNU
versions of my favourite utilities. The Python rewrite sidestepped much
of the silly bash quoting and syntax, and made testing practical.

Licence
-------

Licensed under the `GNU General Public License, version
3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`__. Refer to the
attached LICENSE file or see http://www.gnu.org/licenses/ for details.

Change Log
----------

The current version is 0.1.12. Scripnix is
`semver <http://semver.org/>`__-ish in its versioning scheme.

Scripnix is currently an alpha release, so expect many many breaking
changes. Once ready for prime time, the major version number will jump
to 2 to reflect that this is actually the second incarnation of
Scripnix.

Installation
------------

Following installation using one of the methods below, you may also want
to run the ``install-scripnix`` command as the root user to setup the
system-wide configuration. Any other users that also wish to use
Scripnix should also run that command.

The ``install-scripnix`` command will also suggest changes to your
``~/.bashrc`` or ``~/.profile`` files to persist Scripnix in your
environment. It will also suggest changes to the ``/etc/sudoers`` file
(vi ``visudo``) so that the Scripnix commands can be run via ``sudo``
when necessary.

Homebrew (macOS)
~~~~~~~~~~~~~~~~

On macOS, Homebrew will take care of installing any dependencies,
including Python 3.

::

    brew tap yukondude/tap
    brew install scripnix
    install-scripnix

PyPI (POSIX)
~~~~~~~~~~~~

On \*NIX, you will first need to install Python 3.3 (or higher) using
your preferred method.

::

    pip3 install scripnix
    install-scripnix

Development Setup
-----------------

1. Install Scripnix, as above, so that all of its dependencies are
   available.
2. Create a Python 3 virtualenv for Scripnix:
   ``mkvirtualenv --python=$(which python3) Scripnix``
3. Clone the Scripnix repo:
   ``git clone https://github.com/yukondude/Scripnix.git``
4. Install dependencies:
   ``pip install -r requirements.txt -r requirements-dev.txt -r requirements-test.txt``
5. Install the project in development mode: ``./setup.py develop``
6. Run the unit tests to make sure everything is copacetic:
   ``./setup.py test``
7. Pour a snifter of Martell XO and light up a Bolivar Belicoso.

.. |status| image:: https://img.shields.io/pypi/status/Scripnix.svg
   :target: https://pypi.python.org/pypi/Scripnix/
.. |buildstatus| image:: https://travis-ci.org/yukondude/Scripnix.svg?branch=master
   :target: https://travis-ci.org/yukondude/Scripnix
.. |codecov| image:: https://codecov.io/gh/yukondude/Scripnix/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/yukondude/Scripnix
.. |pypiversion| image:: https://img.shields.io/pypi/v/Scripnix.svg
   :target: https://pypi.python.org/pypi/Scripnix/
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/Scripnix.svg
   :target: https://pypi.python.org/pypi/Scripnix/
.. |licence| image:: https://img.shields.io/pypi/l/Scripnix.svg
   :target: https://www.gnu.org/licenses/gpl-3.0.en.html
