Scripnix
========

Useful Python3 and bash shell scripts for macOS/BSD and \*NIX. Useful to
me, at any rate. YMMV.

|status| |buildstatus| |codecov| |pypiversion| |pyversions| |licence|

Replaces the old `Scripnix0 <https://github.com/yukondude/Scripnix0>`__
project which had grown crufty and was not macOS-friendly.

Licence
-------

Licensed under the `GNU General Public License, version
3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`__. Refer to the
attached LICENSE file or see http://www.gnu.org/licenses/ for details.

Change Log
----------

The current version is 0.1.9. Scripnix is
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
2. Create a Python 3 virtualenv for Scripnix.
3. Clone the Scripnix repo.
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
