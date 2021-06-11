# Copyright Contributors to the Pyro project.
# SPDX-License-Identifier: Apache-2.0

import glob
import os
import re

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get new version.
with open(os.path.join(root, "pyro", "__init__.py")) as f:
    for line in f:
        if line.startswith("version_prefix ="):
            new_version = line.strip().split()[-1]

# Collect potential files.
filenames = []
for path in ["examples", "tutorial/source"]:
    for ext in ["*.py", "*.ipynb"]:
        filenames.extend(glob.glob(os.path.join(root, path, "**", ext),
                                   recursive=True))
filenames.sort()

# Update version string.
pattern = re.compile("assert pyro.__version__.startswith\\('[^']*'\\)")
text = f"assert pyro.__version__.startswith({new_version})"
for filename in filenames:
    with open(filename) as f:
        old_text = f.read()
    new_text = pattern.sub(text, old_text)
    if new_text != old_text:
        print("updating {}".format(filename))
    with open(filename, "w") as f:
        f.write(new_text)
