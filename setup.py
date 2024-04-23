from setuptools import setup, find_packages, Extension

module1 = Extension('fast_diff_match_patch',
                    sources = ['interface.cpp'],
                    include_dirs = [],
                    libraries = [])

setup(
    name='fast_diff_match_patch',
    version='2.1.0',
    description=u'Packages the C++ implementation of google-diff-match-patch for Python for fast byte and string diffs.',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author=u'Joshua Tauberer',
    author_email=u'jt@occams.info',
    url='https://github.com/JoshData/fast_diff_match_patch',
    packages=find_packages(),
    license='Apache License 2.0',
    keywords="diff compare Google match patch diff_match_patch native fast",
    ext_modules=[module1],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    test_suite='tests',
)
