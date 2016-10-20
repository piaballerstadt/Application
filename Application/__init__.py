#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# @formatter:off
#
#                                            ,,
#                                             db
#     \
#     _\,,          `7MM  `7MM  `7MMpMMMb.  `7MM  ,p6"bo   ,pW"Wq.`7Mb,od8 `7MMpMMMb.
#    "-=\~     _      MM    MM    MM    MM    MM 6M'  OO  6W'   `Wb MM' "'   MM    MM
#       \\~___( ~     MM    MM    MM    MM    MM 8M       8M     M8 MM       MM    MM
#      _|/---\\_      MM    MM    MM    MM    MM 8M       8M     M8 MM       MM    MM
#     \        \      MM    MM    MM    MM    MM YM.    , YA.   ,A9 MM       MM    MM
#                     `Mbod"YML..JMML  JMML..JMML.YMbmd'   `Ybmd9'.JMML.   .JMML  JMML.
#
#
#                           written with <3 by Micha Grandel using PyCharm
#                           https://github.com/michagrandel
#
#                       Licensed under the Apache License, Version 2.0 (the "License");
#                       you may not use this file except in compliance with the License.
#                       You may obtain a copy of the License at
#
#                           http://www.apache.org/licenses/LICENSE-2.0
#
#                       Unless required by applicable law or agreed to in writing, software
#                       distributed under the License is distributed on an "AS IS" BASIS,
#                       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#                       See the License for the specific language governing permissions and
#                       limitations under the License.
#
#                                                      __
#                                             _ww   _a+"D
#                                      y#,  _r^ # _*^  y`
#                                     q0 0 a"   W*`    F   ____
#                                  ;  #^ Mw`  __`. .  4-~~^^`
#                                 _  _P   ` /'^           `www=.
#                               , $  +F    `                q
#                               K ]                         ^K`
#                             , §_                . ___ r    ],
#                             _*.^            '.__dP^^~#,  ,_ *,
#                             ^b    / _         ``     _F   ]  ]_
#                              '___  '               ~~^    ]   [
#                              :` ]b_    ~k_               ,`  yl
#                                §P        `*a__       __a~   z~`
#                                §L     _      ^------~^`   ,
#                                 ~-vww*"v_               _/`
#                                         ^"q_         _x"
#                                          __§my..___p/`mma____
#                                      _awP",`,^"-_"^`._ L L  #
#                                    _#0w_^_^,^r___...._ t [],"w
#                                   e^   ]b_x^_~^` __,  .]Wy7` x`
#                                    '=w__^9*§P-*MF`      ^[_.=
#                                        ^"y   qw/"^_____^~9 t
#                                          ]_l  ,'^_`..===  x'
#                                           ">.ak__awwwwWW
#                                             #§WWWWWWWWWWWWWW
#                                            _WWWWWWMM§WWWW_JP^"~-=w_
#                                  .____awwmp_wNw#[w/`     ^#,      ~b___.
#                                   ` ^^^~^"W___            ]Raaaamw~`^``^^~
#                                             ^~"~---~~~~~~`#
# @formatter:on

"""
.. access user specific paths, initiate internationalization, manage configurations, generate argument parser

.. module:: Application
   :platform: Windows, Linux, macOS, OS X
   :synopsis: access user specific paths, initiate internationalization, manage configurations, generate argument parser
.. moduleauthor:: Lydia Seifert <piaballerstadt@googlemail.com>
.. sectionauthor:: Lydia Seifert <piaballerstadt@googlemail.com>
.. versionadded:: 0.1

The :mod:`Application`-module extends the `appdirs <https://pypi.python.org/pypi/appdirs>`_-module and provides some
basic functionality useful for an application. This includes functions for simple *logging*, *configuration management*,
*initialization*, *argument parsing* or simply *accessing platform specific paths* like paths for caches, logging files,
configuration- or data files.

This module inherits many methods and attributes from `appdirs.AppDirs <https://pypi.python.org/pypi/appdirs>`_,
a module written by Trent Mick and Sridhar Ratnakumar!

.. seealso::

   `appdirs <https://pypi.python.org/pypi/appdirs>`_
"""

