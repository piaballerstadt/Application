#!/usr/bin/env python
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
#                           written with <3 by Pia Ballerstadt using PyCharm
#                           https://github.com/piaballerstadt
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
SampleApplication provides a detailed example on how you can use the Application-module.

The Sample Application setup a basic application by initiating a configuration file, configuring an argument parser with
some basic command line arguments and setup some loggers.

After everyhing is set up, the Application gather some information about the system it is running on and send this
to a ReSTful API.

By using the Application module, this Application is ready for internationalisation.
"""

from __future__ import print_function, division
from __future__ import unicode_literals

import textwrap
import platform
import locale
import sys
import os
import urllib2  # fixme: replace urllib2 with request module
from collections import OrderedDict
import logging
from datetime import datetime
from dateutil import tz
import six
from six.moves import configparser

from Application import Application, sniffer

try:
    from Qt import __binding__
except ImportError:
    try:
        from six.moves.tkinter import *
        __binding__ = 'Tkinter'
    except ImportError:
        __binding__ = 'None'

if sys.version_info[:2] <= (2, 7):
    input = raw_input  # Shadowing built-in name "input" is intended.

_ = unicode if six.PY2 else str

__status__ = 'development'
# Translate: this is a proper name
__author__ = _('Unicorn')
__version__ = '0.1'
# Translate: Pia Ballerstadt is a proper name; "<3" should symbolize a heart in ascii characters
__copyright__ = _('written with <3 by Pia Ballerstadt')
# Translate: Apache is a company name; "Apache License" is a open source license
__license__ = _('Apache License, Version 2.0')
__contact__ = 'https://github.com/piaballerstadt'


def main(started_at=None):
    """
    main entry point for the program

    :param started_at: optional point in time where the application has been started
    :return:
    """

    # ### SETUP APPLICATION
    locale.setlocale(locale.LC_ALL, '')
    app_started_at = started_at or datetime.utcnow().replace(tzinfo=tz.tzutc())

    application = Application(appname=six.u(os.path.basename(__file__).split('.')[0]), appauthor=__author__)
    _ = application.ugettext

    # ### SETUP CONFIGURATION
    default_configuration = OrderedDict()

    default_configuration['Privacy'] = OrderedDict()
    default_configuration['Privacy']['Participate in anonymous system analytics'] = 'Yes'

    default_configuration['Logging'] = OrderedDict()
    default_configuration['Logging']['Logging to'] = 'Stream, File'
    default_configuration['Logging']['Disable syslog on'] = 'uberspace.de'

    configuration = application.configuration(
        filename=os.path.join(application.user_config_dir, application.appname.lower() + '.conf'),
        default=default_configuration)

    # get list of hosts on which syslog will be disabled (e.g. on servers like uberspace.de)
    disable_syslog_on_hosts = configuration.get('Logging', 'Disable syslog on').split(',')
    disable_syslog_on_hosts = [hostname.strip() for hostname in disable_syslog_on_hosts]

    # ### SETUP COMMAND LINE OPTIONS
    # command line options in CSV format in a formatted string for easier translation
    cli_options_csvdata = """\
        Argument Flags\tAction\tGroup\tHelp\tOther Options
        --reset\tstore_true\t{reset_opts}\t{reset}\tdefault=False
        --delete\tstore\t{reset_opts}\t{deletes}\tdefault=0
        -h, --help\tstore_true\t{other_opts}\t{help}\tdefault=False
        -v\tcount\t{other_opts}\t{verbose}\tdefault=0
        -V, --version\tversion\t{other_opts}\t{version}\t
        -q, --quiet\tstore_true\t{other_opts}\t{quiet}\tdefault=False
        --logging\tstore\t{other_opts}\t{logging}\tdefault=stream,file
        --nosyslog\tstore_true\t{other_opts}\t{nosyslog}\tdefault={enable_syslog}"""

    cli_options = textwrap.dedent(cli_options_csvdata.format(
        # Translate: Command line option group
        verbose_opts=_('Options for verbosity'),
        # Translate: Command line option group
        other_opts=_('Other Options'),
        # Translate: Command line option group
        reset_opts=_('Application Resetting'),
        # Translate: Command line option to show help
        help=_('Show help and exit'),
        # Translate: Command line option to show version
        version=_('Show version and exit'),
        # Translate: Command line option to show verbose messages
        verbose=_('Show additional information; stackable with -vv or -vvv'),
        # Translate: Command line option to supress all output, overwriting the command line open '-v'
        quiet=_('Suppress all output; overwrites -v, -vv and -vvv'),
        # Translate: Command line option to reset the application
        reset=_('Deletes all reclaimable configuration files'),
        # Translate: Command line option to delete specific configuration files
        deletes=_('Delete specific configuration files and tries to regenerate them at the next start'),
        # Translate: Command line option to configure logging messages (choices: stream, file, stream+file, off)
        logging=textwrap.dedent(_('''\
                Toggles logging; possible values: stream, file, syslog, nteventlog, off or any comma separated list \
                (e.g. stream,file; stream,sys; file,nt ...)''')),
        # Translate: Command line option to disable logging to syslog
        nosyslog=_('disable automatically logging to syslog'),
        # enable syslog by default on all machines except the ones with platform.node() occurring in server_hostnames
        enable_syslog=any(name in platform.node().lower() for name in disable_syslog_on_hosts)))

    # create a temporary argument parser to get initial options to setup logging
    # this parser will be overwritten later to enable localisation of parser messages (like the command line help)
    parser = application.parser(cli_options,
                                copyright=_(__copyright__),
                                contact=_(__contact__),
                                license=_(__license__),
                                author=_(__author__)
                                doc=_(__doc__))
    args = parser.parse_args()

    # ### SETUP LOGGER
    logger = logging.getLogger(application.appname.lower())
    logger.setLevel(logging.DEBUG)
    syslog = logging.getLogger(application.appname.lower() + "_syslog")
    syslog.setLevel(100)

    logging_handlers = args.logging.split(',') if args.nosyslog else '{},system'.format(args.logging).split(',')
    try:
        logging_handlers.extend([handler.strip() for handler in configuration.get('Logging', 'Handlers').split(',')])
    except (configparser.NoSectionError, configparser.NoOptionError):
        pass
    logger, syslog = application.setup_logging_handlers(logging_handlers, verbose=args.v, logger=logger, syslog=syslog)

    # ### SETUP FINAL PARSER
    # this second initialisation enables localisation of the command line interface if preferred
    parser = application.parser(cli_options, copyright=_(__copyright__), contact=_(__contact__), license=_(__license__))
    parser.epilog = '\n{copy}\n{license}\n\n{contact}\n'.format(copy=_(__copyright__),
                                                                license=_(__license__),
                                                                contact=__contact__)
    args = parser.parse_args()

    # ### HANDLE COMMAND LINE ARGUMENTS
    if args.help:
        # handle command line help manually to enable localisation
        parser.print_help()
        sys.exit(0)

    if args.reset:
        application.reset(['language', 'configuration', 'cache', 'log', 'data'])
        for handler in logger.handlers and not args.quiet:
            handler.setLevel(logging.INFO)
        logger.info('Application has been reset. Please restart.')
        sys.exit(0)

    if args.delete:
        to_delete = []
        to_delete.extend([x.lower().strip() for x in args.delete.split(',')])
        application.reset(to_delete)

    # ### SETUP FINISHED

    # ### START APPLICATION
    # Translate: Everything between curled brackets are placeholder;
    # Please replace the %X to set proper date formatting for your language.
    # See http://strftime.org for details.
    logger.info('{application} started at {time}'.format(application=application.appname.lower(), time=app_started_at))

    record = sniffer.record(detailed=True, format='json', cache=application.user_cache_dir)
    if record.startswith('"'):
        record = record[1:]
    if record.endswith('"'):
        record = record[:-1]
    # record = json.loads(record, encoding='utf8')

    url = 'http://localhost:5000'
    endpoint = '/alpha/log/systeminformation'

    # todo: use Module "request" for Http POST requests for Python 3 Support
    request = urllib2.Request(url + endpoint, record)
    project_url = 'https://github.com/piaballerstadt/Sniffer'
    request.add_header('User-Agent', 'Sniffer/{version} by {author} ({url})'.format(version='0.1',
                                                                                    author='Pia Ballerstadt',
                                                                                    url=project_url))

    try:
        f = urllib2.urlopen(request)
        print(f.read())
    except urllib2.HTTPError as e:
        print('HTTP Error {code}: {message}'.format(code=e.code, message=e.read()))


if __name__ == '__main__':
    main()
