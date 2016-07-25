; Turn off old selected section
; 26 06 2015: Fadiga Ibrahima

; -------------------------------
; variables

!define MUI_PRODUCT "RAMED Desktop"
!define MUI_FILE "ramed"
!define MUI_VERSION "1.3"
!define MUI_BRANDINGTEXT "${MUI_PRODUCT} ${MUI_VERSION}"
!define ICON "logo.ico"
!define MEDIA "media"
!define IMAGES "img"
;CRCCheck On
;SetCompressor lzma

Name "${MUI_PRODUCT}"
OutFile "Install ${MUI_PRODUCT} ${MUI_VERSION}.exe"

InstallDir "$PROGRAMFILES\${MUI_PRODUCT}"
!include "MUI2.nsh"
!include "LangFile.nsh"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "French"


Section "install"
	SetOutPath "$INSTDIR"

	; List of files/folders to copy
	File /r dist\*.*
	File /r Shortcut.exe
	File /r ramed.config
	; File ..\ressources\*.dll
	File /r ${IMAGES}

	;create desktop shortcut
	CreateShortCut "$DESKTOP\${MUI_PRODUCT}.lnk" "$INSTDIR\${MUI_FILE}.exe" parameters "$INSTDIR\${MEDIA}\${IMAGES}\${ICON}"

	;create start-menu items
	CreateDirectory "$SMPROGRAMS\${MUI_PRODUCT}"
	CreateShortCut "$SMPROGRAMS\${MUI_PRODUCT}\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\${MEDIA}\${IMAGES}\${ICON}" 0
	CreateShortCut "$SMPROGRAMS\${MUI_PRODUCT}\${MUI_PRODUCT}.lnk" "$INSTDIR\${MUI_FILE}.exe" "" "$INSTDIR\${MEDIA}\${IMAGES}\${ICON}" 0

	;write uninstall information to the registry
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}" "DisplayName" "${MUI_PRODUCT} (remove only)"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}" "UninstallString" "$INSTDIR\Uninstall.exe"

	WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd


;--------------------------------
;Uninstaller Section
Section "un.install"

	;Delete Files
	;RMDir /r "$INSTDIR\*.*"

	;R emove the installation directory
	delete $INSTDIR\*.exe
	delete $INSTDIR\*.config
	delete $INSTDIR\*.dll
	delete $INSTDIR\*.lib
	delete $INSTDIR\*.zip
	delete $INSTDIR\*.pdf
	delete $INSTDIR\*.pyd
	delete $INSTDIR\*.log

	RMDir /r $INSTDIR\build
	RMDir /r $INSTDIR\${MEDIA}
	RMDir /r $INSTDIR\dist
	RMDir /r $INSTDIR\tcl
	RmDir "$INSTDIR"

	;Delete Start Menu Shortcuts
	Delete "$DESKTOP\${MUI_PRODUCT}.lnk"
	Delete "$SMPROGRAMS\${MUI_PRODUCT}\*.*"
	RmDir  "$SMPROGRAMS\${MUI_PRODUCT}"

	;Delete Uninstaller And Unistall Registry Entries
	DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\${MUI_PRODUCT}"
	DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}"

SectionEnd

;--------------------------------
Function .onInstSuccess
	SetOutPath $INSTDIR
	ExecShell "" '"$INSTDIR\${MUI_FILE}"'
FunctionEnd

Function un.onUninstSuccess
	; MessageBox MB_OK "You have successfully uninstalled ${MUI_PRODUCT}."
FunctionEnd

;eof
