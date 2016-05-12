#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Created by: python.exe -m py2exe main.py -W setup_win.py

from distutils.core import setup
import py2exe

from static import Constants


class Target(object):
    '''Target is the baseclass for all executables that are created.
    It defines properties that are shared by all of them.
    '''

    def __init__(self, **kw):
        self.__dict__.update(kw)

        # the VersionInfo resource, uncomment and fill in those items
        # that make sense:

        # The 'version' attribute MUST be defined, otherwise no versioninfo will be built:
        # self.version = "1.0"

        # self.company_name = "Company Name"
        # self.copyright = "Copyright Company Name © 2013"
        # self.legal_copyright = "Copyright Company Name © 2013"
        # self.legal_trademark = ""
        # self.product_version = "1.0.0.0"
        # self.product_name = "Product Name"

        # self.private_build = "foo"
        # self.special_build = "bar"

    def copy(self):
        return Target(**self.__dict__)

    def __setitem__(self, name, value):
        self.__dict__[name] = value

RT_MANIFEST = 24

# A manifest which specifies the executionlevel
# and windows common-controls library version 6

manifest_template = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="*"
    name="%(prog)s"
    type="win32"
  />
  <description>%(prog)s</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel
            level="%(level)s"
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

main = Target(
    # We can extend or override the VersionInfo of the base class:
    version="1.0",
    script=Constants.NAME_MAIN,  # path of the main script
    icon_resources=[(0, Constants.APP_LOGO_ICO)],
    other_resources=[(RT_MANIFEST, 1, (manifest_template % dict(
        prog=Constants.NAME_MAIN, level="asInvoker")).encode("utf-8")), ]
)

py2exe_options = dict(
    packages=["reportlab"],
    includes=['sip', 'PyQt4'],
    excludes=['tkinter'],
    optimize=0,
    compressed=True,  # uncompressed may or may not have a faster startup
    bundle_files=1,
    dist_dir='dist',
)

# Some options can be overridden by command line options...

setup(name="name",
      # console based executables
      console=[],
      # windows subsystem executables (no console)
      windows=[main],
      # py2exe options
      zipfile=None,
      options={"py2exe": py2exe_options, },
      )
