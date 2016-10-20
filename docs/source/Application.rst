Application
===========

.. automodule:: Application
   :members:

Examples
--------

To use the platform specific folders inherited from the :mod:`appdirs`-Module, just use the attributes of the
:class:`Application`-class:

.. code-block:: python

   application = Application(appname='Rainbow', appauthor='unicorn')

   print 'User data dir:', application.user_data_dir
   print 'User config dir:', application.user_config_dir
   print 'User log dir:', application.user_log_dir
   print 'User cache dir:', application.user_cache_dir


To setup a simple configuration for your application, you have to provide a dictionary with default values:

.. code-block:: python

   application = Application(appname='Rainbow', appauthor='unicorn')

   default_configuration = OrderedDict()
   default_configuration['user'] = OrderedDict()
   default_configuration['user']['name'] = 'unicorn'
   default_configuration['user']['password'] = 'secret'

   configuration = application.configuration(default=default_configuration)

You can provide a simple way to clean all generated configurations and data files of you application by using the
:meth:`Application.reset`-Method:

.. code-block:: python

   application = Application(appname='Rainbow', appauthor='unicorn')
   if any(argument == 'reset' for argument in sys.argv):
      application.reset(['language', 'configuration', 'cache', 'log', 'data'])
      print 'Application has been reset.'

For a more in-depth sample, open the 'Examples' Folder inside the source code. There you find some more complex samples
on how to use the :mod:`Application`-module