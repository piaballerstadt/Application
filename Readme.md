# Application

The Application-module provides some basic functionality useful for an application. This includes functions for simple logging, configuration management, initialization, argument parsing or simply accessing platform specific paths like paths for caches, logging files, configuration- or data files.

# Acknowledgments
This module contains the [appdirs module](https://pypi.python.org/pypi/appdirs#downloads) written by Trent Mick and Sridhar Ratnakumar, published under MIT License. Thanks a lot for your great code! I hope, the Application module will be a valuable extension.

# Table of Content
1. [Installation](#Installation)
    * [Installation with pip](#Installation-with-pip)
    * [Installation on Windows](#Installation-on-Windows)
    * [Installation on Linux, BSD or other POSIX Systems](#Installation-on-Linux,-BSD-or-other-POSIX-Systems)
    * [Installation on macOS, OS X or Mac OS X](#Installation-on-macOS,-OS-X-or-Mac-OS-X)
2. [Quickstart](#Quickstart)
3. [Support](#Support)
4. [Contributing](#Contributing)
    * [10 golden rules](#10-golden-rules)

# Installation

## Installation with pip

This module is not yet available for PyPi, so be patient and stay tuned.
Meanwhile, you can use one of the other installations methods described below.

[Back to top](#Application)

## Installation on Windows

<img title="Windows" alt="Windows" src="http://www.datenwerkstatt.com/wp-content/uploads/windows-10-logo.png" align="right" aria-role="presentation" height=40>

If you are familiar with the *Powershell* or *MS DOS command prompt*, you can just use the [Linux-instructions for installation]((#Installation-on-Linux,-BSD-or-other-POSIX-Systems)). Otherwise, download and extract the [Master-Archive](https://github.com/piaballerstadt/Application/archive/master.zip) and run the `setup-windows.ps1` File and follow the instructions. 

[Back to top](#Application)

## Installation on Linux, BSD or other POSIX Systems

<img title="FreeBSD" alt="" src="http://cinelerra-cv.org/images/website/distro-logos/freebsd.png" align="right" aria-role="presentation" height=40>
<img title="Fedora" alt="" src="http://www.mrpt.org/wp-content/uploads/2013/10/Fedora_logo.png" align="right" aria-role="presentation" height=40>
<img title="Linux Mint" alt="" src="https://cdn.thingiverse.com/renders/b3/da/8c/43/c8/Logo_Linux_Mint_thumb_small.jpg" align="right" aria-role="presentation" height=40>
<img title="Ubuntu" alt="" src="http://www.unknown-horizons.org/uploads/images/os-icons/ubuntu_64.png" align="right" aria-role="presentation" height=40>
<img title="Linux" alt="" src="http://www.chromaweb.com/images/linuxlogo.jpg" align="right" aria-role="presentation" height=40>

The easiest way to install this module on Linux is by using git:

```sh
git clone https://github.com/piaballerstadt/Application.git
cd Application
python setup.py install
```

If you don't have git or do not want to use it, you can download all files you need with curl:

```sh
curl -Lo Application-master.zip https://github.com/piaballerstadt/Application/archive/master.zip
unzip Application-master.zip && rm Application-master.zip
cd Application-master.zip
chmod +x setup.py
python setup.py install
```

The setup.py provides some non-standard options to choose from:

| Option for setup.py | Description                                          |
| ------------------- | ---------------------------------------------------- |
| --create-starter    | create a starter entry for Ubuntu, Unity and Gnome   |
| --language=de_DE    | install given language package (in this case, german)|

Example:
```sh
python setup.py install --create-starter
```

[Back to top](#Application)

## Installation on macOS, OS X or Mac OS X

<img title="OS X El Capitan" alt="" src="http://www.christianengvall.se/wp-content/uploads/2015/11/osx-logo.png" align="right" aria-role="presentation" height=64>
<img title="macOS Sierra" alt="" src="https://slice42.com/wp-content/uploads/2016/03/macos-logo-2016.jpg" align="right" aria-role="presentation" height=64>

The installation on macOS, OS X or Mac OS X should work as described in [Installation for Linux](#Installation-on-Linux,-Unix-or-other-POSIX-Systems), but I cannot test it. Please [report any issue during installation](https://github.com/piaballerstadt/Application/issues/new) on you system, I will consider this a high priority issue. Just make sure to include what version of macOS, OS X or Mac OS X you use when sending a report ([How to find out your system version](https://support.apple.com/HT201260)). Thank you very much!

[Back to top](#Application)

# Quick start

After installation, you can run a simple example application by double-clicking `Application.py` in the example folder or executing it on the terminal:
```sh
Application.py
```

There are different examples in the example folder, make sure to check them out!

If you want to start developing, the SimpleApplication.py is a easy way to get started:
```python
#!/usr/bin/env python
from __future__ import print_function, unicode_literals
from Application import Application
from logging import getLogger

if __name__ == '__main__':
    application = Application(appname='Pixidust', appauthor='Unicorn')
    logger = getLogger('Pixidust')
    logger.info(_('Application started.'))
    
```
Replace the contents of `README.md` with your project's:

* Name
* Description
* Installation instructions
* Usage instructions
* Support instructions
* Contributing instructions

Feel free to remove any sections that aren't applicable to your project.

[Back to top](#Application)

# Support

Please [open an issue](https://github.com/piaballerstadt/Application/issues/new) for support.

[Back to top](#Application)

# Contributing

Refer to the [Contribution Guide](http://contribution-guide.org/) for detailed information.

## 10 golden rules:

To make things easy, stick to these ten golden rules:

1. Feel free to contribute bug fixes or features ([open a pull request](https://github.com/piaballerstadt/Application/compare/))
2. Get in contact *early* - this is better than asking too late!
3. Use [Gitflow](http://nvie.com/posts/a-successful-git-branching-model/)
4. When ready to commit, please write a [useful commit message](http://chris.beams.io/posts/git-commit/)!
5. Comment wisely and provide documentation
    * For Python: [ReST](https://de.wikipedia.org/wiki/ReStructuredText) and [Spinx](http://www.sphinx-doc.org/en/stable/index.html) rulez!
6. Only testable code is good code! Provide unit tests for all contributions.
7. Readability is king!
    * For Python: [PEP8](https://www.python.org/dev/peps/pep-0008/) rulez (with a few exceptions)!
8. Use *descriptive* variable names
    * x, y etc. *may* be descriptive if in a mathematical context or as coordinates
9. Compatibility and portability are king!
    * C++ and Python is cross-platform, so your applications should be, too!
    * for Python: use [six](https://pythonhosted.org/six/) for python 2+3 support
    * for PySide/PyQt: Use [Qt.py](https://github.com/mottosso/Qt.py) for support of PySide, PySide2, PyQt4 and PyQt5
    * for C++: Use the latest version of C++ that is supported by major compilers and frameworks (currently [C++11](https://en.wikipedia.org/wiki/C%2B%2B11))
    * build system: Use cmake
10. Usability is king!
    * start early with [i18n and l10n](https://en.wikipedia.org/wiki/C%2B%2B11)
    * watch out for [accessibility](https://en.wikipedia.org/wiki/Accessibility)
    * think about [UX](https://de.wikipedia.org/wiki/User_Experience) even *before* coding
    * make the application fast, unbreakable, and provide useful feedback for the user

But most important: Have fun coding!

[Back to top](#Application)