from __future__ import print_function, division, unicode_literals
import argparse
import gettext
import locale
import platform
import shutil
import tarfile
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED, is_zipfile
import logging
from logging.handlers import *
import appdirs
from datetime import datetime
import six
from six.moves import configparser

try:
    from Qt import __binding__
except ImportError:
    __binding__ = 'console'

_ = unicode if six.PY2 else str

__version__ = '0.1'
__status__ = 'alpha'
# Translate: Pia Ballerstadt is a proper name
__author__ = _('Micha Grandel')
__contact__ = 'https://github.com/michagrandel'
# Translate: Pia Ballerstadt is a proper name; "<3" should symbolize a heart in ascii characters
__copyright__ = _('written with <3 by Micha Grandel')
# Translate: Apache is a company name; "Apache License" is the title of an open source license
__license__ = _('Apache License, Version 2.0')


class Application(appdirs.AppDirs):
    """
    The :class:`Application`-class extends the `appdirs.AppDirs <https://pypi.python.org/pypi/appdirs>`_-class and
    provides some basic functionality useful for an application. In addition to AppDirs platform specific path's,
    the Application class includes functions for simple *logging*, *configuration management*, *internationalization*,
    and *argument parsing*.

    This class inherits many methods and attributes from `appdirs.AppDirs <https://pypi.python.org/pypi/appdirs>`_,
    a module written by Trent Mick and Sridhar Ratnakumar!

    :param unicode appname: application name
    :param unicode appauthor: application author

    .. attribute:: user_config_dir

        user's directory for configuration files

        Inherited from `appdirs.AppDirs <https://pypi.python.org/pypi/appdirs>`_.

    .. attribute:: user_cache_dir

        user's directory for caches

        Inherited from `appdirs.AppDirs <https://pypi.python.org/pypi/appdirs>`_.

    .. attribute:: user_log_dir

        user's directory for logfiles

        Inherited from `appdirs.AppDirs <https://pypi.python.org/pypi/appdirs>`_.

    .. attribute:: user_data_dir

        user's directory for application data

        Inherited from `appdirs.AppDirs <https://pypi.python.org/pypi/appdirs>`_.
    """

    def __init__(self, appname, appauthor):
        """
        initialize Application

        :param unicode appname: application name
        :param unicode appauthor: application author
        """
        super(Application, self).__init__(appname=appname, appauthor=appauthor, roaming=True)
        global __author__
        global __copyright__
        __author__ = appauthor
        __copyright__ = 'written with <3 by {author}'.format(author=appauthor)
        locale.setlocale(locale.LC_ALL, '')
        self._configuration = dict()
        self.language_search_locations = []
        self._locale_path = os.path.join(self.user_data_dir, 'languages')

        self._language_filepack_pattern = re.compile(
            r'^%(name)s-[a-z]{2}_[A-Z]{2}(\.mo|\.qm|\.tar\.gz|\.zip)?$' % {'name': self.appname.lower()})
        self._language_file_pattern = re.compile(r'^%(name)s-[a-z]{2}_[A-Z]{2}(\.mo|\.qm)?$')
        global _
        _ = self._ = self.ugettext = unicode if six.PY2 else str
        self.languages()

    def configuration(self, filename=None, default=None):
        """
        read and write configuration files and returns configuration

        If no file with *filename* exists, a file will created with the `default` values inside the configuration path.
        If *filename* is `None`, a default file named after the application will be used. It will be stored in the
        application's configuration path.

        The configuration file has to be in the `configparser <https://docs.python.org/2/library/configparser.html>`_ Format.

        :param unicode filename: configuration file
        :param dict default: default values if no configuration file is found
        :return: configuration
        :rtype: `configparser <https://docs.python.org/2/library/configparser.html>`_

        .. seealso::

            Module `configparser <https://docs.python.org/2/library/configparser.html>`_:
               Parse configuration data
        """
        filename = os.path.abspath(os.path.expanduser(filename)) or \
            os.path.join(self.user_config_dir, self.appname.lower() + '.conf')
        default = default or {}

        try:
            return self._configuration[os.path.splitext(os.path.basename(filename))[0]]
        except KeyError:
            configuration = configparser.ConfigParser(allow_no_value=True)
            # fixme: replace unicode()-call with code compatible with python2 AND python3
            configuration.optionxform = lambda s: unicode(s) if six.PY2 else str(s)

            for section, keyvalues in six.iteritems(default):
                try:
                    configuration.add_section(section)
                except configparser.DuplicateSectionError:
                    pass
                for option, value in six.iteritems(keyvalues):
                    configuration.set(section, option, value)
            try:
                os.makedirs(os.path.dirname(os.path.abspath(filename)))
                with open(os.path.abspath(filename), 'w') as config_file:
                    configuration.write(config_file)
            except OSError:
                pass
            self._configuration[os.path.splitext(os.path.basename(filename))[0]] = configuration
            return self._configuration[os.path.splitext(os.path.basename(filename))[0]]

    def extract_languages_from_archive(self, archive_file):
        """
        extract .qm- and .mo-files from *archive_file* and stores them in the directory for translation files.

        :param unicode archive_file: filename of an archive file
        :return: count of extracted files
        :rtype: int

        Supported archive formats include ZIP-Files (.zip), TAR-Files (.tar), Compressed TAR-Files (.tar.gz, .tgz).

        Extracted .mo-files will be stored in *user_data_dir*/language/*languagecode*/LC_MESSAGES/\*.mo,
        while .qm-files will be stored in *user_data_dir*/language/*languagecode*/\*.qm.

        `user_data_dir` is replaced by self.user_data_dir.

        `languagecode` is the language code of the target language of the translation files, e.g. en_US, de_DE etc.

        .. seealso::

           Module `appdirs <https://pypi.python.org/pypi/appdirs>`_:
              A small Python module for determining appropriate platform-specific dirs, e.g. a user data dir
        """
        archive_file = os.path.abspath(archive_file)
        domain, language = os.path.splitext(os.path.basename(archive_file))[0].split('-')
        count_extracted_files = 0
        logger = logging.getLogger(self.appname.lower())

        if is_zipfile(archive_file):
            try:
                with ZipFile(archive_file, 'r', compression=ZIP_DEFLATED) as language_archive:
                    for name in language_archive.namelist():
                        if self._language_file_pattern.match(name) is not None:
                            target_path = os.path.join(self._locale_path, language)
                            if os.path.splitext(name)[1] == '.mo':
                                target_path = os.path.join(target_path, 'LC_MESSAGES')
                            os.makedirs(target_path)
                            language_archive.extract(name, path=target_path)
                            count_extracted_files += 1
            except (RuntimeError, OSError):
                logger.warning('Can not extract files from {archive}.'.format(archive=os.path.basename(archive_file)))
                return -1
        elif tarfile.is_tarfile(archive_file):
            try:
                with tarfile.open(archive_file, mode='r:gz') as language_archive:
                    for name in language_archive.getnames():
                        if self._language_file_pattern.match(name) is not None:
                            target_path = os.path.join(self._locale_path, language)
                            if os.path.splitext(name)[1] == '.mo':
                                target_path = os.path.join(target_path, 'LC_MESSAGES')
                            os.makedirs(target_path)
                            language_archive.extract(name, path=target_path)
                            count_extracted_files += 1
            except (RuntimeError, OSError, tarfile.ReadError, tarfile.CompressionError):
                logger.warning('Can not extract files from {archive}.'.format(archive=os.path.basename(archive_file)))
                return -1
        else:
            logger.warning('{archive} is not a supported archive type.'.format(archive=os.path.basename(archive_file)))
            return -1
        return count_extracted_files

    def languages(self):
        """
        copy language files from search directories to language directory

        :return: root directory for internationalization related files

        Copy .mo-files to *user_data_dir*/language/*languagecode*/LC_MESSAGES/\*.mo,
        and copy .qm-files to *user_data_dir*/language/*languagecode*/\*.qm.

        `user_data_dir` is replaced by self.user_data_dir.

        `languagecode` is the language code of the target language of the translation files, e.g. en_US, de_DE etc.

        .. seealso::

           Module `appdirs <https://pypi.python.org/pypi/appdirs>`_:
              A small Python module for determining appropriate platform-specific dirs, e.g. a user data dir

        """

        # @formatter:off
        # paths to search for language files
        self.language_search_locations.extend((
            os.path.join('~/Projects', self.appname.lower()),
            os.path.join('~/Projekte', self.appname.lower()),
            os.path.join(self.user_data_dir, 'lang'),
            os.path.join(self.user_data_dir, 'language'),
            os.path.join(self.user_data_dir, 'translations'),
            os.path.join(self.user_data_dir, 'translation'),
            os.path.join(self.user_data_dir, 'locale')))
        # @formatter:on

        # search .qm- and .mo-files in language_search_directories
        for language_search_directory in self.language_search_locations:
            language_search_directory = os.path.abspath(os.path.expanduser(language_search_directory))
            try:
                for original_file in os.listdir(language_search_directory):
                    # handle translation files
                    if self._language_filepack_pattern.match(original_file) is not None:
                        if not os.path.exists(self._locale_path):
                            os.makedirs(self._locale_path)
                            domain, language = os.path.splitext(original_file)[0].split('-')

                            if os.path.splitext(original_file)[1] == '.zip':
                                self.extract_languages_from_archive(
                                    os.path.join(language_search_directory, original_file))

                            elif original_file.endswith('.tar.gz') or os.path.splitext(original_file)[1] == '.tgz':
                                self.extract_languages_from_archive(
                                    os.path.join(language_search_directory, original_file))
                            else:
                                original_file = os.path.join(language_search_directory, original_file)
                                target_path = os.path.join(self._locale_path, language)

                                if os.path.splitext(original_file)[1] == '.mo':
                                    target_path = os.path.join(target_path, 'LC_MESSAGES')

                                shutil.copy2(original_file,
                                             os.path.join(target_path, domain + os.path.splitext(original_file)[1]))

            except (OSError, IOError):
                pass
        global _
        _ = self._ = self.ugettext = gettext.translation(self.appname, self._locale_path, fallback=True).ugettext
        return self._locale_path

    def parser(self, csvdata, **kwargs):
        """
        setup a argparser to parse command line arguments using *csvdata* (tab-separated).

        :param unicode csvdata: CSV data (tab-separated)
        :param kwargs: additonal keyword arguments as described in "additional options"
        :return: parser or False
        :rtype: argparse.parser or boolean

        The csvdata must include the following columns: Argument Flags, Action, Group, Help, Other Options.

        The arguments are very similar to the argparse parser, because all arguments are used in an add_argument-method.

        .. seealso::

            Module `argparse <https://docs.python.org/2/library/argparse.html>`_:
               The argparse module makes it easy to write user-friendly command-line interfaces.

        Additional Options
        ------------------

        :add_help:
           adds a '-h' argument to the parser that shows the help and exit the application afterwards
        :doc:
           help that will show when the user uses -h or --help as command line argument

        """
        self.languages()

        # @formatter:off
        parser = argparse.ArgumentParser(
            prog=__name__.split('.')[0].lower(), description=kwargs.get('doc', ''), add_help=kwargs.get('add_help', False),
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        # @formatter:on

        # read csv data and thereby ignore first line (it contains column titles)
        reader = [line.split('\t') for line in csvdata.splitlines()][1:]
        argument_groups = dict()

        # parse csv data
        for n, row in enumerate(reader):
            # parse flags and options
            args, kwargs = Application._parse_flag_options(flags=row[0], action=row[1], help_=row[3],
                                                           other_options=row[4])

            # check group column
            if len(row[2]) > 0:
                group_name = row[2]

                # create group if it doesn't exist
                if group_name not in argument_groups:
                    argument_groups[group_name] = parser.add_argument_group(group_name)
                argument_groups[group_name].add_argument(*args, **kwargs)
            else:
                parser.add_argument(*args, **kwargs)
        return parser

    def setup_logging_handlers(self, handlers, logger, syslog, **kwargs):
        """
        add default handlers to *logger* and *syslog*

        :param handlers: string with handler keywords
        :param kwargs: additional options
        :param logger: logger instance for normal logging
        :param syslog: logger instance for logging to syslog
        :return: logger and syslog instances, setup with handlers
        """
        syslog_formatter_str = __name__ + '[%(lineno)s]: %(levelname)s: %(asctime)s: %(funcName)s() \'%(message)s\''
        formatter = {
            'simple':   logging.Formatter('%(message)s'),  # used for verbose messages
            'messages': logging.Formatter('# %(levelname)s: %(message)s'),  # currently not used at all
            'extended': logging.Formatter('%(asctime)s    %(levelname)s   %(message)s', datefmt='%x %X'),  # log to file
            'syslog':   logging.Formatter(syslog_formatter_str)
        }

        for handler in handlers:
            if handler.lower() in ('stream', 'debug') and not any(
                    isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
                logging_error_handler = logging.StreamHandler()

                if handler.lower() == 'debug':
                    logging_error_handler.setLevel(logging.DEBUG)
                elif handler.lower() == 'stream':
                    verbose_level = [logging.ERROR, logging.INFO, logging.INFO, logging.DEBUG]
                    logging_error_handler.setLevel(verbose_level[kwargs.get('verbose', 0)])

                logging_error_handler.setFormatter(formatter['simple'])
                logger.addHandler(logging_error_handler)

            elif handler.lower() == 'file' and not any(
                    isinstance(handler, logging.FileHandler) for handler in logger.handlers):
                try:
                    os.makedirs(self.user_log_dir)
                    logging_file_handler = TimedRotatingFileHandler(
                        os.path.join(self.user_log_dir, __name__.split('.')[0].lower() + '.log'), when='h', interval=1,
                        backupCount=5, encoding='utf-8')
                    logging_file_handler.setLevel(logging.INFO)
                    logging_file_handler.setFormatter(formatter['extended'])
                    logger.addHandler(logging_file_handler)
                    print('Logging to {}'.format(logging_file_handler.baseFilename))
                except (OSError, IOError):
                    # handle this behind the loop
                    # because maybe there is no streamhandler configured yet,
                    # but will be later
                    pass

            elif any(keyword in handler.lower() for keyword in ('sys', 'nt', 'event')) and not any(
                    isinstance(handler, SysLogHandler) for handler in logger.handlers):
                print('setup syslog')
                syslog.setLevel(logging.DEBUG)
                try:
                    servernames = self._configuration[self.appname.lower()].get('Logging', 'Disable syslog on')
                    servernames = servernames.split(',')
                except KeyError:
                    servernames = ['uberspace']
                if not any(name in platform.node().lower() for name in [hostname.strip() for hostname in servernames]):
                    logging_sys_handler = SysLogHandler(address='/dev/log')
                else:
                    syslog_file = os.path.join(self.user_log_dir, 'syslog.log')
                    logging_sys_handler = TimedRotatingFileHandler(syslog_file, backupCount=5, encoding='utf-8')

                logging_sys_handler.setLevel(logging.INFO)
                logging_sys_handler.setFormatter(formatter['syslog'])
                syslog.addHandler(logging_sys_handler)
            else:
                print('Unknown handler ' + handler.lower())

        # react if initializing file handler for logging didn't work
        if 'file' in handlers and not any(isinstance(handler, logging.FileHandler) for handler in logger.handlers):
            syslog.error('''Can't create logging file '{file}'.'''.format(
                file=os.path.join(self.user_log_dir, __name__.split('.')[0].lower() + '.log')))
        return logger, syslog

    def reset(self, parts):
        """
        delete precisely any application related file.

        :param parts: code for what to delete (see table below)
        :type parts: unicode or list
        :return: True if successful, False if not

        ================== ===========================================================================================
        value for parts    what it will delete
        ================== ===========================================================================================
        language           deletes all language files
        configuration      deletes all configuration files
        cache              deletes the cache (warning: include log files)
        log                deletes all log files
        data               deletes all data files, like images, icons, fonts etc. (warning: include language files)
        ================== ===========================================================================================

        Combine any parts in lists of parts to select and delete multiple parts at once.

        """
        if isinstance(parts, (six.string_types, six.text_type)):
            parts = [parts.lower()]
        logger = logging.getLogger(self.appname.lower())
        for part in parts:
            folder = {
                'language': self.user_cache_dir, 'configuration': self.user_config_dir, 'cache': self.user_cache_dir,
                'log':      self.user_log_dir, 'data': self.user_data_dir,
            }.get(part.lower())
            if part == 'cache':
                backup_path = os.path.join(tempfile.gettempdir(), 'log_' + datetime.utcnow().strftime('%H%M%S'))
                shutil.copytree(self.user_log_dir, backup_path)
            elif part == 'data':
                backup_path = os.path.join(tempfile.gettempdir(), 'data_' + datetime.utcnow().strftime('%H%M%S'))
                shutil.copytree(os.path.join(self.user_data_dir, 'languages'), backup_path)
            logger.warning('Reseting all {} files ...'.format(part))
            shutil.rmtree(folder)
            if part == 'cache':
                shutil.copytree(backup_path, self.user_log_dir)
            elif part == 'log':
                shutil.copytree(backup_path, os.path.join(self.user_data_dir, 'languages'))

    @staticmethod
    def _string2value(value):
        """
        parses a given *value* and return valid python values

        :param value: value to convert
        :return: number or boolean

        Parsing table:

        Key              Examples                   parse to
        ================ ========================== ===================
        Numeric strings  1, 2, 3, 2.3, 5.6          int(x) or float(x)
        Boolean Strings  True/False, On/Off, Yes/No True or False
        ================ ========================== ===================
        """
        result = value

        if isinstance(value, six.string_types):
            if value.isnumeric():
                result = int(value)
            elif all(x.isnumeric() for x in value.split('.')):
                result = float(value)
            elif value.lower() in ('true', 'on', 'yes'):
                result = True
            elif value.lower() in ('false', 'off', 'no'):
                result = False

        return result

    @staticmethod
    def _parse_flag_options(flags, action, help_, other_options):
        """
        parse argument flag options for argparser

        :param flags: flags for argparse
        :param action: action for argparse
        :param help_: string that will show up in command line help
        :param other_options: other options for argparse
        :return: args and kwargs for the argparse.add_argument_group-method
        """
        # handle flags
        # flags can also be names for positional arguments
        flags = ''.join(flags.split())

        # these will be used for the argparse.add_argument_group-method
        args = flags.split(',') if ',' in flags else [flags]
        kwargs = dict()

        # other_options may include things like choices, metavar, default etc.
        # they are stored in a string like "option1=value1; option2=value2; ..."
        if len(other_options) > 0:
            # cleanup options
            other_options = other_options.split(';') if ';' in other_options else [other_options]
            for n, option in enumerate(other_options):
                other_options[n] = option.strip()
            # check each option
            for option in other_options:
                # most options separate key and value by a '='
                if "=" in option:
                    name, value = option.split("=")

                # some options are booleans. If present, this means True, if not present False
                else:
                    name, value = option, True

                # check for invalid options
                valid_options = ['nargs', 'const', 'default', 'type', 'choices', 'required', 'metavar', 'dest']

                if name not in valid_options:
                    raise ValueError('Option "{option}" is not valid.\nTry reinstall.'.format(option=name))
                else:
                    if name == 'choices':
                        value = value.split(',')
                        for n, text in enumerate(value):
                            value[n] = Application._string2value(text.strip())
                    elif name == 'default':
                        value = Application._string2value(value)
                    kwargs[name] = value

        # ignore action, if the option has choices
        if 'choices' not in kwargs:
            kwargs['action'] = action

        kwargs['help'] = help_

        return args, kwargs
