from setuptools import setup, find_packages

setup(
    name = "tracknaliser",
    version = "0.1.0",
    packages = find_packages(exclude=['*.test']),
    install_requires = ['pytest','requests','matpltlib','numpy','numpydoc'],
    entry_points = {'console_scripts':['greentrack = tracknaliser-Working-Group-20.command:process']}
)