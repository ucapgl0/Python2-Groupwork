from setuptools import setup, find_packages

setup(
    name = "tracknaliser",
    version = "0.1.0",
    author = 'group20',
    packages = find_packages(exclude=['*.test']),
    install_requires = ['pytest','requests','matplotlib','numpy','numpydoc','Sphinx'],
    entry_points = {'console_scripts':['greentrack = tracknaliser.command:process']}
)
