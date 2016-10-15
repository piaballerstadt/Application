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

""" provide basic logging, configuration management, i18n and argument parsing for any application """

from __future__ import print_function, division, unicode_literals
import argparse
import gettext
import re
import shutil
import os
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED
from logging import getLogger, Formatter, INFO, WARNING, ERROR
from logging.handlers import TimedRotatingFileHandler
import appdirs
from datetime import datetime
import six
from six.moves import configparser

try:
    from Qt import __binding__
except ImportError:
    __binding__ = 'console'

__status__ = 'development'
# Translate: Micha Grandel is a proper name
__author__ = _('Micha Grandel')
__version__ = '0.1'
# Translate: Micha Grandel is a proper name; "<3" should symbolize a heart in ascii characters
__copyright__ = _('written with <3 by Micha Grandel')
# Translate: Apache is a company name; "Apache License" is the title of an open source license
__license__ = _('Apache License, Version 2.0')
__contact__ = 'https://github.com/michagrandel'

_ = lambda x: six.u(x if isinstance(x, six.string_types) else str(x))

class Application(appdirs.AppDirs):
    """ basic logging, configuration management, i18n and argument parsing for any application """

    def __init__(self, author=__author__):
        """
        initialize Application

        :param author: application author
        """
        super(Application, self).__init__(appname=__name__.split('.')[0], appauthor=author, roaming=True)
        self._configuration = dict()
        self.language_search_locations = []
        self._loggers = []
        self.suffix = {
            'config': '.conf',  # suffix used for configuration files
            'log':    '.log',  # suffix used for configuration files
        }
        self.logger()

    def configuration(self, filename=None, default=None):
        """
        read and write configuration files and returns according configparser

        :param filename: filename to read and store configuration
        :param default: dict with default values if no configuration file is found
        :return: configparser
        """
        filename = filename or os.path.join(self.user_config_dir, self.appname.lower() + self.suffix['config'])
        default = default or {}

        try:
            return self._configuration[os.path.splitext(os.path.basename(self._configuration))[0]]
        except KeyError:
            configuration = configparser.ConfigParser(allow_no_value=True)
            configuration.optionxform = lambda s: six.u(str(s))

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
            self._configuration[os.path.splitext(os.path.basename(self._configuration))[0]] = configuration
            return self._configuration[os.path.splitext(os.path.basename(self._configuration))[0]]

    def logger(self, name=None, level=WARNING):
        """
        create default logger with <name> and <level>

        :param name: name of logger, default: appname
        :param level: level of logger, default: logging.WARNING
        :return:
        """
        name = name or self.appname.lower()

        if name not in self._loggers:
            logger = getLogger(name)
            try:
                os.makedirs(self.user_log_dir)
                logging_file_handler = TimedRotatingFileHandler(
                    os.path.join(self.user_log_dir, self.appname.lower() + self.suffix['log']), when='h', interval=1,
                    backupCount=5, encoding='utf-8')
                logging_file_handler.setLevel(level)
                logging_file_handler.setFormatter(
                    Formatter('%(asctime)s    %(levelname)s   %(message)s', datefmt='%x %X'))
                logger.addHandler(logging_file_handler)
            except (OSError, IOError) as e:
                pass
            self._logger.append(name)
        return getLogger(name)

    def languages(self, **kwargs):
        """
        copy language files from search directories to language directory

        :param kwargs: Additional Options
        :return:
        """
        try:
            return self._locale_path
        except AttributeError:
            # set directories to look for translation files (*.mo) language_search_directories=[]
            qt_engines = (
                'qt', 'pyside', 'pyside2', 'pyqt', 'pyqt4', 'pyqt5', 'qt linguist', 'qtlinguist', 'qtranslator')

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
            self._locale_path = os.path.join(self.user_data_dir, 'languages')
            translation_files = dict()
            for language_search_directory in self.language_search_locations:
                language_search_directory = os.path.abspath(os.path.expanduser(language_search_directory))

                language_file_pattern = r'^%(name)s-[a-z]{2}_[A_Z]{2}(\.mo|\.qm|\.tar\.gz|\.zip)?$'
                language_file_pattern = re.compile(language_file_pattern % {'name': self.appname.lower()})

                # language_archive_pattern = r'^%(name)s-[a-z]{2}_[A_Z]{2}(\.tar\.gz|\.zip)?$'
                # language_archive_pattern = re.compile(language_archive_pattern % {'name': self.appname.lower()})

                for original_file in os.listdir(language_search_directory):
                    # handle translation files
                    if language_file_pattern.match(original_file) != None:
                        if not os.path.exists(self._locale_path):
                            try:
                                os.makedirs(self._locale_path)
                                domain, language = os.path.splitext(original_file)[0].split('-')

                                if os.path.splitext(original_file)[1] == '.zip':
                                    try:
                                        with ZipFile(original_file, 'r', compression=ZIP_DEFLATED) as language_archive:
                                            for name in language_archive.namelist():
                                                extract_path = os.path.join(self._locale_path, language)
                                                if os.path.splitext(name)[1] == '.mo':
                                                    extract_path = os.path.join(extract_path, 'LC_MESSAGES')
                                                os.makedirs(extract_path)
                                                language_archive.extract(name, path=extract_path)
                                    except RuntimeError:
                                        pass
                                elif original_file.endswith('.tar.gz'):
                                    # todo: extract translation files from TAR.GZ archive
                                    pass
                                else:
                                    original_file = os.path.join(language_search_directory, original_file)
                                    copy_to_path = os.path.join(self._locale_path, language)

                                    if os.path.splitext(original_file)[1] == '.mo':
                                        copy_to_path = os.path.join(extract_path, 'LC_MESSAGES')

                                    shutil.copy2(
                                        original_file,
                                        os.path.join(copy_to_path, domain + os.path.splitext(original_file)[1]))

                            except (OSError, IOError):
                                pass
            _ = gettext.translation(self.appname, self._locale_path, fallback=True).ugettext
            return self._locale_path

    def parser(self, csvdata, **kwargs):
        """
        setup a parser to parse command line arguments using CSV data (tab-separated).

        :param csvdata: CSV data (tab-separated)
        :return: parser or False

        The data must include the following columns: Argument Flags, Action, Group, Help, Other Options.
        The arguments are very similar to the argparse parser, because all arguments are used in an add_argument-method.

        Argument Flags, Action, Group, Help
        ...................................

        Most columns should be self-explaining. Read the documentation of the argparse module, if you have any questions

        Other Options
        .............

        All options not covered in the other columns, can be added to the other options column. You may add multiple
        options in this column, each separated with a semicolon. Most options consist of some key-value-pair, where
        the key and the value is separated by =, e.g. key=value. For booleans, you might just add the key without value.

        Examples for other options include:

        * choices=yes,no;default=no
        * default=False

        """
        self.languages(data_dir=self.user_data_dir)
        _ = gettext.translation(self.appname, self._locale_path, fallback=True).ugettext

        # @formatter:off
        parser = argparse.ArgumentParser(
            prog=__name__.split('.')[0].lower(), description=__doc__, add_help=kwargs.get('add_help', False),
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

    def reset(self, parts, **kwargs):
        """
        resets application

        let you delete precicely any application related file.
        parts contains what you want to delete:

        value for parts    what it will delete
        ================== ===========================================================================================
        language           deletes all language files
        configuration      deletes all configuration files
        cache              deletes the cache (warning: include log files)
        log                deletes all log files
        data               deletes all data files, like images, icons, fonts etc. (warning: include language files)
        ================== ===========================================================================================

        :param parts: string or list of strings with codes for what to delete (see table above)
        :return: True if successful, False if not
        """
        if isinstance(parts, (six.string_types, six.text_type)):
            parts = [parts.lower()]

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
            self.logger().warning('Reseting all {} files ...'.format(part))
            shutil.rmtree(folder)
            if part == 'cache':
                shutil.copytree(backup_path, self.user_log_dir)
            elif part == 'log':
                shutil.copytree(backup_path, os.path.join(self.user_data_dir, 'languages'))

    @staticmethod
    def _string2value(value):
        """
        parses a given value (string?) and return valid python values

        Parsing table:

        Key              Examples                   parse to
        ================ ========================== ===================
        Numeric strings  1, 2, 3, 2.3, 5.6          int(x) or float(x)
        Boolean Strings  True/False, On/Off, Yes/No True or False
        ================ ========================== ===================

        >>> [string2value(x) for x in '1 1.2 TRUE Off No'.split()]
        [1, 1.2, True, False, False]
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
