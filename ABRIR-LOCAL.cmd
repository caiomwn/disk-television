@echo off
setlocal
cd /d "%~dp0"
where python3 >nul 2>nul
if %errorlevel% equ 0 (
  python3 tools/serve.py
  goto :end
)
where py >nul 2>nul
if %errorlevel% equ 0 (
  py -3 tools/serve.py
  goto :end
)
echo Python 3 nao encontrado. Consulte README.md para publicar no GitHub Pages.
pause
:end
endlocal
