from distutils.core import setup

from blind import __version__


setup(
    name='blind',
    version=__version__,
    author='Kyle Meyer',
    author_email='meyerkya@gmail.com',
    description='Temporarily mask file or directory names',
    license='GPLv3',
    url='http://github.com/kyleam/blind.git',
    py_modules=['blind', 'four_letters'],
    scripts=['bin/blind'],
    long_description=open('README').read(),
    requires=['wxPython'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
)
