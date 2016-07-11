#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# Created by: python.exe -m py2exe main.py -W setup_win.py

import py2exe
from distutils.core import setup

from ramed.static import Constants

RT_MANIFEST = 24

# A manifest which specifies the executionlevel
# and windows common-controls library version 6
manifest_template = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="*"
    name="{prog}"
    type="win32"
  />
  <description>{prog}</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel
            level="{level}"
            uiAccess="false">
        </requestedExecutionLevel>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="*"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
  </dependency>
</assembly>
'''

main = {
    'version': "1.1",
    'script': Constants.MAIN_SCRIPT,  # path of the main script
    'icon_resources': [(0, Constants.ICO_ICON)],
    'other_resources': [
        (RT_MANIFEST, 1, (manifest_template
                          .format(prog=Constants.MAIN_SCRIPT,
                                  level="asInvoker")).encode("utf-8")),
        ]
    }

py2exe_options = {
    'packages': ["reportlab"],
    'includes': ['sip', 'PyQt4'],
    'excludes': ['tkinter'],
    'optimize': 0,
    'compressed': True,  # uncompressed may or may not have a faster startup
    'bundle_files': 1,
    'dist_dir': 'dist',
}

# Some options can be overridden by command line options...
setup(name="RAMED",
      # console based executables
      console=[],
      # windows subsystem executables (no console)
      windows=[main],
      # py2exe options
      zipfile=None,
      options={"py2exe": py2exe_options, })
