from distutils.core import setup, Extension

module1 = Extension('diff_match_patch',
                    sources = ['interface.cpp'],
                    include_dirs = [],
                    libraries = [])

setup (name = 'diff_match_patch',
       version = '1.0',
       description = 'This is a Python extension module that wraps Google\'s diff_match_patch C++ port, rewritten by leutloff at https://github.com/leutloff/diff-match-patch-cpp-stl.',
       author = 'Joshua Tauberer',
       ext_modules = [module1])


