@echo off
setlocal

title Premium File Tools - Installer
cd /d "%~dp0"

set "SCRIPT=%~dp0Outils_Fichiers.py"
set "INSTALL_LANG=%~2"

if /I "%~1"=="--lang" (
    if /I "%INSTALL_LANG%"=="fr" goto :lang_ok
    if /I "%INSTALL_LANG%"=="en" goto :lang_ok
    set "INSTALL_LANG="
)

if "%INSTALL_LANG%"=="" (
    for /f "usebackq delims=" %%L in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "$p=Join-Path $env:APPDATA 'OutilsFichiersPremium\config.json'; if(Test-Path $p){try{(Get-Content $p -Raw | ConvertFrom-Json).language}catch{''}}"`) do set "INSTALL_LANG=%%L"
)

if /I not "%INSTALL_LANG%"=="fr" if /I not "%INSTALL_LANG%"=="en" set "INSTALL_LANG="

:lang_ok

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
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -ArgumentList '--lang','%INSTALL_LANG%' -Verb RunAs"
    exit /b
)

echo.
echo ==========================================
echo   Premium File Tools / Outils Fichiers
echo ==========================================
echo.
echo Installing Windows context menu entries...
if not "%INSTALL_LANG%"=="" echo Language: %INSTALL_LANG%
echo.

where py >nul 2>&1
if "%errorlevel%"=="0" (
    if "%INSTALL_LANG%"=="" (
        py -3 "%SCRIPT%"
    ) else (
        py -3 "%SCRIPT%" --install-lang "%INSTALL_LANG%"
    )
    goto :done
)

where python >nul 2>&1
if "%errorlevel%"=="0" (
    if "%INSTALL_LANG%"=="" (
        python "%SCRIPT%"
    ) else (
        python "%SCRIPT%" --install-lang "%INSTALL_LANG%"
    )
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
