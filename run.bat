@echo off
setlocal enabledelayedexpansion

echo Checking for Python...

:FindPythonCommand
for %%A in (python python3) do (
    where /Q %%A
    if !errorlevel! EQU 0 (
        set "PYTHON_CMD=%%A"
        goto :Found
    )
)

echo Python not found. Please install Python.
pause
exit /B 1

:Found
%PYTHON_CMD% scripts/check_requirements.py requirements.txt
if errorlevel 1 (
    echo Installing missing packages...
    %PYTHON_CMD% -m pip install -r requirements.txt
)

:Menu
echo.
echo Please choose a module to run:
echo 1. fincli
echo 2. fundainsight
echo.
set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" goto RunFincli
if "%choice%"=="2" goto RunFundainsight
echo Invalid choice. Please choose 1 or 2.
goto Menu

:RunFincli
%PYTHON_CMD% -m fincli --hist%*
goto End

:RunFundainsight
%PYTHON_CMD% -m fundainsight --hist%*
goto End

:End
pause
