Sniffer
=======

.. warning::

   This module gather information about the hardware and system you are running on.
   This might offend your user. Even worse, this might interfere with laws in some circumstances in some countries.
   As a rule of thumb, make sure your users will know what you are doing.
   If you have any questions, consult an attorney.

.. automodule:: Application.Sniffer
   :members:

Examples
--------

.. code-block:: python

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