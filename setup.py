from __future__ import print_function, unicode_literals
import textwrap
from setuptools import setup
import codecs
import os

import Application

__project__ = 'Application'
__description__ = 'provide basic logging, configuration management, i18n and argument parsing for any application'
__author__ = Application.__author__
__email__ = 'piaballerstadt@gmail.com'
__url__ = 'https://github.com/' + __author__.lower().replace(' ', '') + '/' + __project__
__platforms__ = 'Windows, Linux, macOS, OS X'

print('''

Running Setup.py for {name} module.
Description: {desc}

Author:      {author}
Project:     {url}

'''.format(
    desc=textwrap.wrap(__description__, 72).replace('\n', '\n' + (' ' * 13)),
    name=__project__, author=__author__, url=__url__)
)


here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with codecs.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


def requirements():
    """ return third party packages required by this package """
    print('Collect requirements ...')
    required = []
    try:
        with codecs.open('requirements.txt', encoding='utf8') as requirements_data:
            for line in requirements_data:
                print('\tAdding requirement for {r}'.format(r=line))
                required.append(line)
    except OSError:
        pass
    print(' ')
    return required


def scripts():
    """ return scripts of this package """
    print('Collect script files ...')
    scripts_ = []
    try:
        for scriptfile in os.listdir('scripts'):
            print('Adding "{s}" Script'.format(s=scriptfile))
            scripts_.append(os.path.join('scripts', scriptfile))
    except OSError:
        pass
    print(' ')


def packagedata():
    """ return dictionary with package data of all packages """
    print('Collect package data ...')
    package_data = dict()
    for path in os.listdir(os.path.abspath(__file__)):
        data_path = os.path.join(os.path.abspath(__file__), path, 'data')
        if os.path.isdir(data_path):
            package_data[path] = []
            for file in os.listdir(data_path):  # note: Shadowing build-in name "file" is no problem
                print('\tAdding {f} to {p}'.format(f=file, p=path))
                package_data[path].append(file)
    print(' ')
    return package_data


def license_classifier():
    """ return license tag """
    if 'apache' in Application.__version__.lower():
        license_ = 'License :: OSI Approved :: Apache Software License',
    elif 'bsd' in Application.__version__.lower():
        license_ = 'License :: OSI Approved :: BSD License',
    elif 'gpl' in Application.__version__.lower():
        license_ = 'License :: OSI Approved :: GNU General Public License (GPL)',
    elif 'mit' in Application.__version__.lower():
        license_ = 'License :: OSI Approved :: MIT License',
    elif 'mozilla' in Application.__version__.lower():
        license_ = 'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    elif 'qt' in Application.__version__.lower():
        license_ = 'License :: OSI Approved :: Qt Public License (QPL)',
    else:
        license_ = 'License :: Other/Proprietary License',
    return license_

env = [
    'Environment :: Console',
    'Environment :: MacOS X',
    # 'Environment :: No Input/Output (Daemon)',
    # 'Environment :: Plugins',
    # 'Environment :: Web Environment',
    'Environment :: Win32 (MS Windows)',
    'Environment :: X11 Applications :: Gnome',
    # 'Environment :: X11 Applications :: GTK',
    'Environment :: X11 Applications :: Qt'
]

long_description = read('README.md')

version = {
    'planning':   'Development Status :: 1 - Planning',
    'pre-alpha':  'Development Status :: 2 - Pre-Alpha',
    'alpha':      'Development Status :: 3 - Alpha',
    'beta':       'Development Status :: 4 - Beta',
    'stable':     'Development Status :: 5 - Production/Stable',
    'production': 'Development Status :: 5 - Production/Stable',
    'old':        'Development Status :: 6 - Mature',
    'mature':     'Development Status :: 6 - Mature',
    'inactive':   'Development Status :: 7 - Inactive',
}.get(Application.__status__.lower(), 'Development Status :: 1 - Planning')


setup(
    author_email=__email__,
    name=__project__,
    version=Application.__version__,
    url=__url__,
    license=Application.__license__,
    author=Application.__author__,

    # tests_require=['pytest'],
    install_requires=requirements,
    # cmdclass={'test': PyTest},
    description=__description__,
    long_description=long_description,
    packages=[__project__],
    package_data=packagedata(),
    include_package_data=True,
    platforms=__platforms__,
    scripts=scripts,
    classifiers=env.extend([
        version,
        license_classifier(),

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',

        'Operating System :: OS Independent',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',

        # 'Intended Audience :: Developers',
        # 'Intended Audience :: End Users/Desktop',

        # 'Framework :: Flask',

        'Natural Language :: English',
        # 'Natural Language :: German',

        # 'Natural Language :: Arabic',
        # 'Natural Language :: Chinese (Simplified)',
        # 'Natural Language :: Chinese (Traditional)',
        # 'Natural Language :: Hebrew',
        # 'Natural Language :: Hindi',
        # 'Natural Language :: Javanese',
        # 'Natural Language :: Korean',
        # 'Natural Language :: Persian',
        # 'Natural Language :: Russian',
        # 'Natural Language :: Spanish',
        # 'Natural Language :: Swedish',

        # 'Topic :: Artistic Software',
        # 'Topic :: Games/Entertainment',
        # 'Topic :: Games/Entertainment :: Board Games',
        # 'Topic :: Games/Entertainment :: First Person Shooters',
        # 'Topic :: Games/Entertainment :: Puzzle Games',
        # 'Topic :: Games/Entertainment :: Real Time Strategy',
        # 'Topic :: Games/Entertainment :: Role-Playing',
        # 'Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games',
        # 'Topic :: Games/Entertainment :: Turn Based Strategy',
        # 'Topic :: Internet',
        # 'Topic :: Internet :: WWW/HTTP',
        # 'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        # 'Topic :: Multimedia :: Graphics',
        # 'Topic :: Multimedia :: Graphics :: 3D Modeling',
        # 'Topic :: Multimedia :: Graphics :: Capture',
        # 'Topic :: Multimedia :: Graphics :: Editors',
        # 'Topic :: Multimedia :: Graphics :: Viewers',
        # 'Topic :: Multimedia :: Video',
        # 'Topic :: Scientific/Engineering',
        # 'Topic :: Scientific/Engineering :: Artificial Intelligence',
        # 'Topic :: Scientific/Engineering :: Image Recognition',
        # 'Topic :: Scientific/Engineering :: Visualization',
        # 'Topic :: Software Development',
        # 'Topic :: Software Development :: Libraries :: Python Modules',
        # 'Topic :: Software Development :: User Interfaces',
        # 'Topic :: Utilities',
        ]),
)

# @formatter:on
