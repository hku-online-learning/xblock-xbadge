"""Setup for xbadge XBlock."""

import os
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='xbadge-xblock',
    version='1.0',
    description='Badge XBlock developed by HKU.',
    license='AGPL v3',
    packages=[
        'xbadge',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'xbadge = xbadge:XBadgeXBlock',
        ]
    },
    package_data=package_data("xbadge", ["static", "public"]),
)
