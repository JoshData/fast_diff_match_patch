from setuptools import setup, find_packages, Extension

module1 = Extension('fast_diff_match_patch',
                    sources = ['interface.cpp'],
                    include_dirs = [],
                    libraries = [])

setup(
    name='fast_diff_match_patch',
    version='2.0.0',
    description=u'fast_diff_match_patch: Python package wrapping the C++ implementation of google-diff-match-patch',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author=u'Joshua Tauberer',
    author_email=u'jt@occams.info',
    url='https://github.com/JoshData/diff_match_patch-python',
    packages=find_packages(),
    license='CC0 (copyright waived)',
    keywords="diff compare Google match patch diff_match_patch native fast",
    ext_modules=[module1],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
)
