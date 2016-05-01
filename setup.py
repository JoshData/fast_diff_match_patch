from setuptools import setup, find_packages, Extension

# Note to self: To upload a new version to PyPI, run:
# python setup.py sdist upload

module1 = Extension('diff_match_patch',
                    sources = ['interface.cpp'],
                    include_dirs = [],
                    libraries = [])

setup (
	name='diff_match_patch_python',
	version='1.0.2',
    packages = find_packages(),
	author=u'Joshua Tauberer',
	author_email=u'jt@occams.info',
	url='https://github.com/JoshData/diff_match_patch-python',
    license='CC0 (copyright waived)',
	description=u'A Python extension module that wraps Google\'s diff_match_patch C++ implementation for very fast string comparisons. Version 1.0.2 fixes a build issue on Macs.',
    long_description=open("README.rst").read(),
    keywords = "diff compare Google match patch diff_match_patch extension native C fast",
	ext_modules = [module1],
	)
