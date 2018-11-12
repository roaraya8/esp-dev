import shutil
import os
from setuptools import setup

import fastentrypoints

setup(
    name='esp-dev-cli',
    description='Wrapper around esp-dev CLIs and tools',
    version='0.0.1',
    packages=['esp_dev_cli'],
    include_package_data=True,
    install_requires=[
        'Click>=7.0',
        'esptool',
    ],
    entry_points="""
        [console_scripts]
        esp=esp_dev_cli.esp_dev_cli:cli
    """,
)
