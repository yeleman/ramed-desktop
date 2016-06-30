# ramed-desktop
Desktop UI to complement ODK Aggregate Export

Requirements
~~~~~~~~~~~~

Windows
~~~~~~~

You need a working windows environment to build Commmande windows packageL

    python-3.4.1.amd64.msi (add C:\Python34;C:\Python34\Scripts; to PATH)

    reboot

    nsis-3.0rc1-setup.exe
    pywin32-210.win32-py3.4.exe
    PyQt4-4.11.2-gpl-Py3.4-Qt4.8.6-x32.exe

    pip install -r requirements.pip 

Once setup, create windows executable:
    cd path\carapace
    ``py -3.4 setup-win.py py2exe --includes sip``

Once windows binary is complete, create installer with:
    ``"C:\Program Files\NSIS\makensis.exe" installer.nsi``
