from distutils.core import setup, Extension

module1 = Extension('diff_match_patch',
                    sources = ['diff_match_patch.cpp', 'interface.cpp'],
                    include_dirs = ['/usr/include/qt4', '/usr/include/qt4/QtCore'],
                    libraries = ['QtCore'])

setup (name = 'diff_match_patch',
       version = '1.0',
       description = 'This is a Python extension module that wraps Google\'s diff_match_patch C++ port.',
       author = 'Joshua Tauberer',
       ext_modules = [module1])


