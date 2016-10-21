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
.. get system information

.. module:: Sniffer
   :platform: Windows, Linux, macOS, OS X
   :synopsis: get information about the hardware and system you are running on
.. moduleauthor:: Micha Grandel <talk@michagrandel.de>
.. sectionauthor:: Micha Grandel <talk@michagrandel.de>
.. versionadded:: 0.1

The :mod:`Sniffer`-module let's you gather information about the machine your application is running on,
including hardware, operation system, network capabilities and more.
"""

from __future__ import unicode_literals, print_function

import babel
import getpass
import json
import locale
import os
import platform
import re
import six
import subprocess
import sys
import tempfile
import textwrap
import zipfile
import urllib2  # fixme: replace urllib2 with request module
from collections import OrderedDict
from contextlib import closing
from datetime import datetime
from urllib2 import urlopen  # fixme: replace urllib2 with request module
from uuid import getnode
import ipgetter
import pyspeedtest
from psutil import virtual_memory, disk_usage, cpu_count, disk_partitions

try:
    import OpenGL
    from OpenGL import GL
    from OpenGL import GLUT

    def gpu(info='', **kwargs):
        """
        returns GPU Vendor, OpenGL Version, GLSL Version and Renderer

        This function is only available, if PyOpenGL is installed on the target machine.

        :param unicode info: 'vendor', 'version', 'shading_language', 'renderer' or 'all'
        :param kwargs: Additional Options
        :return: vendor, version, glsl version, renderer or all

        .. seealso::

            Module :mod:`OpenGL`
        """

        nbsp = kwargs.get('nbsp', False)
        try:
            # initialize OpenGL to get some information about the graphic card
            GLUT.glutInit()
            GLUT.glutInitDisplayMode(GLUT.GLUT_RGBA | GLUT.GLUT_DOUBLE)
            GLUT.glutInitWindowSize(1, 1)
            GLUT.glutInitWindowPosition(10000, 0)
            GLUT.glutCreateWindow("noobtuts.com")

            vendor = GL.glGetString(GL.GL_VENDOR).replace(' ', '\u00a0') if nbsp else GL.glGetString(GL.GL_VENDOR)
            version = GL.glGetString(GL.GL_VERSION).replace(' ', '\u00a0') if nbsp else GL.glGetString(GL.GL_VERSION)
            shading_language = GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION)
            shading_language = shading_language.replace(' ', '\u00a0') if nbsp else shading_language
            renderer = GL.glGetString(GL.GL_RENDERER).replace(' ', '\u00a0') if nbsp else GL.glGetString(GL.GL_RENDERER)
        except OpenGL.error:
            vendor = version = shading_language = renderer = 'Unknown'
        try:
            version = float(version)
        except ValueError:
            pass
        try:
            shading_language = float(shading_language)
        except ValueError:
            pass

        return {
            'vendor': vendor, 'version': version, 'shading language': shading_language, 'renderer': renderer,
        }.get(info.lower(), (vendor, version, shading_language, renderer))


    opengl_enabled = True
except ImportError:
    opengl_enabled = False

__version__ = '0.1'
__author__ = 'Pia Ballerstadt'
__url__ = 'https://github.com/piaballerstadt/Sniffer'


def location():
    """
    Automatically geolocate the user's IP

    :return: location of user's IP
    :rtype: dict

    .. warning:: Privacy Information

       In some countries, the user's IP is considered personal data.
       Gathering it and sending it to a server might interfere with your user's privacy.
       Please consult an attorney to get more information.
    """

    # alternative url: http://freegeoip.net/json/178.203.232.164
    url = 'http://ip-api.com/json/#178.203.232.164'

    with closing(urlopen(url)) as response:
        location_ = json.loads(response.read())
    return location_


def cpu(info='', **kwargs):
    """
    returns name and clock speed of the CPU in this computer

    :param info: 'name' or 'speed', if not set, return both
    :return: name, speed
    :rtype: unicode, float or tuple(unicode, float)

    If *info* is 'name' or 'speed', only the requested value is returned.
    Otherwise it will return a tuple `(name, speed)`.

    On Linux, the returned speed will allways be a float.
    On other systems, it is more likely to be a unicode string.

    """
    
    nbsp = kwargs.get('nbsp', False)
    cpu_name = 'Unknown'
    cpu_speed = 0.

    # on windows, use wmic to get information on the cpu
    if sys.platform.startswith('win'):
        cpu_name = subprocess.check_output(['wmic', 'cpu', 'get', 'name']).strip().split('\n')[1]
        cpu_speed = subprocess.check_output(['wmic', 'cpu', 'get', 'MaxClockSpeed']).strip().split('\n')[1]

    # on macOS, use sysctl to get insformation on the cpu
    elif sys.platform == 'darwin':
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command = "sysctl -n machdep.cpu.brand_string"
        cpu_name = subprocess.check_output(command).strip()
        cpu_speed = cpu_name.split('@')[1].strip()

    # on linux, use cpuinfo to get information on the cpu
    elif sys.platform.startswith('linux'):
        command = 'cat /proc/cpuinfo'
        for line in subprocess.check_output(command, shell=True).strip().split("\n"):
            if "model name" in line:
                cpu_name = re.sub(".*model name.*:", "", line, 1).strip()
            if "cpu MHz" in line:
                cpu_speed = round(float(re.sub(".*cpu MHz.*:", "", line, 1).strip().split('.')[0]) / 1024, 1)
    cpu_name = cpu_name.replace(' ', '\u00a0') if nbsp else cpu_name
    return {
        'name': cpu_name, 'speed': cpu_speed,
    }.get(info.lower(), (cpu_name, cpu_speed))


def system(info='', **kwargs):
    """
    return name or version (release) of system or both

    :param unicode info: 'name', 'version' or 'all'; default: 'all'
    :return: name, version or both

    If possible, the version includes the name of the release (consult list below for examples).

    Examples (this is not a complete list):
    ---------------------------------------

    +----------------------+----------------------------------------------------------------+
    | Name of System       | Expected Version                                               |
    +======================+================================================================+
    | Windows              | Vista, 7, 8, 10                                                |
    +----------------------+----------------------------------------------------------------+
    | macOS                | Sierra                                                         |
    +----------------------+----------------------------------------------------------------+
    | OS X                 | Mavericks, Yosemite, El Capitan                                |
    +----------------------+----------------------------------------------------------------+
    | Mac OS X             | 10.6 "Snow Leopard", 10.7 "Lion", 10.8 "Mountain Lion"         |
    +----------------------+----------------------------------------------------------------+
    | Ubuntu               | 16.04 "Xenial Xerus", 14.04 "Trusty Tahr"                      |
    +----------------------+----------------------------------------------------------------+

    """

    name = version = ''
    nbsp = kwargs.get('nbsp', False)
    
    if sys.platform.startswith('win'):
        name = 'Windows'
        if platform.release() == 10:
            version = '10'
        else:
            if sys.getwindowsversion().major == 6:
                version = 'Vista 7 8 8.1'.split(' ')[sys.getwindowsversion().minor]
            else:
                version = 'XP or older'
    
    elif sys.platform == 'darwin':
        # todo: read macOS release names from configuration file
        version = textwrap.dedent('''\
            10 "Cheetah"
            10.1 "Puma"
            10.2 "Jaguar"
            10.3 "Panther"
            10.4 "Tiger"
            10.5 "Leopard"
            10.6 "Snow Leopard"
            10.7 "Lion"
            10.8 "Mountain Lion"
            Mavericks
            Yosemite
            El Capitan
            Sierra''').splitlines()[int(platform.mac_ver()[0].split('.')[1])]

        # differentiate between "Mac OS X" (10.0 Cheetah til 10.8 Mountain Lion)
        if int(platform.mac_ver()[0].split('.')[1]) < 8:
            name = 'Mac OS X'
        # ... and "OS X" (10.9 Mavericks til 10.11 El Capitan)
        elif 7 < int(platform.mac_ver()[0].split('.')[1]) < 12:
            name = 'OS X'
        # ... and "macOS" (from 10.12 Sierra on)
        else:
            name = 'macOS'

    elif sys.platform.startswith('linux'):
        # get distribution name
        if os.path.exists('/etc/arch-release'):
            name = 'Arch Linux'  # output of platform.linux_distribution on Arch Linux is unknown
        else:
            name = platform.linux_distribution()[0]
            # Expected Output of different Linux Distributions for platform.linux_distribution:
            # Ubuntu:   ('Ubuntu', '12.10', 'quantal')
            # Fedora:   ('Fedora', '21', 'Twenty One')
            # Debian:   ('debian', '6.0.6', '')
            # CentOS:   ('CentOS', '6.3', 'Final')
            # RHEL:     ('Red Hat Enterprise Linux Server', '6.2', 'Santiago')
            # SL:       ('Scientific Linux', '6.2', 'Carbon')
            # SLES      ('SUSE Linux Enterprise Server', '11', 'x86_64')

        if not name and os.path.isfile('/etc/system-release'):
            distribution = platform.linux_distribution(supported_dists=['system'])[0].capitalize()
            if 'Amazon' in distribution:
                name = 'Amazon Linux'
            else:
                name = 'Other Linux'

        # get distribution version / release
        if name.lower().strip() in ('centos', 'scientific linux', 'suse linux enterprise server', 'opensuse'):
            version = platform.linux_distribution()[1]
        elif name.lower() == 'debian':
            # debians output for platform.linux_distribution varies and may include text
            version = platform.linux_distribution()[1].split('.')[0]
            if version.isnumeric():
                # todo: read debians release names from configuration file
                version = textwrap.dedent('''\
                    N/A
                    Buzz
                    Hamm
                    Woody
                    Etch
                    Lenny
                    Squeeze
                    Wheezy
                    Jessie
                    Stretch
                    Buster
                    Bullseye''').splitlines()[int(version)]
            else:
                version = version.split('/')[0]
        elif name.lower() == 'ubuntu':
            # on ubuntu, the release name will be added to the version string
            version = platform.linux_distribution()[1]
            # todo: read Ubunutus release names from configuration file
            version += ' "{}"'.format({
                'yakkety': 'Yakkety Yak', 'xenial': 'Xenial Xerus', 'trusty': 'Trusty Tahr',
                'precise': 'Precise Pangolin',
            }.get(platform.linux_distribution()[2]))
        else:
            version = platform.linux_distribution()[2]

    name = name.replace(' ', '\u00a0') if nbsp else name
    version = version.replace(' ', '\u00a0') if nbsp else version
    
    return {
        'name': name, 'version': version,
    }.get(info.lower(), (name, version))


def desktop():
    """
    returns the desktop environment used by the user
    
    :return: desktop environment
    :rtype: unicode string

    Currently the following desktop environments are supported:

    * Modern UI *(Windows 8, 8.1 or 10)*
    * Aero *(Windows Vista or 7)*
    * Luna *(Windows XP)*
    * Aqua *(macOS, OS X, Mac OS X)*
    * Unity *(Ubuntu)*
    * GNOME 3
    * GNOME 2
    * KDE
    * Cinnamon
    * Mate
    * Xfce 4
    * Lxde
    * Fluxbox
    * Blackbox
    * OpenBox
    * IceWM
    * JWM
    * AfterSTeP
    * Trinity
    * Razor Qt
    * Windowmaker
    """
    # From http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=1139057
    if sys.platform in ["win32", "cygwin"]:
        if platform.release() == 10:
            return 'Modern UI'
        else:
            if sys.getwindowsversion().major == 6:  # Windows Vista, 7, 8 or 8.1
                if sys.getwindowsversion().minor < 2:  # Windows Vista or 7
                    return 'Aero'
                else:
                    return 'Modern UI'  # Windows 8 or 8.1
            else:
                return 'Luna'  # Windows XP or older
    elif sys.platform == "darwin":
        return "Aqua"
    else:  # Most likely either a POSIX system or something not much common
        desktop_session = os.environ.get("DESKTOP_SESSION")
        if desktop_session is not None:  # easier to match if we doesn't have  to deal with caracter cases
            desktop_session = desktop_session.lower()
            if desktop_session in ["gnome",
                                   "unity",
                                   "cinnamon",
                                   "mate",
                                   "xfce4",
                                   "lxde",
                                   "fluxbox",
                                   "blackbox",
                                   "openbox",
                                   "icewm",
                                   "jwm",
                                   "afterstep",
                                   "trinity",
                                   "kde"]:
                return desktop_session.capitalize()
            # ## Special cases
            # Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if using LXDE.
            # There is no guarantee that they will not do the same with the other desktop environments.
            elif "xfce" in desktop_session or desktop_session.startswith("xubuntu"):
                return "Xfce4"
            elif desktop_session.startswith("ubuntu"):
                return "Unity"
            elif desktop_session.startswith("lubuntu"):
                return "Lxde"
            elif desktop_session.startswith("kubuntu"):
                return "KDE"
            elif desktop_session.startswith("razor"):  # e.g. razorkwin
                return "Razor-qt"
            elif desktop_session.startswith("wmaker"):  # e.g. wmaker-common
                return "Windowmaker"
        if os.environ.get('KDE_FULL_SESSION') == 'true':
            return "KDE"
        elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
            if "deprecated" not in os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                return "Gnome2"
        # From http://ubuntuforums.org/showthread.php?t=652320
        elif _is_running("xfce-mcs-manage"):
            return "Xfce4"
        elif _is_running("ksmserver"):
            return "KDE"
    return "unknown"


def _is_running(process):
    """ returns True if the given process is running, else False """
    # From http://www.bloggerpolis.com/2011/05/how-to-check-if-a-process-is-running-using-python/
    # and http://richarddingwall.name/2009/06/18/windows-equivalents-of-ps-and-kill-commands/
    try:  # Linux/Unix
        s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
    except (TypeError, ValueError):  # Windows
        s = subprocess.Popen(["tasklist", "/v"], stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(process, x):
            return True
    return False


def network(info='all'):
    """
    test performance of network

    :param unicode info: 'ping', 'download', 'upload', 'connection' or 'all'; default: 'all'
    :return: ping, download, upload, connection or all

    If *info* is 'connection', it measures the download speed and returns a name for this amount of speed from the
    following table:

    ======================= ===============
    Name                    Download Speed
    ======================= ===============
    UMTS                    384 kbit/s
    DSL 1000                1 Mbit/s
    DSL 2000                2 Mbit/s
    DSL 5000                5 Mbit/s
    16 MBit                 16 Mbit/s
    20 MBit                 20 Mbit/s
    50 MBit (UMTS/HSPA+)    50 Mbit/s
    100 MBit (LTE)          100 Mbit/s
    150 MBit (LTE 150)      150 Mbit/s
    300 MBit (LTE Max)      300 Mbit/s
    500 MBit                500 Mbit/s
    T1                      1,500 Mbit/s
    T3                      44,000 Mbit/s
    ======================= ===============
    """
    
    speedtest = pyspeedtest.SpeedTest()
    download_speed = speedtest.download()
    ping = speedtest.ping()
    
    speed = round(download_speed / 10 ** 6, 1)

    # return a human readable name
    if speed < 0.3:
        connection = 'UMTS'
    elif speed < 1:
        connection = 'DSL 1000'
    elif speed < 2:
        connection = 'DSL 2000'
    elif speed < 5:
        connection = 'DSL 5000'
    elif speed < 16:
        connection = '16 MBit'
    elif speed < 20:
        connection = '20 MBit'
    elif speed < 50:
        connection = '50 MBit (UMTS/HSPA+)'
    elif speed < 100:
        connection = '100 MBit (LTE)'
    elif speed < 150:
        connection = '150 MBit (LTE 150)'
    elif speed < 300:
        connection = '300 MBit (LTE Max)'
    elif speed < 500:
        connection = '500 MBit'
    elif speed < 1500:
        connection = 'T1'
    elif speed < 44000:
        connection = 'T3'
    else:
        connection = 'Unknown'
    return {
        'ping': ping, 'download': download_speed, 'upload': speedtest.upload(), 'connection': connection
    }.get(info.lower(), (ping, download_speed))


def sizeof_fmt(size, binary=True, separator=' ', suffix='B', digits=2):
    """
    takes a *size* (in bytes) and convert it in a human readable format.

    :param size: size in bytes
    :param digits: amount of decimals for any number
    :param binary: `True` for binary (:math:`2^x`) or `False` for decimal (:math:`10^x`) conversion; default: True
    :param separator: separator between number and unit; default: u' '
    :param suffix: B, Byte, byte etc.; default: u'B'
    :return:

    It converts into kilobytes, megabytes, gigabytes, terabytes and so on until the value is readable.
    Then it returns this value with the corresponding unit as a string.

    By setting *binary*, you can choose between *binary* and *decimal* conversion.
    The unit will be set accordingly to *XiB* for binary or *XB* for decimal.

    Examples:

    >>> sizeof_fmt(499999699990)
    u'465.7 GiB'
    >>> sizeof_fmt(499999699990, binary=False)
    u'500.0 GB'
    >>> sizeof_fmt(499999699990, separator='')
    u'465.7GiB'
    >>> sizeof_fmt(499999699990, binary=False, suffix='Byte')
    u'500.0 GByte'
    """
    factor = 1024.0 if binary else 1000.0
    unit = ''
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(size) < factor:
            s = '{s:3.{d}f}{sep:s}{unit:s}{suf:s}'
            # @formatter:off
            return s.format(
                d=digits,
                s=size,
                sep=separator,
                unit=unit if binary and len(unit) > 1 else unit[:-1],
                suf=suffix)
            # @formatter:on
        size /= factor
    return '{:.1f}{:s}{:s}{:s}'.format(size, separator, 'Yi' if binary and len(unit) > 1 else 'Y', suffix)


def record(format_='json', detailed=False, **kwargs):
    """
    return a complete record of system information in a given *format*

    :param format_: 'json', 'csv' or 'sql'
    :param bool detailed: True for detailed information, False for better performance and user privacy
    :param kwargs: Additonal Options (see below)
    :return: json-data, csv-data or sql-querystring

    If *detailed* is True, it returns a full record with all information available.
    If *detailed* is False, some information will be cut off to protect user's privacy and get better performance.

    Results will be cached in user's cache directory.

    *format* varies the output format to 'json' (default), 'sql' (PostgreSQL) or 'csv'

    Additonal Options
    -----------------

    :cache: set directory for cache file

    .. warning:: Privacy Information

       In some countries, some of the information included in a detailed and/or non-detailed record might be considered
       personal data. Gathering it and sending it to a server might interfere with your user's privacy.
       Please consult an attorney to get more information.

       As a rule of thumb, be sure that the user agreed with your usage of these data!
    """
    date = datetime.utcnow()
    record_archive_name = 'record.{date:%Y-%m}.json'.format(date=date)
    cache_path = os.path.abspath(os.path.expanduser(kwargs.get('cache', '~/.cache')))
    archivefilename = os.path.join(cache_path, 'SystemInfo')

    if format_ == 'json':
        # try to read data from cached archive file
        try:
            with zipfile.ZipFile(archivefilename, mode='r', compression=zipfile.ZIP_DEFLATED) as archivefile:
                if record_archive_name in archivefile.namelist():
                    data = archivefile.read(record_archive_name)
                    return six.u(json.dumps(data))
        except (KeyError, RuntimeError, IOError):
            archivefilename = None

    # if no cache is available, get the data
    columns = OrderedDict()
    columns['Record'] = ['Date of Record', 'Time of Record', 'MAC Adress']
    columns['CPU'] = ['CPU Speed', 'Cores']
    columns['Memory'] = ['Drives']
    columns['System'] = ['System']

    date_of_rec = date.strftime('%Y-%m-%d')
    time_of_rec = date.strftime('%H:%M:%S')

    # get mac adress in the known format (##:##:##:##:##:##)
    # if mac adress is invalid (e.g. if there is no network device), the adress will just be an int
    mac_adress = getnode()
    if not (mac_adress >> 40) % 2:
        mac_adress = ':'.join(("%012X" % mac_adress)[i:i + 2] for i in range(0, 12, 2))
    loc = location()
    country = loc['country']

    # detailed information include in-depth information of the computer hardware
    # these information can lead into privacy problems, so the user has to agree on sending this information
    if detailed:
        columns['CPU'] = ['CPU', 'CPU Speed', 'Physical Cores', 'Cores']
        columns['Memory'] = ['Drives']
        columns['System'].extend(['System Version', 'Desktop'])
        columns['GPU'] = ['OpenGL', 'GLSL', 'Renderer']
        columns['Network'] = ['Ping', 'Network (Down)']  # , 'Network (Up)', 'Network Speed']
        columns['Location'] = ['Language', 'City', 'Longitude', 'Latitude']
        columns['Personal'] = ['User IP', 'User Name']

        processor, speed = cpu()
        units = cpu_count(logical=False)
        cores = cpu_count(logical=True)

        disks = []
        for part in disk_partitions(all=False):
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    # skip cd-rom drives with no disk in it; they may raise
                    # ENOENT, pop-up a Windows GUI error for a non-ready
                    # partition or just hang.
                    continue
            usage = disk_usage(part.mountpoint)
            disks.append(
                '{mnt} at {dev} ({used} of {total} used, that is {perc} %)'.format(
                    mnt=part.mountpoint, dev=part.device,
                    used=sizeof_fmt(usage.used), total=sizeof_fmt(usage.total), perc=int(usage.percent)))
        disk = '; '.join(disks)
        os_, release = system()
        gui = desktop()

        vendor, opengl, glsl, renderer = gpu() if opengl_enabled else 'Unknown', 'Unknown', 'Unknown', 'Unknown'
        if 'nvidia' in vendor.lower():
            vendor = 'NVIDIA'
        elif 'ati' in vendor.lower():
            vendor = 'ATI'
        elif 'intel' in vendor.lower():
            vendor = 'Intel'

        ping, down = network()
        ping = int(ping)
        down = round(down / 10 ** 6, 2)
        city = '{city} {zip}'.format(city=loc['city'], zip=loc['zip'])

        longitude = loc['lon']
        latitude = loc['lat']
        try:
            lang = locale.getdefaultlocale()[0].split('_')[0]
            language = babel.Locale.parse('_'.join((lang, loc['countryCode']))).get_language_name()
        except babel.UnknownLocaleError:
            language = babel.Locale.parse('und_' + loc['countryCode']).get_language_name()
        ip_adress = ipgetter.myip()

        # anonymize ip adress if the user wishes or the law require this
        privacy_countries = ['germany', 'france']
        if not detailed or country.lower() in privacy_countries or kwargs.get('anonymize_ip', False):
            ip_adress = ip_adress.split('.')[0:3]
            ip_adress.append('0')
            ip_adress = '.'.join(ip_adress)

        username = getpass.getuser()
        row = [date_of_rec,
               time_of_rec,
               mac_adress,
               processor,
               speed,
               units,
               cores,
               disk,
               os_,
               release,
               gui,
               opengl,
               glsl,
               renderer,
               ping,
               down,
               language,
               city,
               longitude,
               latitude,
               ip_adress,
               username]

    else:
        speed = cpu('speed')
        cores = cpu_count()
        disk_list = [sizeof_fmt(d) for d in [disk_usage(part.mountpoint).total for part in disk_partitions(all=False)]]
        disk = '; '.join(disk_list)
        os_ = system('name')
        vendor = gpu('vendor')
        row = [date_of_rec, time_of_rec, mac_adress, speed, cores, disk, os_]

    columns['Other'] = ['GPU Vendor', 'Memory', 'Country']

    if 'nvidia' in vendor.lower():
        vendor = 'NVIDIA'
    elif 'ati' in vendor.lower():
        vendor = 'ATI'
    elif 'intel' in vendor.lower():
        vendor = 'Intel'
    row.append(vendor)

    memory = virtual_memory().total
    row.append(memory)
    row.append(country)

    if format_.lower() == 'csv':
        csv_columns = ''
        for group in columns.values():
            csv_columns += '\t'.join(group) + '\t'
        csv_row = '\t'.join(row)
        if kwargs.get('header', False):
            return '{}\n{}'.format(csv_columns[:-1], csv_row)
        else:
            return csv_row

    if format_.lower() == 'json':
        data = {}
        cols = []
        for group in columns.values():
            cols.extend(group)
        for n, column in enumerate(cols):
            try:
                data[column] = row[n].replace('"', "'")
            except AttributeError:
                data[column] = row[n]
        try:
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', prefix='record', delete=False) as temp:
                raw_data = json.dumps(data, indent=4, separators=(',', ': '), ensure_ascii=False)
                temp.write(raw_data)
            with zipfile.ZipFile(archivefilename, mode='a', compression=zipfile.ZIP_DEFLATED) as archivefile:
                if record_archive_name not in archivefile.namelist():
                    archivefile.write(filename=temp.name, arcname=record_archive_name)
        except (AttributeError, KeyError, RuntimeError, OSError):
            pass
        return six.u(json.dumps(data))

    if format_.lower() == 'sql':
        table = kwargs.get('table', 'spy_system_information')

        # @formatter:off
        sql_create_table = '''CREATE TABLE IF NOT EXISTS {table_name} (
              "Date of Record" DATE,
              "Time of Record" TIME,
              "Hardware ID" VARCHAR(20)
              "CPU" VARCHAR(80),
              "CPU Speed" REAL,  -- in GHz
              "Physical Cores" SMALLINT,
              "Cores" SMALLINT,
              "Memory" BIGINT,  -- memory in bytes
              "Drives" TEXT,  -- could get long if this machine has many partitions
              "System" VARCHAR(128),
              "System Version" VARCHAR(128),
              "Desktop" VARCHAR(128),
              "GPU Vendor" VARCHAR(64),
              "OpenGL" VARCHAR(80),
              "GLSL" VARCHAR(128),
              "Renderer" TEXT,
              "Ping" SMALLINT,  -- should be between 0 and ~500
              "Network (Down)" REAL,
              "Country" VARCHAR(255),
              "Language" VARCHAR(255),
              "City" VARCHAR(255),  -- longest city name in the world (168 chars) is Bangkok"s native language name:
              -- กรุงเทพมหานคร อมรรัตนโกสินทร์ มหินทรายุธยา มหาดิลกภพ นพรัตนราชธานีบูรีรมย์
              -- อุดมราชนิเวศน์มหาสถาน อมรพิมานอวตารสถิต สักกะทัตติยวิษณุกรรมประสิทธิ์
              "Longitude" DOUBLE PRECISION,
              "Latitude" DOUBLE PRECISION,
              "User IP" VARCHAR(40), -- ipv6 adress strings are about 40 chars long
              "User Name" VARCHAR(800)  -- longest name in history was 746 characters long
        );'''.format(table_name=table)
        # @formatter:on

        template = sql_create_table + '\n' if kwargs.get('createtable', False) else ''
        template += 'SET TIMEZONE TO UTC;\nINSERT INTO {table_name} ({cols})\nVALUES ({values});'
        cols = []
        vals = sql_columns = ''

        for group in columns.values():
            cols.extend(group)

        for n, column in enumerate(cols):
            sql_columns += '"{name}",'.format(name=column)
            try:
                vals += '{value},'.format(value=float(row[n]))
            except ValueError:
                try:
                    vals += '{value},'.format(value=int(row[n]))
                except ValueError:
                    vals += "'{value}',".format(value=row[n].replace("'", '"'))
        sql = template.format(table_name=table, cols=sql_columns[:-1], values=vals[:-1])
        return sql


def post(url, data):
    """
    send json-formatter data to a server

    :param url: adress of server to send data to
    :param data: json formatted data to send
    """
    # todo: use Module "request" for Http POST requests for Python 3 Support

    request = urllib2.Request(url, data)
    request.add_header('User-Agent',
                       'Sniffer/{version} by {author} ({url})'.format(version=__version__,
                                                                      author=__author__,
                                                                      url=__url__))
    f = urllib2.urlopen(request)
    print(f.read())


if __name__ == '__main__':
    try:
        gpu_vendor = gpu('vendor')
        if 'nvidia' in gpu_vendor.lower():
            gpu_vendor = 'NVIDIA'
        elif 'ati' in gpu_vendor.lower():
            gpu_vendor = 'ATI'
        elif 'intel' in gpu_vendor.lower():
            gpu_vendor = 'Intel'
        else:
            gpu_vendor = 'Unknown'
    except AttributeError:
        gpu_vendor = 'Unknown'

    country_code = location['countryCode']
    language_code = locale.getdefaultlocale()[0].split('_')[0]
    
    locale_ = babel.Locale.parse('_'.join((language_code, country_code)))

    hardware_info_text = textwrap.dedent('''\
        System\u00a0Information: {os}\u00a0{ver} with {desktop}\u00a0Desktop,
        running on {count}x\u00a0{cpu} with {ram} RAM,
        with {hdd}\u00a0disk\u00a0space and a {vend}\u00a0GPU with OpenGL\u00a0{gl} (GLSL\u00a0{shading}).
        Location: {city} in {country}, language: {language}''')
    hardware_info_text.format(os=system('name'),
                              ver=system('version'),
                              desktop=desktop(),
                              count=cpu_count(logical=False),
                              cpu=cpu('name'),
                              ram=sizeof_fmt(virtual_memory().total),
                              vend=gpu_vendor,
                              gl=gpu('version').split(' ')[0],
                              shading=gpu('shading language'),
                              hdd=sizeof_fmt(disk_usage('.').total),
                              city=location['city'],
                              country=location['country'],
                              language=locale_.get_language_name('en'))
    print(hardware_info_text)


# @formatter:off
#                                                                                                |\      _,,,---,,_
#                                                                                                /,`.-'`'    -.  -,_
#                                                                                               |,4-  ) )-,_..\ (  `'-'
#                                                                                              '---''(_/--'  `-'\_)
# @formatter:on
