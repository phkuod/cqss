@echo off
REM Quick Gantt Chart Generator - Windows Batch File
REM Generates to the same output file each time

echo Generating Gantt Chart...
python generate.py %*

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Chart generated successfully!
    echo Press any key to exit...
    pause >nul
) else (
    echo.
    echo Generation failed!
    pause
)