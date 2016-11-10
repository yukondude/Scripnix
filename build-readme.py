#!/usr/bin/env python
""" (Re)build the README.md file from README-prefix.md and the output of the describe-scripnix command.
"""

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

from click.testing import CliRunner
import datetime
import os
import scripnix
from scripnix.pybin.describe_scripnix import main


if __name__ == '__main__':
    here = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(here, "README-prefix.md"), "r") as f:
        readme = f.read()

    today = datetime.date.today().strftime("%B %-d, %Y")
    version = scripnix.__version__

    readme = readme.replace("@@TODAY@@", today)
    readme = readme.replace("@@VERSION@@", version)

    runner = CliRunner()
    result = runner.invoke(main)
    readme += result.output

    with open(os.path.join(here, "README.md"), "w") as f:
        f.write(readme)
