from setuptools import setup, find_packages, Extension

module1 = Extension('fast_diff_match_patch',
                    sources = ['interface.cpp'],
                    include_dirs = [],
                    libraries = [])

setup(
    name='fast_diff_match_patch',
    version='2.0.1',
    description=u'Exposes the C++ implementation of google-diff-match-patch to Python for fast diffs.',
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    test_suite='tests',
)
