@echo off
setlocal

title Premium File Tools - Installer
cd /d "%~dp0"

set "SCRIPT=%~dp0Outils_Fichiers.py"

if not exist "%SCRIPT%" (
    echo.
    echo [ERROR] Outils_Fichiers.py was not found next to this installer.
    echo Place Install.bat in the same folder as Outils_Fichiers.py.
    echo.
    pause
    exit /b 1
)

net session >nul 2>&1
if not "%errorlevel%"=="0" (
    echo Requesting administrator rights...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

echo.
echo ==========================================
echo   Premium File Tools / Outils Fichiers
echo ==========================================
echo.
echo Installing Windows context menu entries...
echo.

where py >nul 2>&1
if "%errorlevel%"=="0" (
    py -3 "%SCRIPT%"
    goto :done
)

where python >nul 2>&1
if "%errorlevel%"=="0" (
    python "%SCRIPT%"
    goto :done
)

echo [ERROR] Python 3 was not found.
echo Install Python 3 from https://www.python.org/downloads/
echo Make sure to enable "Add python.exe to PATH" during installation.
echo.
pause
exit /b 1

:done
set "RESULT=%errorlevel%"
echo.
if "%RESULT%"=="0" (
    echo Installation finished.
) else (
    echo Installation finished with error code %RESULT%.
)
echo.
pause
exit /b %RESULT%
