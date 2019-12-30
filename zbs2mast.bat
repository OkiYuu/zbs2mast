@echo off
:start
cls
echo **********************************
echo *   ZBSpac to MAST Format Tool   *
echo **********************************
echo *   Select from options:         *
echo *                                *
echo *   1. Convert specific subdir   *
echo *   2. Convert ALL from IN       *
echo *   3. Quit                      *
echo *                                *
echo **********************************

set /p choice=Select option: 
if '%choice%'=='1' goto :opt1
if '%choice%'=='2' goto :opt2
if '%choice%'=='3' goto :EOF
goto :start

:opt1
:: Folder select code by rojo on Stackoverflow
:: URL: https://stackoverflow.com/questions/15885132/file-folder-chooser-dialog-from-a-windows-batch-script
setlocal
set "psCommand="(new-object -COM 'Shell.Application')^
.BrowseForFolder(0,'Please choose a folder.',0,0).self.path""
for /f "usebackq delims=" %%I in (`powershell %psCommand%`) do set "folder=%%I"
setlocal enabledelayedexpansion

:: DEBUG CODE
:: python "source\main.py" "%folder%"
source\main.exe "%folder%"

endlocal
echo Ran conversion script on %folder%.
echo Press any key to continue...
pause >NUL
goto :start

:opt2

:: DEBUG CODE
::python "source\main.py"
source\main.exe

echo Ran conversion on all .bin files from IN directory!
echo Press any key to continue...
pause >NUL
goto :start